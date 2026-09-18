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
#FIM AGREGADO PAGAMENTO
