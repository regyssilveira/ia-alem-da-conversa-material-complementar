# Laboratório de seleção e ajuste fino

Este laboratório mostra o ciclo de decisão sem exigir GPU, conta ou treinamento pago. Os dados são
sintéticos e ensinam um comportamento estável: responder a consultas sem fonte com abstenção
explícita.

## Percurso

1. Leia `experiment-manifest.json`.
2. Inspecione `data/train.jsonl`, `validation.jsonl` e `test.jsonl`.
3. Execute a validação:

```powershell
python examples/fine-tuning-lab/validate_dataset.py
```

4. Compare a hipótese com alternativas mais simples: instrução, exemplos, RAG ou ferramenta.
5. Use `lora-config.json` apenas como configuração didática; adapte-a ao modelo, biblioteca, hardware
   e licença escolhidos.
6. Treine fora deste repositório somente depois de registrar direitos, infraestrutura, orçamento e
   critérios de interrupção.
7. Avalie no conjunto de teste retido e preencha `promotion-report-template.md`.

## O que o exemplo demonstra

- proveniência e finalidade;
- separação por identificador de cenário;
- ausência de sobreposição entre treino, validação e teste;
- contrato observável de saída;
- hipótese e baseline;
- regressões proibidas;
- versionamento e rollback.

## O que ele não demonstra

- equivalência entre métodos de ajuste;
- qualidade de um modelo comercial;
- adequação da configuração a qualquer GPU;
- autorização para usar dados reais;
- ganho que justifique implantação.

Um treinamento concluído é apenas um candidato. A decisão depende da comparação com a alternativa
mais simples e do custo total de operação.
