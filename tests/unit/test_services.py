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

# #Segundo teste: Tentativa de reserva conflitante
# def test_verificador_bloqueia_conflito_de_horario():
#     vaga = Vaga(id_vaga=1, tipo=TipoVaga.CARRO, status=StatusVaga.LIVRE)
#     reserva_existente = Reserva(
#         id_reserva=101,
#         data_reserva=datetime(2026, 9, 20, 14, 0, 0),
#         data_fim=datetime(2026, 9, 20, 16, 0, 0),
#         placa_veiculo_reserva="ABC1D23",
#     )

#     inicio_tentativa = datetime(2026, 9, 20, 15, 0, 0)
#     fim_tentativa = datetime(2026, 9, 20, 17, 0, 0)

#     assert (VerificarDisponibilidadeVaga.validar(vaga, inicio_tentativa, fim_tentativa, [reserva_existente]) is False)

# #Fim do segundo teste no Domain Service VerificadorDisponibilidadeVaga
