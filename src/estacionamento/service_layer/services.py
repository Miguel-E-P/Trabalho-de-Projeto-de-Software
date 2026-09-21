import math
from datetime import datetime
from src.estacionamento.domain.model import Dinheiro, TipoVaga, StatusVaga, Vaga, Reserva, Pagamento

class CalculadoraTarifa:
    """Domain Service que calcula o valor da permanência para cada veículo (RN-02)"""

    TARIFA_CARRO = 10.0
    TARIFA_MOTO = 5.0
    TARIFA_CAMINHONETE = 15.0
    TAXA_RECARGA = 8.0

    @staticmethod
    def calcular(tipo_veiculo: TipoVaga, entrada: datetime, saida: datetime, recarga: bool = False) -> Dinheiro:
        segundos = (saida - entrada).total_seconds()
        # Tolerância de 15 minutos
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
        if vaga.status != StatusVaga.LIVRE:
            return False
        for reserva in reservas_existentes:
            inicio_reserva = reserva.data_reserva
            fim_reserva = reserva.duracao_reserva
            if inicio < fim_reserva and fim > inicio_reserva:
                return False

        return True



