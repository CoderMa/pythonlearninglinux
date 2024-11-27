import os
import time
import pytest
# from selenium import webdriver
from selenium.webdriver.common.by import By
# from testcases.web.nginx import nginxServer, NginxConfig
from testcases.web.nginx import NginxConfig, nginxServer
from utils.waitutil import wait_for


@pytest.mark.web
class TestWeb(object):

    def test_page_is_up(self, web_driver, expensive_operation):
        # driver = webdriver.Chrome()
        web_driver.get("https://convertlive.com/c/convert/data-size")
        assert "converter" in web_driver.title, "Cannot detect website being available"

    def test_convert_Mb_to_mb(self, web_driver):
        web_driver.get("https://convertlive.com/c/convert/data-size")
        input_field = web_driver.find_element(By.ID, "convert-value")
        input_field.clear()
        input_field.send_keys("350")
        web_driver.find_element(By.ID, "convert-submit").click()

        # time.sleep(0.5)
        def found_element():
            return web_driver.find_element(By.CLASS_NAME, "result-to").text.strip() != ""

        wait_for(found_element, timeout=10, msg="Cannot detect the result in time")
        # or
        wait_for(lambda: web_driver.find_element(By.CLASS_NAME, "result-to").text.strip() != "", timeout=10,
                 msg="Cannot detect the result in time")

        result_field = web_driver.find_element(By.CLASS_NAME, "result-to")
        assert "2936" in result_field.text, "Cannot detect correct result for conversion"

    def test_temp(self, expensive_operation):
        print("expensive_operation")
        assert True

    # @pytest.mark.xfail(2 > 1, reason="windows unsupported")
    def test_local_site(self, web_driver):
        config = NginxConfig(location=os.path.join(os.getcwd(), "testcases", "web"))

        with nginxServer(config):
            web_driver.get("http://localhost:8090")
            assert "Trombone" in web_driver.title, "Cannot detect web page"

        # with nginxServer(os.path.join(os.getcwd(), "testcases", "web")):
        #     web_driver.get("http://localhost:8090")
        #     assert "text" in web_driver.title, "Cannot detect web page"


if __name__ == '__main__':
    pytest.main(['-vs', '/home/majilei/work/pythonlearning/testcases/web/test_web.py::test_local_site'])

