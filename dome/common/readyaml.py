import yaml
import traceback
import os
from dome.conf.setting import FILE_PATH

def get_testcase_yaml(file):
    # testcase_list = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data
            # if len(data) <= 1:
            #     yam_data = data[0]
            #     base_info = yam_data.get('baseInfo')
            #     for ts in yam_data.get('testCase'):
            #         param = [base_info, ts]
            #         testcase_list.append(param)
            #     return testcase_list
            # else:
            #     return data
    except Exception as e:
        print(e)


class ReadYamlData:

    """读写接口的YAML格式测试数据"""

    def __init__(self, yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = FILE_PATH['LOGIN']

    @property
    def get_yaml_data(self, node_name):
        """
        获取测试用例yaml数据
        :param file: YAML文件
        :return: 返回list
        """
        # Loader=yaml.FullLoader表示加载完整的YAML语言，避免任意代码执行，无此参数控制台报Warning
        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as f:
                self.yaml_data = yaml.safe_load(f)
                return self.yaml_data
        except Exception as e:
            print(e)


    def write_yaml_data(self, value):
        """
        写入数据需为dict，allow_unicode=True表示写入中文，sort_keys按顺序写入
        写入YAML文件数据,主要用于接口关联
        :param value: 写入数据，必须用dict
        :return:
        """

        file = None
        file_path = FILE_PATH['EXTRACT']
        if not os.path.exists(file_path):
            os.system(file_path)
        try:
            file = open(file_path, 'a', encoding='utf-8')
            if isinstance(value, dict):
                write_data = yaml.dump(value, allow_unicode=True, sort_keys=False)
                file.write(write_data)
            else:
                print('写入[extract.yaml]的数据必须为dict格式')
        except Exception as e:
            print(e)
        finally:
            file.close()

    def get_extract_yaml(self, node_name, second_node_name=None):
        """
        用于读取接口提取的变量值
        :param node_name:
        :return:
        """
        if os.path.exists(FILE_PATH['EXTRACT']):
            pass
        else:
            print('extract.yaml不存在')
            file = open(FILE_PATH['EXTRACT'], 'w')
            file.close()
            print('extract.yaml创建成功！')
        try:
            with open(FILE_PATH['EXTRACT'], 'r', encoding='utf-8') as rf:
                ext_data = yaml.safe_load(rf)
                if second_node_name is None:
                    return ext_data[node_name]
                else:
                    return ext_data[node_name][second_node_name]
        except Exception as e:
            print(f"【extract.yaml】没有找到：{node_name},--%s" % e)


if __name__ == '__main__':
    res = get_testcase_yaml(FILE_PATH['LOGIN'])
    url = res[0]['baseInfo']['url']
    nest_url = 'http://127.0.0.1:8787' + url
    method = res[0]['baseInfo']['method']
    data = res[0]['testCase'][0]['data']
    # from sendrequest import SendRequest
    # res = SendRequest().run_main(url=nest_url, method=method, data=data, header=None)
    # print(res)
    #
    # write_token = {"Token": res['token']}
    # print(write_token)
    #
    write_yaml = ReadYamlData()
    # write_yaml.write_yaml_data(write_token)
    res2 = write_yaml.get_extract_yaml('Params')
    print(res2)