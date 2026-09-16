Optei por realizar a estrutura inicial das classes do agregado cliente/ veiculo para deixar explicitado as dependências de classe de cima pra baixo,
sinalizando por comentários qual atributo específico depende da classe de cima para sua composição. Cada classe já está com sua classificação:
value object, entidade simples e entidade raiz. A class Placa não possui atributo "id" própria por que foi classificada como value object, pois,
é definida apenas pelo valor e é imutável.

Pedro: Para proteger contra golpes. Vamos precisar de algum sistema de verificacao de tempo. Ou seja, quando o pagamento ocorrer, e o ticket for atualizado para valido, o sistema precisa verificar se o ticket foi usado ate certo periodo de tempo, se nao, atualizar ele para invalido novamente. Pois se nao, teremos um sistema em que um cliente pode entrar no estacionamento, pagar o ticket, e permanecer horas/dias a mais no estacionamento, e sair no fim de tudo tendo pago como se tivesse ficado apenas minutos dentro do estacionamento.
