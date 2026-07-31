# IA Além da Conversa — Material Complementar

Laboratório executável, testes e templates do livro **IA Além da Conversa: Como ir além do ChatGPT e
construir soluções com LLMs, agentes, RAG, MCP e automação**, de Régys Borges da Silveira.

O material transforma princípios do livro em artefatos que podem ser executados, preenchidos,
revisados e adaptados. Ele é independente de fornecedor e não exige chave de API, conta ou serviço
pago.

## Comece aqui

- [`examples/evolving-case`](examples/evolving-case): laboratório do assistente de políticas e
  solicitações;
- [`resources/templates`](resources/templates): contratos, matrizes, dataset e runbook;
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

Os nove testes cobrem proveniência, abstenção, controle de acesso, confirmação vinculada, autorização
no ponto do efeito, idempotência, conflito de políticas, minimização do trace e invariantes da
avaliação.

## Executar o benchmark

```powershell
python examples/evolving-case/benchmark.py
```

O benchmark compara uma recuperação lexical ingênua e uma configuração governada usando um dataset
sintético versionado. Ele mede sucesso, evidência, abstenção, exposição indevida, conflito e latência
local. Use `--json` para obter saída estruturada.

## Relação com o livro

Este repositório acompanha a primeira edição da obra. O livro explica as decisões e os modelos mentais;
o repositório oferece uma implementação mínima e artefatos reutilizáveis. O laboratório não é uma
aplicação pronta para produção e não substitui análise de requisitos, segurança, proteção de dados,
testes ou avaliação jurídica.

## Atualizações e correções

Use as [issues do repositório](https://github.com/regyssilveira/ia-alem-da-conversa-material-complementar/issues)
para relatar erros, sugerir melhorias ou propor novos cenários. Alterações relevantes serão registradas
nas versões publicadas.

## Licenças

O código-fonte em `examples/` é distribuído sob a licença MIT. Os textos, templates e demais conteúdos
em `resources/` são distribuídos sob a licença Creative Commons Atribuição 4.0 Internacional
(CC BY 4.0). Consulte [LICENSE.md](LICENSE.md).

Copyright © 2026 Régys Borges da Silveira.
