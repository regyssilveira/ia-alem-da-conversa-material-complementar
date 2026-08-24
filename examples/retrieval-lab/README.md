# Laboratório de recuperação governada

Este laboratório compara recuperação lexical, uma representação conceitual determinística e uma
combinação híbrida. Ele não finge reproduzir embeddings comerciais: a camada conceitual usa um
vocabulário pequeno e visível para que ranking, filtros e métricas possam ser inspecionados sem conta,
rede ou dependência externa.

```powershell
python examples/retrieval-lab/retrieve.py
python examples/retrieval-lab/retrieve.py --mode hybrid --json
python -m unittest discover -s examples/retrieval-lab/tests -v
```

## O que observar

- versões revogadas são removidas antes do ranking;
- unidade e data fazem parte do contrato de consulta;
- a exceção local e a regra global podem aparecer juntas;
- sinônimos alteram lexical e recuperação conceitual de maneiras diferentes;
- pergunta fora da coleção deve produzir abstenção;
- `recall@3`, MRR e acerto de abstenção medem propriedades diferentes.

## Experimentos

1. Remova um sinônimo de `CONCEPTS` e compare os três modos.
2. Mude o limite de score e observe recuperação contra abstenção.
3. Publique novamente a versão revogada e veja o teste falhar.
4. Divida um trecho em unidades menores e meça a nova posição.
5. Substitua `conceptual()` por embeddings reais mantendo o mesmo contrato e os mesmos casos.

O passo 5 é deliberadamente opcional. O objetivo é ensinar uma arquitetura avaliável e governada,
não promover um banco vetorial ou provedor.
