import allure
import pytest

from dome.base.apiutil import RequestBase
from dome.common.readyaml import get_testcase_yaml
from dome.conf.setting import FILE_PATH


@allure.feature('商品管理')
class TestLogin:

    @allure.story('获取商品列表')
    @pytest.mark.parametrize('params', get_testcase_yaml(FILE_PATH['PRODUCT']))
    def test_get_product_list(self, params):
        RequestBase().specification_yaml(params)

    @allure.story('获取商品详情信息')
    @pytest.mark.parametrize('params', get_testcase_yaml(FILE_PATH['PRODUCTDetail']))
    def test_get_product_detail(self, params):
        RequestBase().specification_yaml(params)
