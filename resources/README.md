# Recursos complementares

Materiais reutilizáveis de *IA Além da Conversa*. Eles transformam decisões apresentadas no livro em
artefatos que podem ser preenchidos, revisados e versionados.

## Templates

| Arquivo | Uso |
|---|---|
| `templates/memo-de-decisao.md` | comparar alternativas e registrar por que uma arquitetura foi escolhida |
| `templates/contrato-de-ferramenta.md` | definir entrada, autoridade, efeito, erro e idempotência |
| `templates/avaliacao-rag.csv` | formar um conjunto inicial de avaliação de recuperação e geração |
| `templates/matriz-de-autonomia.md` | limitar informação, escolha, ação, duração e gasto de um agente |
| `templates/modelo-de-ameacas.md` | conectar fronteiras, ameaças, controles, sinais e recuperação |
| `templates/runbook-de-incidente.md` | responder a regressão, indisponibilidade ou efeito indevido |
| `templates/ficha-de-caso.md` | comparar casos de uso pela menor arquitetura suficiente |
| `templates/banca-de-arquitetura.md` | comparar regra, prompt, RAG, ferramenta, ajuste e modelo maior |
| `templates/ficha-de-dataset.md` | registrar finalidade, origem, divisão, cobertura e manutenção |
| `templates/orcamento-de-serving.csv` | registrar carga, latência, throughput, erro e custo por sucesso |
| `templates/roteiro-menor-arquitetura.md` | comparar resultado, baseline, variação, evidência, autoridade, alternativas e operação |

Copie o arquivo antes de preencher. Não registre segredos, dados pessoais ou conteúdo de produção nos
templates. Use identificadores e evidências minimizadas.

## Caso brasileiro

`caso-brasileiro-lgpd.md` adapta a jornada do assistente corporativo ao contexto de proteção de dados
no Brasil, com fontes oficiais da ANPD e limites explícitos entre arquitetura e análise jurídica.

## Laboratório executável

Os laboratórios usam somente a biblioteca padrão do Python:

- `examples/evolving-case`: arquitetura, benchmark conectável, roteamento e porta de liberação;
- `examples/fine-tuning-lab`: dataset, manifesto, LoRA ilustrativo e promoção;
- `examples/serving-lab`: carga, fila, batching, throughput e custo.

`study-tracks.md` organiza o livro em trilhas de quatro semanas, oito encontros e percursos por papel.
O diretório `workshop/` contém o pacote de facilitação, caderno, cartões de mudança e rubrica da banca
para transformar a trilha de oito encontros em oficina corporativa.
