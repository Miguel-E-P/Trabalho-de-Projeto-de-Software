"""Peço aos colegas que concentrem as importações de lib aqui em cima,
na medida do possível"""

import datetime
from dataclasses import dataclass
from enum import Enum

# Agregado Cliente / Veículo
# Abordagem: da class mais simples até chegar na class raiz


# class value object
@dataclass(frozen=True)
class Placa:
    numero = str


# class entidade
class Veiculo:
    id_veiculo = int
    """atributo placa depende do uso de uma placa da class de cima (Placa)"""
    placa = str
    tipo = str


# class entidade raiz do agregado
class Cliente:
    id_cliente = int
    nome = str
    """atributo veiculo depende de um veiculo da class de cima (Veiculo)"""
    veiculo = str

    # método que vai cadastrar veiculo para um cliente
    def cadastrar_veiculo():
        placas = str


# Fim do agregado cliente/ veiculo

# Agregado Estacionamento
class TipoVaga(Enum):
    CARRO = "carro"
    MOTO = "moto"
    CARRO_ELETRICO = "carro elétrico"


class StatusVaga(Enum):
    LIVRE = "livre"
    OCUPADA = "ocupada"
    RESERVADA = "reservada"


@dataclass
class Vaga:
    id_vaga: int
    tipo: TipoVaga
    status: StatusVaga = StatusVaga.LIVRE


@dataclass
class Estacionamento:
    vagas: list[Vaga]


#Agregado Reserva

class Ticket:
    horarioEntrada:datetime
    horarioSaida:datetime
    idTicket:int

@dataclass(frozen=True)
class Reserva:
    id_reserva: int
    data_reserva: datetime
    duracao_reserva: datetime.time
    placa_veiculo_reserva: str


# Fim do Agregado Reserva


# AGREGADO PAGAMENTO

# ini-dinheiro
@dataclass(frozen=True)
class Dinheiro:
    valor: float

    # INVARIANTE: protege contra valor negativo.
    def __post_init__(self):
        if self.valor < 0.0:
            raise ValueError("Valor NAO pode ser negativo.")


# fim-dinheiro

#ini-tipo_pagamento
class TipoPagamento(Enum):
    CREDITO = "credito"
    DEBITO = "debito"
    PIX = "pix"
    DINHEIRO_VIVO = "dinheiro_vivo"

#fim-tipo_pagamento

# ini-pagamento
@dataclass
class Pagamento:
    id_pagamento: int 
    id_ticket: int
    valor: Dinheiro
    tipo_pagamento: TipoPagamento | None = None
    pago: bool = False
    
    def pagar(self, tipo: TipoPagamento):
        self.tipo_pagamento = tipo
        self.pago = True


# fim-pagamento

#fim-AGREGADO PAGAMENTO

