# DB에 사용한 key를 생성하여 해당 함수로 넘겨준다.
# 값의 구성은 다음과 같다.
# - '년월일시분초밀리센터'
# 단, 이전에 반환한 값과 중복될시 생성된 값을 변경(이전값 + 1)하여 반환(중복값 제거)
#
# @UniqueKey
# def test(key):
#     print(key)
# 
# 결과값 : 20190829233824305624
# import time

import datetime
import logging

class UniqueKey():
    def __init__(self, fnc):
        self.__name__   = fnc.__name__
        self.fnc        = fnc
        self.unique_key = self.current_datetime_fmt()
        # self.keymap     = """abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&|*\\/+-=<>(){}[]_,.?;:`'"""
        self.keymap     = """abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ~!@#$%^&*()-=_+<>?/:|;'"""
        self.keymap_len = len(self.keymap)
        self.logger     = logging.getLogger(__name__)


    def __call__(self, *args, **kwargs): 
        self.logger.debug('<< ResponseMessage Decorator >>')

        # print(self.fnc)
        # 현재시간을 키로 사용한다.
        current_datetime = self.current_datetime_fmt()
        # key생성
        current_key = self.get_key(current_datetime)

        # 중복값인 경우에는 이전값 + 1로 처리한다. 
        # (중복값이 나오지않도록 한다.)
        if self.unique_key == current_key:
            current_datetime    = str(int(current_datetime) + 1) 
            self.unique_key     = self.get_key(str(int(current_datetime) + 1))
        else:
            self.unique_key     = current_key

        result = self.fnc(self.unique_key, *args, **kwargs)
        return result

    def current_datetime(self):
        return datetime.datetime.now()
    
    def current_datetime_fmt(self, fmt="%Y%m%d%H%M%S%f"):
        return self.current_datetime().strftime(fmt)

    def get_key(self, datetime_str): 
        """ key 생성 """
        key0    = int(datetime_str[0:2])    % self.keymap_len    # 년1
        key1    = int(datetime_str[2:4])    % self.keymap_len    # 년2
        key2    = int(datetime_str[4:6])    % self.keymap_len    # 월
        key3    = int(datetime_str[6:8])    % self.keymap_len    # 일
        key4    = int(datetime_str[8:10])   % self.keymap_len   # 시
        key5    = int(datetime_str[10:12])  % self.keymap_len  # 분
        key6    = int(datetime_str[12:14])  % self.keymap_len  # 초 
        key7    = int(datetime_str[14:16])  % self.keymap_len  # ms1
        key8    = int(datetime_str[16:18])  % self.keymap_len  # ms2
        key9    = int(datetime_str[18:20])  % self.keymap_len  # ms3

        # print(''.join([
        #     str(key0),
        #     str(key1),
        #     str(key2),
        #     str(key3),
        #     str(key4),
        #     str(key5),
        #     str(key6),
        #     str(key7),
        #     str(key8),
        #     str(key9),
        # ]))

        return ''.join([
            self.keymap[key0],
            self.keymap[key1],
            self.keymap[key2],
            self.keymap[key3],
            self.keymap[key4],
            self.keymap[key5],
            self.keymap[key6],
            self.keymap[key7],
            self.keymap[key8],
            self.keymap[key9],
        ])

# @UniqueKey
# def test(key):
#     print(key, 'test')

# @UniqueKey
# def test2(key):
#     print(key, 'test2')


# for i in range(1, 20):
#     test()
#     test2()


# test2()
# test2()
# test2()
# test2()
# test2()
# test2()
# test2()
# @UniqueKey
# def test(ss) :
#     print(ss)

# for i in range(1,100):
#     test()