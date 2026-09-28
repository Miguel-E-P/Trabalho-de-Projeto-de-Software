from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from src.estacionamento.domain import model
from estacionamento.adapters import repository
from estacionamento.adapters.repository import AbstractRepository, FakePagamentoRepository, FakeReservaRepository, FakeTicketRepository
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
    pagamento = model.Pagamento(
        id_ticket=101,
        valor=50.50,
        tipo_pagamento=model.TipoPagamento.CREDITO,
        data_hora_pagamento=datetime(2023, 10, 27, 14, 30)
    )

    repo.add(pagamento)

    pagamento_salvo = repo.get(101)
    assert pagamento_salvo == pagamento
    assert pagamento_salvo.valor == 50.50

#Reserva
def test_fake_reserva_salva_e_recupera_reserva():
    repo = FakeReservaRepository()
    reserva = model.Reserva(
        id_reserva=12,
        data_reserva=datetime(2026, 9, 28, 18, 54),
        hoje=datetime(2026, 9, 27, 18, 54),
        placa_veiculo_reserva="AAA-321"
    )
    repo.add(reserva)
    reserva_salva = repo.get(12)
    assert reserva_salva == reserva
    assert reserva_salva.placa_veiculo_reserva == "AAA-321"

def test_fake_ticket_salva_e_recupera_ticket():
    repo = FakeTicketRepository()
    ticket = model.Ticket(
        idTicket=43,
        horarioEntrada=datetime(2026, 9, 27, 10, 30),
        horarioSaida=datetime(2026, 9, 27, 12, 50),
        pago=True
    )
    repo.add(ticket)
    ticket_salvo = repo.get(43)
    assert ticket_salvo == ticket
    assert ticket_salvo.horarioEntrada == datetime(2026, 9, 27, 10, 30)

# Agregado Estacionamento
def test_get_estacionamento_cadastrado():
    estacionamento = model.Estacionamento(1, [])
    repo = repository.FakeEstacionamentoRepository([estacionamento])

    assert repo.get(1) == estacionamento


def test_get_estacionamento_nao_cadastrado():
    repo = repository.FakeEstacionamentoRepository([])

    assert repo.get(1) is None


def test_list_estacionamentos():
    estacionamento_1 = model.Estacionamento(1, [])
    estacionamento_2 = model.Estacionamento(2, [])

    repo = repository.FakeEstacionamentoRepository([estacionamento_1, estacionamento_2])

    resultado = repo.list()

    assert len(resultado) == 2
    assert estacionamento_1 in resultado
    assert estacionamento_2 in resultado
