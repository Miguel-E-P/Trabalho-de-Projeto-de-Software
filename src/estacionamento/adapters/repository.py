import abc
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from estacionamento.domain.model import Cliente


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