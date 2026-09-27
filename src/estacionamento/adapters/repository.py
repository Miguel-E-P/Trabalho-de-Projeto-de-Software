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

class SqlAlchemyPagamentoRepository(AbstractPagamentoRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, pagamento: model.Pagamento) -> None:
        self.session.add(pagamento)

    def get(self, id_ticket: int) -> Optional[model.Pagamento]:
        return self.session.query(model.Pagamento).filter_by(id_ticket=id_ticket).first()


class FakePagamentoRepository(AbstractPagamentoRepository):
    def __init__(self, pagamentos: list[model.Pagamento] = None):
        self._pagamentos = list(pagamentos) if pagamentos else []

    def add(self, pagamento: model.Pagamento) -> None:
        self._pagamentos.append(pagamento)

    def get(self, id_ticket: int) -> Optional[model.Pagamento]:
        try:
            return next(p for p in self._pagamentos if p.id_ticket == id_ticket)
        except StopIteration:
            return None

#PAGAMENTO FIM


#Agregado Reserva Início

#Reserva
class AbstractReservaRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, reserva: model.Reserva) -> None:
        "adiciona uma reserva no repositório"
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_reserva:int) -> Optional[model.Reserva]:
        "retorna uma reserva por meio de seu id"
        raise NotImplementedError

class SqlAlchemyReservaRepository(AbstractReservaRepository):
    def __init__(self, session: Session):
            self.session = session

    def add(self, reserva: model.Reserva) -> None:
        self.session.add(reserva)

    def get(self, id_reserva: int) -> model.Reserva:
        return(  self.session.query(model.Reserva).filter_by(id_reserva=id_reserva).first()  )

    def list(self):
        return self.session.query(model.Reserva).all()

class FakeReservaRepository(AbstractReservaRepository):
    def __init__(self, reservas):
        self.reservas = set(reservas)
    
    def add(self, reserva):
        self.reservas.add(reserva)
    
    def get(self, id_reserva):
        return next(r for r in self._reservas if r.id_reserva == id_reserva)
    
    def list(self):
        return list(self._reservas)

#Ticket
class AbstractTicketRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, ticket: model.Ticket) -> None:
        "adiciona um ticket no repositório"
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, idTicket:int) -> Optional[model.Ticket]:
        "retorna um ticket por meio de seu id"
        raise NotImplementedError


class SqlAlchemyTicketRepository(AbstractTicketRepository):
    def __init__(self, session: Session):
            self.session = session

    def add(self, ticket: model.Ticket) -> None:
        self.session.add(ticket)

    def get(self, idTicket: int) -> model.Ticket:
        return(  self.session.query(model.Ticket).filter_by(idTicket=idTicket).first()  )

    def list(self):
        return self.session.query(model.Ticket).all()

class FakeTicketRepository(AbstractTicketRepository):
    def __init__(self, tickets):
        self.tickets = set(tickets)
    
    def add(self, ticket):
        self.tickets.add(ticket)
    
    def get(self, idTicket):
        return next(t for t in self._tickets if t.idTicket == idTicket)
    
    def list(self):
        return list(self._tickets)
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
