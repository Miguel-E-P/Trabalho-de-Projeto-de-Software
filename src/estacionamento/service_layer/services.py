import math
from abc import ABC, abstractmethod
from datetime import datetime
import inspect
from typing import Dict, Type, Union
from src.estacionamento.domain.model import TipoVaga, StatusVaga, Vaga, Reserva, Pagamento, Ticket

#Imports para agregado Cliente
from uuid import UUID, uuid4
from typing import Optional, List, Dict, Any
from estacionamento.adapters.repository import AbstractRepository
from estacionamento.domain.model import Cliente, Veiculo, Placa
#Fim dos imports para agregado Cliente

class EstrategiaTarifa(ABC):
    """Abstração base para estratégias de tarifação por tipo de veículo (OCP)."""

    VALOR_HORA: float = 0.0

    def calcular(self, horas: float, recarga: bool = False) -> float:
        if horas <= 0.25:  # Tolerância de 15 minutos (RN-02)
            return 0.0
        return math.ceil(horas) * self.VALOR_HORA


class TarifaCarro(EstrategiaTarifa):
    VALOR_HORA = 10.0

class TarifaMoto(EstrategiaTarifa):
    VALOR_HORA = 5.0

class TarifaSUV(EstrategiaTarifa):
    VALOR_HORA = 15.0

class TarifaCarroEletrico(EstrategiaTarifa):
    VALOR_HORA = 10.0
    TAXA_RECARGA = 8.0

    def calcular(self, horas: float, recarga: bool = False) -> float:
        valor_base = super().calcular(horas, recarga)
        if valor_base > 0.0 and recarga:
            valor_base += self.TAXA_RECARGA
        return valor_base

class CalculadoraTarifa:
    """Domain Service que calcula o valor da permanência para cada veículo (RN-02)."""

    _ESTRATEGIAS: Dict[str, Type[EstrategiaTarifa]] = {
        "CARRO": TarifaCarro,
        "MOTO": TarifaMoto,
        "SUV": TarifaSUV,
        "CAMINHONETE": TarifaSUV,
        "CARRO ELÉTRICO": TarifaCarroEletrico,
        "CARRO_ELETRICO": TarifaCarroEletrico,
    }

    @classmethod
    def registrar_estrategia(
        cls, tipo_veiculo: str, estrategia: Type[EstrategiaTarifa]
    ) -> None:
        cls._ESTRATEGIAS[tipo_veiculo.upper()] = estrategia

    @staticmethod
    def calcular_permanencia_horas(entrada: datetime, saida: datetime) -> float:
        if saida < entrada:
            raise ValueError("Data de saida nao pode ser anterior a data de entrada.")
        return (saida - entrada).total_seconds() / 3600.0

    @classmethod
    def calcular(
        cls,
        *args,
        tipo_veiculo: Union[str, TipoVaga, None] = None,
        entrada: Union[datetime, None] = None,
        saida: Union[datetime, None] = None,
        recarga: bool = False,
        **kwargs
    ) -> float:
        if args:
            if isinstance(args[0], datetime):
                entrada = args[0]
                saida = args[1]
                tipo_veiculo = args[2] if len(args) > 2 else tipo_veiculo
            else:
                tipo_veiculo = args[0]
                entrada = args[1] if len(args) > 1 else entrada
                saida = args[2] if len(args) > 2 else saida

        if entrada is None or saida is None or tipo_veiculo is None:
            raise ValueError("Os parametros entrada, saida e tipo_veiculo sao obrigatorios.")

        horas = cls.calcular_permanencia_horas(entrada, saida)
        chave = (
            tipo_veiculo.value
            if hasattr(tipo_veiculo, "value")
            else str(tipo_veiculo)
        ).upper()

        if chave not in cls._ESTRATEGIAS:
            raise ValueError(f"Tipo de veiculo nao suportado: {tipo_veiculo}")
        estrategia = cls._ESTRATEGIAS[chave]()
        
        sig = inspect.signature(estrategia.calcular)
        if "recarga" in sig.parameters or any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values()):
            return estrategia.calcular(horas, recarga=recarga)
        
        return estrategia.calcular(horas)


class VerificarDisponibilidadeVaga:
    """Domain Service para checagem de vagas e evitar sobreposição de reservas (RN-03)"""

    @staticmethod
    def validar(vaga: Vaga, inicio: datetime, fim: datetime, reservas_existentes: list[Reserva]) -> bool:
        if vaga.status != StatusVaga.LIVRE:
            return False
        if inicio.date() != fim.date():
            return False
        data_solicitada = inicio.date()
        return not any(
            reserva.data_reserva.date() == data_solicitada
            for reserva in reservas_existentes
        )

class AutorizadorSaidaVeiculo:
    """Domain Service responsável por validar se o veículo pode sair (RN-04)"""

    MULTA_PERNOITE = 50.0

    @staticmethod
    def autorizar(vaga: Vaga, ticket: Ticket, pagamento: Pagamento) -> bool:
        if vaga.status != StatusVaga.OCUPADA:
            return False
        if ticket.horarioSaida is None:
            return False
        
        total_devido = CalculadoraTarifa.calcular(tipo_veiculo=vaga.tipo, entrada=ticket.horarioEntrada, saida=ticket.horarioSaida)

        if ticket.horarioSaida.date() != ticket.horarioEntrada.date():
            total_devido += AutorizadorSaidaVeiculo.MULTA_PERNOITE
        if not ticket.pago or pagamento.id_ticket != ticket.idTicket:
            return False

        return True

#Os casos de uso orquestram a busca no Repositório, executam as regras
#  do Domínio e salvam a alteração na Sessão
#AGREGADO CLIENTE - UC01 - Cadastrar Cliente

class ClienteNaoEncontradoException(Exception):
    pass


class InvalidInputException(Exception):
    pass

#UC01
def cadastrar_cliente(
    nome: str,
    cpf: str,
    telefone: str,
    email: str,
    repo: AbstractRepository,
    session,
) -> str:
    id_cliente = uuid4()
    cliente = Cliente(
        id_cliente=id_cliente,
        nome=nome,
        cpf=cpf,
        telefone=telefone,
        email=email,
    )
    repo.add(cliente)
    session.commit()
    return str(id_cliente)

# UC02 - Cadastrar Veículo para Cliente
def cadastrar_veiculo_cliente(
    id_cliente_str: str,
    placa_str: str,
    tipo: str,
    repo: AbstractRepository,
    session,
) -> str:
    try:
        id_cliente = UUID(id_cliente_str)
    except ValueError:
        raise InvalidInputException("ID do cliente inválido.")

    cliente = repo.get(id_cliente)
    if not cliente:
        raise ClienteNaoEncontradoException(f"Cliente {id_cliente_str} não encontrado.")

    id_veiculo = uuid4()
    veiculo = Veiculo(
        id_veiculo=id_veiculo,
        placa=Placa(placa_str),
        tipo=tipo,
    )

    # Invoca o método de negócio da raiz do Agregado
    cliente.cadastrar_veiculo(veiculo)
    session.commit()
    return str(id_veiculo)

# Consulta de Apoio para API/Testes
def buscar_cliente(id_cliente_str: str, repo: AbstractRepository) -> Dict[str, Any]:
    cliente = repo.get(UUID(id_cliente_str))
    if not cliente:
        raise ClienteNaoEncontradoException(f"Cliente {id_cliente_str} não encontrado.")
    
    return {
        "id_cliente": str(cliente.id_cliente),
        "nome": cliente.nome,
        "cpf": cliente.cpf,
        "telefone": cliente.telefone,
        "email": cliente.email,
        "veiculos": [
            {"id_veiculo": str(v.id_veiculo), "placa": v.placa.numero, "tipo": v.tipo}
            for v in cliente.veiculos
        ],
    }

