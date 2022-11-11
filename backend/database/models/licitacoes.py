from sqlalchemy import Column, Integer, DateTime, Float, String
from database.config import Base, classproperty
from collections import namedtuple

class Licitacoes(Base):
    """ Licitacoes Entity """

    __table_args__  = { 'extend_existing': True } 
    __tablename__   = f"licitacoes"
    id                  = Column(Integer, primary_key=True)
    numeroLicitacao     = Column(Integer, nullable=False)
    codUG               = Column(Integer, nullable=False)
    codModalidadeCompra = Column(Integer, nullable=False)
    codOrgaoSuperior    = Column(Integer, nullable=False)
    codOrgao            = Column(Integer, nullable=False)
    codMunicipio        = Column(Integer, nullable=False)
    numeroProcesso      = Column(String, nullable=False)
    objeto              = Column(String, nullable=False)
    situacaoLicitacao   = Column(String, nullable=False)
    dataAbertura        = Column(DateTime, nullable=True)
    dataResultado       = Column(DateTime, nullable=True)
    valor               = Column(Float, nullable=True)

    @classproperty
    def table_name(cls):
        return cls.__tablename__

    def __repr__(self):
        return f"""Licitacoes(
            id = {self.id}
            numeroLicitacao = {self.numeroLicitacao}
            codUG = {self.codUG}
            codModalidadeCompra = {self.codModalidadeCompra}
            codOrgaoSuperior = {self.codOrgaoSuperior}
            codOrgao = {self.codOrgao}
            codMunicipio = {self.codMunicipio}
            numeroProcesso = {self.numeroProcesso}
            objeto = {self.objeto}
            situacaoLicitacao = {self.situacaoLicitacao}
            dataAbertura = {self.dataAbertura}
            dataResultado = {self.dataResultado}
            valor = {self.valor}
        )"""

    def __eq__(self, other):
        return (
            self.id == other.id
            or (
                self.numeroLicitacao == other.numeroLicitacao
                and self.numeroProcesso == other.numeroProcesso
            )
        )

    def __iter__(self):
        yield self.id
        yield self.numeroLicitacao
        yield self.codUG
        yield self.codModalidadeCompra
        yield self.codOrgaoSuperior
        yield self.codOrgao
        yield self.codMunicipio
        yield self.numeroProcesso
        yield self.objeto
        yield self.situacaoLicitacao
        yield self.dataAbertura
        yield self.dataResultado
        yield self.valor

LicitacoesModel = namedtuple("Licitacoes", [
    "id",
    "numeroLicitacao",
    "codUG",
    "codModalidadeCompra",
    "codOrgaoSuperior",
    "codOrgao",
    "codMunicipio",
    "numeroProcesso",
    "objeto",
    "situacaoLicitacao",
    "dataAbertura",
    "dataResultado",
    "valor"
])