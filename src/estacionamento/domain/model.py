"""Peço aos colegas que concentrem as importações de lib aqui em cima,
na medida do possível"""

from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID
from typing import List

# Agregado Cliente / Veículo
# Abordagem: da class mais simples até chegar na class raiz

# class value object para Placa (imutável)
@dataclass(frozen=True)
class Placa:
    numero: str

# class entidade
@dataclass
class Veiculo:
    id_veiculo: UUID
    """atributo placa depende do uso de uma placa da class de cima (Placa)"""
    placa: Placa
    tipo: str

# class entidade raiz do agregado
@dataclass
class Cliente:
    id_cliente: UUID
    nome: str
    cpf: str
    telefone: str
    email: str
    """atributo veiculos depende de um veiculo da class de cima (Veiculo)"""
    veiculos: List[Veiculo] = field(default_factory=list)

    # método que vai cadastrar veiculo para um cliente
    def cadastrar_veiculo(self, veiculo: Veiculo) -> None:
        # Verifica se já existe um veículo cadastrado com a mesma placa
        for v in self.veiculos:
            if v.placa == veiculo.placa:
                raise ValueError("Já existe um veículo cadastrado com esta placa.")

        self.veiculos.append(veiculo)

    #metodo p/remover veiculo de um cliente
    def remover_veiculo(self, placa: Placa) -> None:
        self.veiculos = [v for v in self.veiculos if v.placa != placa]

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

class VagaIndisponivel(Exception):
    pass


class VagaNaoEncontrada(Exception):
    pass


@dataclass
class Vaga:
    id_vaga: int
    tipo: TipoVaga
    status: StatusVaga = StatusVaga.LIVRE

    def ocupar(self) -> None:
        if self.status != StatusVaga.LIVRE:
            raise VagaIndisponivel(f"Vaga {self.id_vaga} indisponível.")

        self.status = StatusVaga.OCUPADA


@dataclass
class Estacionamento:
    vagas: list[Vaga]

    def buscar_vaga(self, id_vaga: int) -> Vaga:
        for vaga in self.vagas:
            if vaga.id_vaga == id_vaga:
                return vaga

        raise VagaNaoEncontrada(f"Vaga {id_vaga} não encontrada.")

    def ocupar_vaga(self, id_vaga: int) -> None:
        vaga = self.buscar_vaga(id_vaga)
        vaga.ocupar()


#Agregado Reserva
class DataInvalida(ValueError):
    pass

class Ticket:
    horarioEntrada:datetime
    horarioSaida:datetime
    idTicket:int
    

@dataclass(frozen=True)
class Reserva:
    id_reserva: int
    data_reserva: datetime
    hoje: datetime
    placa_veiculo_reserva: str

    # INVARIANTE: protege contra valor negativo.
    # Data de reserva do veículo não pode ser anterior à data hoje
    def __post_init__(self):
        if self.id_reserva < 0:
            raise ValueError("Valor não pode ser negativo.")

        if self.data_reserva < self.hoje:
            raise DataInvalida("Essa data está indisponível para reserva.")
        

    
            

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
class PagamentoJaRealizadoError(Exception):
    pass

@dataclass
class Pagamento:
    id_pagamento: int 
    id_ticket: int
    valor: Dinheiro
    tipo_pagamento: TipoPagamento | None = None
    pago: bool = False
    data_hora_pagamento: datetime | None = None
    
    def pagar(self, tipo: TipoPagamento, momento: datetime):
        if self.pago:
            raise PagamentoJaRealizadoError("ERROR: Ticket ja esta pago.")
        
        self.tipo_pagamento = tipo
        self.pago = True
        self.data_hora_pagamento = momento


# fim-pagamento

#fim-AGREGADO PAGAMENTO

