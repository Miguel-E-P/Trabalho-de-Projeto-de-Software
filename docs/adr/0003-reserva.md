# 0003. Refatoração de Fronteiras do Ticket e Imutabilidade da Reserva

Status: aceito (Fase 1)

## Contexto

As áreas de controle de entrada/saída (`Ticket`) e alocação antecipada (`Reserva`) possuem regras de negócio estritas sobre tempo e integridade de dados. O domínio exige a prevenção de anomalias, como datas de saída anteriores à entrada, reservas em datas passadas e IDs negativos. Durante o desenvolvimento inicial, detectou-se um acoplamento inadequado onde a classe `Pagamento` estava assumindo responsabilidades do domínio de `Ticket`, passando a controlar indevidamente a saída do veículo. Além disso, as instâncias de `Reserva` precisavam de garantias contra alterações indevidas de propriedades (como a placa ou data) após a sua criação em memória.

## Decisão:

Redefinição de Responsabilidades: A entidade `Ticket` recebeu o controle exclusivo sobre o seu ciclo de vida, o que inclui atualizar o `horarioSaida` e alternar o status `pago` para verdadeiro.

Adoção de Value Object para Reserva: A classe Reserva foi modelada como um Objeto de Valor (Value Object) imutável (@dataclass(frozen=True)). Isso impede que atributos como o ID da reserva ou a placa do veículo sejam alterados após a validação inicial.

Isolamento da Infraestrutura: Foram criados Repositórios "falsos" em memória (FakeReservaRepository, FakeTicketRepository) e Repositórios SQLAlchemy reais (SqlAlchemyReservaRepository) para isolar as regras de Reserva e Ticket das tecnologias de banco de dados e mapeamento ORM e mantendo as classes de domínio limpas.

## Alternativas consideradas

1. Unificar Reserva e Ticket numa única entidade genérica, partilhando o mesmo fluxo e identificador. Não foi possível pois suas restrições e ciclos de vida são diferentes

2. Permitir a definição do Horário de Saída na criação da Reserva. Rejeitado pois foi chegada à conclusão que um horário de saída não seria predeterminado, podendo o cliente sair em qualquer horário até antes do fechamento do estacionamento


## Consequências:

Vantagens: O domínio tornou-se coeso, desacoplado e altamente testável de forma isolada (testes em memória n). A centralização da lógica de proteção de datas diretamente no `Ticket` evita problemas sistêmicos ou fraudes.

Desvantagens: A imutabilidade da `Reserva` significa que qualquer alteração de data ou placa por parte do cliente exigirá a exclusão da instância atual e a geração de uma nova. Adicionalmente, a separação estrutural entre Ticket e Pagamento exigirá que a camada de serviços orquestre chamadas a repositórios distintos para efetivar e registrar a saída de um veículo.