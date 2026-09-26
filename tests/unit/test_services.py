from datetime import datetime
from uuid import uuid4
import pytest

from src.estacionamento.domain.model import Dinheiro, TipoVaga, StatusVaga, Vaga, Reserva, Ticket, Pagamento
from src.estacionamento.service_layer.services import CalculadoraTarifa, VerificarDisponibilidadeVaga, AutorizadorSaidaVeiculo


# Teste do Domain Service CalculadoraTarifa
def test_calculadora_tolerancia():
    entrada = datetime(2026, 9, 20, 10, 0, 0)
    saida = datetime(2026, 9, 20, 10, 15, 0)
    valor = CalculadoraTarifa.calcular(TipoVaga.CARRO, entrada, saida)
    assert valor == Dinheiro(valor=0.0)

#Fim do teste do Domain Service CalculadoraTarifa

# Testes do Domain Service VerificarDisponibilidadeVaga
def test_validar_disponibilidade_sucesso():
    vaga_livre = Vaga(id_vaga=1, tipo=TipoVaga.CARRO, status=StatusVaga.LIVRE)
    inicio = datetime(2026, 10, 15, 8, 0)
    fim = datetime(2026, 10, 15, 18, 0)
    reservas = []

    assert VerificarDisponibilidadeVaga.validar(vaga_livre, inicio, fim, reservas) is True

def test_validar_conflito_com_reserva_existente():
    vaga_livre = Vaga(id_vaga=1, tipo=TipoVaga.CARRO, status=StatusVaga.LIVRE)
    data_conflito = datetime(2026, 10, 15, 10, 0)

    reserva_existente = Reserva(
        id_reserva=1,
        data_reserva=data_conflito,
        hoje=datetime(2026, 10, 1),
        placa_veiculo_reserva="ABC1D23"
    )

    inicio = datetime(2026, 10, 15, 8, 0)
    fim = datetime(2026, 10, 15, 18, 0)

    assert VerificarDisponibilidadeVaga.validar(vaga_livre, inicio, fim, [reserva_existente]) is False

# Fim dos testes do Domain Service VerificarDisponibilidadeVaga

# Testes do Domain Service AutorizadorSaidaVeiculo
def test_autorizar_saida():
    vaga = Vaga(id_vaga=1, tipo=TipoVaga.CARRO, status=StatusVaga.OCUPADA)
    ticket = Ticket(horarioEntrada=datetime(2026, 10, 15, 10, 0), horarioSaida=datetime(2026, 10, 15, 12, 0), idTicket=100)
    pagamento = Pagamento(id_pagamento=1, id_ticket=100, valor=Dinheiro(20.0), pago=True)

    assert AutorizadorSaidaVeiculo.autorizar(vaga, ticket, pagamento) is True

def test_negar_saida_pagamento_pendente():
    vaga = Vaga(id_vaga=1, tipo=TipoVaga.CARRO, status=StatusVaga.OCUPADA)
    ticket = Ticket(horarioEntrada=datetime(2026, 10, 15, 10, 0), horarioSaida=datetime(2026, 10, 15, 12, 0), idTicket=100)
    pagamento = Pagamento(id_pagamento=1, id_ticket=100, valor=Dinheiro(20.0), pago=False)

    assert AutorizadorSaidaVeiculo.autorizar(vaga, ticket, pagamento) is False


def test_autorizar_saida_com_multa_pernoite_paga():
    vaga = Vaga(id_vaga=1, tipo=TipoVaga.CARRO, status=StatusVaga.OCUPADA)
    ticket = Ticket(
        horarioEntrada=datetime(2026, 10, 15, 22, 0),
        horarioSaida=datetime(2026, 10, 16, 2, 0),
        idTicket=100
    )
    
    pagamento = Pagamento(id_pagamento=1, id_ticket=100, valor=Dinheiro(90.0), pago=True)

    assert AutorizadorSaidaVeiculo.autorizar(vaga, ticket, pagamento) is True

# Fim dos testes do Domain Service AutorizadorSaidaVeiculo
