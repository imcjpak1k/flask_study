import logging
from app.model.models import User
# from flaskr import get_bcrypt


logger = logging.getLogger(__name__)


def test():
    """
    SQLAlchemy ORM - Textual SQL 사용한 방법

    # 모델에 정의된 컬럼정보 사용
    stmt =   db.text('select email, name  from user')
    db.session.query(User.email, User.name).from_statement(stmt).all()

    # 모델에 정의된 컬럼정보 사용
    stmt =   db.text('select email, name from user where email = :email')
    stmt = stmt.bindparams(email='imcjpak1k@naver.com')
    db.session.query(User.email, User.name).from_statement(stmt).all()

    # 컬럼정보를 입력한
    stmt =   db.text('select email, name from user where email = :email')
    stmt = stmt.bindparams(email='imcjpak1k@naver.com')
    db.session.query(db.Column('email', db.String(20)), db.Column('name', db.String(20))).from_statement(stmt).all()


    # 컬럼정보 입력 및 바인드변수
    stmt =   db.text('select email, name from user where email = :email')
    stmt = stmt.bindparams(email='imcjpak1k@naver.com')
    db.session.query(db.Column('email', db.String), db.Column('name', db.String)).from_statement(stmt).all()


    아래방법은 컬럼정보를 지정하지 않고 조회가능함..
    stmt =   db.text('select email, name  from user')
    db.session.connection().execute(stmt)

    stmt =   db.text('select email, name  from user')
    db.engine.connect().execute(stmt).fetchall()
    """
    pass

def login(id=None, pwd=None):
    """
    사용자로그인 
     - 아이디, 비밀번호 확인 후 일치하지 않으면 오류발생
    """

    # ORM 
    user = inquiry_user_info_by_email(id)
    
    # 자용자정보 확인
    if user is None or not user.count() == 1:
        raise RuntimeError("요청하신 자용자 정보가 존재하지 않습니다.")

    # 비밀번호 확인
    db_user = user.one()
    
    # 비밀번호 체크
    if not db_user.check_password(pwd):
        raise RuntimeError("비밀번호가 일치하지 않습니다.") 
    
    return db_user.toDict()


def inquiry_user_info_by_email(email=None):
    """
    이메일주소로 사용자정보 조회  
    """
    return User.query.filter_by(email=email)

    