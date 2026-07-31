# Mapa de capítulos, práticas e evidências

Use este mapa depois da leitura ou como plano de oficina. “No capítulo” indica que a prática produz
um artefato livre; os demais caminhos apontam para arquivos preenchíveis ou laboratórios.

| Cap. | Prática principal | Arquivo de apoio | Evidência produzida |
|---:|---|---|---|
| 1 | comparar três arquiteturas | `templates/roteiro-menor-arquitetura.md` | decisão inicial e baseline |
| 2 | separar regra de aprendizagem | `templates/memo-de-decisao.md` | hipótese de uso de IA |
| 3 | explicar previsão e limite | no capítulo | modelo mental verificável |
| 4 | orçar contexto | no capítulo | orçamento e estratégia de corte |
| 5 | testar ilusão de competência | `templates/memo-de-decisao.md` | falha, risco e controle |
| 6 | transformar pedido em contrato | no capítulo | especificação de tarefa |
| 7 | montar pacote de contexto | no capítulo | fontes, exemplos e limites |
| 8 | decompor e localizar falhas | no capítulo | cadeia com contratos |
| 9 | construir porta de liberação | `examples/evolving-case` | dataset, benchmark e decisão |
| 10 | contratar uma ferramenta | `templates/contrato-de-ferramenta.md` | esquema, efeito e erro |
| 11 | inventariar memória | no capítulo | ciclo de vida do estado |
| 12 | testar vizinhos intrusos | no capítulo | casos de fronteira semântica |
| 13 | publicar e revogar evidência | `templates/avaliacao-rag.csv` | avaliação de recuperação |
| 14 | realizar audiência da autonomia | `templates/matriz-de-autonomia.md` | necessidade e orçamento de agência |
| 15 | planejar com orçamento | `templates/matriz-de-autonomia.md` | parada, limite e escalonamento |
| 16 | atacar composição de permissões | `templates/contrato-de-ferramenta.md` | matriz de autoridade |
| 17 | projetar recuperação | `templates/runbook-de-incidente.md` | escada de falha e resposta |
| 18 | retirar um agente | `templates/memo-de-decisao.md` | contribuição marginal por papel |
| 19 | quebrar o consumidor | no capítulo | contrato e fixtures de compatibilidade |
| 20 | testar dois hosts MCP | `templates/modelo-de-ameacas.md` | fronteiras de host e servidor |
| 21 | percorrer pergunta e evidência | `templates/avaliacao-rag.csv` | métricas de ingestão, busca e resposta |
| 22 | executar processo fora de ordem | no capítulo | estados, idempotência e compensação |
| 23 | realizar banca de promoção | `templates/banca-de-arquitetura.md` | requisitos e portas de maturidade |
| 24 | selecionar e adaptar modelo | `examples/fine-tuning-lab` | manifesto, splits e promoção |
| 25 | simular indisponibilidade | `templates/memo-de-decisao.md` | topologia e modo degradado |
| 26 | simular carga e custo | `examples/serving-lab` | latência, fila e custo por sucesso |
| 27 | executar oficina de ameaça | `templates/modelo-de-ameacas.md` | ameaça, controle e evidência |
| 28 | investigar uma regressão | `templates/runbook-de-incidente.md` | trace, decisão e recuperação |
| 29 | defender a menor solução | `workshop/` | roteiro, memo e banca |
| 30 | avaliar uma promessa nova | `templates/memo-de-decisao.md` | radar e experimento de aprendizagem |

## Percurso mínimo de um projeto

Se não houver tempo para todas as práticas, use esta sequência:

1. capítulo 1: roteiro da menor arquitetura;
2. capítulo 9: conjunto e porta de avaliação;
3. capítulo 14: teste de necessidade de agente;
4. capítulo 19 ou 22: contrato ou workflow;
5. capítulo 23: promoção;
6. capítulos 26 a 28: custo, risco e observabilidade;
7. capítulo 29: banca final.

O objetivo não é preencher mais documentos. Cada artefato deve sustentar uma decisão, um teste ou uma
condição de parada.
