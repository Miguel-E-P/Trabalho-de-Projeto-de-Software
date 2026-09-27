from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from src.estacionamento.domain import model
from estacionamento.adapters.repository import AbstractRepository, FakePagamentoRepository
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

# PAGAMENTO INI
def test_fake_repository_salva_e_recupera_pagamento():
    repo = FakePagamentoRepository()
    dinheiro = model.Dinheiro(50.50)
    pagamento = model.Pagamento(
        id_ticket=101,
        valor=dinheiro,
        tipo_pagamento=model.TipoPagamento.CREDITO,
        data_hora_pagamento=datetime(2023, 10, 27, 14, 30)
    )

    repo.add(pagamento)

    pagamento_salvo = repo.get(101)
    assert pagamento_salvo == pagamento
    assert pagamento_salvo.valor == model.Dinheiro(50.50)
