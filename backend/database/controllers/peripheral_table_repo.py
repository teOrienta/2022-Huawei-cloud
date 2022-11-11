from database.models import make_peripheral_table
from sqlalchemy import func, cast, types, or_, join, select
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from typing import List
import traceback

class PeripheralTableRepo():
    """ Class to manage PeripheralTable Repository """
    
    @staticmethod
    def create(engine: Engine, peripheral_table_name: str):
        """ Creates PeripheralTable if not exists """
        PeripheralTable, _ = make_peripheral_table(peripheral_table_name)
        insp = inspect(engine)
        if not insp.has_table(PeripheralTable.table_name, schema=None):
            PeripheralTable.__table__.create(engine)
        return PeripheralTable
    
    @staticmethod
    def insert(session: Session, peripheral_table_name: str, name: str, id: int = None):
        """ Inserts a row in the PeripheralTable. """
        PeripheralTable, PeripheralTableModel = make_peripheral_table(peripheral_table_name)
        
        new_peripheral = PeripheralTable(nome = name)
        if id is not None:
            new_peripheral = PeripheralTable(id = id, nome = name)

        session.add(new_peripheral)
        session.commit()
        
        return PeripheralTableModel._make(new_peripheral)

    @staticmethod
    def insert_many(session: Session, peripheral_table_name: str, peripheral_list: list):
        """ Inserts many rows into PeripheralTable. """

        PeripheralTable, _ = make_peripheral_table(peripheral_table_name)
        peripheral_list = list(map(lambda dic: PeripheralTable(**dic), peripheral_list))

        for peripheral in peripheral_list:
            session.merge(peripheral)

        session.commit()
        return peripheral_list
    
    @staticmethod
    def count(session: Session, peripheral_table_name: str):
        """ Return the count of the PeripheralTable. """
        PeripheralTable, _ = make_peripheral_table(peripheral_table_name)
        return session.query(PeripheralTable.id).count()

    @staticmethod
    def select(session: Session, peripheral_table_name: str, id: int = None, name: str = None):
        """ Selects PeripheralTable by a dict of filters """
        PeripheralTable, PeripheralModel = make_peripheral_table(peripheral_table_name)
        
        filter = {}
        if id is not None:
            filter["id"] = id
        if name is not None:
            filter["nome"] = name

        peripherals = session.query(PeripheralTable).filter_by(**filter).all()
        return list(map(PeripheralModel._make, peripherals))

    @staticmethod
    def select_all(session: Session, peripheral_table_name: str):
        """ Returns all the rows in PeripheralTable. """
        PeripheralTable, PeripheralModel = make_peripheral_table(peripheral_table_name)
        peripherals = session.query(PeripheralTable).all()
        return list(map(PeripheralModel._make, peripherals))

    @staticmethod
    def drop(engine: Engine, peripheral_table_name: str):
        """ Drop PeripheralTable if exists """
        PeripheralTable, _ = make_peripheral_table(peripheral_table_name)
        insp = inspect(engine)
        if insp.has_table(PeripheralTable.table_name, schema=None):
            PeripheralTable.__table__.drop(engine)
        return PeripheralTable