import shutil
import sys
import io
import os
import pytest
import webbrowser
from conf.setting import REPORT_TYPE
from dome.common import assertions

if __name__ == '__main__':
    pytest.main()
    os.system(f'allure serve ./report/temp')
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    # if REPORT_TYPE == 'allure':
    #     pytest.main(
    #         ['-s', '-v', '--alluredir=./report/temp', './testcase', '--clean-alluredir',
    #          '--junitxml=./report/results.xml'])
    #
    #     shutil.copy('./environment.xml', './report/temp')
    #     os.system(f'allure serve ./report/temp')
    #
    # elif REPORT_TYPE == 'tm':
    #     pytest.main(['-vs', '--pytest-tmreport-name=testReport.html', '--pytest-tmreport-path=./report/tmreport'])
    #     webbrowser.open_new_tab(os.getcwd() + '/report/tmreport/testReport.html')
