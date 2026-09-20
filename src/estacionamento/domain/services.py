import math
from datetime import datetime
from estacionamento.domain.model import Dinheiro, TipoVaga

class CalculadoraTarifa:
    """Domain Service que calcula o valor da permanência para cada veículo (RN-02)"""

    TARIFA_CARRO = 10.0
    TARIFA_MOTO = 5.0
    TARIFA_CAMINHONETE = 15.0
    TAXA_RECARGA = 8.0

    @staticmethod
    def calcular(tipo_veiculo: TipoVaga, entrada: datetime, saida: datetime, recarga: bool = False) -> Dinheiro:
        horas = (saida - entrada).total_seconds() / 3600
        if horas <= 0:
            return Dinheiro(valor= 0.0)
        horas_cobranca = math.ceil(horas)

        if tipo_veiculo == TipoVaga.MOTO:
            taxa = CalculadoraTarifa.TARIFA_MOTO 
        elif tipo_veiculo.value == "caminhonete":
            taxa = CalculadoraTarifa.TARIFA_CAMINHONETE
        else:
            taxa = CalculadoraTarifa.TARIFA_CARRO

        total = float(horas_cobranca * taxa)
        if tipo_veiculo == TipoVaga.CARRO_ELETRICO and recarga:
            total+=CalculadoraTarifa.TAXA_RECARGA
        return Dinheiro(valor=total)



