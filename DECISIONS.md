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

**20-09-26**:
Implementei o refactor (refatoração de melhoria) no agregado Cliente.
Também segui as fases Red e Green da abordagem TDD para os novos testes. A vivência desse processo (Refactor) mostrou que de fato utilizei menos códigos e menos alterações no Agregado Cliente para realizar a refatoração de melhoria, conforme o conceito do TDD descreve.

**22-09-26**:
Iniciei o repository pattern para o agregado Cliente para aplicar os padrões Repository Pattern, DDD (Domain-Driven Design) e Clean Architecture de acordo com o cosmic python. Isso traz alguns benefícios como: A lógica de negócio trabalha apenas com AbstractRepository, sem depender de detalhes do SQLAlchemy ou de banco de dados; Facilidade para Testes (Testabilidade); Tornará simples a troca do ORM ou do banco de dados no futuro mantendo a mesma interface do sistema.
Instalei local o pacote sqlAlchemy, ele traduz Python para SQL (e vice-versa) e fica flexível se o grupo optar por trabalhar com o sqlite ou outro banco de dados depois.

**23-09-26**:
O código do ORM conecta as tabelas do banco de dados às classes puras do código, neste caso, nas classes (Cliente e Veiculo). Ou seja, realiza o mapeamento de dados sem misturar código do banco com o código de negócio.

**24-09-26**:
Com a criação do repositório falso para realizar estes testes unitários são considerados ultra rápidos, porque os 'set' são armazenados em memória RAM, sem manipular conexões de rede e disco. Permite testar as regras de negócio do domínio de forma isolada. No futuro permitirá testar as regras de negócio do domínio pelo repositório em memória (FakeRepository) sem precisar alterar uma única linha das regras de negócio (Clean Architecture / DDD).

Ajuste na class fakeRepository sintaxe python para evitar a falha na função add cliente, de 'set' para 'dicionário' para armazenar em memória RAM. Concluída a fase Green de testes para abstractRepository do agregado Cliente (add e get).

**25-09-26**:
Criado o file conftest.py para configurar os testes do pytest que serve para compartilhar configurações e recursos de teste (chamados de fixtures) entre vários arquivos sem precisar repetir código ou fazer import manual. Funciona como um preparador de ambiente automatizado para os testes.

Foram criados os arquivos __init__.py dentro das pastas de testes, para que o Python trate as pastas como packages distintos, mesmo havendo o mesmo nome de arquivo test na pasta 'unit' e 'integration'.
Foram realizados os testes de integração para o agregado cliente passando 'verde'. Portanto validou a escrita e leitura em banco de dados real em memória RAM.

**28-09-26**:
Essa camada de serviços para o agegado Cliente serve como uma ponte entre a API (ou interface) e a regra de negócio:
- Isola o banco de dados: Usa abstrações (repo, session) para não depender de frameworks como SQLAlchemy ou SQL puro;
- Orquestra o fluxo: Controla transações (commit), busca dados, executa regras de negócio e trata erros de entrada.
A posteriori será implementado a camada API (ou interface) do agregado Cliente, lá no flask_app.py.

**29-09-26**:
O flask_app traduz entrada e saída da requisição para parâmetros Python e transforma retornos/exceções em respostas HTTP (JSON + Status Code). Gerencia o ciclo de vida da Sessão, ou seja, instancia o repositório (SqlAlchemyRepository) e garante o fechamento da sessão de banco.

**07-10-26**:

# Registro de Decisões e Autorelato - Checkpoint Fase 1

## Declarativo do Uso de IA
Utilizei apoio de Inteligência Artificial para diagnosticar e resolver uma sequência de falhas nos testes de integração e E2E do **Agregado Cliente** (ajustes no mapeamento ORM das chaves estrangeiras com `GUID`, conversão de parâmetros no SQLite e alinhamento dos atributos do Value Object `Placa`).

---

## Validação E2E do Agregado Cliente

Foi realizado com sucesso o teste de integração End-to-End para o Agregado Cliente (`Cliente`, `Veiculo` e `Placa`), cobrindo os seguintes cenários:
- **UC01:** Cadastrar Cliente via API (`POST /clientes`)
- **UC02:** Cadastrar Veículo para o Cliente (`POST /clientes/{id_cliente}/veiculos`)
- **Validação E2E:** Consultar Cliente e verificar a persistência do veículo inserido (`GET /clientes/{id_cliente}`)

### Arquivos Envolvidos
- `domain/model.py`
- `adapters/orm.py`
- `service_layer/services.py`
- `entrypoints/flask_app.py`
- `tests/e2e/test_api.py`

---

## Conclusão e Justificativa do Checkpoint Final (Fase 1)

Optei por concluir o checkpoint final da Fase 1 garantindo o pleno funcionamento e a estabilização do **Agregado Cliente**, pois esta validação trouxe maior confiabilidade no código com a suíte completa de testes unitários e, principalmente, de integração/E2E (48 testes aprovados).

Esta base consolidada servirá como ponto de partida seguro para a Fase 2 do projeto, independente das novas demandas que eventualmente tragam mudanças de arquitetura, frameworks ou abordagens diferentes das definidas inicialmente com base no livro *Cosmic Python*.

**15-10-26**:

Apenas foram criados os dir docs e adr limpos com seus respectivos files .md para responder fase2-checkpoint-1 . Conforme enunciado do trabalho fase 2 e Apêndice B do livro-texto.

**Uso declarativo de IA**:

Utilizou-se a IA para organizar as informações dispersas do projeto (arquivos, medições, comandos Python e premissas do *Cosmic Python*), o que estruturou o texto de análise e permitiu corrigir falhas no SQLite (`GUID`), ajustar DTOs (Data Transfer Objects) e validar o Agregado Cliente em E2E preservando o domínio puro.

**Autorrelato**:

Realizei uma versão preliminar sobre a descrição e análise da arquitetura do projeto. Conforme o checklist de apoio para a resposta das páginas 34 e 35 do slide/aula *"Arquitetura de Software - Aula 2"*.


**16-10-26**:

**Uso declarativo de IA**:

A assistência de Inteligência Artificial foi utilizada para diagnosticar e corrigir falhas de integração no banco SQLite e no Value Object `Placa`, auxiliando na implementação do `TypeDecorator` (`GUID`), no ajuste dos DTOs (Data Transfer Objects) na camada de serviço e na refatoração dos testes E2E sem violar o isolamento do domínio.

**Autorrelato**:

Atuei na estabilização do Agregado Cliente para o encerramento da Fase 1. Implementei o TypeDecorator (GUID), reajustei os DTOs (Data Transfer Objects) na camada de serviço e validei a suíte E2E com 100% de aprovação, mantendo o domínio puro e totalmente desacoplado do ORM.

**22-10-26**:

**Uso declarativo de IA**:

Utilizei a Inteligência Artificial na retomada e organização de informações dispersas (arquivos, comandos Python, medições e notas de arquitetura) para estruturar o texto de análise da arquitetura e o ADR do Agregado Cliente, além de atuar no diagnóstico dos logs do SQLite e acelerar a construção da classe GUID, viabilizando a aprovação de 100% dos testes E2E (48 testes) sem violar o domínio puro.

**Autorrelato**:

No encerramento e consolidação do checkpoint da Fase 1, atuei diretamente na estabilização do Agregado Cliente, no saneamento das falhas de integração e na formalização da documentação arquitetural.

Arquivos e Modificações: Implementei a conversão de UUID/string com TypeDecorator (GUID) em src/estacionamento/adapters/orm.py, ajustei os DTOs e Value Objects em src/estacionamento/service_layer/services.py, validei a suíte automatizada REST em tests/e2e/test_api.py e estruturei os registros formais de decisão técnica e arquitetura em docs/arquitetura.md, adr001-cliente.md e decision.md.

Commits do Autor:

2124f7d - requisitos, estilos, visões e análise de trade-offs

bc9b0bf - descrição e análise preliminar da arquitetura do projeto

15767b9 - adr001-cliente.md e decision.md.







### Pedro
**16-09-26**:
Para proteger contra golpes. Vamos precisar de algum sistema de verificacao de tempo. Ou seja, quando o pagamento ocorrer, e o ticket for atualizado para valido, o sistema precisa verificar se o ticket foi usado ate certo periodo de tempo, se nao, atualizar ele para invalido novamente. Pois se nao, teremos um sistema em que um cliente pode entrar no estacionamento, pagar o ticket, e permanecer horas/dias a mais no estacionamento, e sair no fim de tudo tendo pago como se tivesse ficado apenas minutos dentro do estacionamento.

**17-09-26**:
Adicionei um enum TipoPagamento para guardar informacao de qual foi o metodo utilizado no pagamento. Modifiquei Pagamento para que ele funcione com ele. Ja testei o codigo na minha maquina, mas ainda nao tenho certeza se os testes estao de acordo com os metodos ensinados em aula. Irei verificar isso e, entao, adicionar-los ao projeto.

**18-09-26**:
Adicionei os testes de Dinheiro, para verificar se ele esta funcionando da forma esperada. Todos os testes tiveram sucesso. Adicionei data_hora_pagamento do tipo datetime para guardar informacao de quando exatamente o pagamento ocorreu. O intuito aqui eh que, se um certo tempo de 'saida' passar, quando ocorrer a checagem para validar a saida, a saida sera considerada invalida, protegendo contra fraude. Na minha concepcao, a funcao que checaria se o pagamento esta pago tambem checaria o tempo do pagamento e compararia com o tempo atual. Pensei tambem eh utilizar datatime.now(), mas isso fere a pureza do dominio.

**20-09-26**:
Refatorei o codigo para acessar as classes por meio do model. Utilizei um CI que encontrei online para automatizar o teste do projeto. Corrigi algumas coisas, e adicionei outras, para garantir o CI verde. Precisamos discutir sobre o Dominio e Proposta. Por que pagamento guarda controla saida do veiculo? Isso nao deveria ser parte de ticket? 

**26-09-26**
Percebi que havia um erro na estrutura do projeto. Pagamento estava cuidando de diversas coisas que eram do dominio de Ticket. Apos discutir com os membros Gustavo e Miguel, chegamos a conclusao que isso precisava mudar. Refatorei o codigo, portanto, transformando pagamento em um mero registro(recibo) do pagamento que ocorre para pagar um ticket. Para evitar que isso quebrasse o codigo, tive que alterar o resto do projeto tambem. Implementei o AbstractPagamentoRepository. 

**21-10-26**
Detalhei o arquivo arquitetura.md de acordo com as diretrizes da Fase 2. Destaquei os atributos de qualidade de maior importância para o nosso escopo. Alguns desses atributos ainda não foram totalmente implementados no projeto, mas, como este checkpoint foca em mapear como aprimorar nossa arquitetura, e eles sao de grande importancia para o projeto, preferi descreve-los. Alterei tambem os atributos que ja estavam descritos para eles estarem no formato pedido.

Uso de IA: O Gemini foi utilizado para formatar o texto e pesquisar termos(ex: "Explique Unit of Work em detalhe sem erros."). Tambem foi utilizado para debater escolhas da arquitetura. A primeira coisa debatida foi se era vantajoso ou nao manter a mesma arquitetura. Apos debate com a IA e com outros integrantes do grupo(Gustavo & Miguel) foi decidido que era melhor manter a estrutura atual. Tambem foi debatido a melhor maneira de descrever os atributos, e se era necessario ou nao detalhar a tecnica que seria utilizada para aumentar um atributo de qualidade em nosso projeto.

**22-10-26**
Escrevi o ADR da imutabilidade do `Pagamento`, agregado pelo qual sou responsável, em `docs/adr/[número]-[título].md` (commit `[hash]`). O ADR registra uma decisão já implementada em `domain/model.py`: o `Pagamento` deixou de usar `@dataclass(frozen=True)`, porque o `frozen=True` bloqueava o atributo `_sa_instance_state`, que o SQLAlchemy grava em cada instância no mapeamento imperativo. Passou a usar um `__setattr__` customizado, que libera esse atributo e a atribuição inicial e bloqueia qualquer reatribuição. O ADR descreve o contexto, a decisão, as alternativas consideradas (o `frozen=True` original, propriedades somente leitura e um modelo de persistência separado) e as consequências.

Decisão de projeto: manter a imutabilidade do `Pagamento` com `__setattr__` customizado, em vez de separar o modelo de persistência do modelo de domínio, para continuar usando o mapeamento imperativo sem duplicar classes nem escrever código de tradução no Repository.

Uso de IA: Claude foi usado para gerar o rascunho inicial do ADR, a partir do código do `Pagamento` e da descrição do problema. Depois usei o Claude para: (1) entender o que o enunciado pede de um ADR e qual o formato (contexto, decisão, alternativas e consequências); (2) revisar o rascunho, o que apontou a falta da seção de alternativas, o conflito de numeração com o ADR-0001, a diferença entre o código do rascunho e o `model.py`, o acoplamento ao prefixo `_sa_` e a possível brecha na imutabilidade após o `commit`; (3) sugerir um teste para verificar essa brecha; e (4) revisar o texto da alternativa "modelo de persistência separado", corrigindo a justificativa e acrescentando a vantagem real dessa alternativa. Reescrevi o ADR com base nessas revisões e conferi o código e o texto final.

Hash do Commits:
de33ff2b45a3ac7a7e45a7834112191549889fdd
Arquivos modificados: arquitetura.md, DECISIONS.md

1f67a257124c626832a2d492bdd390d31f815124
Arquivos modificados: 0004-titulo.md, 0004-pagamento.md DECISIONS.md

### Gustavo
**16-09-26**:
Primeiro, estou organizando nosso repositório; devo fazer esse tipo de varredura mais vezes e, a não ser que eu esqueça, subir o commit com uma flag de "_refact_". A título de curiosidade, o linter/code formatter que uso chama-se [ruff](https://docs.astral.sh/ruff/).

Segundo, estou apagando o conteúdo das classes Vaga e Estacionamento, que são, hoje, minha responsabilidade. Resolvi criar classes Enum ao invés de tratar Tipo e Status da Vaga como int pra evitar problemas. A princípio, Status até poderia ser uma variável `ocupada: bool`, mas como vamos lidar com reservas no futuro, imaginei que seria melhor definir como `status: StatusVaga` mesmo. Ainda não me decidi quanto ao Estacionamento, mas devo melhorar a lógica dele em breve.

**20-09-26**:
Hoje, resolvi trabalhar no model de Estacionamento. A lógica de ocupar vagas é um pouco complexa, ela vai ser melhor desenvolvida no futuro, quando implementar o service. Por ora, basta saber que uma Vaga só pode mudar de status pra **OCUPADA** caso ela estiver **LIVRE** (o tratamento de vagas reservadas deve ser feito separadamente).

Coloquei o método `ocupar()` dentro de Vaga e criei dois métodos em Estacionamento, um pra selecionar uma vaga dentro da lista, outro pra ocupar a vaga selecionada. Acredito que dê pra melhorar a busca, mas pretendo deixar a refatoração para depois dos testes, caso necessária. Por exemplo, acho interessante separar as exceções de domínio, não gosto dessas exceções genéricas `ValueError`. Mais tarde, escrevo os testes e dou uma olhada nisso.

Escrevi cinco testes: dois pro método ocupar() do model Vaga (livre/indisponível), dois para a busca do Estacionamento (cadastrada/não cadastrada) e um último teste, que chama ocupar_vaga() de estacionamento; esse, só passaria se os últimos passassem, acredito, mas nada custa escrever outro teste, só temos a ganhar.

Por fim, resolvi refatorar as _Exceções de Domínio_ em classes separadas: **VagaIndisponivel** e **VagaNaoEncontrada**. Tive que alterar suas chamadas nos testes, além de implementá-las dentro dos models de Vaga e Estacionamento.

---

Verifiquei que um colega acidentalmente apagou meu código, estou subindo mais uma vez.

**26-09-26**:
Considerando que o Estacionamento é uma Entidade, estou adicionando um atributo id_estacionamento. Talvez fosse interessante adicionar outras colunas (endereço, por exemplo), só para testar a questão do Repository. Por ora, vou optar por manter apenas os atributos estritamente necessários, seguindo o princípio KISS.

Fiz os três repositórios (Abstract, SQLAlchemy e Fake), seguindo os modelos apresentados durante a aula. Gostaria de melhorar um pouco eles, mas prefiro deixar a etapa de refactoring pra depois dos testes. Diferente dos meus colegas, optei por não usar Optional nos repositories: sou contra o uso indiscriminado de bibliotecas, quando a linguagem oferece recursos similares. Ademais, pretendo verificar as vantagens de fazer o método `add()` retornar algo caso a operação seja bem sucedida.

---

NOVAMENTE, um colega apagou por acidente algo que eu commitei (dessa vez, no arquivo de DECISIONS). Espero que o mesmo não esteja acontecendo com os demais, pois não sei se estão conferindo o repositório, então peço mais atenção e deixo a seguir a documentação do [Git](https://git-scm.com/docs).

**27-09-26**:
Comecei, hoje, consertando a identação do código do FakeEstacionamentoRepository e os testes de model que falharam ao adicionar o id_estacionamento.

Adicionei as tabelas de Estacionamento e Vagas no arquivo ORM, criando seus respectivos mappers. Declarei de forma que uma Vaga não pudesse existir sem um Estacionamento através do "delete-orphan".

Ainda, resolvi configurar o `pytest.ini` e remover do projeto/adicionar ao `.gitignore` arquivos gerados pela IDE do PyCharm e pelo UV, ferramentas usadas por nós desenvolvedores.

Ao escrever testes para os repositories de Estacionamento, notei um erro no método get. Esse erro me fez perceber que não posso tratar estacionamentos como um set, o que ocasionou mudanças no FakeEstacionamentoRepository.

Não encontrei dificuldades ao fazer os testes de integração com o SQLAlchemy.

**21-10-26**
Passei os últimos dias analisando o projeto e discutindo com os pares quanto as decisões que tomaríamos daqui pra frente.

Resolvi, por enquanto, não subir nenhuma alteração.

**22-10-26**
Depois de analisar a aplicação como um todo e o agregado o qual fiquei responsável, separei duas decisões tomadas na Fase 01 como candidatas para meu ADR: o encapsulamento das regras de negócio dentro das classes de domínio (Estacionamento e Vaga) e o uso do repository pattern pra esconder a lógica de sessão do SQLAlchemy nas operações realizadas em Estacionamento.

A primeira trataria da decisão de implementar exceções de domínio como uma espécie de validação da consistência de cada modelo, ao invés de fazer essas verificações posteriormente na camada de serviço. A escolhida, trata do acesso aos dados no SQLAlchemy, realizada, segundo as orientações do professor, através de uma classe que implementasse o Repository Pattern.

```md
7dce39e - **docs: ADR sobre uso do repository pattern no estacionamento**
+ Decisions.md
+ 0002-estacionamento.md
```


Preferi não usar IA nesse checkpoint pra correção ou análise do código; ainda, relato usar como ferramenta de busca, perguntando "que tipo de decisão se documenta num adr" (prompt), pois senti falta de exemplos nos slides visto em aula.

Assim que todos os integrantes do grupo finalizarem sua atuação nesse checkpoint, pretendo submeter o tag-commit. 


### Matheus

**18-09-26**: 
Criei o arquivo services.py com a regra de calcular o preço do estacionamento.
Como calcular o preço depende do tipo do veículo e de quanto tempo ele ficou guardado, ou seja, uma conta que envolve coisas diferentes do sistema, achei melhor colocar essa lógica em uma ferramenta separada, em vez de embolar tudo dentro de uma classe só.  
Usei o @staticmethod, porque a calculadora só precisa receber as horas e o tipo do veículo para fazer a conta e devolver o preço. Assim evita guardar dados na memória toda vez que for cobrar alguém. 

**20-09-26**: Implementei as taxas de caminhonetes/SUVs e as de uso das tomadas para carros elétricos e na CalculadoraTarifa dentro de services.py. Criei a estrutura inicial em tests/unit/test_services.py e adicionei os testes para validar a precificação de cada categoria de veículo.   

**26-09-26**: Ajustei a regra do Domain Service VerificarDisponibilidadeVaga para se adequar a reserva com limite de ocupação de apenas 1 dia. Implementei também o AutorizadorSaidaVeiculo, aplicando uma regra de cobrança de multa para caso o veículo ocupe a vaga por mais de 24 horas. Criei e executei os testes dessa mesma classe.

**22-10-26**: Criei o documento docs/adr/0005-domain-service.md para registrar a decisão de isolar o cálculo da tarifa do estacionamento em um Domain Service (CalculadoraTarifa).
Também atualizei a Seção 4 (Trade-offs) do docs/arquitetura.md comparando essa abordagem com o uso de entidades ricas. 

#### Decisão de Projeto
O serviço CalculadoraTarifa ficou puro e sem estado, totalmente separado de ORMs e do banco de dados.
Fiz isso para seguir o Princípio de Responsabilidade Única e conseguir rodar os testes unitários de forma isolada, sem depender do SQLite.

Uso de IA: Utilizada para ajudar na estruturação, formatar as seções e validar os critérios.

### Miguel
**16/09/26**:
Comecei fazendo o esqueleto básico das classes ticket e reserva, que serão atualizados e talvez sofram alguma correção no futuro

**20/09/2026**
Criei os testes da classe reserva e ticket uma proteção contra a reserva de uma vaga em um dia anterior ao dia de hoje e e a emissão de m horario de saida anterior ao de entrada no ticket uma proteção contra o cadastro de uma vaga e ticket com id de reserva negativo. Os testes em relação a essas proteções funcionaram perfeitamente. Os outros testes de relacionam à imutabilidade dos atributos, à igualdade da classe reserva, já que é umo objeto de valor, e em relação à inicialização de uma instânicia da classe. Todos esses testes demonstraram a que essas funcionalidades funcionam corretamente

**26/09/2026**
Comecei a implementação do AbstractReservaRepository, com as funções "add", que adiciona uma reserva no repositório, e a função "get", que retorna uma reserva por meio de seu id

**27/09/2026**
Implementei a SqlAlchemyReservaRepository e a FakeReservaRepository da Reserva e do Ticket, cada uma segundo o proposto pelo conteúdo disponibilizado na diciplina

Adicionado o mapper e as tabelas de ticket e reserva na orm. Corrigido erros de SqlAlchemyRepository e FakeRepository de Reserva e Ticket. Implementado os testes de FakeRepository de Reserva e Ticket

**22/10/2026**
Modifiquei o arquitetura.md para se adequar melhor ao que é requerido pela Fase 2. Dei ênfase nas vantagens da arquitetura para os atributos, mas também documentei certas desvantagens e riscos que podem decorrer do seu uso, que será importante na hora de considerar como a arquitetura pode ser melhorada. Documentei o adrs do agregado Reverva 

Uso de IA: De forma semelhante ao que foi relatado pelo integrante Pedro no dia 21/10/2016, o Gemini foi utilizado para formatar o texto e para debater escolhas da arquitetura, que resultou na decisão de manter a estrutura atual. Também documento usar o Gemini para saber como se reporta um adr, pois senti que não havia conhecimento suficiente naquele instante para fazer isso.

Hashs dos commits: 
f6334e5449c020e6a586a8407ee915bb5c829be4f6334e5449c020e6a586a8407ee915bb5c829be4
Arquivos modificados: arquitetura.md

7c0ac29095376c9e972e2d27209939abbaa6a2a5
Arquivos modificados: decisions.md

2f117545ce0ba164a64ba3b2969ccea128c84d6c
Arquivos modificados: decisions.md, 0003-titulo.md, 0003-reserva.md

