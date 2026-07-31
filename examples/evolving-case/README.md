# Laboratório — assistente de políticas e solicitações

Implementação mínima do caso evolutivo de *IA Além da Conversa*. O laboratório mostra as fronteiras
arquiteturais do livro sem exigir conta, chave de API, framework ou serviço pago.

Ele não tenta simular um LLM. A interpretação e a redação ficam atrás de interfaces substituíveis; o
exemplo executa as propriedades que não podem depender do modelo:

- políticas possuem versão, vigência, jurisdição e nível de acesso;
- recuperação retorna evidência com proveniência;
- ausência ou conflito produz abstenção;
- resposta documental permanece separada do estado transacional;
- ação começa como proposta sem efeito;
- confirmação fica vinculada à proposta exata;
- autorização é verificada no momento da execução;
- chave de idempotência impede efeito duplicado;
- trace registra decisões sem copiar o conteúdo sensível.

## Requisitos

- Python 3.11 ou superior;
- nenhuma dependência externa.

## Executar a demonstração

No diretório raiz do repositório de material complementar:

```powershell
python examples/evolving-case/demo.py
```

## Executar os testes

```powershell
python -m unittest discover -s examples/evolving-case/tests -v
```

## Executar o benchmark quantitativo

```powershell
python examples/evolving-case/benchmark.py
```

O comando compara uma busca lexical deliberadamente ingênua com a configuração governada. O dataset
versionado está em `evaluation/cases.json`. O relatório mede sucesso da tarefa, evidência correta,
abstenção, exposição indevida, detecção de conflito e latência local. Use `--json` para integrar o
resultado a outra ferramenta.

Os números demonstram um protocolo reproduzível, não a qualidade de um modelo comercial. Os casos são
sintéticos e a latência não inclui inferência de LLM.

Os testes cobrem:

1. resposta sustentada por política vigente;
2. abstenção quando a evidência não é suficiente;
3. bloqueio por nível de acesso;
4. confirmação alterada ou inválida;
5. autorização negada no ponto do efeito;
6. repetição segura da mesma solicitação;
7. conflito entre políticas aplicáveis;
8. minimização do trace;
9. invariantes do benchmark governado.

## Percurso sugerido

1. Leia `policy_assistant/domain.py` para conhecer os contratos.
2. Veja a recuperação determinística em `policy_assistant/repository.py`.
3. Percorra a jornada em `policy_assistant/service.py`.
4. Execute `demo.py`.
5. Execute `benchmark.py` e compare as configurações.
6. Injete uma falha e observe qual teste a detecta.

## Onde conectar um modelo

Uma implementação real pode substituir duas decisões:

- extrair intenção e parâmetros da pergunta;
- redigir uma resposta a partir das evidências autorizadas.

O modelo não deve substituir vigência, autorização, confirmação, idempotência ou estado
transacional. Essas propriedades permanecem no aplicativo.

## Limites deliberados

- busca lexical pequena, adequada apenas ao laboratório;
- armazenamento em memória;
- autenticação representada por um ator já identificado;
- confirmação por hash, não por interface real;
- sem aconselhamento jurídico ou interpretação automática de LGPD.

Esses limites são parte do exemplo: cada um indica o componente que precisaria mudar antes de uma
implantação.
