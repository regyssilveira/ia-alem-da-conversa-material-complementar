# IA Além da Conversa — Material Complementar

Laboratório executável, testes e templates do livro **IA Além da Conversa: Como ir além do ChatGPT e
construir soluções com LLMs, agentes, RAG, MCP e automação**, de Régys Borges da Silveira.

O material transforma princípios do livro em artefatos que podem ser executados, preenchidos,
revisados e adaptados. Ele é independente de fornecedor e não exige chave de API, conta ou serviço
pago.

## Comece aqui

- [`examples/evolving-case`](examples/evolving-case): laboratório do assistente de políticas e
  solicitações;
- [`examples/fine-tuning-lab`](examples/fine-tuning-lab): dataset, manifesto e ciclo de ajuste fino;
- [`examples/serving-lab`](examples/serving-lab): simulador de carga, filas, batching e custo;
- [`resources/templates`](resources/templates): contratos, matrizes, dataset e runbook;
- [`resources/study-tracks.md`](resources/study-tracks.md): trilhas de estudo e oficina corporativa;
- [`resources/workshop`](resources/workshop): pacote completo para facilitar a oficina corporativa;
- [`resources/community`](resources/community): modelos para compartilhar decisões, falhas e incidentes;
- [`resources/chapter-practice-map.md`](resources/chapter-practice-map.md): mapa de capítulos,
  práticas, arquivos e evidências;
- [`review`](review): protocolo e formulário de leitura-piloto;
- [`resources/caso-brasileiro-lgpd.md`](resources/caso-brasileiro-lgpd.md): aplicação arquitetural ao
  contexto brasileiro de proteção de dados.

## Executar a demonstração

Requisitos:

- Python 3.11 ou superior;
- nenhuma dependência externa.

```powershell
python examples/evolving-case/demo.py
```

## Executar os testes

```powershell
python -m unittest discover -s examples/evolving-case/tests -v
```

Os 15 testes cobrem arquitetura, autorização, idempotência, benchmark, replay, roteamento, porta de
liberação, divisão de datasets e serving.

Os testes também são executados automaticamente nas versões de Python declaradas no workflow do
repositório. Uma release identifica um estado reproduzível dos códigos e laboratórios; o texto do
livro mantém seu próprio ciclo editorial.

## Executar o benchmark

```powershell
python examples/evolving-case/benchmark.py
```

O benchmark compara uma recuperação lexical ingênua e uma configuração governada usando um dataset
sintético versionado. Ele mede sucesso, evidência, abstenção, exposição indevida, conflito e latência
local. Use `--json` para obter saída estruturada.

O `model_benchmark.py` funciona offline por replay ou pode usar um endpoint compatível configurado por
variáveis de ambiente. Nenhum segredo deve ser salvo no repositório.

## Relação com o livro

Este repositório acompanha a primeira edição da obra. O livro explica as decisões e os modelos mentais;
o repositório oferece uma implementação mínima e artefatos reutilizáveis. O laboratório não é uma
aplicação pronta para produção e não substitui análise de requisitos, segurança, proteção de dados,
testes ou avaliação jurídica.

## Atualizações e correções

Use as [issues do repositório](https://github.com/regyssilveira/ia-alem-da-conversa-material-complementar/issues)
para relatar erros, sugerir melhorias ou propor novos cenários. Alterações relevantes serão registradas
nas versões publicadas.

Há formulários diferentes para caso de decisão, aprendizado de incidente e correção técnica. Antes de
publicar, remova dados pessoais, segredos, nomes de clientes e detalhes que ampliem risco. A comunidade
existe para comparar decisões e aprender com falhas, não para expor organizações ou pessoas.

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) e use os modelos em `resources/community/` para preparar
uma contribuição reproduzível.

## Versões e compatibilidade

A primeira edição do livro corresponde à release `v1.3.0`. Consulte [CHANGELOG.md](CHANGELOG.md) para
entender o que mudou e [COMPATIBILITY.md](COMPATIBILITY.md) para versões verificadas do Python e
comandos de validação.

## Licenças

O código-fonte em `examples/` é distribuído sob a licença MIT. Os textos, templates e demais conteúdos
em `resources/` são distribuídos sob a licença Creative Commons Atribuição 4.0 Internacional
(CC BY 4.0). Consulte [LICENSE.md](LICENSE.md).

Copyright © 2026 Régys Borges da Silveira.
