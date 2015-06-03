#!/usr/bin/python
import os.path
import sys
sys.path.append(os.path.pardir)
from server import Server


if __name__ == "__main__":
    server = Server()
    server.run()