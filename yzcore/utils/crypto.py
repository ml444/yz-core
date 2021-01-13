#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-
@desc: ...
"""
"""
Django's standard crypto functions and utilities.
"""
import hashlib
import hmac
import random
import time

from .encoding import force_bytes
# from yzcore.core.default_settings import get_settings
#
# settings = get_settings()

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn('A secure pseudo-random number generator is not available '
                  'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False



def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Return a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    # if not using_sysrandom:
    #     # This is ugly, and a hack, but it makes things better than
    #     # the alternative of predictability. This re-seeds the PRNG
    #     # using a value that is hard for an attacker to predict, every
    #     # time a random string is required. This may change the
    #     # properties of the chosen random sequence slightly, but this
    #     # is better than absolute predictability.
    #     random.seed(
    #         hashlib.sha256(
    #             ('%s%s%s' % (random.getstate(), time.time(), settings.SECRET_KEY)).encode()
    #         ).digest()
    #     )
    return ''.join(random.choice(allowed_chars) for i in range(length))


def constant_time_compare(val1, val2):
    """Return True if the two strings are equal, False otherwise."""
    return hmac.compare_digest(force_bytes(val1), force_bytes(val2))


def pbkdf2(password, salt, iterations, dklen=0, digest=None):
    """Return the hash of password using pbkdf2."""
    if digest is None:
        digest = hashlib.sha256
    dklen = dklen or None
    password = force_bytes(password)
    salt = force_bytes(salt)
    return hashlib.pbkdf2_hmac(digest().name, password, salt, iterations, dklen)
