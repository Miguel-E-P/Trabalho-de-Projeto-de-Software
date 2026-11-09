from datetime import datetime

import pytest

from estacionamento.adapters.repository import (
    FakePagamentoRepository,
    FakeTicketRepository,
)
from estacionamento.domain import model
from estacionamento.service_layer.pagamento_observer import (
    AuditoriaDePagamentos,
    MarcarTicketComoPago,
    ObservadorDePagamento,
    RegistradorDePagamentos,
    TicketNaoEncontrado,
)

ENTRADA = datetime(2026, 11, 2, 13, 0)
AGORA = datetime(2026, 11, 2, 14, 30)


def _pagamento(id_ticket=1, valor=50.0, tipo=model.TipoPagamento.PIX):
    return model.Pagamento(id_ticket, valor, tipo, AGORA)


class Espiao(ObservadorDePagamento):
    """Observador de teste: anota quem foi avisado e de qual ticket."""

    def __init__(self, nome, chamadas):
        self.nome = nome
        self.chamadas = chamadas

    def atualizar(self, pagamento):
        self.chamadas.append((self.nome, pagamento.id_ticket))


class AutoRemovivel(ObservadorDePagamento):
    def __init__(self, publicador):
        self.publicador = publicador
        self.vezes = 0

    def atualizar(self, pagamento):
        self.vezes += 1
        self.publicador.remover(self)


def test_registrar_guarda_o_pagamento_e_avisa_os_observadores_na_ordem():
    repo = FakePagamentoRepository()
    registrador = RegistradorDePagamentos(repo)
    chamadas = []
    registrador.adicionar(Espiao("a", chamadas))
    registrador.adicionar(Espiao("b", chamadas))
    pagamento = _pagamento(7)

    registrador.registrar(pagamento)

    assert repo.get(7) is pagamento
    assert chamadas == [("a", 7), ("b", 7)]


def test_observador_removido_nao_e_avisado():
    registrador = RegistradorDePagamentos(FakePagamentoRepository())
    chamadas = []
    removido = Espiao("removido", chamadas)
    registrador.adicionar(removido)
    registrador.adicionar(Espiao("fica", chamadas))
    registrador.remover(removido)

    registrador.registrar(_pagamento(1))

    assert chamadas == [("fica", 1)]


def test_observador_pode_se_remover_durante_a_notificacao():
    registrador = RegistradorDePagamentos(FakePagamentoRepository())
    chamadas = []
    auto = AutoRemovivel(registrador)
    registrador.adicionar(auto)
    registrador.adicionar(Espiao("outro", chamadas))

    registrador.registrar(_pagamento(1))
    registrador.registrar(_pagamento(2))

    assert auto.vezes == 1
    assert chamadas == [("outro", 1), ("outro", 2)]


def test_registrar_pagamento_marca_o_ticket_como_pago():
    ticket = model.Ticket(1, ENTRADA, None)
    registrador = RegistradorDePagamentos(FakePagamentoRepository())
    registrador.adicionar(MarcarTicketComoPago(FakeTicketRepository([ticket])))

    registrador.registrar(_pagamento(1))

    assert ticket.pago is True


def test_um_registro_aciona_observadores_de_naturezas_diferentes():
    ticket = model.Ticket(3, ENTRADA, None)
    linhas = []
    registrador = RegistradorDePagamentos(FakePagamentoRepository())
    registrador.adicionar(MarcarTicketComoPago(FakeTicketRepository([ticket])))
    registrador.adicionar(AuditoriaDePagamentos(linhas.append))

    registrador.registrar(_pagamento(3, 12.5, model.TipoPagamento.DEBITO))

    assert ticket.pago is True
    assert linhas == ["pagamento registrado: ticket=3 valor=12.50 tipo=debito"]


def test_ticket_inexistente_levanta_erro_de_dominio():
    registrador = RegistradorDePagamentos(FakePagamentoRepository())
    registrador.adicionar(MarcarTicketComoPago(FakeTicketRepository()))

    with pytest.raises(TicketNaoEncontrado, match="Ticket 9 nao encontrado."):
        registrador.registrar(_pagamento(9))


def test_ticket_ja_pago_propaga_o_erro_do_dominio():
    ticket = model.Ticket(1, ENTRADA, None, pago=True)
    registrador = RegistradorDePagamentos(FakePagamentoRepository())
    registrador.adicionar(MarcarTicketComoPago(FakeTicketRepository([ticket])))

    with pytest.raises(model.PagamentoJaRealizadoError, match="Ticket ja foi pago."):
        registrador.registrar(_pagamento(1))


def test_falha_de_um_observador_interrompe_os_seguintes():
    registrador = RegistradorDePagamentos(FakePagamentoRepository())
    chamadas = []
    registrador.adicionar(MarcarTicketComoPago(FakeTicketRepository()))
    registrador.adicionar(Espiao("depois", chamadas))

    with pytest.raises(TicketNaoEncontrado):
        registrador.registrar(_pagamento(1))

    assert chamadas == []


def test_pagamento_recusado_pelo_repositorio_nao_avisa_ninguem():
    registrador = RegistradorDePagamentos(FakePagamentoRepository())
    chamadas = []
    registrador.registrar(_pagamento(1))
    registrador.adicionar(Espiao("a", chamadas))

    with pytest.raises(model.PagamentoJaRealizadoError):
        registrador.registrar(_pagamento(1, 99.0))

    assert chamadas == []