
import pytest
import requests


class SendRequest:
    """发送接口请求，暂时只写了get和post方法的请求"""

    # def __init__(self, cookie=None):
        # self.cookie = cookie
        # self.read = ReadYamlData()
    def __init__(self):
        pass
    def get(self, url, data, header):
        """
        :param url: 接口地址
        :param data: 请求参数
        :param header: 请求头
        :return:
        """
        # requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            if data is None:
                response = requests.get(url, headers=header, verify=False)
            else:
                response = requests.get(url, data, headers=header, verify=False)
            return response.json()
        # except requests.RequestException as e:
        #     print(e)
        #     return None
        except Exception as e:
            print(e)
        #     return None
        # 响应时间/毫秒
        # res_ms = response.elapsed.microseconds / 1000
        # # 响应时间/秒
        # res_second = response.elapsed.total_seconds()
        # response_dict = dict()

        # 接口响应状态码
        # response_dict['code'] = response.status_code
        # # 接口响应文本
        # response_dict['text'] = response.text
        # try:
        #     response_dict['body'] = response.json().get('body')
        # except Exception:
        #     response_dict['body'] = ''
        # response_dict['res_ms'] = res_ms
        # response_dict['res_second'] = res_second
        # return response_dict

    def post(self, url, data, header):
        """
        :param url:
        :param data: verify=False忽略SSL证书验证
        :param header:
        :return:
        """
        # 控制台输出InsecureRequestWarning错误
        # requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            if data is None:
                response = requests.post(url, header, verify=False)
            else:
                response = requests.post(url, data, headers=header, verify=False)
            return response.json()
        except requests.RequestException as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            # return None
        # 响应时间/毫秒
        # res_ms = response.elapsed.microseconds / 1000
        # # 响应时间/秒
        # res_second = response.elapsed.total_seconds()
        # response_dict = dict()
        # # 接口响应状态码
        # response_dict['code'] = response.status_code
        # # 接口响应文本
        # response_dict['text'] = response.text
        # try:
        #     response_dict['body'] = response.json().get('body')
        # except Exception:
        #     response_dict['body'] = ''
        # response_dict['res_ms'] = res_ms
        # response_dict['res_second'] = res_second
        # return response_dict

    def update(self, url, data, header):
        """
        :param url:
        :param data:
        :param header:
        :return:
        """
        pass

    def delete(self, url, data, header):
        """
        :param url:
        :param data:
        :param header:
        :return:
        """
        pass

    def send_request(self, method, url, data, header=None):

        session = requests.session()
        result = None
        cookie = {}
        try:
            result = session.request(method, url, data, headers=header)
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                cookie['Cookie'] = set_cookie
                self.read.write_yaml_data(cookie)
                print("cookie：%s" % cookie)
            print("接口返回信息：%s" % result.text if result.text else result)
        except requests.exceptions.ConnectionError:
            print("ConnectionError--连接异常")
            pytest.fail("接口请求异常，可能是request的连接数过多或请求速度过快导致程序报错！")
        except requests.exceptions.HTTPError:
            print("HTTPError--http异常")
        except requests.exceptions.RequestException as e:
            print(e)
            pytest.fail("请求异常，请检查系统或数据是否正常！")
        return result

    def run_main(self, url, header, data, method):
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
        res = None
        if method.upper() == 'GET':
            return self.get(url, data, header)
        elif method.upper() == 'POST':
            return self.post(url, data, header)
        else:
            print('不支持其他请求')
        return  res


if __name__ == '__main__':
    url = 'http://127.0.0.1:8787/dar/user/login'
    data = {'user_name': 'test01', 'passwd': 'admin123'}
    header = None
    method = 'POST'
    result = SendRequest().run_main(url=url, header=header, data=data, method=method)
    print(result)