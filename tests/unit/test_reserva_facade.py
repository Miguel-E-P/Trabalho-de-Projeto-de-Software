from datetime import datetime

import pytest

from estacionamento.adapters.repository import (
    FakeEstacionamentoRepository,
    FakeReservaRepository,
    FakeTicketRepository,
)
from estacionamento.domain import model
from estacionamento.service_layer.pagamento_observer import TicketNaoEncontrado
from estacionamento.service_layer.reserva_facade import (
    EstacionamentoNaoEncontrado,
    FachadaReserva,
    ReservaJaExiste,
    TicketJaExiste,
)

AGORA = datetime(2026, 11, 2, 10, 0)
ENTRADA = datetime(2026, 11, 2, 10, 0)


class FakeSession:
    def __init__(self):
        self.commits = 0

    def commit(self):
        self.commits += 1


class CalculadoraEspia:
    """Calculadora de teste: prova que a fachada delega o calculo."""

    def __init__(self, valor=42.0):
        self.valor = valor
        self.chamadas = []

    def calcular(self, *, tipo_veiculo, entrada, saida, recarga=False):
        self.chamadas.append((tipo_veiculo, entrada, saida, recarga))
        return self.valor


def _montar(vagas=None, calculadora=None):
    estacionamento = model.Estacionamento(
        1, vagas if vagas is not None else [model.Vaga(10, model.TipoVaga.CARRO)]
    )
    reservas = FakeReservaRepository()
    tickets = FakeTicketRepository()
    session = FakeSession()
    fachada = FachadaReserva(
        reservas,
        tickets,
        FakeEstacionamentoRepository([estacionamento]),
        calculadora=calculadora,
        session=session,
        agora=lambda: AGORA,
    )
    return fachada, reservas, tickets, estacionamento, session


# --- reservar ---------------------------------------------------------------

def test_reservar_guarda_a_reserva_e_faz_commit():
    fachada, reservas, _, _, session = _montar()
    data = datetime(2026, 12, 1, 9, 0)

    reserva = fachada.reservar(5, data, "ABC1D23")

    assert reservas.get(5) is reserva
    assert reserva.hoje == AGORA
    assert reserva.data_reserva == data
    assert session.commits == 1


def test_reservar_com_id_repetido_e_recusado():
    fachada, reservas, _, _, session = _montar()
    fachada.reservar(5, datetime(2026, 12, 1), "ABC1D23")

    with pytest.raises(ReservaJaExiste, match="Reserva 5 ja existe."):
        fachada.reservar(5, datetime(2026, 12, 2), "XYZ9A88")

    assert len(reservas.list()) == 1
    assert session.commits == 1


def test_reservar_data_no_passado_propaga_erro_do_dominio_sem_gravar():
    fachada, reservas, _, _, session = _montar()

    with pytest.raises(model.DataInvalida):
        fachada.reservar(5, datetime(2026, 1, 1), "ABC1D23")

    assert reservas.list() == []
    assert session.commits == 0


# --- registrar_entrada ------------------------------------------------------

def test_entrada_abre_ticket_sem_saida_e_ocupa_a_vaga():
    fachada, _, tickets, estacionamento, session = _montar()

    ticket = fachada.registrar_entrada(1, id_estacionamento=1, id_vaga=10)

    assert tickets.get(1) is ticket
    assert ticket.horarioEntrada == AGORA
    assert ticket.horarioSaida is None
    assert ticket.pago is False
    assert isinstance(estacionamento.buscar_vaga(10).status, model.VagaOcupada)
    assert session.commits == 1


def test_entrada_usa_o_horario_informado():
    fachada, *_ = _montar()
    horario = datetime(2026, 11, 2, 8, 30)

    ticket = fachada.registrar_entrada(1, 1, 10, horario_entrada=horario)

    assert ticket.horarioEntrada == horario


def test_entrada_em_vaga_ocupada_nao_grava_ticket():
    fachada, _, tickets, _, session = _montar(
        vagas=[model.Vaga(10, model.TipoVaga.CARRO, model.VagaOcupada())]
    )

    with pytest.raises(model.VagaIndisponivel):
        fachada.registrar_entrada(1, 1, 10)

    assert tickets.list() == []
    assert session.commits == 0


def test_entrada_aplica_a_politica_de_ocupacao():
    fachada, _, tickets, estacionamento, _ = _montar(
        vagas=[model.Vaga(10, model.TipoVaga.MOTO)]
    )
    carro = model.Veiculo(None, model.Placa("ABC1D23"), "carro")

    with pytest.raises(model.VagaIndisponivel, match="não autorizado"):
        fachada.registrar_entrada(
            1, 1, 10, veiculo=carro, politica=model.PoliticaVagaMoto()
        )

    assert tickets.list() == []
    assert isinstance(estacionamento.buscar_vaga(10).status, model.VagaLivre)


def test_entrada_em_vaga_inexistente():
    fachada, _, tickets, _, _ = _montar()

    with pytest.raises(model.VagaNaoEncontrada):
        fachada.registrar_entrada(1, 1, 99)

    assert tickets.list() == []


def test_entrada_em_estacionamento_inexistente():
    fachada, *_ = _montar()

    with pytest.raises(EstacionamentoNaoEncontrado, match="Estacionamento 7"):
        fachada.registrar_entrada(1, 7, 10)


def test_entrada_com_id_de_ticket_repetido_nao_ocupa_outra_vaga():
    fachada, _, tickets, estacionamento, _ = _montar(
        vagas=[
            model.Vaga(10, model.TipoVaga.CARRO),
            model.Vaga(11, model.TipoVaga.CARRO),
        ]
    )
    fachada.registrar_entrada(1, 1, 10)

    with pytest.raises(TicketJaExiste, match="Ticket 1 ja existe."):
        fachada.registrar_entrada(1, 1, 11)

    assert len(tickets.list()) == 1
    assert isinstance(estacionamento.buscar_vaga(11).status, model.VagaLivre)


def test_entrada_com_id_invalido_nao_ocupa_a_vaga():
    fachada, _, tickets, estacionamento, session = _montar()

    with pytest.raises(ValueError, match="negativo"):
        fachada.registrar_entrada(-1, 1, 10)

    assert tickets.list() == []
    assert isinstance(estacionamento.buscar_vaga(10).status, model.VagaLivre)
    assert session.commits == 0


# --- registrar_saida --------------------------------------------------------

def test_saida_grava_horario_e_devolve_o_valor_da_tarifa_real():
    fachada, _, tickets, _, session = _montar()
    fachada.registrar_entrada(1, 1, 10, horario_entrada=ENTRADA)

    valor = fachada.registrar_saida(
        1, "CARRO", horario_saida=datetime(2026, 11, 2, 12, 0)
    )

    assert valor == 20.0  # 2 h x R$ 10,00
    assert tickets.get(1).horarioSaida == datetime(2026, 11, 2, 12, 0)
    assert session.commits == 2  # entrada + saida


def test_saida_dentro_da_tolerancia_nao_cobra():
    fachada, *_ = _montar()
    fachada.registrar_entrada(1, 1, 10, horario_entrada=ENTRADA)

    valor = fachada.registrar_saida(
        1, "CARRO", horario_saida=datetime(2026, 11, 2, 10, 15)
    )

    assert valor == 0.0


def test_saida_de_carro_eletrico_com_recarga_soma_a_taxa():
    fachada, *_ = _montar(vagas=[model.Vaga(10, model.TipoVaga.CARRO_ELETRICO)])
    fachada.registrar_entrada(1, 1, 10, horario_entrada=ENTRADA)

    valor = fachada.registrar_saida(
        1,
        model.TipoVaga.CARRO_ELETRICO,
        horario_saida=datetime(2026, 11, 2, 11, 0),
        recarga=True,
    )

    assert valor == 18.0  # 1 h x R$ 10,00 + R$ 8,00 de recarga


def test_saida_delega_o_calculo_para_a_calculadora_injetada():
    calculadora = CalculadoraEspia(valor=42.0)
    fachada, *_ = _montar(calculadora=calculadora)
    fachada.registrar_entrada(1, 1, 10, horario_entrada=ENTRADA)
    saida = datetime(2026, 11, 2, 13, 0)

    valor = fachada.registrar_saida(1, "MOTO", horario_saida=saida, recarga=True)

    assert valor == 42.0
    assert calculadora.chamadas == [("MOTO", ENTRADA, saida, True)]


def test_saida_usa_o_relogio_da_fachada_quando_nao_informada():
    calculadora = CalculadoraEspia()
    fachada, _, tickets, _, _ = _montar(calculadora=calculadora)
    fachada.registrar_entrada(1, 1, 10, horario_entrada=datetime(2026, 11, 2, 8, 0))

    fachada.registrar_saida(1, "CARRO")

    assert tickets.get(1).horarioSaida == AGORA


def test_saida_de_ticket_inexistente():
    fachada, *_ = _montar()

    with pytest.raises(TicketNaoEncontrado, match="Ticket 9 nao encontrado."):
        fachada.registrar_saida(9, "CARRO")


def test_saida_antes_da_entrada_nao_altera_o_ticket():
    fachada, _, tickets, _, session = _montar()
    fachada.registrar_entrada(1, 1, 10, horario_entrada=ENTRADA)

    with pytest.raises(model.DataInvalida):
        fachada.registrar_saida(1, "CARRO", horario_saida=datetime(2026, 11, 1))

    assert tickets.get(1).horarioSaida is None
    assert session.commits == 1  # so a entrada


def test_saida_com_tipo_de_veiculo_invalido_desfaz_a_saida():
    fachada, _, tickets, _, session = _montar()
    fachada.registrar_entrada(1, 1, 10, horario_entrada=ENTRADA)

    with pytest.raises(ValueError, match="nao suportado"):
        fachada.registrar_saida(
            1, "HELICOPTERO", horario_saida=datetime(2026, 11, 2, 12, 0)
        )

    assert tickets.get(1).horarioSaida is None
    assert session.commits == 1


# --- fluxo completo e acesso direto ----------------------------------------

def test_fluxo_completo_reserva_entrada_e_saida():
    fachada, reservas, tickets, _, _ = _montar()

    fachada.reservar(1, datetime(2026, 11, 2, 11, 0), "ABC1D23")
    fachada.registrar_entrada(1, 1, 10, horario_entrada=ENTRADA)
    valor = fachada.registrar_saida(
        1, "SUV", horario_saida=datetime(2026, 11, 2, 10, 30)
    )

    assert valor == 15.0  # 30 min arredondam para 1 h x R$ 15,00
    assert reservas.get(1) is not None
    assert tickets.get(1).horarioSaida == datetime(2026, 11, 2, 10, 30)


def test_fachada_nao_impede_o_uso_direto_do_subsistema():
    fachada, _, tickets, _, _ = _montar()
    fachada.registrar_entrada(1, 1, 10, horario_entrada=ENTRADA)

    # Quem precisa de controle fino continua falando com o repositorio e o modelo.
    tickets.get(1).registrar_pagamento()

    assert tickets.get(1).pago is True


def test_fachada_funciona_sem_sessao():
    fachada = FachadaReserva(
        FakeReservaRepository(),
        FakeTicketRepository(),
        FakeEstacionamentoRepository([model.Estacionamento(1, [])]),
        agora=lambda: AGORA,
    )

    assert fachada.reservar(1, datetime(2026, 12, 1), "ABC1D23").id_reserva == 1
