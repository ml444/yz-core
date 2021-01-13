# readme-template

--------------

## Introduction

Introduction 部分用于阐述项目基本情况和功能（是什么，用来做什么的）。


代码结构介绍：
```
.
├── docs		说明文档、接口文档等文档的存放目录
├── migrations		数据表迁移文件存放目录
├── src
│   ├── app		应用程序主代码的目录
│   │   ├── controllers 控制层：封装数据交互操作
│   │   ├── models	模型层：实现数据表与模型的定义
│   │   └── views	视图层：接口定义层
│   ├── conf		配置文件的存放目录
│   ├── const		公共常量存放目录
│   ├── core		核心代码的存放目录
│   ├── main.py		程序的入口文件
│   ├── settings.py	程序的设置文件
│   └── utils		抽离出的公共代码模块存放目录
└── tests		测试文件的存放目录
```

## Quick start

Quick Start 部分主要包括两部分内容：简易的安装部署说明(Deployment)和使用案例(Example)。特别是对于一些基础库，必须包括Example模块。


## Documentation

Documentation 部分是核心的文档，对于大型项目可以使用超链接，如使用以下这种形式：

For the full story, head over to the [documentation](https://git.k8s.io/community/contributors/devel#readme).

## 迁移
```
alembic init migrations                             # 创建迁移环境
alembic revision --autogenerate -m "commit content" # 自动生成迁移文件
alembic upgrade head                                # 升级到最近版本
alembic upgrade <revision_id>                       # 升级到指定版本
alembic downgrade <revision_id>                     # 回退到指定版本
```