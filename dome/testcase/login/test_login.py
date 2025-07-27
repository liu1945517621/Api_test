import pytest
from dome.common import readyaml

class TestLogin:
    @pytest.mark.parametrize('params', readyaml.get_testcase_yaml('loginName.yaml'))
    def test_login(self, params):
        print('获得参数:',  params)
