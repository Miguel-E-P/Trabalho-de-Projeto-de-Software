# Padrão GoF Façade (estrutural) para o agregado Reserva (Reserva e Ticket).
#
# Participantes:
#    Facade     -> FachadaReserva
#    Subsistema -> Reserva, Ticket, Estacionamento (modelo) e
#                  AbstractReservaRepository, AbstractTicketRepository,
#                  AbstractEstacionamentoRepository (portas de saida) e
#                  CalculadoraTarifa (Domain Service)
#
# Cada operacao da fachada e um caso de uso que antes exigia que o cliente
# (rota Flask, script, teste) conhecesse varias classes e a ordem certa das
# chamadas. A fachada nao tem regra de negocio: as regras continuam no modelo
# (Ticket, Reserva, Vaga) e no Domain Service. Ela so orquestra.

from datetime import datetime
from typing import Callable, Optional, Protocol, Union

from estacionamento.adapters.repository import (
    AbstractEstacionamentoRepository,
    AbstractReservaRepository,
    AbstractTicketRepository,
)
from estacionamento.domain import model
from estacionamento.service_layer.pagamento_observer import TicketNaoEncontrado


class ReservaJaExiste(Exception):
    pass


class TicketJaExiste(Exception):
    pass


class EstacionamentoNaoEncontrado(Exception):
    pass


class CalculadoraDeTarifa(Protocol):
    """O que a fachada precisa do Domain Service de tarifa.

    `CalculadoraTarifa` (service_layer/services.py) ja satisfaz este contrato,
    inclusive como classe, porque `calcular` e um classmethod.
    """

    def calcular(
        self,
        *,
        tipo_veiculo: Union[str, model.TipoVaga],
        entrada: datetime,
        saida: datetime,
        recarga: bool = False,
    ) -> float: ...


# Facade
class FachadaReserva:
    """Interface unica e simples para reservar, dar entrada e dar saida.

    Os repositorios, a calculadora e o modelo continuam acessiveis
    diretamente para quem precisar de controle fino; a fachada nao os
    esconde, so evita que o cliente precise conhece-los para o fluxo comum.
    """

    def __init__(
        self,
        reservas: AbstractReservaRepository,
        tickets: AbstractTicketRepository,
        estacionamentos: AbstractEstacionamentoRepository,
        calculadora: Optional[CalculadoraDeTarifa] = None,
        session=None,
        agora: Callable[[], datetime] = datetime.now,
    ) -> None:
        if calculadora is None:
            # Import tardio: services.py importa o modelo por outra raiz
            # (`src.estacionamento...`), e quem injeta a calculadora nao
            # precisa carregar esse modulo.
            from estacionamento.service_layer.services import CalculadoraTarifa

            calculadora = CalculadoraTarifa
        self._reservas = reservas
        self._tickets = tickets
        self._estacionamentos = estacionamentos
        self._calculadora = calculadora
        self._session = session
        self._agora = agora

    def reservar(
        self,
        id_reserva: int,
        data_reserva: datetime,
        placa_veiculo: str,
    ) -> model.Reserva:
        """Cria e guarda uma reserva. `hoje` vem do relogio da fachada."""
        if self._reservas.get(id_reserva) is not None:
            raise ReservaJaExiste(f"ERROR: Reserva {id_reserva} ja existe.")

        reserva = model.Reserva(id_reserva, data_reserva, self._agora(), placa_veiculo)
        self._reservas.add(reserva)
        self._commit()
        return reserva

    def registrar_entrada(
        self,
        id_ticket: int,
        id_estacionamento: int,
        id_vaga: int,
        horario_entrada: Optional[datetime] = None,
        veiculo: Optional[model.Veiculo] = None,
        politica: Optional[model.PoliticaOcupacao] = None,
    ) -> model.Ticket:
        """Abre um ticket e ocupa a vaga, ou nao faz nenhuma das duas coisas."""
        if self._tickets.get(id_ticket) is not None:
            raise TicketJaExiste(f"ERROR: Ticket {id_ticket} ja existe.")

        estacionamento = self._estacionamentos.get(id_estacionamento)
        if estacionamento is None:
            raise EstacionamentoNaoEncontrado(
                f"ERROR: Estacionamento {id_estacionamento} nao encontrado."
            )

        # O ticket e criado antes de ocupar a vaga: se a entrada for invalida
        # (id negativo), a vaga ainda nao foi alterada.
        ticket = model.Ticket(id_ticket, horario_entrada or self._agora(), None)
        estacionamento.ocupar_vaga(id_vaga, veiculo, politica)

        self._tickets.add(ticket)
        self._commit()
        return ticket

    def registrar_saida(
        self,
        id_ticket: int,
        tipo_veiculo: Union[str, model.TipoVaga],
        horario_saida: Optional[datetime] = None,
        recarga: bool = False,
    ) -> float:
        """Registra a saida no ticket e devolve o valor devido.

        Nao registra o pagamento: isso e do agregado Pagamento
        (RegistradorDePagamentos). Se a tarifa nao puder ser calculada, a
        saida nao fica gravada no ticket.
        """
        ticket = self._tickets.get(id_ticket)
        if ticket is None:
            raise TicketNaoEncontrado(f"ERROR: Ticket {id_ticket} nao encontrado.")

        saida_anterior = ticket.horarioSaida
        saida = horario_saida or self._agora()
        ticket.updateSaida(saida)
        try:
            valor = self._calculadora.calcular(
                tipo_veiculo=tipo_veiculo,
                entrada=ticket.horarioEntrada,
                saida=saida,
                recarga=recarga,
            )
        except Exception:
            ticket.horarioSaida = saida_anterior
            raise

        self._commit()
        return valor

    def _commit(self) -> None:
        if self._session is not None:
            self._session.commit()
