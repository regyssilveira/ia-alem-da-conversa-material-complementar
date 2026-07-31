# Como contribuir

Contribuições podem corrigir um laboratório, propor um caso de decisão ou registrar um aprendizado de
falha ou incidente de forma sanitizada.

## Antes de abrir

1. remova dados pessoais, credenciais, nomes de clientes e informações confidenciais;
2. descreva o resultado esperado e a menor arquitetura considerada;
3. inclua passos ou evidência que permitam reproduzir a observação;
4. declare limitações e o que não foi testado;
5. confirme que possui direito de compartilhar código, dados e texto.

Não envie datasets reais de organizações. Prefira exemplos sintéticos que preservem a propriedade
que deseja demonstrar.

## Código

Execute:

```powershell
python -m unittest discover -s examples/evolving-case/tests -v
python examples/fine-tuning-lab/validate_dataset.py
python examples/serving-lab/simulate.py --requests 20
```

Explique a decisão arquitetural alterada, não apenas a diferença no código. Mudanças devem permanecer
sem dependência paga por padrão e não devem exigir segredos para os testes básicos.

## Decisões e incidentes

Use os modelos em `resources/community/`. Um incidente publicado deve ser um estudo de aprendizado:
linha do tempo mínima, condição contribuidora, detecção, contenção, evidência e mudança verificável.
Não atribua culpa individual.

Ao contribuir, você concorda que código seja distribuído sob MIT e textos/templates sob CC BY 4.0,
conforme `LICENSE.md`.
