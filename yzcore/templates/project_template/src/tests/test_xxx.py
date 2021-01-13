#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-
@desc: ...
"""
import time
import subprocess
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.background import BackgroundTask


# subprocess.check_output

async def signup(request):
    data = await request.json()
    username = data['username']
    email = data['email']
    task = BackgroundTask(send_welcome_email, to_address=email)
    print("---->", task)
    message = {'status': 'Signup successful'}
    return JSONResponse(message, background=task)

async def send_welcome_email(to_address):
    """"""
    time.sleep(5)
    print("====>", to_address)
    


routes = [
    Route('/user/signup', endpoint=signup, methods=['POST'])
]

app = Starlette(routes=routes)