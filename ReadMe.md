# MD파일 TEST
## MD파일 TEST

https://flask-docs-kr.readthedocs.io/ko/latest/tutorial/dbinit.html

강의 : https://www.youtube.com/watch?v=WxGBoY5iNXY&t=748s

pip install Flask
pip install mybatis-mapper2sql
pip install pytest
pip install beautifulsoup4
pip install PyMySQL
pip install pymysql-pool
pip install SQLAlchemy
pip install Flask-SQLAlchemy
pip install Flask-Bcrypt      #암호화
        https://github.com/maxcountryman/flask-bcrypt
        https://flask-bcrypt.readthedocs.io/en/latest/
pip install APScheduler
pip install Flask-APSchedulerpip

왜안되지?? 무슨모듈이 없는거야??
>>> from flask.ext.bcrypt import Bcrypt
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'flask.ext'

이렇게 하니...된다.. ㅡㅡ;;
from flask_bcrypt import Bcrypt    


https://flask-docs-kr.readthedocs.io/ko/latest/patterns/viewdecorators.html


pip install bcrypt            #암호화

https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_textual_sql.htm
https://github.com/hhyo/mybatis-mapper2sql
https://pypi.org/project/mybatis-mapper2sql/
https://docs.sqlalchemy.org/en/13/intro.html#installation-guide
https://docs.sqlalchemy.org/en/13/orm/tutorial.html

https://www.sqlalchemy.org/
https://pypi.org/project/Flask-SQLAlchemy/
https://github.com/pallets/flask-sqlalchemy
https://flask-sqlalchemy.palletsprojects.com/en/2.x/

engine = create_engine("pymysql://root:fjfj1305@127.0.0.1:3306/stock", encoding='utf-8', echo=True)

C:\myproject\stock>pip list
Package            Version
------------------ -------
atomicwrites       1.3.0
attrs              18.2.0
beautifulsoup4     4.8.0
Click              7.0
colorama           0.4.1
cycler             0.10.0
Flask              1.1.1
Flask-MySQL        1.4.0
importlib-metadata 0.19
itsdangerous       1.1.0
Jinja2             2.10.1
kiwisolver         1.1.0
MarkupSafe         1.1.1
matplotlib         3.1.1
more-itertools     7.2.0
numpy              1.17.0
ordered-set        3.1.1
packaging          19.1
pdfkit             0.6.1
pdflatex           0.1.3
pip                19.2.2
pluggy             0.12.0
py                 1.8.0
PyLaTeX            1.3.0
PyMySQL            0.9.3
pyparsing          2.4.2
pytest             5.0.1
python-dateutil    2.8.0
python-pdf         0.37
quantities         0.12.3
selenium           3.141.0
setuptools         40.8.0
six                1.12.0
soupsieve          1.9.2
urllib3            1.25.3
virtualenv         16.7.2
wcwidth            0.1.7
Werkzeug           0.15.5
wfastcgi           3.0.0
zipp               0.5.2




C:\myproject\stock>pip list
Package            Version
------------------ -------
atomicwrites       1.3.0
attrs              18.2.0
beautifulsoup4     4.8.0
Click              7.0
colorama           0.4.1
cycler             0.10.0
Flask              1.1.1
Flask-MySQL        1.4.0
importlib-metadata 0.19
itsdangerous       1.1.0
Jinja2             2.10.1
kiwisolver         1.1.0
MarkupSafe         1.1.1
matplotlib         3.1.1
more-itertools     7.2.0
numpy              1.17.0
ordered-set        3.1.1
packaging          19.1
pdfkit             0.6.1
pdflatex           0.1.3
pip                19.2.2
pluggy             0.12.0
py                 1.8.0
PyLaTeX            1.3.0
PyMySQL            0.9.3
pyparsing          2.4.2
pytest             5.0.1
pytest-flask       0.15.0



<< pytest-flask 미설치시 다음과 같은 오류가 발생하는 경우.>>
C:\myproject\stock>pytest -v app_test.py
=============================================================================== test session starts ===============================================================================
platform win32 -- Python 3.7.3, pytest-5.0.1, py-1.8.0, pluggy-0.12.0 -- c:\python37\python.exe
cachedir: .pytest_cache
rootdir: C:\myproject\stock
collected 3 items

app_test.py::test_index ERROR                                                                                                                                                [ 33%]
app_test.py::test_login ERROR                                                                                                                                                [ 66%]
app_test.py::test_logout ERROR                                                                                                                                               [100%]

===================================================================================== ERRORS ======================================================================================
__________________________________________________________________________ ERROR at setup of test_index ___________________________________________________________________________
file C:\myproject\stock\app_test.py, line 11
  def test_index(client):
E       fixture 'client' not found
>       available fixtures: app, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, doctest_namespace, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

C:\myproject\stock\app_test.py:11
__________________________________________________________________________ ERROR at setup of test_login ___________________________________________________________________________
file C:\myproject\stock\app_test.py, line 16
  def test_login(client):
E       fixture 'client' not found
>       available fixtures: app, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, doctest_namespace, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

C:\myproject\stock\app_test.py:16
__________________________________________________________________________ ERROR at setup of test_logout __________________________________________________________________________
file C:\myproject\stock\app_test.py, line 21
  def test_logout(client):
E       fixture 'client' not found
>       available fixtures: app, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, doctest_namespace, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

C:\myproject\stock\app_test.py:21
================================================================================ warnings summary =================================================================================
c:\python37\lib\site-packages\jinja2\utils.py:485
  c:\python37\lib\site-packages\jinja2\utils.py:485: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated, and in 3.8 it will stop working
    from collections import MutableMapping

c:\python37\lib\site-packages\jinja2\runtime.py:318
  c:\python37\lib\site-packages\jinja2\runtime.py:318: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated, and in 3.8 it will stop working
    from collections import Mapping

-- Docs: https://docs.pytest.org/en/latest/warnings.html
======================================================================= 2 warnings, 3 error in 0.35 seconds =======================================================================

C:\myproject\stock>









C:\myproject\stock>pytest -v app_test.py
=============================================================================== test session starts ===============================================================================
platform win32 -- Python 3.7.3, pytest-5.0.1, py-1.8.0, pluggy-0.12.0 -- c:\python37\python.exe
cachedir: .pytest_cache
rootdir: C:\myproject\stock
plugins: flask-0.15.0
collected 1 item

app_test.py::test_index ERROR                                                                                                                                                [100%]

===================================================================================== ERRORS ======================================================================================
__________________________________________________________________________ ERROR at setup of test_index ___________________________________________________________________________

request = <SubRequest '_monkeypatch_response_class' for <Function test_index>>, monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000001B4939A49B0>

    @pytest.fixture(autouse=True)
    def _monkeypatch_response_class(request, monkeypatch):
        """Set custom response class before test suite and restore the original
        after. Custom response has `json` property to easily test JSON responses::

            @app.route('/ping')
            def ping():
                return jsonify(ping='pong')

            def test_json(client):
                res = client.get(url_for('ping'))
                assert res.json == {'ping': 'pong'}

        """
        if 'app' not in request.fixturenames:
            return

        app = getfixturevalue(request, 'app')
        monkeypatch.setattr(app, 'response_class',
>                           _make_test_response_class(app.response_class))
E       AttributeError: 'FlaskClient' object has no attribute 'response_class'

c:\python37\lib\site-packages\pytest_flask\plugin.py:96: AttributeError


















---------------------------------------
-- 함수의 파라미터를 체크하는거 같음... 확인필ㅇ././

from pytz import timezone, utc
import six

try:
    from inspect import signature
except ImportError:  # pragma: nocover
    from funcsigs import signature


    
    try:
        sig = signature(func)
    except ValueError:
        # signature() doesn't work against every kind of callable
        return

    for param in six.itervalues(sig.parameters):
        if param.kind == param.POSITIONAL_OR_KEYWORD:
            if param.name in unmatched_kwargs and unmatched_args:
                pos_kwargs_conflicts.append(param.name)
            elif unmatched_args:
                del unmatched_args[0]
            elif param.name in unmatched_kwargs:
                unmatched_kwargs.remove(param.name)
            elif param.default is param.empty:
                unsatisfied_args.append(param.name)
        elif param.kind == param.POSITIONAL_ONLY:
            if unmatched_args:
                del unmatched_args[0]
            elif param.name in unmatched_kwargs:
                unmatched_kwargs.remove(param.name)
                positional_only_kwargs.append(param.name)
            elif param.default is param.empty:
                unsatisfied_args.append(param.name)
        elif param.kind == param.KEYWORD_ONLY:
            if param.name in unmatched_kwargs:
                unmatched_kwargs.remove(param.name)
            elif param.default is param.empty:
                unsatisfied_kwargs.append(param.name)
        elif param.kind == param.VAR_POSITIONAL:
            has_varargs = True
        elif param.kind == param.VAR_KEYWORD:
            has_var_kwargs = True





-------------------------------------
INFO:sqlalchemy.engine.base.Engine:SELECT apscheduler_jobs.next_run_time 
FROM apscheduler_jobs
WHERE apscheduler_jobs.next_run_time IS NOT NULL ORDER BY apscheduler_jobs.next_run_time
 LIMIT %(param_1)s
 * Serving Flask app "flaskr" (lazy loading)
INFO:sqlalchemy.engine.base.Engine:{'param_1': 1}
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.DEBUG:sqlalchemy.engine.base.Engine:Col ('next_run_time',)

DEBUG:sqlalchemy.pool.impl.QueuePool:Connection <pymysql.connections.Connection object at 0x00000219557BA668> being returned to pool
DEBUG:sqlalchemy.pool.impl.QueuePool:Connection <pymysql.connections.Connection object at 0x00000219557BA668> rollback-on-return

위 오류메세지는.....
참조 : https://stackoverflow.com/questions/51025893/flask-at-first-run-do-not-use-the-development-server-in-a-production-environmen
참조 : https://flask.palletsprojects.com/en/1.1.x/config/