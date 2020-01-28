class DatabaseError(Exception):
    def __init__(self, message):
        pass
        # self.e  = e 


class MessageError(Exception):
    def __init__(self, message):
        pass
        # Exception.__init__(message)
        # self.e  = e 

# try :
#     try :
#         raise RuntimeError('error test   bbr')
#     except Exception as e:
#         raise MessageError(e)
#         # raise
# except MessageError as e:
#     print(dir(e))
#     print("메세지오류 {}".format(e))
# except :
#     raise