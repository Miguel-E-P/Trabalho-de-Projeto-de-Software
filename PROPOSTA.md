# “Taverna” - Plataforma de Gestão de RPG
**Plataforma de Gestão Multi-Sistema para RPG de Mesa**

O domínio do sistema é o gerenciamento de sessões de RPG de mesa (Role-Playing Game). 

Diferente de plataformas engessadas em um único jogo, o domínio visa ser flexivel, permitindo a criação de Campanhas e Personagens cujas regras e atributos (stats) são moldados dinamicamente pelos Sistemas de RPG escolhidos (ex: D&D, Cyberpunk, Call of Cthulhu). 

O sistema gerencia a relação entre o Mestre (DM), os Jogadores, as fichas de personagens (com validação de pontos e limites de atributos) e a distribuição de itens.



### Entidades de Negócio
O sistema é composto por, pelo menos, 6 entidades de negócio distintas:
**User (Usuário)**: Representa a pessoa física que utiliza a plataforma (autenticação e identidade).

**RPGSystem (Sistema de RPG)**: A matriz de regras de um jogo. Define os atributos base (base stats) permitidos e os itens daquele universo.

**Campaign (Campanha)**: A instância de uma aventura em andamento, atrelada a um System específico.

**CampaignMembership (Vínculo de Campanha)**: Entidade associativa que define o papel de um User dentro de uma Campaign (ex: "Mestre", "Jogador", "Pendente").

**Character (Personagem)**: O avatar de um jogador dentro de uma Campanha. Possui atributos flexíveis (stats) que devem obedecer às regras do System.

**Item (Item/Equipamento)**: Um objeto tangível no universo do jogo (ex: Espada, Poção), que é catalogado no System e pode ser possuído por um(ou mais) Character.

**Trait**: Utilizado para representar classe, raça, e habilidades do Character. Um trait é catalogado no System e pode ser possuído por um(ou mais) Character.



### Agregados Previstos e Invariantes
O projeto será dividido em 3 grandes Agregados para proteger a consistência das regras de negócio:

Agregado 1: Campaign (Campanha)
Raiz de Agregação: Campaign
**Invariantes a proteger**:

**Regra de Moderação**: Uma Campanha não pode existir sem pelo menos 1 membro ativo com a role (papel) de "Mestre" (DM).

**Validação de Membros**: Um usuário não pode criar ou visualizar fichas de Character nesta campanha se o seu CampaignMembership estiver com status "Pendente" (não aprovado pelo DM).

**Unicidade de Vínculo**: Um User não pode ter mais de um registro de associação ativo na mesma Campanha simultaneamente.



Agregado 2: Character (Personagem)
Raiz de Agregação: Character
**Invariantes a proteger**:

**Conformidade de Ficha**: A estrutura de atributos (stats) do Personagem deve bater obrigatoriamente com o modelo de base_stats ditado pelo Sistema da campanha.
**Limite de Pontos**: A soma dos atributos do personagem não pode exceder o teto máximo (Cap) de pontos de criação configurado no sistema.

Integridade do Inventário: Um personagem não pode ter um item em seu inventário com quantidade negativa (< 0). Se chegar a zero, o item deve ser desanexado do personagem.

**Traits Exclusivas**: Certas traits não podem existir ao mesmo tempo no mesmo personagem. Essas traits são marcadas como Exclusivas. Caso o DM tente adicionar uma trait exclusiva quando já existir uma trait exclusiva, ele deve receber um aviso que perderá a trait exclusiva que já existe para ganhar a nova.

**Traits com Pré-Requisitos**: Algumas Traits possuem pré-requisitos. Ao adicionar uma trait com pré-requisito a um personagem, os pré-requisitos devem ser atendidos. Caso não sejam, o personagem não pode ganhar a trait.



Agregado 3: RpgSystem (Sistema de RPG)
Raiz de Agregação: System
**Invariantes a proteger**:
**Unicidade de Atributos**: O sistema (schema base) não pode ser configurado com stats de nomes duplicados (ex: não podem existir dois atributos "Força").

Unicidade de Itens: O sistema não aceita itens duplicados. Uma tocha usada por vários personagens não significa que guardamos tocha duas vezes no sistema, mas sim apenas que ambos os usuários são marcados como dono do mesmo item.

Unicidade de Traits: O sistema (schema base) não pode ser configurado com Traits de nomes duplicados (ex: não podem existir duas traits “Elfo”).

Integridade de Deleção: O blueprint de um Sistema não pode sofrer deleção de um atributo se já existirem Campanhas e Personagens ativos utilizando aquele esquema, pois isso corromperia os personagens existentes.



