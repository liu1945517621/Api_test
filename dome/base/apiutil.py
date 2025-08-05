import json
import re
from json import JSONDecodeError
import logging

from dome.common.assertions import Assertions
import allure
from dome.common.recordlog import logs
from dome.common.debugtalk import DebugTalk
from dome.common.readyaml import ReadYamlData, get_testcase_yaml
from dome.common.sendrequest import SendRequest
from dome.conf.operationConfig import OperationConfig
import jsonpath

from dome.conf.setting import FILE_PATH

assert_res = Assertions()


class RequestBase:

    def __init__(self):
        self.read = ReadYamlData()
        self.conf = OperationConfig()
        self.send = SendRequest()

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

    def specification_yaml(self, case_info):
        try:
            params_type = ['data', 'json', 'params']
            url_host = self.conf.get_section_for_data('api_envi', 'host')
            url = url_host + case_info['baseInfo']['url']
            allure.attach(url, f'接口地址:{url}')
            api_name = case_info['baseInfo']['api_name']
            allure.attach(api_name, f'接口名称:{api_name}')
            method = case_info['baseInfo']['method']
            allure.attach(method, f'请求方式:{method}')
            header = case_info['baseInfo']['header']
            allure.attach(str(header), f'请求头:{header}', allure.attachment_type.TEXT)
            # 处理cookie
            cookie = None
            # if case_info.get('cookies') is not None:
            try:
                cookie = eval(self.replace_load(case_info['cookies']))
                # allure.attach(str(cookie), f'Cookie:{cookie}', allure.attachment_type.JSON)
            except:
                pass

            for tc in case_info['testCase']:
                case_name = tc.pop('case_name')
                allure.attach(case_name, f'用例名称:{case_name}')
                validation = tc.pop('validation')
                # print('数值：', validation)
                extract = tc.pop('extract', None)
                extract_list = tc.pop('extract_list', None)
                for key, value in tc.items():
                    if key in params_type:
                        tc[key] = self.replace_load(value)

                res = self.send.run_main(name=api_name,
                                         url=url,
                                         case_name=case_name,
                                         header=header,
                                         method=method,
                                         file=None,
                                         cookies=cookie,
                                         **tc)
                res_text = res.text
                # allure.attach(res.text, f'响应信息:{res.text}', allure.attachment_type.TEXT)
                res_json = res.json()
                # print('接口响应信息：', res_json)
                if extract is not None:
                    self.extract_data(extract, res_text)
                if extract_list is not None:
                    self.extract_data_list(extract_list, res_text)

                # 处理断言
                assert_res.assert_result(validation, res_json, res.status_code)
        except AssertionError:
            # 重新抛出断言异常，让pytest能够正确识别测试失败
            raise
        except Exception as e:
            print(e)

    def extract_data(self, testcase_extract, response):
        """
        提取接口的返回值，支持正则表达式和json提取器
        :param testcase_extract: testcase文件yaml中的extract值
        :param response: 接口的实际返回值
        :return:
        """
        try:
            pattern_lst = ['(.*?)', '(.+?)', r'(\d)', r'(\d*)']
            for key, value in testcase_extract.items():

                # 处理正则表达式提取
                for pat in pattern_lst:
                    if pat in value:
                        ext_lst = re.search(value, response)
                        if pat in [r'(\d+)', r'(\d*)']:
                            extract_data = {key: int(ext_lst.group(1))}
                        else:
                            extract_data = {key: ext_lst.group(1)}
                        self.read.write_yaml_data(extract_data)
                # 处理json提取参数
                if '$' in value:
                    ext_json = jsonpath.jsonpath(json.loads(response), value)[0]
                    if ext_json:
                        extract_data = {key: ext_json}
                        logs.info('提取接口的返回值：', extract_data)
                    else:
                        extract_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                    self.read.write_yaml_data(extract_data)
        except Exception as e:
            logs.error(e)

    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_date = {key: ext_list}
                        logs.info('正则提取到的参数：%s' % extract_date)
                        self.read.write_yaml_data(extract_date)
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml_data(extract_date)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')


if __name__ == '__main__':
    data = get_testcase_yaml(FILE_PATH['LOGIN'])[0]
    # print(data)
    request = RequestBase().specification_yaml(data)
    print(request)
