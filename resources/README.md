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

Copie o arquivo antes de preencher. Não registre segredos, dados pessoais ou conteúdo de produção nos
templates. Use identificadores e evidências minimizadas.

## Caso brasileiro

`caso-brasileiro-lgpd.md` adapta a jornada do assistente corporativo ao contexto de proteção de dados
no Brasil, com fontes oficiais da ANPD e limites explícitos entre arquitetura e análise jurídica.

## Laboratório executável

O caso de referência está em `examples/evolving-case`. Ele usa somente a biblioteca padrão do Python
e possui testes automatizados.
