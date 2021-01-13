#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-
@desc: ...
"""
import os
import sys
from yzcore.core.management import execute_from_command_line


def main():
    # os.environ.setdefault('YZCORE_SETTINGS_MODULE', '{{ project_name }}.settings')
    # try:
    #
    # except ImportError as exc:
    #     raise ImportError(
    #         "Couldn't import yzcore. Are you sure it's installed and "
    #         "available on your PYTHONPATH environment variable? Did you "
    #         "forget to activate a virtual environment?"
    #     ) from exc
    print(sys.argv)
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()