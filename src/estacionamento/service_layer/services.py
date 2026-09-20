import math
from datetime import datetime
from estacionamento.domain.model import Dinheiro, TipoVaga, Vaga, Reserva, Pagamento

class CalculadoraTarifa:
    """Domain Service que calcula o valor da permanência para cada veículo (RN-02)"""

    TARIFA_CARRO = 10.0
    TARIFA_MOTO = 5.0
    TARIFA_CAMINHONETE = 15.0
    TAXA_RECARGA = 8.0

    @staticmethod
    def calcular(tipo_veiculo: TipoVaga, entrada: datetime, saida: datetime, recarga: bool = False) -> Dinheiro:
        # Tolerância de 15 minutos
        segundos = (saida - entrada).total_seconds()
        if segundos <= 900:
            return Dinheiro(valor= 0.0)
        horas = segundos / 3600
        horas_cobranca = math.ceil(horas)

        categoria = (tipo_veiculo.value if hasattr(tipo_veiculo, "value") else str(tipo_veiculo))

        if categoria == TipoVaga.MOTO.value:
            taxa = CalculadoraTarifa.TARIFA_MOTO
        elif categoria in ["caminhonete", "SUV"]:
            taxa = CalculadoraTarifa.TARIFA_CAMINHONETE
        else:
            taxa = CalculadoraTarifa.TARIFA_CARRO

        total = float(horas_cobranca * taxa)
        if tipo_veiculo == TipoVaga.CARRO_ELETRICO and recarga:
            total+=CalculadoraTarifa.TAXA_RECARGA
        return Dinheiro(valor=total)

class VerificarDisponibilidadeVaga:
    """Domain Service para checagem de vagas e evitar sobreposição de reservas (RN-03)"""


    @staticmethod
    def validar(vaga: Vaga, inicio: datetime, fim: datetime, reservas_existentes: list[Reserva]) -> bool:
        for reserva in reservas_existentes:
            if reserva.id_vaga != vaga.id_vaga:
                continue
        if inicio < reserva.fim and fim > reserva.inicio:
            return False

        return True



