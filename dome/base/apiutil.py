import json
from json import JSONDecodeError

import allure

from dome.common.debugtalk import DebugTalk
from dome.common.readyaml import ReadYamlData, get_testcase_yaml
from dome.conf.operationConfig import OperationConfig
import jsonpath

class RequestBase:

    def __init__(self):
        self.read = ReadYamlData()
        self.conf = OperationConfig()

    def replace_load(self, data):
        """yaml数据替换解析"""
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)
            # print('从yaml文件获取的原始数据：', str_data)
        for i in range(str_data.count('${')):
            if '${' in str_data and '}' in str_data:
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                ref_all_params = str_data[start_index:end_index + 1]
                # 取出yaml文件的函数名
                func_name = ref_all_params[2:ref_all_params.index("(")]
                # 取出函数里面的参数
                func_params = ref_all_params[ref_all_params.index("(") + 1:ref_all_params.index(")")]
                # 传入替换的参数获取对应的值,类的反射----getattr,setattr,del....
                extract_data = getattr(DebugTalk(), func_name)(*func_params.split(',') if func_params else "")

                if extract_data and isinstance(extract_data, list):
                    extract_data = ','.join(e for e in extract_data)
                str_data = str_data.replace(ref_all_params, str(extract_data))
                # print('通过解析后替换的数据：', str_data)

        # 还原数据
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    def specification_yaml(self, base_info, test_case):
        """
        接口请求处理基本方法
        :param base_info: yaml文件里面的baseInfo
        :param test_case: yaml文件里面的testCase
        :return:
        """
        try:
            params_type = ['data', 'json', 'params']
            url_host = self.conf.get_section_for_data('api_envi', 'host')
            api_name = base_info['api_name']
            allure.attach(api_name, f'接口名称：{api_name}', allure.attachment_type.TEXT)
            url = url_host + base_info['url']
            allure.attach(api_name, f'接口地址：{url}', allure.attachment_type.TEXT)
            method = base_info['method']
            allure.attach(api_name, f'请求方法：{method}', allure.attachment_type.TEXT)
            header = self.replace_load(base_info['header'])
            allure.attach(api_name, f'请求头：{header}', allure.attachment_type.TEXT)
            # 处理cookie
            cookie = None
            if base_info.get('cookies') is not None:
                cookie = eval(self.replace_load(base_info['cookies']))
            case_name = test_case.pop('case_name')
            allure.attach(api_name, f'测试用例名称：{case_name}', allure.attachment_type.TEXT)
            # 处理断言
            val = self.replace_load(test_case.get('validation'))
            test_case['validation'] = val
            validation = eval(test_case.pop('validation'))
            # 处理参数提取
            extract = test_case.pop('extract', None)
            extract_list = test_case.pop('extract_list', None)
            # 处理接口的请求参数
            for key, value in test_case.items():
                if key in params_type:
                    test_case[key] = self.replace_load(value)

            # 处理文件上传接口
            file, files = test_case.pop('files', None), None
            if file is not None:
                for fk, fv in file.items():
                    allure.attach(json.dumps(file), '导入文件')
                    files = {fk: open(fv, mode='rb')}

            res = self.run.run_main(name=api_name, url=url, case_name=case_name, header=header, method=method,
                                    file=files, cookies=cookie, **test_case)
            status_code = res.status_code
            allure.attach(self.allure_attach_response(res.json()), '接口响应信息', allure.attachment_type.TEXT)

            try:
                res_json = json.loads(res.text)  # 把json格式转换成字典字典
                if extract is not None:
                    self.extract_data(extract, res.text)
                if extract_list is not None:
                    self.extract_data_list(extract_list, res.text)
                # 处理断言
                self.asserts.assert_result(validation, res_json, status_code)
            except JSONDecodeError as js:
                print('系统异常或接口未请求！')
                raise js
            except Exception as e:
                print(e)
                raise e

        except Exception as e:
            raise e


if __name__ == '__main__':
    data = get_testcase_yaml('../loginName.yaml')[0]
    # print(data)
    request = RequestBase().replace_load(data)
    print(request)