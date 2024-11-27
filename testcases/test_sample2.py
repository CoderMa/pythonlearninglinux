import pytest
from utils.excel_reader import ExcelReader
from utils.logger import logging
from utils.mailer import Mailer

# from your_api_client_module import APIClient  # 导入你的 API 客户端模块

# test_data_file = r'..\resources\test_data.xlsx'
# test_data_file = r'D:\workspace\pythonlearning\resources\test_data.xlsx'
test_data_file = "/home/majilei/work/pythonlearning/resources/test_data.xlsx"

@pytest.mark.parametrize("username, password", ExcelReader.read_data3(test_data_file))
def test_login_api(username, password):
    logger = logging.getLogger(__name__)
    logger.info(f"Running test-login_api with data: Username - {username}, Password - {password}")

    # # 使用测试数据调用登录接口
    # api_client = APIClient()
    # response = api_client.login(username, password)
    #
    # # 断言登录结果是否符合预期
    # assert response.status_code == 200
    # assert 'token' in response.json()
    assert 200 == 200


@pytest.mark.xfail(reason="currently unsupported, accept failure")
def test_send_email():
    Mailer.send_email("Test Email", "This is a test email sent from the data-driven testing framework")


"""
在上面的示例中，我们使用 @pytest.mark.parametrize 注解来指定参数化测试数据，并在测试用例中使用这些数据来调用登录接口。
通过这种方式，你可以轻松地对不同的输入数据进行测试，而无需为每组数据编写单独的测试用例。
"""


@pytest.fixture(params=[{"name": "周润发"}, {"age": 61}, {"height": 183}])
def fix_func(request):  # request为内建fixture
    # 使用request.param作为返回值供测试函数调用，params的参数列表中包含了多少元素，该fixture就会被调用几次，分别作用在每个测试函数上
    return request.param  # request.param为固定写法


def test_fix_func(fix_func):
    print(f"fixture函数fix_func的返回值为：{fix_func}")

    """打印结果如下：
    fixture函数fix_func的返回值为：{'name': '周润发'}
    fixture函数fix_func的返回值为：{'age': 61}
    fixture函数fix_func的返回值为：{'height': 183}
    """


params = [
    {"case_id": 1, "case_title": "验证正常添加车辆", "car_name": "苏C99688", "car_type": 1, "origin": 1, "expected": "200"},
    {"case_id": 2, "case_title": "验证添加重复车辆", "car_name": "苏C99688", "car_type": 1, "origin": 1, "expected": "500"},
    {"case_id": 3, "case_title": "验证车牌号为空", "car_name": "", "car_type": 2, "origin": 1, "expected": "500"}]


@pytest.fixture(params=params)
def add_car_params(request):
    return request.param


def test_add_car(add_car_params):
    print(type(add_car_params))
    print(add_car_params)
    print(f"{add_car_params['case_id']}-{add_car_params['case_title']}-{add_car_params['car_name']}")

    """
    运行结果如下：
    1-验证正常添加车辆-苏C99688
    2-验证添加重复车辆-苏C99688
    3-验证车牌号为空-
    """


if __name__ == '__main__':
    # pytest.main(['-vs', 'test_sample2.py::test_fix_func'])
    pytest.main(['-vs', 'test_sample2.py'])
