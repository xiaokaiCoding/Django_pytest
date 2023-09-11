# tests/base.py
import multiprocessing
import time
import unittest
# from . import api_server
import os, sys
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_PATH)

class TestApiServer():
    """
    Test case class that sets up an HTTP server which can be used within the tests
    """
    def setup_class(self):
        os.system(r"python ")
        pass

    def teardown_class(cls):
        pass

    def test01(self):
        print("test01……")