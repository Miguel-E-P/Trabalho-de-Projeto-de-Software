import math
from datetime import datetime
from src.estacionamento.domain.model import TipoVaga, StatusVaga, Vaga, Reserva, Pagamento, Ticket
#Imports para agregado Cliente
from uuid import UUID, uuid4
from typing import Optional, List, Dict, Any
from estacionamento.adapters.repository import AbstractRepository
from estacionamento.domain.model import Cliente, Veiculo, Placa
#Fim dos imports para agregado Cliente

class CalculadoraTarifa:
    """Domain Service que calcula o valor da permanência para cada veículo (RN-02)"""

    TARIFA_CARRO = 10.0
    TARIFA_MOTO = 5.0
    TARIFA_CAMINHONETE = 15.0
    TAXA_RECARGA = 8.0

    @staticmethod
    def calcular(tipo_veiculo: TipoVaga, entrada: datetime, saida: datetime, recarga: bool = False) -> float:
        segundos = (saida - entrada).total_seconds()
        # Tolerância de 15 minutos
        if segundos <= 900:
            return 0.0
        horas = segundos / 3600
        horas_cobranca = math.ceil(horas)

        categoria = (tipo_veiculo.value if hasattr(tipo_veiculo, "value") else str(tipo_veiculo))
        if categoria == TipoVaga.MOTO.value:
            taxa = CalculadoraTarifa.TARIFA_MOTO
        elif categoria in ["caminhonete", "SUV"]:
            taxa = CalculadoraTarifa.TARIFA_CAMINHONETE
        else:
            taxa = CalculadoraTarifa.TARIFA_CARRO

        total = float(horas_cobranca * taxa)
        if tipo_veiculo == TipoVaga.CARRO_ELETRICO and recarga:
            total+=CalculadoraTarifa.TAXA_RECARGA
        return total


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
            {"id_veiculo": str(v.id_veiculo), "placa": v.placa.valor, "tipo": v.tipo}
            for v in cliente.veiculos
        ],
    }

