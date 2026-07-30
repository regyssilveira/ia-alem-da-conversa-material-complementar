# Caso brasileiro — assistente corporativo e proteção de dados

Este material adapta o caso evolutivo a uma organização brasileira. Ele oferece perguntas de
arquitetura e governança, não aconselhamento jurídico. A definição de hipótese legal, papéis,
obrigações e comunicação deve envolver jurídico, encarregado e responsáveis pelo tratamento.

## Cenário

Uma empresa disponibiliza um assistente para responder políticas internas e iniciar solicitações de
trabalho remoto. A jornada pode tratar identidade funcional, localização, datas, liderança,
justificativas e registros de aprovação. O fato de a interface ser conversacional não altera a
necessidade de definir finalidade, acesso, retenção e responsabilidade.

## Decisões antes do modelo

1. identificar controlador, operadores, eventual suboperador e encarregado aplicáveis ao fluxo;
2. mapear dado, finalidade, origem, destinatário, retenção e cópias derivadas;
3. confirmar a hipótese legal e as obrigações do caso concreto;
4. separar conteúdo de política, dado transacional e conversa;
5. impedir que prompts, logs e índices se tornem repositórios paralelos;
6. definir como o titular obtém informação, correção e demais direitos aplicáveis;
7. preparar detecção, avaliação e resposta a incidente.

O guia oficial da ANPD sobre agentes de tratamento explica os papéis de controlador, operador,
suboperador e encarregado e deve ser consultado em sua versão vigente:

- https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-para-definicoes-dos-agentes-de-tratamento-de-dados-pessoais-e-do-encarregado

## Mapa mínimo da jornada

| Etapa | Dados possíveis | Decisão arquitetural |
|---|---|---|
| autenticação | identificador e vínculo | manter fora do prompt sempre que possível |
| pergunta | texto livre | avisar finalidade e reduzir dados não necessários |
| recuperação | política e metadados | filtrar acesso antes de enviar contexto |
| resposta | orientação e citações | não revelar existência de conteúdo restrito |
| proposta | destino, período e justificativa | separar de execução e confirmar conteúdo exato |
| workflow | estado, aprovação e eventos | aplicar autorização e idempotência |
| observabilidade | versões e códigos | minimizar conteúdo e definir retenção |

## Exercício de minimização

Para cada campo, complete:

> Sem este dado, a decisão muda? Existe forma menos identificável de produzir o mesmo resultado?

Remova campos sem finalidade demonstrável. Depois percorra banco, cache, índice, memória, trace,
avaliação e backup. A exclusão do registro principal não basta se uma cópia derivada continuar
influenciando o sistema.

## Incidente

A Resolução CD/ANPD nº 15/2024 regulamenta a comunicação de incidentes de segurança. A ANPD informa
que o controlador deve avaliar incidentes e comunicar a Autoridade e os titulares quando puderem
ocasionar risco ou dano relevante, conforme as condições do regulamento. Consulte a fonte vigente:

- https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-aprova-o-regulamento-de-comunicacao-de-incidente-de-seguranca
- https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis

O runbook do sistema deve permitir:

- determinar quais pessoas e dados foram afetados;
- identificar versões, ferramentas e efeitos envolvidos;
- conter a rota ou credencial;
- preservar evidência sem ampliar exposição;
- apoiar a avaliação jurídica e regulatória;
- comunicar de modo claro quando aplicável;
- corrigir derivados e adicionar o incidente à regressão.

## Porta de promoção

O caso só avança quando a equipe consegue demonstrar finalidade, minimização, acesso por identidade,
exclusão de derivados, trace minimizado, resposta a incidente e caminho de contestação. “O provedor é
compatível com LGPD” não substitui essas propriedades na arquitetura concreta.
