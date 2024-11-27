import os
import shlex
import psutil
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class NginxServer(object):

    def __init__(self, config_file, location):
        self.nginx_location = location
        self.config_file = config_file
        self.process = None

    def __init__(self, config, location):
        self.nginx_location = location
        config.write_to("/tmp/generated_config.cfg")
        self.config_file = "/tmp/generated_config.cfg"

        self.process = None

    def start(self):
        """
        self.nginx_location refers to the path of the Nginx executable.
        -p . sets the prefix directory for Nginx, usually the current directory.
        -c {config_file} specifies the path to the Nginx configuration file.

        shlex.split(command): Safely splits the command into a list of arguments, preventing errors caused by spaces or special characters.
        psutil.Popen: Starts the Nginx process in the current working directory (cwd=os.getcwd()) while providing access to process management via the psutil library.
        """
        command = "{} -p . -c {}".format(self.nginx_location, self.config_file)
        logger.info(f"Starting Nginx Server {command}")
        self.process = psutil.Popen(shlex.split(command), cwd=os.getcwd())

    def stop(self):
        logger.info("Stopping Nginx server...")
        if self.process and self.process.is_running():
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except psutil.TimeoutExpired:
                logger.error("Failed to stop server in time, killing it...")
                self.process.kill()
            finally:
                self.process = None


@contextmanager
def nginxServer(config_file, location="/usr/sbin/nginx"):
    server = NginxServer(config_file, location)
    try:
        server.start()
        yield server
    finally:
        server.stop()


class NginxConfig(object):

    def __init__(self,
                 processes=1,
                 daemon=False,
                 error_log="nginx_error.log",
                 worker_connections=1024,
                 port=8090,
                 location="/var/www/html"
                 ):
        self.body = """
worker_processes {};
daemon {};
error_log {};
events {{
    worker_connections {};
}}

http {{
    server {{
        listen {};
        location / {{
            root {};
        }}
    }}
}}      
""".format(processes, "on" if daemon else "off", error_log, worker_connections, port, location)

    def to_string(self):
        return self.body

    def write_to(self, filename):
        with open(filename, "w") as fw:
            fw.write(self.body)
