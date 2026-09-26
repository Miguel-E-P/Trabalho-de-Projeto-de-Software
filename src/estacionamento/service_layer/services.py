import math
from datetime import datetime
from src.estacionamento.domain.model import Dinheiro, TipoVaga, StatusVaga, Vaga, Reserva, Pagamento, Ticket

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
        if inicio.date() != fim.date():
            return False
        data_solicitada = inicio.date()
        return not any(
            reserva.data_reserva.date() == data_solicitada
            for reserva in reservas_existentes
        )

class AutorizadorSaidaVeiculo:
    """Domain Service responsável por validar se o veículo pode sair (RN-04)"""

    MULTA_PERNOITE = 50.0

    @staticmethod
    def autorizar(vaga: Vaga, ticket: Ticket, pagamento: Pagamento) -> bool:
        if vaga.status != StatusVaga.OCUPADA:
            return False
        if ticket.horarioSaida is None:
            return False
        
        tarifa_base = CalculadoraTarifa.calcular(tipo_veiculo=vaga.tipo, entrada=ticket.horarioEntrada, saida=ticket.horarioSaida)
        total_devido = tarifa_base.valor

        if ticket.horarioSaida.date() != ticket.horarioEntrada.date():
            total_devido += AutorizadorSaidaVeiculo.MULTA_PERNOITE
        if not pagamento.pago or pagamento.id_ticket != ticket.idTicket:
            return False

        return True



