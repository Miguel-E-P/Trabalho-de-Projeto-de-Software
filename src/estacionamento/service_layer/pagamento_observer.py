# Padrão GoF Observer (comportamental) para o agregado Pagamento.

# Participantes:
#    Subject          -> PublicadorDePagamentos
#   ConcreteSubject  -> RegistradorDePagamentos
#    Observer         -> ObservadorDePagamento
#    ConcreteObserver -> MarcarTicketComoPago, AuditoriaDePagamentos


import logging
from abc import ABC, abstractmethod
from typing import Callable, Optional

from estacionamento.adapters.repository import (
    AbstractPagamentoRepository,
    AbstractTicketRepository,
)
from estacionamento.domain import model


class TicketNaoEncontrado(Exception):
    pass


# Observer
class ObservadorDePagamento(ABC):
    @abstractmethod
    def atualizar(self, pagamento: model.Pagamento) -> None:
        """Reage a um pagamento que acabou de ser registrado."""
        raise NotImplementedError


# Subject
class PublicadorDePagamentos:
    def __init__(self) -> None:
        self._observadores: list[ObservadorDePagamento] = []

    def adicionar(self, observador: ObservadorDePagamento) -> None:
        self._observadores.append(observador)

    def remover(self, observador: ObservadorDePagamento) -> None:
        self._observadores.remove(observador)

    def notificar(self, pagamento: model.Pagamento) -> None:
        # Percorre uma copia: um observador pode se remover durante a notificacao.
        for observador in list(self._observadores):
            observador.atualizar(pagamento)


# ConcreteSubject
class RegistradorDePagamentos(PublicadorDePagamentos):
    def __init__(self, repo: AbstractPagamentoRepository) -> None:
        super().__init__()
        self._repo = repo

    def registrar(self, pagamento: model.Pagamento) -> None:
        """Guarda o pagamento e avisa os observadores.

        Nao faz commit. Se o repositorio recusar o pagamento, ninguem e avisado.
        Se um observador falhar, os seguintes nao sao avisados e quem chamou
        deve desfazer a transacao (rollback).
        """
        self._repo.add(pagamento)
        self.notificar(pagamento)


# ConcreteObserver
class MarcarTicketComoPago(ObservadorDePagamento):
    """O ticket de um pagamento registrado passa a pago."""

    def __init__(self, tickets: AbstractTicketRepository) -> None:
        self._tickets = tickets

    def atualizar(self, pagamento: model.Pagamento) -> None:
        ticket = self._tickets.get(pagamento.id_ticket)
        if ticket is None:
            raise TicketNaoEncontrado(
                f"ERROR: Ticket {pagamento.id_ticket} nao encontrado."
            )
        ticket.registrar_pagamento()


# ConcreteObserver
class AuditoriaDePagamentos(ObservadorDePagamento):
    """Escreve uma linha de auditoria para cada pagamento registrado."""

    def __init__(self, escrever: Optional[Callable[[str], None]] = None) -> None:
        self._escrever = escrever or logging.getLogger(__name__).info

    def atualizar(self, pagamento: model.Pagamento) -> None:
        self._escrever(
            f"pagamento registrado: ticket={pagamento.id_ticket} "
            f"valor={pagamento.valor:.2f} tipo={pagamento.tipo_pagamento.value}"
        )
