import math
from datetime import datetime
from estacionamento.domain.model import Dinheiro, TipoVaga

class CalculadoraTarifa:
    """Domain Service que calcula o valor da permanência para cada veículo (RN-02)"""

    TARIFA_CARRO = 10.0
    TARIFA_MOTO = 5.0

    @staticmethod
    def calcular(tipo_veiculo: TipoVaga, entrada: datetime, saida: datetime) -> Dinheiro:
        horas = (saida - entrada).total_seconds() / 3600
        if horas <= 0:
            return Dinheiro(valor= 0.0)
        horas_cobranca = math.ceil(horas)
        taxa = CalculadoraTarifa.TARIFA_MOTO if tipo_veiculo == TipoVaga.MOTO else CalculadoraTarifa.TARIFA_CARRO
        return Dinheiro(valor=float(horas_cobranca * taxa))



