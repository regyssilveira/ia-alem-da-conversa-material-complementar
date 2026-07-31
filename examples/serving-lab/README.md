# Laboratório de serving, filas e custo

Simulador determinístico para explorar capacidade antes de conectar uma GPU ou endpoint real.

```powershell
python examples/serving-lab/simulate.py
python examples/serving-lab/simulate.py --workers 2 --arrival-ms 40 --service-ms 120
python examples/serving-lab/simulate.py --workers 4 --batch-size 4 --arrival-ms 20
```

O relatório apresenta tarefas aceitas e rejeitadas, throughput, p50, p95, espera em fila, utilização
aproximada e custo por sucesso. Altere uma variável por vez.

## Experimentos sugeridos

1. Reduza o intervalo de chegada até surgir fila.
2. Aumente trabalhadores e observe custo e utilização.
3. Aumente o lote e compare throughput com latência.
4. Defina prazo máximo de fila e observe rejeição transparente.
5. Modifique a taxa de sucesso e compare custo por tentativa com custo por sucesso.

O simulador não prevê desempenho de hardware. Ele ensina relações e ajuda a formular um teste de carga
real com modelo, contexto e infraestrutura identificados.
