import os
import sys
import logging
from flask import Blueprint, request, session, jsonify, g, render_template
# 비밀번호 hash
# from werkzeug import generate_password_hash, check_password_hash

# plot import
import io
import random
from flask import Response, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


this = Blueprint('sample', __name__, url_prefix='/sample')
# print(sys.path)

# path추가 전
# ['C:\\myproject\\stock', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib', 'C:\\Python37', 'C:\\Python37\\lib\\site-packages']
# path 추가 후 
# ['C:\\myproject\\stock', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib', 'C:\\Python37', 'C:\\Python37\\lib\\site-packages', 'C:\\myproject\\stock']
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
# 등록된 결과만 보면 배열의 첫번째 위치는 flaskr.py를 실행시킨 위치 즉, root경로 이므로 아래처럼 사용해도 됨.
sys.path.append(sys.path[0])
# print(sys.path)
# from app.module import login_required
# from app.module.decorator import login_required as reqLogin
from app.module.request_util import get_req_data
from app.module.decorator.login_required import LoginRequired
from app.module.decorator.unique_key import UniqueKey
# from flaskr import get_flask_app

# C:\myproject\stock>python flaskr.py
# Traceback (most recent call last):
#   File "flaskr.py", line 92, in <module>
#     app = flask_app()
#   File "flaskr.py", line 83, in flask_app
#     module = importlib.import_module(blueprint)
#   File "C:\Python37\lib\importlib\__init__.py", line 127, in import_module
#     return _bootstrap._gcd_import(name[level:], package, level)
#   File "<frozen importlib._bootstrap>", line 1006, in _gcd_import
#   File "<frozen importlib._bootstrap>", line 983, in _find_and_load
#   File "<frozen importlib._bootstrap>", line 967, in _find_and_load_unlocked
#   File "<frozen importlib._bootstrap>", line 677, in _load_unlocked
#   File "<frozen importlib._bootstrap_external>", line 728, in exec_module
#   File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
#   File "C:\myproject\stock\app\routes\user.py", line 8, in <module>
#     from flaskr import get_flask_app
#   File "C:\myproject\stock\flaskr.py", line 92, in <module>
#     app = flask_app()
#   File "C:\myproject\stock\flaskr.py", line 84, in flask_app
#     flask_app.register_blueprint(module.this)
# AttributeError: module 'app.routes.user' has no attribute 'this'
# (주의) 이 위치에서 Blueprint 호출하면 위와 같은 오류가 발생한다.
# 정확한 이유는 알수 없으나 flaskr를 찾고하기 위해서 path를 추가하면서 path정보가 변경된듯 한다.
# this = Blueprint('user', __name__, url_prefix='/user')

# app = get_flask_app()    
# print(app)

@this.route('/test')
# @LoginRequired
def test():
    return "test page"

@this.route('/uniquekey')
@UniqueKey
def index(uniquekey):
    """
    unique key decorator

    """
    return uniquekey

@this.route('/go_plot')
def go_plot_png():
    return render_template("sample/plot.html")



@this.route('/plot.stock.png')
def plot_stock_png():
    import pandas as pd
    import matplotlib.pyplot as plt 
    
    xs = range(100)
    kospi_stock_data    = [random.randint(1, 50) for x in xs]
    overseas_stock_data = [random.randint(1, 50) for x in xs]

    compare_stock_dict = {
        'KOSPI200'	: kospi_stock_data,
        'SPI@SPX'	: overseas_stock_data,
    }
    
    price_df 	= pd.DataFrame(compare_stock_dict)
    # 이전의 값으로 NA값 대체
    price_df	= price_df.fillna(method="ffill")
    if price_df.isnull().values.any():
        # 이후 값으로 NA값 대체
        price_df	= price_df.fillna(method="bfill")

    import matplotlib.pyplot as plt
    plt.figure(figsize=(2, 2))
    # plt.plot(price_df.get('KOSPI200'))
    # plt.plot(price_df.get('SPI@SPX'))
    plt.plot(price_df.get('KOSPI200') / price_df.get('KOSPI200').iloc[0] * 100)
    plt.plot(price_df.get('SPI@SPX')  / price_df.get('SPI@SPX').iloc[0] * 100)
    plt.legend(loc=0)
    # plt.grid(True, color='0.7', linestyle=':', linewidth=1)
    output = io.BytesIO()
    plt.savefig(output, format='png', dpi=200)
    
    # fig = create_figure()
    # plt.Figure(output)
    # print(dir(plt))

    # plt.FigureCanvas().print_png
    # plt.FigureCanvas().print_png(output)
    # FigureCanvas(fig).print_png(output)
    # return Response(output.getvalue(), mimetype='image/png')
    output.seek(0)
    return send_file(output, mimetype='image/png')

@this.route('/plot.png')
def plot_png():
    # import matplotlib.pyplot as plt 
    # plt.FigureCanvas().print_png(output)

    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


