import json

from dome.common.debugtalk import DebugTalk
from dome.common.readyaml import ReadYamlData, get_testcase_yaml


class RequestBase:

    def __init__(self):
        self.read = ReadYamlData()

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


if __name__ == '__main__':
    data = get_testcase_yaml('../loginName.yaml')[0]
    # print(data)
    request = RequestBase().replace_load(data)
    print(request)