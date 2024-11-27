import pytest
# from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By

"""
params表示fixture的参数化功能。
这里会有一个request参数，主要用来接收fixture的返回结果。并通过request.param返回结果内容。
"""
"""
ids
　　ids表示在fixture对参数化的内容进行加上标识(自定义显示结果)，比如让别人知道这个传入的参数是什么意思。用于什么样的测试用例。默认是传参数内容：
"""

data = ['guest', 'test', 'admin']


@pytest.fixture(params=data, ids=['user=guest', 'user=test', 'user=admin'])
def login(request):  # request为内建fixture
    print('登录功能')
    # 使用request.param作为返回值供测试函数调用，params的参数列表中包含了多少元素，该fixture就会被调用几次，分别作用在每个测试函数上
    yield request.param   # request.param为固定写法
    print('退出登录')


stars = ["刘德华", "张学友", "黎明", "郭富城"]
# 利用列表生成式生成一个用例名称的列表
ids = [f"test-case-{d}" for d in range(len(stars))]


# 注：ids生成的用例名称数量一定要和用例数量一致，否则会报错。


@pytest.mark.parametrize("name", stars, ids=ids)
def test_multi_param(name):
    print(f"my name is {name}")


"""
2）用法二：提供灵活的类似setup和teardown功能
Pytest的fixture另一个强大的功能就是在函数执行前后增加操作，类似setup和teardown操作，但是比setup和teardown的操作更加灵活；具体使用方式是同样定义一个函数，然后用装饰器标记为fixture，然后在此函数中使用一个yield语句，yield语句之前的就会在测试用例之前使用，yield之后的语句就会在测试用例执行完成之后再执行。
常见的应用场景：@pytest.fixture可以用在selenium中测试用例执行前后打开、关闭浏览器的操作：
"""


@pytest.fixture()
def fixture_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


"""
3）用法三：利用pytest.mark.usefixtures叠加调用多个fixture
如果一个方法或者一个class用例想要同时调用多个fixture，可以使用@pytest.mark.usefixtures()进行叠加。注意叠加顺序，先执行的放底层，后执行的放上层。需注意：

① 与直接传入fixture不同的是，@pytest.mark.usefixtures无法获取到被fixture装饰的函数的返回值；

② @pytest.mark.usefixtures的使用场景是：被测试函数需要多个fixture做前后置工作时使用；
"""


@pytest.fixture
def func_1():
    print("用例前置操作---1")
    yield
    print("用例后置操作---1")


@pytest.fixture
def func_2():
    print("用例前置操作---2")
    yield
    print("用例后置操作---2")


@pytest.fixture
def func_3():
    print("用例前置操作---3")
    yield
    print("用例后置操作---3")


"""
4.Pytest fixture四种作用域
fixture(scope='function'，params=None，autouse=False，ids=None，name=None)
fixture里面有个scope参数可以控制fixture的作用范围：

function：每一个函数或方法都会调用
class：每一个类调用一次，一个类中可以有多个方法
module：每一个.py文件调用一次，该文件内又有多个function和class
session：多个文件调用一次，可以跨.py文件调用（通常这个级别会结合conftest.py文件使用）
"""


class Test_01:
    def test_01(self, login):
        print('---用例01---')
        print('登录的用户名：%s' % login)

    def test_02(self):
        print('---用例02---')

    # 2）用法二
    def test_baidu(self, fixture_driver):
        driver = fixture_driver
        driver.get("http://www.baidu.com")
        driver.find_element(By.ID, 'kw').send_keys("python fixture")
        driver.find_element(By.ID, 'su').click()

    # 3）用法三
    @pytest.mark.usefixtures("func_3")  # 最后执行func_3
    @pytest.mark.usefixtures("func_2")  # 再执行func_1
    @pytest.mark.usefixtures("func_1")  # 先执行func_1
    def test_func(self):
        print("这是测试用例")


if __name__ == '__main__':
    pytest.main(['-vs', 'test_pytest.py'])
    # pytest.main(['-vs', '--setup-show'])

"""
通过执行结果可以看到，我们的test_01一共执行了3次，每次都是不同的参数，参数也是通过login进行接收的。
"""
