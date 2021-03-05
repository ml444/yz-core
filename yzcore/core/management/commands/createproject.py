#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2021/3/5
@desc: ...
"""
from yzrpc.commands.createproject import Command as Cmd

class Command(Cmd):
    """"""
    template_dir = "/Users/edz/cmlpy/yz-core/yzcore/templates/project_template_rpc"

    def handle(self, **options):
        print("=====wahhahaahahahh=====")
        return super().handle(**options)
