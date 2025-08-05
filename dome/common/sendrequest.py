import json

import allure
import pytest
import requests
from urllib3.exceptions import InsecureRequestWarning

from dome.common.readyaml import ReadYamlData, get_testcase_yaml
from dome.conf import setting
from dome.common.recordlog import logs
from requests import utils

from dome.conf.setting import FILE_PATH


class SendRequest:
    """发送接口请求，暂时只写了get和post方法的请求"""

    def __init__(self, cookie=None):
        self.cookie = cookie
        self.read = ReadYamlData()

    def send_request(self, **kwargs):
        session = requests.session()
        result = None
        cookie = {}
        try:
            result = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                cookie['Cookie'] = set_cookie
                # self.read.write_yaml_data(cookie)
                logs.info(f'cookie: {cookie}')
            logs.info("接口的实际返回信息：%s" % result.json() if result.json() else result)
            # logs.info(f'接口的实际返回信息: {result}')
        except requests.exceptions.ConnectionError:
            logs.error("ConnectionError--连接异常")
            pytest.fail("接口请求异常，可能是request的连接数过多或请求速度过快导致程序报错！")
        except requests.exceptions.HTTPError:
            logs.error("HTTPError--http异常")
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail("请求异常，请检查系统或数据是否正常！")
        return result

    def run_main(self, name, url, case_name, header, method, cookies=None, file=None, **kwargs):
        """
        接口请求
        :param name: 接口名
        :param url: 接口地址
        :param case_name: 测试用例
        :param header:请求头
        :param method:请求方法
        :param cookies：默认为空
        :param file: 上传文件接口
        :param kwargs: 请求参数，根据yaml文件的参数类型
        :return:
        """

        try:
            # 收集报告日志
            logs.info(f'接口名称：{name}')
            logs.info(f'请求地址：：{url}')
            logs.info(f'请求方式：：{method}')
            logs.info(f'测试用例名称：：{case_name}')
            logs.info(f'请求头：：{header}')
            logs.info(f'Cookie：：{cookies}')
            req_params = json.dumps(kwargs, ensure_ascii=False)
            if "data" in kwargs.keys():
                allure.attach(req_params, f'请求参数: {req_params}', allure.attachment_type.TEXT)
                # logs.info("请求参数：%s" % kwargs)
            elif "json" in kwargs.keys():
                allure.attach(req_params, f'请求参数: {req_params}', allure.attachment_type.TEXT)
                # logs.info("请求参数：%s" % kwargs)
            elif "params" in kwargs.keys():
                allure.attach(req_params, f'请求参数: {req_params}', allure.attachment_type.TEXT)
                # logs.info("请求参数：%s" % kwargs)
        except Exception as e:
            logs.error(e)
        # time.sleep(0.5)
        # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = self.send_request(method=method,
                                     url=url,
                                     headers=header,
                                     cookies=cookies,
                                     files=file,
                                     timeout=setting.API_TIMEOUT,
                                     verify=False,
                                     **kwargs)
        # print(response)
        allure.attach(json.dumps(response.json(), ensure_ascii=False), f'响应结果: {response.status_code}',
                      allure.attachment_type.TEXT)
        return response


if __name__ == '__main__':
    params_type = ['data', 'json', 'params']
    data = get_testcase_yaml(FILE_PATH['LOGIN'])[0]
    # print(data)
    url = data['baseInfo']['url']
    new_url = 'http://127.0.0.1:8787' + url
    method = data['baseInfo']['method']
    header = data['baseInfo']['header']
    name = data['baseInfo']['api_name']
