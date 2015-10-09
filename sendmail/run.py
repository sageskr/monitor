#!/usr/bin/env python
# -*-coding:utf8-*-
__author__ = 'Kairong'
from app import config
from app import app
app.run(debug=True,port=config.Srv_port)