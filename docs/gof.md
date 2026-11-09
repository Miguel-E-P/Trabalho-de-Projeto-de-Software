**Agregado Cliente (class raiz cliente): Política de descontos por categoria de cliente (sem desconto - cliente avulso, cliente mensalista - 20%, cliente VIP - 35%).**

**Autor: Kennedy Soares**

**Nome e Categoria: Strategy (Padrão Comportamental de Objeto).**

**Contexto e Problema:**

A necessidade de aplicar regras variadas de cálculo de desconto/tarifa no uso do estacionamento para diferentes categorias de clientes (Avulso, Mensalista, VIP) sem encher a classe Cliente com verificações condicionais (if self.tipo == 'MENSALISTA': ...).

**Alternativas Consideradas:** 

- Herança tradicional (ClienteMensalista, ClienteVIP): 
Descartada por ser estática (não permite trocar a categoria do cliente sem recriar a entidade) e causar explosão de classes.   

- State: 
Descartada por ter um foco maior em ciclos de vida e transições de estado complexas, o que adicionaria complexidade desnecessária para apenas calcular preços.

**Mapeamento dos Participantes:**

- Contexto: Cliente.   
- Estratégia Abstrata: EstrategiaDesconto.   
- Estratégias Concretas: SemDesconto, DescontoMensalista, DescontoVIP.   

**Custo da Aplicação (Trade-off):**

Ligeiro aumento na quantidade de arquivos/classes no projeto, contrabalançado pela total flexibilidade de estender novos planos de desconto sem alterar o código existente do Agregado Cliente (OCP).


**Diagrama de Classes, destacando os participantes:**



![alt text](image.png)

======================================================================


Class Veiculo (Agregado Cliente):

**Nome e Categoria: Factory Method (Padrão Criacional de Classe)**. 

**Autor: Kennedy Soares**

**Contexto e Problema**: 

A necessidade de instanciar objetos Veiculo garantindo a definição padronizada de suas modalidades (Carro, Moto, etc.) sem expor os detalhes de criação e a geração manual de UUIDs para a camada de aplicação/cliente.

**Alternativas Consideradas**:

Instanciação Direta (Veiculo(id, placa, "CARRO")): Descartada por espalhar strings mágicas (Magic Numbers/Strings) pelo código e não validar padronização de tipo.   

Abstract Factory: Descartada por ser excessivamente complexa para criar apenas uma classe de produto (Veiculo), sem a necessidade de famílias de objetos relacionados.


**Mapeamento dos Participantes**:

Produto (Product): VeiculoCriador

Abstrato (Creator): CriadorVeiculo

Criadores Concretos (Concrete Creators): CriadorCarro, CriadorMoto

Produtos Concretos (Concrete Product):

- Produto Concreto Veiculo com o tipo "CARRO";

- Produto Concreto Veiculo com o tipo "MOTO".



**Custo da Aplicação (Trade-off)**:

Pequeno aumento na quantidade de classes criadoras, compensado pela centralização da lógica de instanciação e facilidade de extensão para novas categorias (ex.: CriadorCaminhonete)

**Diagrama de Classes**



![alt text](image-1.png)


## Integrante: Pedro Quintaes — Observer

**Módulo / Agregado:** Agregado Pagamento (`Pagamento`)

---

### 1. Nome e categoria
**Observer** — padrão **comportamental**.

### 2. Contexto no sistema e problema
O `Pagamento` é um registro (recibo) imutável de um pagamento feito para um ticket e se liga a ele apenas por `id_ticket`. Registrar um pagamento tem consequências fora do agregado: o `Ticket` correspondente precisa passar a pago (`Ticket.registrar_pagamento()`) e é desejável deixar uma linha de auditoria do pagamento. Sem o padrão, o código que registra o pagamento teria de conhecer e chamar cada uma dessas reações, e toda reação nova obrigaria a alterar esse código.

Com o Observer, quem registra o pagamento só avisa que ele foi registrado. Cada reação é um observador independente, que pode ser adicionado ou removido sem tocar no registro.

### 3. Por que esse padrão
Alternativas consideradas:

- **Chamadas diretas no serviço** (`repo.add(...)`, depois `ticket.registrar_pagamento()`, depois a auditoria): é a mais simples, mas acopla o registro a cada reação e viola o OCP, porque cada reação nova altera a função.
- **Eventos do SQLAlchemy (`after_insert`)**: o framework já implementa o Observer, então usá-lo não conta como implementar o padrão. Além disso, prenderia regra de negócio ao ciclo de vida do ORM, o oposto do que o ADR-0006 (DIP) removeu do `Pagamento`.
- **Eventos de domínio com barramento de mensagens** (Cosmic Python): mais geral, mas exige infraestrutura (barramento, unit of work) que o projeto não usa. O Observer dá o desacoplamento necessário com cinco classes pequenas.

**Onde fica:** na camada de serviço, e não no `model.py`. As regras de negócio já estão no modelo (`Ticket.registrar_pagamento()` e as invariantes do `Pagamento`); o Observer só liga "pagamento registrado" a reações em dois agregados e usa repositórios, que o domínio não pode importar.

### 4. Participantes mapeados para o código
O `Pagamento` é passado aos observadores como argumento (modelo *push*). Todas as classes estão em `src/estacionamento/service_layer/pagamento_observer.py`.

| Participante (GoF) | Classe |
|---|---|
| Subject | `PublicadorDePagamentos` |
| ConcreteSubject | `RegistradorDePagamentos` |
| Observer | `ObservadorDePagamento` |
| ConcreteObserver | `MarcarTicketComoPago` |
| ConcreteObserver | `AuditoriaDePagamentos` |

`Pagamento`, `Ticket` e os repositórios abstratos aparecem no diagrama só como colaboradores.

### 5. Diagrama de classes
Participantes do padrão em azul.

```mermaid
classDiagram
    direction LR

    class ObservadorDePagamento {
        <<Observer>>
        +atualizar(pagamento)*
    }
    class PublicadorDePagamentos {
        <<Subject>>
        -observadores
        +adicionar(observador)
        +remover(observador)
        +notificar(pagamento)
    }
    class RegistradorDePagamentos {
        <<ConcreteSubject>>
        +registrar(pagamento)
    }
    class MarcarTicketComoPago {
        <<ConcreteObserver>>
        +atualizar(pagamento)
    }
    class AuditoriaDePagamentos {
        <<ConcreteObserver>>
        +atualizar(pagamento)
    }
    class Pagamento
    class Ticket {
        +registrar_pagamento()
    }
    class AbstractPagamentoRepository {
        <<abstract>>
        +add(pagamento)
    }
    class AbstractTicketRepository {
        <<abstract>>
        +get(idTicket)
    }

    PublicadorDePagamentos "1" o-- "*" ObservadorDePagamento : observadores
    PublicadorDePagamentos <|-- RegistradorDePagamentos
    ObservadorDePagamento <|.. MarcarTicketComoPago
    ObservadorDePagamento <|.. AuditoriaDePagamentos
    RegistradorDePagamentos --> AbstractPagamentoRepository : add
    RegistradorDePagamentos ..> Pagamento : notifica
    MarcarTicketComoPago --> AbstractTicketRepository : get
    MarcarTicketComoPago ..> Ticket : registrar_pagamento

    style ObservadorDePagamento fill:#cfe2ff,stroke:#084298,stroke-width:2px
    style PublicadorDePagamentos fill:#cfe2ff,stroke:#084298,stroke-width:2px
    style RegistradorDePagamentos fill:#cfe2ff,stroke:#084298,stroke-width:2px
    style MarcarTicketComoPago fill:#cfe2ff,stroke:#084298,stroke-width:2px
    style AuditoriaDePagamentos fill:#cfe2ff,stroke:#084298,stroke-width:2px
```

### 6. Testes que exercitam o padrão
Arquivo `tests/unit/test_pagamento_observer.py` (9 testes). Os principais:

- `test_registrar_guarda_o_pagamento_e_avisa_os_observadores_na_ordem`: o `RegistradorDePagamentos` guarda o pagamento e avisa os observadores na ordem em que foram adicionados.
- `test_observador_removido_nao_e_avisado`: depois de `remover`, o observador deixa de ser avisado.
- `test_registrar_pagamento_marca_o_ticket_como_pago`: com `MarcarTicketComoPago` e `FakeTicketRepository`, o `Ticket` passa a pago.
- `test_um_registro_aciona_observadores_de_naturezas_diferentes`: um único registro marca o ticket como pago e escreve a linha de auditoria.
- `test_pagamento_recusado_pelo_repositorio_nao_avisa_ninguem`: um segundo pagamento para o mesmo ticket levanta `PagamentoJaRealizadoError` e nenhum observador é avisado.
- `test_falha_de_um_observador_interrompe_os_seguintes`: documenta o custo descrito abaixo.

### 7. Custo da aplicação do padrão
- **Indireção:** cinco classes novas para o que, sem o padrão, seria uma chamada direta. A reação "marcar o ticket como pago" deixa de estar visível no ponto onde o pagamento é registrado.
- **Falhas:** se um observador levanta exceção, os seguintes não são avisados e o pagamento já foi adicionado ao repositório. Quem chama precisa fazer rollback, pois `registrar` não faz commit.
- **Ordem importa:** `MarcarTicketComoPago` deve ser adicionado antes da auditoria. Se a auditoria vier antes e o ticket falhar, ela registra um pagamento que será desfeito.
- **Montagem obrigatória:** a reação só acontece se o observador for adicionado onde a aplicação é montada. Esquecer `MarcarTicketComoPago` deixa o ticket sem pagar e nada acusa o erro.
- **Banco durante a notificação:** `MarcarTicketComoPago` consulta o repositório de tickets, o que pode disparar o autoflush do INSERT do pagamento dentro da notificação.
- **Auditoria via `logging`:** por padrão ela escreve no nível INFO, então as linhas só aparecem se o `logging` estiver configurado para esse nível.