# 0002 — Abstração de acesso ao Banco de Dados, através do Repository Pattern
Status: aceito (Fase 1)

## Contexto
Seguindo as orientações do professor, implementamos uma série de padrões de projeto, com a intenção de eliminar code smells e aprendermos boas práticas de design orientado ao domínio (DDD). Nossa aplicação é grande e possui muitas classes, que precisam de mais do que uns poucos métodos CRUD; conforme a base de código fosse crescendo, mais necessário se tornaria testar os componentes da aplicação separadamente.

Nosso sistema usa a biblioteca SQLAlchemy pra lidar com a persistência dos dados, o que implica necessidade de lidar com sessões e conexão com o banco.

## Decisão
Uso do repository pattern pra esconder a lógica de sessão do SQLAlchemy nas operações realizadas em Estacionamento.

## Alternativas consideradas
- Seguir o estilo ActiveRecord, onde as classes de domínio conhecem a infraestrutura e implementam os métodos de acesso (CRUD): menor número de classes, mas fortemente acoplado ao banco de dados, o que dificulta os testes.
- Criar um EstacionamentoDAO (Data Access Object), eliminando a interface abstrata e a implementação fake: um pouco menos abstrato que o repository, mas também dificultaria os testes.

## Consequências
+ Código objetivo, mais legível: podemos chamar o método `get()`, por exemplo, sem nos preocuparmos com questões de infra. 
− Aumento do número de classes: temos classes abstract, sqlalchemy e fake pra cada repositório implementado.
