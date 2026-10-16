# 0005. Uso de Domain Service para Cálculo de Tarifa de Estacionamento

Status: aceito (Fase 1)

## Contexto
O valor de uma permanência ou reserva depende de vários fatores ao mesmo tempo: o tempo total em que o veículo permaneceu estacionado, o tipo de veículo (carro, moto, SUV/caminhonete), o uso de recursos adicionais (como pontos de recarga para elétricos) e taxas de permanência. Essa conta não cabe dentro de uma única entidade (como Reserva ou Veiculo), pois exige cruzar dados de diferentes partes do sistema.

## Decisão
Implementar um Serviço de Domínio (`CalculadoraTarifa` em `src/estacionamento/domain/services.py`), sem dependência do SQLAlchemy ou de frameworks externos. A aplicação só precisa entregar os dados ou entidades necessárias para esse serviço, e ele devolve o valor final detalhado.

## Alternativas consideradas
1. Colocar a lógica na entidade Reserva: Deixaria a entidade desnecessariamente presa e acoplada nas tabelas de preço do estacionamento.
2. Fazer o cálculo na camada de Aplicação/API (Flask): Espalharia regras de negócio na camada de infraestrutura/entrada, o que deixaria os testes unitários isolados bem mais difíceis.

## Consequências
+ Facilidade de testes: Permite rodar testes unitários rápidos em tests/unit/, sem a necessidade de subir um banco SQLite em memória.
+ Desacoplamento: O domínio continua totalmente puro (o comando `grep -rn sqlalchemy src/estacionamento/domain/` continua sem retornar resultados).
- Complexidade Adicional: Adiciona mais uma classe na arquitetura que precisa ser mantida.





