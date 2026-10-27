"""Peço aos colegas que concentrem as importações de lib aqui em cima,
na medida do possível"""

from datetime import datetime
from dataclasses import dataclass, field, FrozenInstanceError
from enum import Enum
import re
from uuid import UUID
from typing import List

# Agregado Cliente / Veículo
# Abordagem: da class mais simples até chegar na class raiz

# class value object para Placa (imutável)
# Value Object Placa com validação própria (SRP)
@dataclass(frozen=True)
class Placa:
    numero: str

    def __post_init__(self):
        # Garante a invariante de domínio do próprio Value Object
        if not self.numero or not self._validar_formato(self.numero):
            raise ValueError(f"Placa inválida: '{self.numero}' não atende ao formato esperado.")

    @staticmethod
    def _validar_formato(placa_str: str) -> bool:
        # Aceita padrão antigo (ABC1234) ou Mercosul (ABC1D23)
        padrao = r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$'
        return bool(re.match(padrao, placa_str.upper().replace("-", "")))


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
    id_estacionamento: int
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

class PagamentoJaRealizadoError(Exception):
    pass

@dataclass
class Ticket:
    idTicket: int
    horarioEntrada:datetime
    horarioSaida:datetime | None
    pago: bool = False

    # INVARIANTE: protege contra valor negativo.
    def __post_init__(self):
        if self.idTicket < 0:
            raise ValueError("Valor não pode ser negativo.")

    # Data de saída do veículo não pode ser anterior à data de entrada
    def updateSaida(self, horarioSaida: datetime) -> None:
        if horarioSaida < self.horarioEntrada:
            raise DataInvalida("Essa data está indisponível para a saída.")
        self.horarioSaida = horarioSaida

    def registrar_pagamento(self) -> None:
        if self.pago:
            raise PagamentoJaRealizadoError("ERROR: Ticket ja foi pago.")
        self.pago = True


    

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
    id_ticket: int
    valor: float
    tipo_pagamento: TipoPagamento
    data_hora_pagamento: datetime

    def __post_init__(self):
        if self.valor < 0.0:
            raise ValueError("ERROR: Valor do pagamento NAO pode ser negativo")

    def __setattr__(self, name, value):
        if name in self.__dataclass_fields__ and name in self.__dict__:
            raise FrozenInstanceError("ERROR: Nao pode alterar pagamento")
        super().__setattr__(name, value)
# fim-pagamento

#fim-AGREGADO PAGAMENTO

