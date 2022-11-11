from sqlalchemy.ext.declarative import declarative_base

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

Base = declarative_base()