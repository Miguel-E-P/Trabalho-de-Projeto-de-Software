''' Peço aos colegas que concentrem as importações de lib aqui em cima,
na medida do possível'''

from dataclasses import dataclass


# Agregado Cliente / Veículo
# Abordagem: da class mais simples até chegar na class raiz

#class value object 
@dataclass(frozen=True)
class Placa:
    numero = str

#class entidade
class Veiculo:
    id_veiculo = int
    '''atributo placa depende do uso de uma placa da class de cima (Placa)'''
    placa = str 
    tipo = str

#class entidade raiz do agregado
class Cliente:
    id_cliente = int
    nome = str
    '''atributo veiculo depende de um veiculo da class de cima (Veiculo)'''
    veiculo = str 
#método que vai cadastrar veiculo para um cliente
    def cadastrar_veiculo():
        placas = str
#Fim do agregado cliente/ veiculo
      
