from uuid import uuid4
from dataclasses import FrozenInstanceError

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
def test_dinheiro_invariante_negativa():
    with pytest.raises(ValueError, match="Valor NAO pode ser negativo."):
        Dinheiro(valor=-67.00)

def test_dinheiro_igualdade():
    assert Dinheiro(67.0) == Dinheiro(67.0)
    assert Dinheiro(67.0) != Dinheiro(14.0)

def test_dinheiro_imutabilidade():
    dinheiro = Dinheiro(15.0)
    with pytest.raises(FrozenInstanceError):
        dinheiro.valor = 25.0

def test_pagamento_inicializacao():
    valor = Dinheiro(valor=50.0)
    pagamento = Pagamento(id_pagamento=1, id_ticket=100, valor=valor)

    assert pagamento.id_pagamento == 1
    assert pagamento.id_ticket == 100
    assert pagamento.valor == valor
    assert pagamento.pago is False
    assert pagamento.tipo_pagamento is None
    assert pagamento.data_hora_pagamento is None

def test_pagamento_execucao_sucesso():
    valor = Dinheiro(valor=35.0)
    pagamento = Pagamento(id_pagamento=1, id_ticket=100, valor=valor)
    momento_pagamento = datetime(2026, 9, 18, 10, 30, 0)

    pagamento.pagar(tipo=TipoPagamento.PIX, momento=momento_pagamento)

    assert pagamento.pago is True
    assert pagamento.tipo_pagamento == TipoPagamento.PIX
    assert pagamento.data_hora_pagamento == momento_pagamento

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
    estacionamento = model.Estacionamento([vaga])

    assert estacionamento.buscar_vaga(vaga.id_vaga) == vaga


def test_buscar_vaga_nao_cadastrada():
    vaga_cadastrada = model.Vaga(1, model.TipoVaga.CARRO, model.StatusVaga.LIVRE)
    vaga_nao_cadastrada = model.Vaga(2, model.TipoVaga.CARRO, model.StatusVaga.LIVRE)

    estacionamento = model.Estacionamento([vaga_cadastrada])

    with pytest.raises(model.VagaNaoEncontrada, match=f"Vaga {vaga_nao_cadastrada.id_vaga} não encontrada."):
        estacionamento.buscar_vaga(vaga_nao_cadastrada.id_vaga)

def test_ocupar_vaga_estacionamento():
    vaga = model.Vaga(1, model.TipoVaga.CARRO, model.StatusVaga.LIVRE)
    estacionamento = model.Estacionamento([vaga])

    estacionamento.ocupar_vaga(vaga.id_vaga)
    
    assert vaga.status == model.StatusVaga.OCUPADA