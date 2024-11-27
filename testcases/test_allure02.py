import os
import random
import sys
import time

import allure
import pytest


# 1. xfail
@allure.feature('test_xfail_expected_failure')
@pytest.mark.xfail(reason='该功能尚未实现')
def test_xfail_expected_failure():
    print("该功能尚未实现")
    assert False


@allure.feature('test_xfail_unexpected_pass')
@pytest.mark.xfail(reason='该Bug尚未修复')
def test_xfail_unexpected_pass():
    print("该Bug尚未修复")
    assert True


# 2. skipif
# 当条件为True则跳过执行
@allure.feature("test_skipif")
@pytest.mark.skipif("darwin" in sys.platform, reason="如果操作系统是Mac则跳过执行")
def test_skipif():
    print("操作系统是Mac，test_skipif()函数跳过执行")


# 3. paramtrize
@allure.step
def simple_step(step_param1, step_param2=None):
    pass


@pytest.mark.parametrize('param1', [True, False], ids=['1', '2'])
def test_parameterize_with_id(param1):
    simple_step(param1)


@pytest.mark.parametrize('param1', [True, False])
@pytest.mark.parametrize('param2', ['1', '2'])
def test_parametrize_with_two_parameters(param1, param2):
    simple_step(param1, param2)


# 4.feature

# 模块名称，功能点描述

# 5.step
@allure.step("步骤二")
def passing_step():
    pass


@allure.step("步骤三")
def step_with_nested_steps():
    nested_step()


@allure.step("步骤四")
def nested_step():
    nested_step_with_arguments(1, 'abc')


@allure.step("步骤五")
def nested_step_with_arguments(arg1, arg2):
    pass


@allure.step("步骤一")
def test_with_nested_steps():
    passing_step()
    step_with_nested_steps()


@pytest.fixture
def attach_file_in_module_scope_fixture_with_finalizer(request):
    allure.attach('在fixture前置操作里面添加一个附件txt', 'fixture前置附件', allure.attachment_type.TEXT)

    def finalizer_module_scope_fixture():
        allure.attach('在fixture后置操作里面添加一个附件txt', 'fixture后置附件', allure.attachment_type.TEXT)

    request.addfinalizer(finalizer_module_scope_fixture)


def test_with_attachments_in_fixture_and_finalizer(attach_file_in_module_scope_fixture_with_finalizer):
    pass


def test_multiple_attachments():
    allure.attach('<head></head><body>html page</body>', 'Attach with HTML type', allure.attachment_type.HTML)
    allure.attach.file(r'D:\workspace\pythonlearning\resources\test.html', attachment_type=allure.attachment_type.HTML)


# 7.description
# 描述类信息，比如对函数的描述，说明这个函数的作用，如：注册接口。
# 语法一：@allure.description()
# 语法二：@allure.description_html()#
@allure.description_html("""
<h1>这是html描述</h1>
<table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th>
    <th>Age</th>
  </tr>
  <tr align="center">
    <td>jade</td>
    <td>mr</td>
    <td>18</td>
  </tr>
  <tr align="center">
    <td>road</td>
    <td>Tester</td>
    <td>18</td>
  </tr>
</table>
""")
def test_html_description():
    assert True


@allure.description("""多行描述""")
def test_description_from_decorator():
    assert 42 == int(6 * 7)


def test_unicode_in_docstring_description():
    """在函数下方描述也可"""
    assert 42 == int(6 * 7)


# 8.title
# 添加测试用例标题，通俗来讲就是将函数名直接改成我们想要的，使得测试用例的标题更具有可读性
# 支持占位符传递关键字参数（动态标题，结合@pytest.mark.parametrize使用）
@allure.title("断言2+2=4")
def test_with_a_title():
    assert 2 + 2 == 4


@allure.title("动态标题: {param1} + {param2} = {expected}")
@pytest.mark.parametrize('param1,param2,expected', [(2, 2, 4), (1, 2, 5)])
def test_with_parameterized_title(param1, param2, expected):
    assert param1 + param2 == expected


@allure.title("这是个动态标题，会被替换")
def test_with_dynamic_title():
    assert 2 + 2 == 4
    allure.dynamic.title('测试结束，做为标题')


# 9.link
# 将测试报告与缺陷跟踪或测试管理系统整合，@allure.link、@allure.issue和@allure.testcase。
@allure.link('https://www.cnblogs.com/mrjade/')
def test_with_link():
    pass


@allure.link('https://www.cnblogs.com/mrjade/', name='点击进入mrjade博客园')
def test_with_named_link():
    pass


@allure.issue('https://github.com/allure-framework/allure-python/issues/642', 'bug issue链接')
def test_with_issue_link():
    pass


@allure.testcase("https://www.cnblogs.com/mrjade/", '测试用例地址')
def test_with_testcase_link():
    pass


# 10.Retries
# Allure允许测试报告中显示单个测试运行期间重新执行的测试的信息，以及一段时间内测试执行的历史,需与Pytest插件结合使用。
# windows：pip install pytest-rerunfailures
# mac：pip3 install pytest-rerunfailures
@allure.step
def passing_step():
    pass


@allure.step
def flaky_broken_step():
    if random.randint(1, 5) != 1:
        raise Exception('Broken!')


"""需安装【pip3 install pytest-rerunfailures】"""


@pytest.mark.flaky(reruns=3, reruns_delay=1)  # 如果失败则延迟1s后重试
def test_broken_with_randomized_time():
    passing_step()
    time.sleep(random.randint(1, 3))
    flaky_broken_step()


# 11.tags
"""
我们希望对执行的测试用例保持灵活性。Pytest允许使用标记修饰符@pytest.mark，Allure提供了3种类型的标记装饰符

BDD样式的标记装饰器
@allure.epic：敏捷里面的概念，定义史诗，往下是feature
@allure.feature：功能点的描述，理解成模块往下是story
@allure.story：故事，往下是title
优先级（严重程度）标记装饰器 根据严重程度来标记你的测试。严重程度装饰器，它使用一个allure.severity_level enum值作为参数。如：@allure.severity(allure.severity_level.TRIVIAL)
自定义标记装饰器
"""


@pytest.fixture(scope="session")
def login_fixture():
    print("前置登录")


@allure.step("步骤1")
def step_1():
    print("操作步骤1")


@allure.step("步骤2")
def step_2():
    print("操作步骤2")


@allure.step("步骤3")
def step_3():
    print("操作步骤3")


@allure.step("步骤4")
def step_4():
    print("操作步骤4")


@allure.epic("会员项目")
@allure.feature("登录")
class TestAllureALL:

    @allure.testcase("https://www.cnblogs.com/mrjade/", '测试用例,点我一下')
    @allure.issue("https://github.com/allure-framework/allure-python/issues/642", 'Bug 链接,点我一下')
    @allure.title("用户名错误")
    @allure.story("登录测试用例1")
    @allure.severity(allure.severity_level.TRIVIAL)  # 不重要的
    # @allure.severity(allure.severity_level.MINOR) # 轻微的
    # @allure.severity(allure.severity_level.BLOCKER)  # 阻塞的
    # @allure.severity(allure.severity_level.CRITICAL)  # 严重的
    # @allure.severity(allure.severity_level.NORMAL)  # 普通的
    def test_case_1(self):
        """
        公众号：测试工程师成长之路
        """
        print("测试用例1")
        step_1()
        step_2()

    @allure.title("用户名正确，密码错误")
    @allure.story("登录测试用例2")
    def test_case_2(self):
        print("测试用例2")
        step_1()
        step_3()


@allure.epic("订单项目")
@allure.feature("支付")
class TestAllureALL2:
    @allure.title("支付成功")
    @allure.story("支付测试用例例1")
    def test_case_1(self, login_fixture):
        print("支付测试用例例1")
        step_3()

    @allure.title("支付失败")
    @allure.story("支付测试用例例2")
    def test_case_2(self, login_fixture):
        print("支付测试用例例2")
        step_4()


"""
12.environment：环境信息

新建environment.properties文件
编写如下环境信息
systemVersion=Windows-10-10.0.19045-SP0
pythonVersion=3.8
allureVersion=2.13.5
baseUrl=http://192.168.1.1:8080
projectName=SIT
author=TesterRoad
将environment.properties放在项目根目录或其它目录，在执行测试用例时将其复制到allure-results目录下
"""

# --clean-alluredir:每次执行前清空数据，这样在生成的报告中就不会追加，只显示当前执行的用例
if __name__ == '__main__':
    pytest.main(['-s', '-q', 'test_allure02.py', '--clean-alluredir', '--alluredir=../testoutput/result'])
    # os.system('cp ../environment.properties ../testoutput/resultenvironment.properties')
    os.system('copy ../environment.properties ../testoutput/resultenvironment.properties')
    # os.system(r"allure serve ../testoutput/result/")

    os.system(r"allure generate -c -o ../testoutput/report/")
    # os.system(r"allure open ../testoutput/report/")
