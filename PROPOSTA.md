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

### Agregado Pagamento
**Pagamento:** cobrança realizada pelo uso do estacionamento
**Tarifa:** regras utilizadas para calcular o valor cobrado

### Agregado Reserva
**Reserva:** agendamento antecipado de uma vaga
**Ticket:** registro de utilização de uma vaga

---

TODO: descrever as regras de negócio de cada agregado.
