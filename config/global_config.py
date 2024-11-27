# 配置http 接口域名， 方便一套脚本用于多套环境运行
# HTTP_POST_HOST = 'https://jsonplaceholder.typicode.com/posts'
# HTTP_GET_HOST = 'https://jsonplaceholder.typicode.com/posts/1'

CAOLIAO_HTTP_POST_HOST = "https://cli.im"
CAOLIAO_HTTP_GET_HOST = "https://nc.cli.im"

BAIDU_HTTP_GET_HOST = "https://baidu.com"


class g_var(object):
    _global_dict = {}

    def set_dict(self, key, value):
        self._global_dict[key] = value

    def get_dict(self, key):
        return self._global_dict[key]

    def show_dict(self):
        return self._global_dict

