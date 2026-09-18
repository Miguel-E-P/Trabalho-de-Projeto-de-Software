from uuid import uuid4
from dataclasses import FrozenInstanceError

import pytest

import src.estacionamento.domain.model


#Testes unitários para o agregado cliente
#Primeiro teste: verificar se um cliente consegue cadastrar um veículo

def test_cliente_pode_cadastrar_um_veiculo():
    cliente = estacionamento.domain.model.Cliente(
        id_cliente=uuid4(),
        nome="João",
        cpf="11111111111",
        telefone="21999999999",
        email="joao@email.com",
    )

    veiculo = estacionamento.domain.model.Veiculo(
        id_veiculo=uuid4(),
        placa=estacionamento.domain.model.Placa("ABC1D23"),
        tipo="Carro",
    )

    cliente.cadastrar_veiculo(veiculo)

    assert veiculo in cliente.veiculos
    
#Fim do primeiro teste no agregado cliente


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
