import abc
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from estacionamento.domain.model import Cliente
from estacionamento.domain import model
#Kennedy, melhor importar o model. Assim ficamos com model.Cliente, model.Pagamento, model.x
#assim sempre sabemos de onde a classe vem. Ademais, essa metodologia eh +alinhada com o livro.

#Interface abstrata (AbstractRepository)
class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, cliente: Cliente) -> None:
        """Adiciona um novo cliente (Agregado Root) ao repositório."""
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_cliente: UUID) -> Optional[Cliente]:
        """Recupera um cliente pelo seu ID único."""
        raise NotImplementedError


#Implementação concreta para SQLAlchemy (SqlAlchemyRepository)
class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, cliente: Cliente) -> None:
        self.session.add(cliente)

    def get(self, id_cliente: UUID) -> Optional[Cliente]:
        return self.session.query(Cliente).filter_by(id_cliente=id_cliente).first()

#Parcial para add e get para o agregado Cliente
#Parcial para a camada de repositório do agregado Cliente

#PAGAMENTO INI
class AbstractPagamentoRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, pagamento: model.Pagamento) -> None:
        """add um pagamento no repositorio"""
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_ticket:int) -> Optional[model.Pagamento]:
        """busca pagamento pelo id do ticket"""
        raise NotImplementedError


#PAGAMENTO FIM


#Reserva Início
class AbstractReservaRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, reserva: model.Reserva) -> None:
        "adiciona uma reserva no repositório"
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_reserva:int) -> Optional[model.Reserva]:
        "retorna uma reserva por meio de seu id"
#Reserva Fim

# Agregado de Estacionamento
class AbstractEstacionamentoRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, estacionamento: model.Estacionamento) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_estacionamento: int) -> model.Estacionamento | None:
        raise NotImplementedError


class SqlAlchemyEstacionamentoRepository(AbstractEstacionamentoRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, estacionamento: model.Estacionamento) -> None:
        self.session.add(estacionamento)

    def get(self, id_estacionamento: int) -> model.Estacionamento | None:
        return (
            self.session.query(model.Estacionamento)
            .filter_by(id_estacionamento=id_estacionamento)
            .first()
        )

    def list(self):
        return self.session.query(model.Estacionamento).all()


    class FakeEstacionamentoRepository(AbstractEstacionamentoRepository):
        def __init__(self, estacionamentos):
            self._estacionamentos = set(estacionamentos)

        def add(self, estacionamento):
            self._estacionamentos.add(estacionamento)

        def get(self, id_estacionamento):
            return next(e for e in self._estacionamentos if e.id_estacionamento == id_estacionamento)

        def list(self):
         return list(self._estacionamentos)
