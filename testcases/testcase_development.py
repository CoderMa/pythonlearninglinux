import os
from xToolkit import xfile
from hctest_excel_to.excel_to import Excel
import allure
import requests
import pytest
import jsonpath
from string import Template

# from venv.exceltest.global_value import g_var
from config.global_config import g_var

file_path = "/venv/exceltest/testdata/testcases.xlsx"
# file_path = r"D:\workspace\pythonlearning\venv\exceltest\testdata\testcases.xlsx"
testlist = xfile.read(file_path).excel_to_dict(sheet=0)
print(testlist)


def test_stringtemplate():
    aa = {"token": "afdsagffdsgfadsf"}
    url = "http://baidu.com?token=${token}"
    test = Template(url).substitute(aa)
    print(test)  # "http://baidu.com?token=afdsagffdsgfadsf"


@pytest.mark.parametrize("case_info", testlist)
def test_case_exec(case_info):
    url = case_info["URL"]
    dic = g_var().show_dict()
    if "$" in url:
        url = Template(url).substitute(dic)

    rep = requests.request(
        url=case_info["URL"],
        method=case_info["METHOD_type"],
        params=eval(case_info["URL_params"]),
        data=eval(case_info["JSON_params"])
    )

    # 数据写入到对象中去
    if case_info["提取参数"] != None or case_info["提取参数"] != "":
        lst = jsonpath.jsonpath(rep.json(), '$..' + case_info["提取参数"])
        g_var().set_dict(case_info["提取参数"], lst[0])

    assert rep.status_code == case_info["expected_code"]


if __name__ == '__main__':
    # pytest 启动命令
    pytest.main(['-vs', '--capture=sys', 'testcase_development.py', '--clean-alluredir', '--alluredir=../testoutput/result'])
    os.system('copy ../environment.properties ../testoutput/result/environment.properties')
    # os.system(r"allure generate -c -o ../testoutput/report/")
    os.system("allure generate ../testoutput/result/ -o ../testoutput/report/ --clean")
    os.system("allure serve ../testoutput/result/")

    # test_stringtemplate()
