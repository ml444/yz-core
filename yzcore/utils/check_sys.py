#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-
@desc: ...
"""
import os
import sys


def platform_check():
    msg = ''
    if sys.platform.startswith(('dragonfly', 'freebsd')):
        msg = 'pkg install'
    elif sys.platform == 'win32':
        msg += '#install-imagemagick-on-windows'
    elif sys.platform == 'darwin':
        mac_pkgmgrs = {'brew': 'brew install freetype imagemagick',
                       'port': 'port install imagemagick'}
        for pkgmgr in mac_pkgmgrs:
            with os.popen('which ' + pkgmgr) as f:
                if f.read().strip():
                    msg = mac_pkgmgrs[pkgmgr]
                    break
        else:
            msg += '#install-imagemagick-on-mac'
    elif hasattr(sys.platform, 'linux_distribution'):
        distname, _, __ = sys.platform.linux_distribution()
        distname = (distname or '').lower()
        if distname in ('debian', 'ubuntu'):
            msg = 'apt-get install libmagickwand-dev'
        elif distname in ('fedora', 'centos', 'redhat'):
            msg = 'yum install ImageMagick-devel'
    raise ImportError('MagickWand shared library not found.\n'
                      'You probably had not installed ImageMagick library.\n'
                      'Try to install:\n  ' + msg)
