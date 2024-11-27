import logging
import time
import traceback
import pytest
import requests
from selenium import webdriver

"""
conftest.py的特点:
pytest 会默认读取 conftest.py里面的所有 fixture
conftest.py 文件名称是固定的，不能改动
conftest.py 只对同一个 package 下的所有测试用例生效
不同目录可以有自己的 conftest.py，一个项目中可以有多个 conftest.py
测试用例文件中不需要手动 import conftest.py，pytest 会自动查找
"""

"""
fixtrue的优势
1. 命名方式灵活，不限于setup和teardown两种命名
2. conftest.py可以实现数据共享，不需要执行import 就能自动找到fixture
3. scope=module，可以实现多个.py文件共享前置
4. scope=“session” 以实现多个.py 跨文件使用一个 session 来完成多个用例
"""

"""
如果用例执行前需要先登录获取token值，就要用到conftest.py文件了
作用：conftest.py 配置里可以实现数据共享，不需要import导入 conftest.py，pytest用例会自动查找
scope参数为session，那么所有的测试文件执行前执行一次
scope参数为package：主要应用于每个包下的fixture。
scope参数为module，那么每一个测试文件执行前都会执行一次conftest文件中的fixture
scope参数为class，那么每一个测试文件中的测试类执行前都会执行一次conftest文件中的fixture
scope参数为function，那么所有文件的测试用例执行前都会执行一次conftest文件中的fixture
"""

"""
fixture里面有个scope参数可以控制fixture的作用范围：默认取值为function（函数级别），控制范围的排序为：session > module > class > function

function：每一个函数或方法都会调用
class：每一个类调用一次，一个类中可以有多个方法
module：每一个.py文件调用一次，该文件内又有多个function和class
session：多个文件调用一次，可以跨.py文件调用（通常这个级别会结合conftest.py文件使用）
"""


# 获取到登录请求返回的ticket值，@pytest.fixture装饰后，testcase文件中直接使用函数名"login_ticket"即可得到ticket值
@pytest.fixture(scope="session")
def login_ticket():
    header = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    params = {
        "loginId": "username",
        "pwd": "password",
    }
    url = 'http://testxxxxx.xx.com/doLogin'
    logging.info('开始调用登录接口:{}'.format(url))
    res = requests.post(url, data=params, headers=header, verify=False)  # verify：忽略https的认证
    try:
        ticket = res.headers['Set-Cookie']
    except Exception as ex:
        logging.error('登录失败！接口返回：{}'.format(res.text))
        traceback.print_tb(ex)
    logging.info('登录成功，ticket值为：{}'.format(ticket))
    return ticket


# 测试一下conftest.py文件和fixture的作用
@pytest.fixture(scope="session")
def login_test():
    print("运行用例前先登录！")

    # 使用yield关键字实现后置操作，如果上面的前置操作要返回值，在yield后面加上要返回的值
    # 也就是yield既可以实现后置，又可以起到return返回值的作用
    yield "runBeforeTestCase"
    print("运行用例后退出登录！")


"""
4）session级别(使用conftest.py共享fixture)
当fixture的scope定义为session时，是指在当前目录下的所有用例之前和之后执行fixture对应的操作

fixture为session级别是可以跨.py模块调用的，也就是当我们有多个.py文件的用例的时候，如果多个用例只需调用一次fixture，那就可以设置为scope="session"，并且写到conftest.py文件里

使用方式：

① 定义测试用例文件

② 在指定目录下创建conftest.py（固定命名，不可修改）文件，然后在conftest.py文件中定义fixture方法，将scope指定为session，此时在当前目录下只要有一个用例使用了此fixture，则就会在当前目录下所有用例之前和之后会执行fixture定义的对应的操作。

@pytest.fixture(scope="session")
def session_auto():
    #session级别的fixture,针对该目录下的所有用例都生效
    print("\n---session级别的用例前置操作---")
    yield
    print("---session级别的用例后置操作---")
定义了session级别的fixture，存放于该用例文件的同一个目录下的conftest.py文件中，该目录下的任一用例文件中的任一测试用例，引用了这个session级别的fixture，则这个session级别的fixture会针对这整个用例文件生效。若存放在根目录下，则针对整个工程的所有用例都会生效。

class TestSessionAutoFixture:
    # session级别的fixture任意一个用例引用即可
    def test_session_auto_fixture_1(self, session_auto):
        print("session 1 print")

    def test_session_auto_fixture_2(self):
        print("session 1 print")


def test_session_auto_fixture():
    print("session 1 print")
"""


@pytest.fixture
def expensive_operation(request):
    if "last_in_group" in list(request._pyfuncitem.keywords.keys()):
        request.addfinalizer(cleanup_manager)
    time.sleep(0.5)


def cleanup_manager():
    print("\nCleaning up after expensive operation tests...\n")


@pytest.fixture(scope="class")
def web_driver(request):
    driver = webdriver.Firefox()

    def stop_driver():
        driver.close()

    request.addfinalizer(stop_driver)
    return driver


@pytest.fixture(scope="class")
def web_driver2(request):
    driver = webdriver.Chrome()
    yield driver
    driver.close()


@pytest.hookimpl()
def pytest_collection_modifyitems(items, config):
    items.sort(key=lambda test: "expensive_operation" in test.fixturenames)

    # reverse = True: Tests using "expensive_operation" are moved to the start of the list.
    # items.sort(key=lambda test: "expensive_operation" in test.fixturenames, reverse=True)
    # Usage
    # pytest -m web --collect-only

    if items:
        items[-1].add_marker("last_in_group")
