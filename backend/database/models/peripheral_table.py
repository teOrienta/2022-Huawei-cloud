from sqlalchemy import Column, Integer, String
from database.config import Base, classproperty
from collections import namedtuple

def make_peripheral_table(peripheral_table_name: str):
    class Peripheral(Base):
        """ Peripheral Entity """

        __table_args__  = { 'extend_existing': True } 
        __tablename__   = f"{peripheral_table_name}"
        id      = Column(Integer, nullable=False, primary_key=True)
        nome    = Column(String, nullable=False)

        @classproperty
        def table_name(cls):
            return cls.__tablename__

        def __repr__(self):
            return f"""{peripheral_table_name}(
                id      = {self.id}
                nome    = {self.nome}
            )"""

        def __eq__(self, other):
            return self.id == other.id

        def __iter__(self):
            yield self.id
            yield self.nome
            
    peripheralModel = namedtuple(f"{peripheral_table_name}", ["id", "nome"])
    
    return Peripheral, peripheralModel

