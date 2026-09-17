# Plataforma de Controle e Gestão de Estacionamentos
## Project Backlog (nossas decisões)

### Kennedy
**16-09-26**:
Optei por realizar a estrutura inicial das classes do agregado cliente/ veiculo para deixar explicitado as dependências de classe de cima pra baixo,
sinalizando por comentários qual atributo específico depende da classe de cima para sua composição. Cada classe já está com sua classificação:
value object, entidade simples e entidade raiz. A class Placa não possui atributo "id" própria por que foi classificada como value object, pois,
é definida apenas pelo valor e é imutável.

### Pedro
**16-09-26**:
Pedro: Para proteger contra golpes. Vamos precisar de algum sistema de verificacao de tempo. Ou seja, quando o pagamento ocorrer, e o ticket for atualizado para valido, o sistema precisa verificar se o ticket foi usado ate certo periodo de tempo, se nao, atualizar ele para invalido novamente. Pois se nao, teremos um sistema em que um cliente pode entrar no estacionamento, pagar o ticket, e permanecer horas/dias a mais no estacionamento, e sair no fim de tudo tendo pago como se tivesse ficado apenas minutos dentro do estacionamento.

### Gustavo
**16-09-26**:
Primeiro, estou organizando nosso repositório; devo fazer esse tipo de varredura mais vezes e, a não ser que eu esqueça, subir o commit com uma flag de "_refact_". A título de curiosidade, o linter/code formatter que uso chama-se [ruff](https://docs.astral.sh/ruff/).

Segundo, estou apagando o conteúdo das classes Vaga e Estacionamento, que são, hoje, minha responsabilidade. Resolvi criar classes Enum ao invés de tratar Tipo e Status da Vaga como int pra evitar problemas. A princípio, Status até poderia ser uma variável `ocupada: bool`, mas como vamos lidar com reservas no futuro, imaginei que seria melhor definir como `status: StatusVaga` mesmo. Ainda não me decidi quanto ao Estacionamento, mas devo melhorar a lógica dele em breve.