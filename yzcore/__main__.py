#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-
@desc: ...
"""
# import sys
# from yzrpc.commands import CommandUtility
#
#
# def main():
#     cmd = CommandUtility()
#     cmd.run_from_argv(sys.argv)
#
#
# if __name__ == '__main__':
#     main()

import sys
from yzcore.core.management import execute_from_command_line


def main():
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()