#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-
@desc: ...
"""
import os


class CommandError(Exception):
    pass


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    # utility = ManagementUtility(argv)
    # utility.execute()
    from yzrpc.commands import CommandUtility
    if argv[0] == 'yzrpc':
        utility = CommandUtility()
    else:
        utility = CommandUtility(
            command_dir=os.path.join(os.path.dirname(__file__), "commands"),
            module_path="yzcore.core.management.commands"
        )
    utility.run_from_argv(argv)
