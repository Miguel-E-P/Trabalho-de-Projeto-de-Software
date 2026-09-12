# Plataforma de Controle e Gestão de Estacionamentos
Decidimos modelar um software de gestão para um estacionamento comercial.

O sistema tem como objetivo controlar o cadastro de clientes e veículos, a disponibilidade e utilização das vagas, as reservas, os tickets de estacionamento e os pagamentos, aplicando regras de negócio para garantir a consistência das operações.

O sistema é composto pelos seguintes objetos e tipos de objetos (Cosmic Python):

### Cliente: Entidade (Entity)
 Representa a pessoa que utiliza os serviços do estacionamento. Possui identidade própria (id_cliente) e ciclo de vida.

### Veículo: Entidade (Entity)
 Representa um veículo pertencente a um cliente. Possui identidade própria (id_veiculo) e está associado a um único cliente.

### Estacionamento: Entidade e Aggregate Root
 Representa a unidade física do estacionamento. É a raiz do Agregado Estacionamento e gerencia suas vagas.

### Vaga: Entidade (Entity)
 Representa uma vaga física do estacionamento. Possui identidade própria (id_vaga) e estados que controlam sua utilização.

### Reserva: Entidade e Aggregate Root
 Representa um agendamento antecipado de vaga. É responsável por garantir as regras de exclusividade das reservas.

### Ticket: Entidade (Entity)
 Representa o registro da utilização efetiva de uma vaga durante um período de estacionamento.

### Pagamento: Entidade e Aggregate Root
 Representa a quitação financeira de um ticket. Controla o estado da cobrança e a autorização de saída do veículo.

## Value Objects

### Placa: Value Object
 Representa a placa do veículo. É definida apenas pelo seu valor e não possui identidade própria.

### Endereço: Value Object
 Representa a localização do estacionamento. É definido pelos seus atributos de endereço.

### PeríodoReserva: Value Object
 Representa um intervalo de datas e horários para uma reserva.

### TempoPermanência: Value Object
 Representa a duração da estadia do veículo no estacionamento.

### Dinheiro: Value Object
 Representa um valor monetário utilizado nos cálculos e pagamentos.
 

## Agregados (Aggregates)

### Agregado Cliente

Root: Cliente
Entidades internas: Veículo
Regra principal: RN-01 Cadastro de Veículos

### Agregado Estacionamento

Root: Estacionamento
Entidades internas: Vaga
Regra principal: RN-03 Ocupação de Vagas

### Agregado Reserva

Root: Reserva
Entidades internas: Ticket
Regra principal: RN-05 Exclusividade de Reserva

### Agregado Pagamento

Root: Pagamento
Entidades internas: nenhuma (inicialmente)
Regra principal: RN-04 Liberação mediante Pagamento


## Domain Services

### CalculadoraTarifa: Domain Service
 Responsável por calcular o valor da permanência do veículo com base no tempo de uso e no tipo do veículo (RN-02).

### VerificadorDisponibilidadeVaga: Domain Service
 Responsável por verificar se uma vaga está disponível para ocupação ou reserva.

### AutorizadorSaidaVeiculo: Domain Service
 Responsável por validar se o veículo pode sair do estacionamento, considerando ticket, pagamento e situação da vaga.


 ## Visão Geral

### Cliente                → Entidade + Aggregate Root
### Veículo                → Entidade

### Estacionamento         → Entidade + Aggregate Root
### Vaga                   → Entidade

### Reserva                → Entidade + Aggregate Root
### Ticket                 → Entidade

### Pagamento              → Entidade + Aggregate Root

### Placa                  → Value Object
### Endereço               → Value Object
### PeríodoReserva         → Value Object
### TempoPermanência       → Value Object
### Dinheiro               → Value Object

### CalculadoraTarifa      → Domain Service
### VerificadorDisponibilidadeVaga → Domain Service
### AutorizadorSaidaVeiculo → Domain Service

---

### Regras de negócio

### Agregado Cliente:
RN-01: Cadastro de Veículos
Descrição: Um cliente pode cadastrar um ou mais veículos no sistema, porém cada veículo deve estar associado a apenas um cliente.

### Agregado Tarifa:
RN-02: Precificação por Tipo de Veículo e Tempo de Permanência
Descrição: O valor cobrado pela estadia do veículo no estacionamento é calculado com base na categoria do veículo (carro, moto, caminhonete/SUV) e na sua duração de permanência, aplicando regras específicas de tolerância e fracionamento.

### Agregado Estacionamento:
RN-03: Ocupação de Vagas
Descrição: Uma vaga somente pode ser ocupada se estiver com status Livre. Vagas com status Ocupada, Reservada ou Em Manutenção não podem receber novos veículos até que seu estado seja alterado.

### Agregado Pagamento:
RN-04: Liberação do Veículo mediante Pagamento
Descrição: A saída do veículo do estacionamento somente poderá ser autorizada após a confirmação do pagamento da tarifa correspondente ao ticket de estacionamento. Enquanto houver débito pendente, o ticket permanecerá aberto e a vaga continuará ocupada.

### Agregado Reserva:
RN-05: Exclusividade de Reserva de Vaga
Descrição: Uma vaga não pode possuir duas reservas ativas para períodos de tempo que se sobreponham. Ao realizar uma nova reserva, o sistema deve verificar a disponibilidade da vaga para o intervalo solicitado e impedir conflitos de agendamento.


TODO: revisar as regras de negócio de cada agregado.
