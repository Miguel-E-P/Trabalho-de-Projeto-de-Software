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


