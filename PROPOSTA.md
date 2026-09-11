# Plataforma de Controle e Gestão de Estacionamentos
Decidimos modelar um software de gestão para um estacionamento comercial.

O sistema tem como objetivo controlar o cadastro de clientes e veículos, a disponibilidade e utilização das vagas, as reservas, os tickets de estacionamento e os pagamentos, aplicando regras de negócio para garantir a consistência das operações.

O sistema é composto pelos seguintes agregados e entidades:

### Agregado Cliente
**Cliente:** a pessoa que utiliza os serviços do estacionamento
**Veículo:** pertence a um cliente, tem placa e tipo

### Agregado Estacionamento
**Estacionamento:** unidade física que contém vagas
**Vaga:** possui número, tipo e estado

### Agregado Tarifa
Calcular e precificar o valor da permanência. Regras utilizadas para calcular o valor cobrado com base no tempo decorrido

### Agregado Pagamento
Executar e validar as transações financeiras. Responsável pela quitação da cobrança da tarifa

### Agregado Reserva
**Reserva:** agendamento antecipado de uma vaga
**Ticket:** registro de utilização de uma vaga

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


TODO: revisar e/ou acrescentar as regras de negócio de cada agregado.
