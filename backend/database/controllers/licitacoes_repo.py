from database.models import Licitacoes, LicitacoesModel
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from datetime import datetime

class LicitacoesRepository():
    """ Class to manage Licitacoes Repository """
    
    @staticmethod
    def create(engine: Engine) -> Licitacoes:
        """ Creates Licitacoes table if not exists. """
        insp = inspect(engine)
        if not insp.has_table(Licitacoes.table_name, schema=None):
            Licitacoes.__table__.create(engine)
        return Licitacoes
    
    @staticmethod
    def insert(session: Session, numero_licitacao: int, cod_ug: int,
            cod_modalidade_compra: int, cod_orgao_superior: int,
            cod_orgao: int, cod_municipio: int, numero_processo: str,
            situacao_licitacao: str, objeto: str = None,
            data_abertura: datetime = None, data_resultado: datetime = None,
            valor: float = None
    ) -> LicitacoesModel:
        """ Inserts a row in Licitacoes table. """
        new_licitacao = Licitacoes(
            numeroLicitacao = numero_licitacao,
            codUG = cod_ug,
            codModalidadeCompra = cod_modalidade_compra,
            codOrgaoSuperior = cod_orgao_superior,
            codOrgao = cod_orgao,
            codMunicipio = cod_municipio,
            numeroProcesso = numero_processo,
            objeto = objeto,
            situacaoLicitacao = situacao_licitacao,
            dataAbertura = data_abertura,
            dataResultado = data_resultado,
            valor = valor
        )
        session.add(new_licitacao)
        session.commit()

        return LicitacoesModel._make(new_licitacao)

    @staticmethod
    def insert_many(session: Session, licitacoes_list: list[dict]) -> list[Licitacoes]:
        """ Inserts many rows into Licitacoes table. """

        licitacoes_list = list(map(lambda dic: Licitacoes(**dic), licitacoes_list))

        for licitacao in licitacoes_list:
            session.merge(licitacao)
        session.commit()

        return licitacoes_list
    
    @staticmethod
    def count(session: Session):
        """ Return the count of the Licitacoes table. """
        return session.query(Licitacoes.id).count()

    @staticmethod
    def select(session: Session, filters: dict) -> list[LicitacoesModel]:
        """ 
        Selects Licitacoes table by:
            - id
            - numeroLicitacao
            - codUG
            - codModalidadeCompra
            - codOrgaoSuperior
            - codOrgao
            - codMunicipio
            - numeroProcesso
        """
        licitacoes = (
            session.query(Licitacoes)
            .filter_by(**filters)
            .all()
        )
        
        return list(map(LicitacoesModel._make, licitacoes))

    @staticmethod
    def select_all(session: Session) -> list[LicitacoesModel]:
        """ Returns all the rows in Licitacoes table. """
        licitacoes = session.query(Licitacoes).all()
        return list(map(LicitacoesModel._make, licitacoes))

    @staticmethod
    def drop(engine: Engine):
        """ Drop Licitacoes table if exists """
        insp = inspect(engine)
        if insp.has_table(Licitacoes.table_name, schema=None):
            Licitacoes.__table__.drop(engine)
        return Licitacoes