# Plataforma de Controle e Gestão de Estacionamentos
## Project Backlog (nossas decisões)

### Kennedy
**16-09-26**:
Optei por realizar a estrutura inicial das classes do agregado cliente/ veiculo para deixar explicitado as dependências de classe de cima pra baixo,
sinalizando por comentários qual atributo específico depende da classe de cima para sua composição. Cada classe já está com sua classificação:
value object, entidade simples e entidade raiz. A class Placa não possui atributo "id" própria por que foi classificada como value object, pois,
é definida apenas pelo valor e é imutável.

**17-09-26**:
Para realizar o primeiro teste no agregado cliente, implementei o teste para saber se um cliente consegue cadastrar um veículo, para alinhar ao
TDD (Test-Driven Development) proposto no cosmic python que não é implementar detalhadamente as classes/ objetos inicialmente, mas sim desenvolver 
com abordagem orientada a testes e conforme as respostas dos testes informam o que estão faltando, depois ir completando as classes e objetos 
a serem testados. Como deu erro 'Cliente() takes no arguments === 1 failed in 0.60s' observei que as classes do agregado cliente do arquivo
model.py ainda estão vazias ou não inicializadas com construtor __init__, nem mesmo a função cadastrar cliente existe, o qual o teste está exigindo
no arquivo test_model.py. Ao estudar o TDD me dei conta de que o agregado cliente está na fase "Red" do ciclo Red-Green-Refactor do TDD, indicando que o
RED: Você escreve o teste para a nova regra de negócio ou contrato e o executa. Ele deve falhar (ficar vermelho no seu test runner). E em seguida vou
desenvolver para chegar em GREEN: Você escreve o mínimo de código necessário no arquivo de produção apenas para fazer o teste passar.

**19-09-26**:
Testei commit pelo git desktop.

Testei alteração pelo git desktop no user adicionei Kennedy Soares e no email alterei para o meu email uff kennedysoares@id.uff.br. Esta alteração de dados foi Global e serão usados automaticamente para todos os repositórios que Eu abrir, alterar ou criar na minha máquina através do GitHub Desktop.

Fiz os ajustes no agregado Cliente para passar o primeiro teste unitário (verificar se um cliente consegue cadastrar um veículo)  de Red para Green de acordo com o TDD. Depois fiz merge da 
minha branch de testes locais para a branch main do projeto.  

Implementei o segundo teste unitário no agregado Cliente para verificar se um cliente pode ter vários veículos referente a regra de negócio RN-01.

Implementei o terceiro teste unitário no agregado Cliente para verificar e proteger uma regra "Não permitir duas placas iguais para o mesmo cliente."

Implementei o quarto teste unitário no agregado Cliente para verificar se um cliente recém-criado inicia sem veículos. Em resumo e recapitulando que já passaram 4 testes e este agregado está na fase Green de acordo com TDD.

Ao refazer cada teste a cada função teste do agregado, o terceiro teste houve necessidade de correção na função cadastrar veiculo no dominio model, percebi um equívoco no comando do pytest que deveria ter editado a cada vez o nome da função de teste, mas já foi resolvido. Concluindo 4 testes e este agregado está na fase Green de acordo com TDD.





### Pedro
**16-09-26**:
Para proteger contra golpes. Vamos precisar de algum sistema de verificacao de tempo. Ou seja, quando o pagamento ocorrer, e o ticket for atualizado para valido, o sistema precisa verificar se o ticket foi usado ate certo periodo de tempo, se nao, atualizar ele para invalido novamente. Pois se nao, teremos um sistema em que um cliente pode entrar no estacionamento, pagar o ticket, e permanecer horas/dias a mais no estacionamento, e sair no fim de tudo tendo pago como se tivesse ficado apenas minutos dentro do estacionamento.

**17-09-26**:
Adicionei um enum TipoPagamento para guardar informacao de qual foi o metodo utilizado no pagamento. Modifiquei Pagamento para que ele funcione com ele. Ja testei o codigo na minha maquina, mas ainda nao tenho certeza se os testes estao de acordo com os metodos ensinados em aula. Irei verificar isso e, entao, adicionar-los ao projeto.

**18-09-26**:
Adicionei os testes de Dinheiro, para verificar se ele esta funcionando da forma esperada. Todos os testes tiveram sucesso. Adicionei data_hora_pagamento do tipo datetime para guardar informacao de quando exatamente o pagamento ocorreu. O intuito aqui eh que, se um certo tempo de 'saida' passar, quando ocorrer a checagem para validar a saida, a saida sera considerada invalida, protegendo contra fraude. Na minha concepcao, a funcao que checaria se o pagamento esta pago tambem checaria o tempo do pagamento e compararia com o tempo atual. Pensei tambem eh utilizar datatime.now(), mas isso fere a pureza do dominio.

### Gustavo
**16-09-26**:
Primeiro, estou organizando nosso repositório; devo fazer esse tipo de varredura mais vezes e, a não ser que eu esqueça, subir o commit com uma flag de "_refact_". A título de curiosidade, o linter/code formatter que uso chama-se [ruff](https://docs.astral.sh/ruff/).

Segundo, estou apagando o conteúdo das classes Vaga e Estacionamento, que são, hoje, minha responsabilidade. Resolvi criar classes Enum ao invés de tratar Tipo e Status da Vaga como int pra evitar problemas. A princípio, Status até poderia ser uma variável `ocupada: bool`, mas como vamos lidar com reservas no futuro, imaginei que seria melhor definir como `status: StatusVaga` mesmo. Ainda não me decidi quanto ao Estacionamento, mas devo melhorar a lógica dele em breve.

### Matheus

**18-09-27**: 
Criei o arquivo services.py com a regra de calcular o preço do estacionamento.
Como calcular o preço depende do tipo do veículo e de quanto tempo ele ficou guardado, ou seja, uma conta que envolve coisas diferentes do sistema, achei melhor colocar essa lógica em uma ferramenta separada, em vez de embolar tudo dentro de uma classe só.  
Usei o @staticmethod, porque a calculadora só precisa receber as horas e o tipo do veículo para fazer a conta e devolver o preço. Assim evita guardar dados na memória toda vez que for cobrar alguém. 
