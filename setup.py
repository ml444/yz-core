#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-
@desc: ...
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yzcore",  # Replace with your own username
    version="0.0.3",
    author="cml",
    author_email="fu477521@163.com",
    description="An ID generator for distributed microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fu477521/yzcore.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.8',
    install_requires=[
        "fastapi>=0.61.1",
        "sqlalchemy>=1.3.19",
        "uvicorn>=0.11.8",
        "orjson>=3.3.1"
    ]
)