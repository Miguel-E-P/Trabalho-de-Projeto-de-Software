from datetime import datetime
import pytest

from src.estacionamento.domain.model import Dinheiro, TipoVaga, StatusVaga, Vaga, Reserva
from src.estacionamento.service_layer.services import CalculadoraTarifa#, VerificarDisponibilidadeVaga


#Primeiro teste: verificar a gratuidade nos casos inclusos na tolerência de 15 minutos
def test_calculadora_tolerancia():
    entrada = datetime(2026, 9, 20, 10, 0, 0)
    saida = datetime(2026, 9, 20, 10, 15, 0)
    valor = CalculadoraTarifa.calcular(TipoVaga.CARRO, entrada, saida)
    assert valor == Dinheiro(valor=0.0)

#Fim do primeiro teste no Domain Service CalculadoraTarifa


