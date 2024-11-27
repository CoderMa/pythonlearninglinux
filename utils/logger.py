import logging
import configparser

config = configparser.ConfigParser()
config.read('..\\config\\config.ini')

print(config.sections())

# log_file = config['LOGGING']['log_file']
try:
    log_file = config['LOGGING']['log_file']
except KeyError as e:
    print(f"Missing configuration key: {e}")
    log_file = "..\\logs\\test.txt"

"""
常见占位符：
%(asctime)s  时间戳
%(name)s 记录器名称
%(levelname)s 日志级别
%(message)s 日志内容
"""
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# logger = logging.getLogger(__name__)

class LoggerWrite(object):
    @staticmethod
    def write(logger):
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
