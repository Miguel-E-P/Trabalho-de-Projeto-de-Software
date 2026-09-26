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
