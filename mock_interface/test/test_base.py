# tests/base.py
import multiprocessing
import time
# from . import api_server
import os, sys
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_PATH)
import pytest

class TestApiServer():
    """
    Test case class that sets up an HTTP server which can be used within the tests
    """
    def setup_class(self):
        self.api_server_process = multiprocessing.Process(
            target=exit_api_server
        )
        self.api_server_process.start()
        time.sleep(0.1)
        # os.system(f"python {os.path.join(BASE_PATH, 'manage.py')} runserver")
        pass

    def teardown_class(self):
        self.api_server_process.terminate()
        # os._exit(0)
        pass

    def test01(self):
        time.sleep(20)
        print("test01……")

def exit_api_server():
    os.system(f"python {os.path.join(BASE_PATH, 'manage.py')} runserver")       