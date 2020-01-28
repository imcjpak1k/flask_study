from flask_sqlalchemy import Model

class DictModel(Model):
    def toDict(self):
        """
        Model데이터를 dict로 반환함
        """
        # ret_data = {}
        # for column in self.__table__.columns:
        #     if column.name.startswith('_'): continue
        #     ret_data[column.name] = getattr(self, column.name)
        # return ret_data
        return {column.name : getattr(self, column.name) for column in self.__table__.columns if not column.name.startswith('_')}
