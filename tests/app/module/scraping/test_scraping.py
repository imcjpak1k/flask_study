import pytest
import unittest
from flask import Flask
import json
import sys
import os

from app.module.scraping import naver_stock
from app.module.date_util import current_date_fmt

def test_naver():
    naver_stock.daily_stock_price(code='051910', base_dt=current_date_fmt())
    pass