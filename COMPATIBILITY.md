# Compatibilidade

| Edição do livro | Release complementar | Python verificado | Estado |
|---|---|---|---|
| 1ª edição, manuscrito de 31 jul. 2026 | `v1.3.0` | 3.11, 3.12 e 3.13 | recomendado |
| 1ª edição, estado anterior à oficina | `v1.2.1` | 3.11 | preservado |
| 1ª edição, laboratórios iniciais | `v1.0.0` a `v1.2.0` | 3.11 | histórico |

## Contrato da v1.3.0

Comandos de verificação:

```powershell
python -m unittest discover -s examples/evolving-case/tests -v
python examples/fine-tuning-lab/validate_dataset.py
python examples/serving-lab/simulate.py --requests 20
```

Os laboratórios básicos não exigem dependências externas, chave de API ou serviço pago. O modo
conectado é opcional. Releases posteriores podem ampliar as versões testadas sem prometer que versões
anteriores ou futuras do Python funcionarão sem verificação.

## Relação com o livro

Uma release identifica o estado reproduzível dos códigos e recursos, não uma nova edição do texto.
Correções editoriais podem ocorrer sem release de código; mudanças de contrato, comando ou evidência
dos laboratórios exigem atualização deste arquivo e do changelog.
