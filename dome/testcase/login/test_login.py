import pytest
from dome.common.readyaml import get_testcase_yaml
from dome.common.sendrequest import SendRequest
from dome.conf.setting import FILE_PATH


class TestLogin:
    @pytest.mark.parametrize('params', get_testcase_yaml(FILE_PATH['LOGIN']))
    def test_login01(self, params):
        # print('获得参数:',  params)
        url = params['baseInfo']['url']
        nest_url = 'http://127.0.0.1:8787' + url
        method = params['baseInfo']['method']
        data = params['testCase'][0]['data']

        res = SendRequest().run_main(url=nest_url, method=method, data=data, header=None)
        # print('响应数据:', res)
        assert res['msg'] == '登录成功'

    @pytest.mark.parametrize('params', get_testcase_yaml(FILE_PATH['LOGIN']))
    def test_login02(self, params):
        # print('获得参数:',  params)
        url = params['baseInfo']['url']
        nest_url = 'http://127.0.0.1:8787' + url
        method = params['baseInfo']['method']

        data = {'user_name': 'test01', 'password': '123'}

        res = SendRequest().run_main(url=nest_url, method=method, data=data, header=None)
        print('响应数据:', res)
        assert res['msg'] == '登录成功'
