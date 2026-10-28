from uuid import uuid4
from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from estacionamento.domain import model
from estacionamento.domain.model import Cliente, Veiculo, Placa


#Testes unitários para o agregado cliente
#Primeiro teste: verificar se um cliente consegue cadastrar um veículo

def test_cliente_pode_cadastrar_um_veiculo():
    cliente = Cliente(
        id_cliente=uuid4(),
        nome="João",
        cpf="11111111111",
        telefone="21999999999",
        email="joao@email.com",
    )

    veiculo = Veiculo(
        id_veiculo=uuid4(),
        placa=Placa("ABC1D23"),
        tipo="Carro",
    )

    cliente.cadastrar_veiculo(veiculo)

    assert veiculo in cliente.veiculos
    
#Fim do primeiro teste no agregado cliente

#Segundo teste
#A RN-01 diz que um cliente pode ter vários veículos.
def test_cliente_pode_cadastrar_varios_veiculos():
    cliente = Cliente(
        id_cliente=uuid4(),
        nome="João",
        cpf="11111111111",
        telefone="21999999999",
        email="joao@email.com",
    )

    veiculo1 = Veiculo(
        id_veiculo=uuid4(),
        placa=Placa("ABC1D23"),
        tipo="Carro",
    )

    veiculo2 = Veiculo(
        id_veiculo=uuid4(),
        placa=Placa("XYZ9A88"),
        tipo="Moto",
    )

    cliente.cadastrar_veiculo(veiculo1)
    cliente.cadastrar_veiculo(veiculo2)

    assert len(cliente.veiculos) == 2

#Fim do segundo teste no agregado cliente

#Terceiro teste
#Não permitir duas placas iguais para o mesmo cliente.
def test_nao_permite_cadastrar_duas_vezes_a_mesma_placa():
    cliente = Cliente(
        id_cliente=uuid4(),
        nome="João",
        cpf="11111111111",
        telefone="21999999999",
        email="joao@email.com",
    )

    veiculo1 = Veiculo(
        id_veiculo=uuid4(),
        placa=Placa("ABC1D23"),
        tipo="Carro",
    )

    veiculo2 = Veiculo(
        id_veiculo=uuid4(),
        placa=Placa("ABC1D23"),
        tipo="Carro",
    )

    cliente.cadastrar_veiculo(veiculo1)

    with pytest.raises(Exception):
        cliente.cadastrar_veiculo(veiculo2)


#Fim do terceiro teste no agregado cliente

#Quarto teste
#Verificar se um cliente recém-criado inicia sem veículos.
def test_cliente_novo_comeca_sem_veiculos():
    cliente = Cliente(
        id_cliente=uuid4(),
        nome="João",
        cpf="11111111111",
        telefone="21999999999",
        email="joao@email.com",
    )

    assert len(cliente.veiculos) == 0

#Fim do quarto teste unitário no agregado cliente

#Testes no Agregado Cliente para implementar o Refactor (melhorar o código) do TDD
def test_cliente_possui_veiculo_cadastrado():
    cliente = Cliente(
        id_cliente=uuid4(),
        nome="João",
        cpf="11111111111",
        telefone="21999999999",
        email="joao@email.com",
    )
    veiculo = Veiculo(
        id_veiculo=uuid4(),
        placa=Placa("ABC1D23"),
        tipo="Carro",
    )
    cliente.cadastrar_veiculo(veiculo)

    assert veiculo in cliente.veiculos


def test_cliente_nao_possui_veiculo_inexistente():
    cliente = Cliente(
        id_cliente=uuid4(),
        nome="João",
        cpf="11111111111",
        telefone="21999999999",
        email="joao@email.com",
    )
    veiculo_inexistente = Veiculo(
        id_veiculo=uuid4(),
        placa=Placa("XYZ9Y88"),
        tipo="Moto",
    )

    assert veiculo_inexistente not in cliente.veiculos

def test_remover_veiculo():
    cliente = Cliente(
        id_cliente=uuid4(),
        nome="João",
        cpf="11111111111",
        telefone="21999999999",
        email="joao@email.com",
    )
    veiculo = Veiculo(
        id_veiculo=uuid4(),
        placa=Placa("ABC1D23"),
        tipo="Carro",
    )
    cliente.cadastrar_veiculo(veiculo)

    #Implementar o método remover_veiculo na entidade Cliente
    cliente.remover_veiculo(veiculo.placa)

def test_alterar_tipo_de_veiculo():
    veiculo = Veiculo(
        id_veiculo=uuid4(),
        placa=Placa("ABC1D23"),
        tipo="Carro",
    )

    # Ação: Altera o atributo tipo do Veículo
    veiculo.tipo = "SUV"

    assert veiculo.tipo == "SUV"



#INI AGREGADO PAGAMENTO
def test_pagamento_dinheiro_invariante_negativa():
    momento = datetime(2026, 9, 18, 10, 30, 0)
    with pytest.raises(ValueError, match="ERROR: Valor do pagamento NAO pode ser negativo"):
        model.Pagamento(
            id_ticket=100,
            valor=-67.00,
            tipo_pagamento=model.TipoPagamento.PIX,
            data_hora_pagamento=momento
        )

def test_pagamento_inicializacao():
    momento = datetime(2026, 9, 18, 10, 30, 0)
    pagamento = model.Pagamento(id_ticket=100, valor=50.0, tipo_pagamento=model.TipoPagamento.PIX, data_hora_pagamento=momento)

    assert pagamento.id_ticket == 100
    assert pagamento.valor == 50.0
    assert pagamento.tipo_pagamento == model.TipoPagamento.PIX
    assert pagamento.data_hora_pagamento == momento

def test_pagamento_imutabilidade():
    valor = 50.0
    momento = datetime(2026, 9, 18, 10, 30, 0)
    pagamento = model.Pagamento(id_ticket=100, valor=50.0, tipo_pagamento=model.TipoPagamento.PIX, data_hora_pagamento=momento)

    with pytest.raises(FrozenInstanceError):
        pagamento.id_ticket = 101


@pytest.mark.parametrize(
    "campo, novo_valor",
    [
        ("valor", 99.0),
        ("tipo_pagamento", model.TipoPagamento.DEBITO),
        ("data_hora_pagamento", datetime(2030, 1, 1)),
    ],
)
def test_pagamento_todos_os_campos_sao_imutaveis(campo, novo_valor):
    pagamento = model.Pagamento(100, 50.0, model.TipoPagamento.PIX, datetime(2026, 9, 18, 10, 30))

    with pytest.raises(FrozenInstanceError):
        setattr(pagamento, campo, novo_valor)


def test_pagamento_nao_bloqueia_atributos_que_nao_sao_campos_de_dominio():
    pagamento = model.Pagamento(100, 50.0, model.TipoPagamento.PIX, datetime(2026, 9, 18, 10, 30))

    pagamento._estado_externo = "a"
    pagamento._estado_externo = "b"

    assert pagamento._estado_externo == "b"


def test_pagamento_valor_zero_e_valido():
    pagamento = model.Pagamento(100, 0.0, model.TipoPagamento.DINHEIRO_VIVO, datetime(2026, 9, 18, 10, 30))

    assert pagamento.valor == 0.0

#FIM AGREGADO PAGAMENTO

# Testes Agregado Estacionamento
def test_ocupar_vaga_livre():
    vaga = model.Vaga(1, model.TipoVaga.CARRO, model.StatusVaga.LIVRE)
    vaga.ocupar()

    assert vaga.status == model.StatusVaga.OCUPADA


def test_ocupar_vaga_indisponivel():
    vaga = model.Vaga(1, model.TipoVaga.CARRO, model.StatusVaga.OCUPADA)

    with pytest.raises(model.VagaIndisponivel, match=f"Vaga {vaga.id_vaga} indisponível."):
        vaga.ocupar()


def test_buscar_vaga_cadastrada():
    vaga = model.Vaga(1, model.TipoVaga.CARRO, model.StatusVaga.LIVRE)
    estacionamento = model.Estacionamento(1, [vaga])

    assert estacionamento.buscar_vaga(vaga.id_vaga) == vaga


def test_buscar_vaga_nao_cadastrada():
    vaga_cadastrada = model.Vaga(1, model.TipoVaga.CARRO, model.StatusVaga.LIVRE)
    vaga_nao_cadastrada = model.Vaga(2, model.TipoVaga.CARRO, model.StatusVaga.LIVRE)

    estacionamento = model.Estacionamento(1, [vaga_cadastrada])

    with pytest.raises(model.VagaNaoEncontrada, match=f"Vaga {vaga_nao_cadastrada.id_vaga} não encontrada."):
        estacionamento.buscar_vaga(vaga_nao_cadastrada.id_vaga)

def test_ocupar_vaga_estacionamento():
    vaga = model.Vaga(1, model.TipoVaga.CARRO, model.StatusVaga.LIVRE)
    estacionamento = model.Estacionamento(1, [vaga])

    estacionamento.ocupar_vaga(vaga.id_vaga)

    assert vaga.status == model.StatusVaga.OCUPADA


#Testes unitários para o agregado Reserva
 
#testes de ticket
def test_ticket_inicializacao():
    ticket = model.Ticket(112, datetime(2026, 12, 2, 18, 13), None)
 
    assert ticket.idTicket == 112
    assert ticket.horarioEntrada == datetime(2026, 12, 2, 18, 13)
    assert ticket.horarioSaida == None
    assert ticket.pago is False
 
 
def test_ticket_invariante_negativa():
    with pytest.raises(ValueError, match="Valor não pode ser negativo."):
        model.Ticket(-112, datetime(2026, 12, 2, 18, 13), None)
 
def test_ticket_saida():
    ticket = model.Ticket(112, datetime(2026, 12, 2, 18, 13), None)
    horarioSaida=datetime(2025, 12, 2, 18, 13)
    with pytest.raises(model.DataInvalida, match="Essa data está indisponível para a saída."):
        ticket.updateSaida(horarioSaida)
       
def test_ticket_pagamento_sucesso():
    ticket = model.Ticket(112, datetime(2026, 12, 2, 18, 13), None)
    ticket.registrar_pagamento()
    assert ticket.pago is True
 
def test_ticket_prevenir_pagamento_duplicado():
    ticket = model.Ticket(112, datetime(2026, 12, 2, 18, 13), None)
    ticket.registrar_pagamento()
 
    with pytest.raises(model.PagamentoJaRealizadoError, match ="ERROR: Ticket ja foi pago."):
        ticket.registrar_pagamento()
 
 
#tests reserva
def test_reserva_igualdade():
    hoje = datetime(2026, 9, 2)
    assert model.Reserva(12, datetime(2026, 12, 2), hoje, "ASD-3456") == model.Reserva(12, datetime(2026, 12, 2), hoje, "ASD-3456")
    assert model.Reserva(12, datetime(2026, 12, 2), hoje, "ASD-3456") != model.Reserva(16, datetime(2026, 10, 4), hoje, "FHE-3782")
 
   
def test_reserva_imutabilidade():
    reserva = model.Reserva(12, datetime(2026, 12, 2), datetime(2026, 9, 2), "ASD-3456")
    with pytest.raises(FrozenInstanceError):
        reserva.id_reserva = 13
 
def test_reserva_inicializacao():
    hoje = datetime(2026, 9, 2)
    data_reserva = datetime(2026, 12, 2)
    reserva = model.Reserva(12, data_reserva, hoje, "ASD-3456")
 
    assert reserva.id_reserva == 12
    assert reserva.data_reserva == data_reserva
    assert reserva.hoje == hoje
    assert reserva.placa_veiculo_reserva == "ASD-3456"
 
def test_reserva_invariante_negativa():
    with pytest.raises(ValueError, match="Valor não pode ser negativo."):
        model.Reserva(-12, datetime(2026, 12, 2), datetime(2026, 9, 2), "ASD-3456")
 
 
def test_reserva_data_passado():
    with pytest.raises(model.DataInvalida, match="Essa data está indisponível para reserva."):
        model.Reserva(12, datetime(2025, 8, 12), datetime(2026, 9, 2), "ASD-3456")
 
#Fim do primeiro teste no agregado reserva
 

def test_ticket_e_reserva_aceitam_id_zero():
    ticket = model.Ticket(0, datetime(2026, 12, 2, 18, 13), None)
    reserva = model.Reserva(0, datetime(2026, 12, 2), datetime(2026, 9, 2), "ASD-3456")
 
    assert ticket.idTicket == 0
    assert reserva.id_reserva == 0
 
 
def test_ticket_saida_valida_atualiza_horario():
    ticket = model.Ticket(112, datetime(2026, 12, 2, 18, 13), None)
    saida = datetime(2026, 12, 2, 20, 0)
 
    ticket.updateSaida(saida)
 
    assert ticket.horarioSaida == saida
 
 
def test_ticket_saida_igual_a_entrada_e_valida():
    entrada = datetime(2026, 12, 2, 18, 13)
    ticket = model.Ticket(112, entrada, None)
 
    ticket.updateSaida(entrada)
 
    assert ticket.horarioSaida == entrada
 
 
def test_ticket_saida_invalida_nao_altera_horario_anterior():
    ticket = model.Ticket(112, datetime(2026, 12, 2, 18, 13), None)
 
    with pytest.raises(model.DataInvalida):
        ticket.updateSaida(datetime(2026, 12, 1, 10, 0))
 
    assert ticket.horarioSaida is None
 
 
def test_reserva_para_o_proprio_dia_de_hoje_e_valida():
    hoje = datetime(2026, 9, 2, 10, 0)
 
    reserva = model.Reserva(12, hoje, hoje, "ASD-3456")
 
    assert reserva.data_reserva == hoje
