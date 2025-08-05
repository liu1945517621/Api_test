# -*- coding: utf-8 -*-
import sys
import time

import pytest

from common.readyaml import ReadYamlData
from conf.setting import dd_msg
import warnings
from dome.common.recordlog import logs

read = ReadYamlData()


@pytest.fixture(scope="session", autouse=True)
def clear_extract_data():
    """清除yaml数据"""
    read.clear_yaml_data()


@pytest.fixture(scope="session", autouse=True)
def fixture_test():
    """前后置操作"""
    logs.info('----------接口测试开始------------')
    sys.stdout.flush()  # 强制刷新
    yield
    logs.info('-----------接口测试结束-----------')
    sys.stdout.flush()  # 强制刷新
