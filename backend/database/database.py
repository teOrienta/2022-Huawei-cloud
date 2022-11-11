
from database.controllers import LicitacoesRepository, PeripheralTableRepo
from database.config import db_conn, verify_connection

class PostgreSQL:
    def __init__(self):
        self.connection = db_conn
        self.engine = None
        self.__migration()

    def __migration(self):
        self.is_connected = False
        try:
            self.engine = self.connection.get_engine()

            LicitacoesRepository.create(self.engine)
            PeripheralTableRepo.create(self.engine, "modalidadeCompras")
            PeripheralTableRepo.create(self.engine, "unidadesGestoras")
            PeripheralTableRepo.create(self.engine, "orgaosSuperiores")
            PeripheralTableRepo.create(self.engine, "municipios")
            PeripheralTableRepo.create(self.engine, "orgaos")

            self.is_connected = True
        except Exception as e:
            print("DATABASE NOT CONNECTED:", e)
        return self.is_connected

    @verify_connection
    def call_function_with_session(self, func, *args, **kwargs):
        """ Abstract function to call a function with a session """
        with self.connection.get_session() as session:
            return func(session, *args, **kwargs)

    # Municipios Functions
    def get_all_municipios(self):
        function = PeripheralTableRepo.select_all
        municipios = self.call_function_with_session(function, "municipios")

        return [ r[1] for r in municipios ]

    # Modalidades Functions
    def get_all_modalidades(self):
        function = PeripheralTableRepo.select_all
        modalidades = self.call_function_with_session(function, "modalidades")

        return [ r[1] for r in modalidades ]

    # Licitacoes Functions

