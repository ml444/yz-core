#!/usr/bin/env python3.5+
# -*- coding: utf-8 -*-
"""
@auth: cml
@date: 2019-07-10
@desc: ...
"""
import logging


class NotSetFilter(logging.Filter):

    def filter(self, record):
        return False


class DebugFilter(logging.Filter):

    def filter(self, record):
        level = record.levelname.upper()
        if level == 'DEBUG':
            return True
        return False


class InfoFilter(logging.Filter):

    def filter(self, record):
        level = record.levelname.upper()
        # if level in {'INFO', 'WARNING', 'ERROR'}:
        if level == 'INFO':
            return True
        return False


class WarningFilter(logging.Filter):

    def filter(self, record):
        level = record.levelname.upper()
        if level == 'WARNING':
            return True
        return False


class ErrorFilter(logging.Filter):

    def filter(self, record):
        level = record.levelname.upper()
        if level == 'ERROR':
            return True
        return False


class CriticalFilter(logging.Filter):

    def filter(self, record):
        level = record.levelname.upper()
        if level == 'CRITICAL':
            return True
        return False