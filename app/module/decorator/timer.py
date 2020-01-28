# 출처 : https://jupiny.com/2016/09/25/decorator-class/
import time

class Timer():
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        result = self.function(*args, **kwargs)
        end_time = time.time()
        print("실행시간은 {time}초입니다.".format(time=end_time-start_time))
        return result