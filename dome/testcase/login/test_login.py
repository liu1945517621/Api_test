import logging

import allure
import pytest
from dome.common.readyaml import get_testcase_yaml
from dome.common.sendrequest import SendRequest
from dome.conf.setting import FILE_PATH
from dome.common.recordlog import logs
from dome.base.apiutil import RequestBase


@allure.feature('登录模块')
class TestLogin:
    @allure.story('登录正常模块')
    @pytest.mark.parametrize('params', get_testcase_yaml(FILE_PATH['LOGIN']))
    def test_login01(self, params):
        RequestBase().specification_yaml(params)

    # @allure.story('登录异常模块')
    # @pytest.mark.parametrize('params', get_testcase_yaml(FILE_PATH['LOGIN']))
    # def test_login02(self, params):
    #     RequestBase().specification_yaml(params)

