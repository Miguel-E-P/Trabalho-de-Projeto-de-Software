from typing import Optional
from uuid import UUID, uuid4

from estacionamento.adapters.repository import AbstractRepository
from estacionamento.domain.model import Cliente

#Implementa o FakeRepository e realiza os testes unitários no agregado Cliente

class FakeRepository(AbstractRepository):
    def __init__(self, clientes=None):
        # Converte para string para evitar inconsistências de UUID vs str
        self._clientes = {str(c.id_cliente): c for c in (clientes or [])}

    def add(self, cliente: Cliente) -> None:
        self._clientes[str(cliente.id_cliente)] = cliente

    def get(self, id_cliente: UUID) -> Optional[Cliente]:
        return self._clientes.get(str(id_cliente))


def test_fake_repository_salva_e_recupera_cliente():
    repo = FakeRepository()
    id_c = uuid4()
    cliente = Cliente(
        id_cliente=id_c,
        nome="Maria",
        cpf="12345678900",
        telefone="11999998888",
        email="maria@email.com",
    )

    repo.add(cliente)

    cliente_salvo = repo.get(id_c)
    assert cliente_salvo == cliente
    assert cliente_salvo.nome == "Maria"

#Fim dos testes unitários no agregado Cliente