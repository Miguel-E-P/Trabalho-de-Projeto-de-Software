from datetime import datetime
from uuid import uuid4
import pytest

from src.estacionamento.domain.model import Dinheiro, TipoVaga, StatusVaga, Vaga, Reserva
from src.estacionamento.service_layer.services import CalculadoraTarifa#, VerificarDisponibilidadeVaga


# Teste do Domain Service CalculadoraTarifa
def test_calculadora_tolerancia():
    entrada = datetime(2026, 9, 20, 10, 0, 0)
    saida = datetime(2026, 9, 20, 10, 15, 0)
    valor = CalculadoraTarifa.calcular(TipoVaga.CARRO, entrada, saida)
    assert valor == Dinheiro(valor=0.0)

#Fim do teste do Domain Service CalculadoraTarifa

# Testes do Domain Service VerificarDisponibilidadeVaga
def validar_disponibilidade_sucesso(vaga_livre):
    vaga_livre = Vaga(id_vaga=1, tipo=TipoVaga.CARRO, status=StatusVaga.LIVRE)
    inicio = datetime(2026, 10, 15, 8, 0)
    fim = datetime(2026, 10, 15, 18, 0)
    reservas = []

    assert VerificarDisponibilidadeVaga.validar(vaga_livre, inicio, fim, reservas) is True

def validar_conflito_com_reserva_existente(vaga_livre):
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
