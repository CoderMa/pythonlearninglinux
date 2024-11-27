import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest
from utils.excel_reader import ExcelReader
from utils.logger import logging, LoggerWrite

from utils.mailer import Mailer

# test_data_file = r'..\resources\test_data.xlsx'
# test_data_file = r'D:\workspace\pythonlearning\resources\test_data.xlsx'
test_data_file = "/home/majilei/work/pythonlearning/resources/test_data.xlsx"



# data1 = ExcelReader.read_data(test_data_file)
# data2 = ExcelReader.read_data2(test_data_file)
# data3 = ExcelReader.read_data3(test_data_file)

@pytest.mark.parametrize("data", ExcelReader.read_data3(test_data_file))
def test_data_driven(data):
    print(data)
    logger = logging.getLogger(__name__)
    logger.info(f"Running test-test_data_driven with data: {data}")
    logger.debug(f"logger debug: {data}")
    logger.warning(f"logger warning: {data}")
    logger.error(f"logger error: {data}")
    logger.critical(f"logger critical: {data}")

    # logger = logging.getLogger(__name__)
    # LoggerWrite.write(logger)

    # Your test logic here

    assert True


@pytest.mark.xfail(reason="currently not implement yet, accept failure right now.")
def test_send_email():
    Mailer.send_email("Test Email", "This is a test email sent from the data-driven testing framework")


@pytest.mark.parametrize("argument", ["", "-r", "-t", "-rt"])
@pytest.mark.skipif(sys.platform.startswith("win"), reason="Skipping since cannot be run on windows")
@pytest.mark.notrunning
def test_ls_order(argument):
    try:
        folder_path = "/tmp/testfolder"
        file_path1 = os.path.join(folder_path, "first.txt")
        file_path2 = os.path.join(folder_path, "second.doc")

        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        Path(file_path1).touch()
        time.sleep(0.1)
        Path(file_path2).touch()

        command = ["ls", argument, folder_path]
        arguments = " ".join(x for x in command if x != "")
        # arguments = arguments.split(" ")

        result = subprocess.run(shlex.split(arguments), stdout=subprocess.PIPE)
        print("result: [{}]".format(result.stdout))
        assert result.stdout.decode("UTF-8").startswith(
            "first.txt" if argument in ["",
                                        "-rt"] else "second.doc"), f"Output of ls with argument '{argument}' was wrong!"
    finally:
        shutil.rmtree(folder_path)


@pytest.mark.parametrize("argument", ["", "/O:N", "/O:D", "/O:S"])
@pytest.mark.skipif(not sys.platform.startswith("win"), reason="skipping since cannot be run on none-windows")
def test_ls_order(argument):
    try:
        folder_path = r"C:\tmp\testfolder"
        file_path1 = os.path.join(folder_path, "first.txt")
        file_path2 = os.path.join(folder_path, "second.doc")

        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        Path(file_path1).touch()
        time.sleep(0.1)
        Path(file_path2).touch()

        """
        在 Windows 上运行 subprocess.run(["dir"]) 是不正确的，因为 dir 是一个内置于命令提示符（cmd）的命令，而不是独立的可执行程序。subprocess.run() 需要可执行文件或直接调用命令解释器。
        正确的用法
        要运行 dir 命令，可以通过调用 cmd 来实现：
        # 使用 cmd 调用 dir
        # result = subprocess.run(["cmd", "/c", "dir"], capture_output=True, text=True)
        """

        command = ["cmd", "/c", "dir", argument, r"C:\tmp\testfolder"]
        # arguments = " ".join(x for x in command if x != "")
        # # arguments = arguments.split(" ")

        # result = subprocess.run(shlex.split(arguments), stdout=subprocess.PIPE)
        result = subprocess.run(command, stdout=subprocess.PIPE)
        print("result: [{}]".format(result.stdout))
        assert result.stdout
        # assert result.stdout.decode("UTF-8").startswith(
        #     "first.txt" if argument in ["", "-rt"] else "second.doc"), "Output of dir with argument '{}' was wrong!".format(argument)
    finally:
        shutil.rmtree(folder_path)


if __name__ == '__main__':
    # pytest.main(['-vs', 'test_sample.py'])

    # 运行包含order的case
    # pytest test-sample.py -k order

    # 运行marker为notrunning的case
    # pytest test-sample.py -m notrunning

    # 运行没有marker为notrunning的case
    # pytest test-sample.py -m "not notrunning"

    # pytest.main(['-vs', 'test_sample.py'])
    pytest.main(['-vs', '--capture=sys', 'test_sample.py', '--clean-alluredir', '--alluredir=../testoutput/result'])
    os.system('copy ../environment.properties ../testoutput/result/environment.properties')
    os.system("allure generate ../testoutput/result/ -o ../testoutput/report/ --clean")

    # os.system("allure serve ../testoutput/result/")
    os.system("allure open ../testoutput/report/")
