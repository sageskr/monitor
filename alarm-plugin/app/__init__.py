#!/usr/bin/env python
# -*-coding:utf8-*-
__author__ = 'Kairong'
from flask import Flask

app = Flask(__name__)
from app import views
