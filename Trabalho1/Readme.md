Padaria Mineração
Introdução
O projeto "Padaria Mineração" tem como objetivo analisar as associações entre produtos vendidos em uma padaria. Para isso, focamos em identificar quais produtos são frequentemente adquiridos juntos. Os principais produtos em análise incluem: Café, Pão, Presunto, Queijo, Pastel, Doce e Refrigerante.


Etapas do Processo
1 - Carregamento do Arquivo JSON
A primeira etapa foi carregar o arquivo JSON que contém os dados de vendas. Para transformar esses dados em um formato utilizável, utilizamos a função json_normalize do Python, que converte o arquivo JSON em um DataFrame, facilitando a manipulação e análise dos dados.


2 - Remoção de Colunas Irrelevantes
No segundo passo, removemos a coluna "compra", que continha um número igual para todas as entradas. Essa coluna não contribuía para a análise de associação e, portanto, sua remoção foi crucial para focar nos produtos de interesse.


3 - Foco nos Produtos
O terceiro passo consistiu em simplificar a análise ao eliminar marcas e preferências pessoais. Assim, mantivemos apenas as informações essenciais sobre os produtos, como Pão, Presunto, Pastel, Queijo, entre outros, permitindo que a análise se concentre nos itens realmente relevantes para a identificação de padrões de compra.


4 - Formatação dos Nomes
Por fim, formatamos os nomes dos produtos para garantir uniformidade. Essa etapa é importante para evitar discrepâncias nas nomenclaturas e facilitar a análise, assegurando que cada produto seja reconhecido da mesma forma, independentemente de variações em sua escrita.


5 - Transformação em Colunas de True e False
Nessa etapa, criamos uma coluna para cada produto, indicando True se o produto está presente na compra e False se não está. Isso foi feito através da explosão da coluna de produtos e da aplicação do one-hot encoding, permitindo que cada produto fosse representado como uma coluna binária. Após agrupar os dados, as ocorrências foram somadas e convertidas para valores booleanos.




6 - Aplicar o Princípio Apriori
Utilizamos o Princípio Apriori para identificar conjuntos frequentes de itens. Esse princípio nos permite encontrar quais produtos são frequentemente comprados juntos e gerar regras de associação baseadas em métricas como suporte, confiança e lift.


7 - Análise das Regras
As 5 principais regras de associação foram exibidas, juntamente com a regra mais influente que mostra a relação direta entre dois produtos. Além disso, foram identificadas as regras que implicam a compra de "Doce", permitindo uma visão mais detalhada sobre as preferências dos consumidores.


8 - Interpretação das Regras
As regras geradas incluem informações sobre o antecedente (produto analisado), consequente (produto frequentemente comprado junto), suporte (frequência da regra em relação ao total de transações), confiança (probabilidade de compra do consequente quando o antecedente é adquirido) e lift (medida da frequência do consequente em relação à sua frequência global quando o antecedente é comprado).



