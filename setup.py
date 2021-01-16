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
    version="0.0.7",
    author="cml",
    author_email="fu477521@163.com",
    description="An ID generator for distributed microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fu477521/yzcore.git",
    packages=setuptools.find_packages(),
    package_data={'yzcore': [
        'templates/project_template/*',
        'templates/project_template/docs/*',
        'templates/project_template/migrations/*',
        'templates/project_template/src/*',
        'templates/project_template/src/apps/*',
        'templates/project_template/src/conf/*',
        'templates/project_template/src/const/*',
        'templates/project_template/src/tests/*',
        'templates/project_template/src/utils/*',
        'templates/project_template/.gitignore',
    ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.8',
    install_requires=[
        "fastapi>=0.63",
        "sqlalchemy>1.3",
        "uvicorn>0.13",
        "orjson>=3.3.1"
    ]
)