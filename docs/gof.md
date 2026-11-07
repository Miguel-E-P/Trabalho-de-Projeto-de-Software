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


**diagrama de classes em Mermaid ou PlantUML, destacando os participantes:**


![alt text](image.png)