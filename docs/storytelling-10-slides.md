# Storytelling — Case Passos Mágicos (10 slides)

Roteiro pra apresentação gerencial. Cada bloco = 1 slide: título, conteúdo e
o gráfico/tabela de origem (notebook + célula). Fonte de todos os números:
`notebooks/01_modelagem.ipynb`, `02_eda_desempenho.ipynb`,
`03_eda_psicossocial.ipynb`.

---

## Slide 1 — Capa / Contexto

**Título:** Do dado ao cuidado: o que o PEDE revela sobre os alunos da Passos Mágicos

- Associação Passos Mágicos, 35 anos, educação + apoio psicossocial pra
  crianças e jovens em vulnerabilidade (Embu-Guaçu)
- Base: PEDE 2022-2024, painel longitudinal — 3.030 registros, 1.661 alunos,
  468 acompanhados nos 3 anos completos
- O que essa análise entrega: 10 respostas de negócio + 2 modelos preditivos
  + 1 dashboard de triagem operacional

*Visual: nenhum gráfico, só os 3 números grandes (3.030 / 1.661 / 468).*

---

## Slide 2 — Como chegamos aos números

**Título:** Antes de responder, arrumar a casa

- As 3 planilhas (2022/2023/2024) tinham nomes de coluna diferentes, uma
  coluna morta (`INDE 23` 100% vazia), idades corrompidas em data pelo
  Excel, fase colada com turma — tudo corrigido e documentado
- Definição de evasão: aluno ausente no ano seguinte, **exceto** quem já
  estava na fase/idade de saída natural do programa
- Por quê isso importa: sem essa limpeza, qualquer número abaixo estaria
  errado sem dar erro nenhum

*Fonte: `docs/decisions/0001-consolidacao-painel.md`. Visual: lista curta dos
4 problemas corrigidos (não precisa gráfico).*

---

## Slide 3 — O paradoxo da defasagem (Q1 + Q10)

**Título:** O perfil de defasagem melhora — mas será que é o programa, ou é quem fica?

- Olhando a safra inteira a cada ano, a defasagem melhora: alunos "adequados"
  (IAN=10) sobem de 30% (2022) pra 54% (2024); "severos" praticamente
  desaparecem (3,3% → 0,3%)
- Mas nos 468 alunos que ficaram os 3 anos completos, o INDE médio não se
  move: 7,38 → 7,36 → 7,38. E o movimento de pedra é quase simétrico (29%
  sobe, 26% desce)
- Leitura: parte da melhora "agregada" pode ser o aluno mais defasado saindo
  da amostra (evadindo), não virando aluno adequado

*Fonte: notebook 03 Q1 + notebook 02 Q10. Visual: os dois gráficos de barra
lado a lado (perfil por ano / INDE da coorte fixa).*

---

## Slide 4 — Aprendizado e engajamento não seguem uma linha reta

**Título:** IDA oscila, mas engajamento é o fio condutor

- IDA médio não tem tendência única: 6,09 (2022) → 6,66 (2023) → 6,35
  (2024), e varia por fase sem padrão de "quanto mais avançado, melhor"
- IEG (engajamento) é o que consistentemente acompanha desempenho e ponto de
  virada: r=0,54 com IDA, r=0,56 com IPV
- Leitura: nota isolada oscila por diversos fatores; engajamento é o sinal
  mais estável pra equipe pedagógica observar

*Fonte: notebook 02 Q2 + Q3. Visual: linha do IDA por ano + os 2 scatterplots
de IEG.*

---

## Slide 5 — O aluno nem sempre sabe onde está

**Título:** Autoavaliação bate pouco com a realidade

- IAA (autoavaliação) correlaciona fraco com desempenho real (r=0,12 com
  IDA) e engajamento (r=0,13 com IEG)
- 16,5% dos alunos se avaliam bem acima do que os dados mostram; 11,6% bem
  abaixo — quase 3 em cada 10 têm uma percepção de si descolada
- Leitura: autoavaliação sozinha não é um bom termômetro — nem pra cima
  (excesso de confiança) nem pra baixo (autoestima baixa não condizente)

*Fonte: notebook 03 Q4. Visual: histograma do gap autoavaliação × realidade.*

---

## Slide 6 — Psicossocial e psicopedagógico: sinal fraco, e isso é um achado

**Título:** O que os avaliadores psicossociais enxergam nem sempre aparece nos números

- IPS (psicossocial) quase não prediz nada nos dois modelos — nunca foi o
  driver dominante em nenhuma predição, em nenhum dos dois riscos
  (correlação com os alvos ≈ 0)
- IPP (psicopedagógico) concorda pouco com a defasagem: 33% dos alunos já
  identificados como defasados pelo IAN têm avaliação psicopedagógica boa
  (IPP ≥ 7,5) — sem sinalizar o problema
- Leitura: não é erro de dado (checamos: não falta mais que os outros
  indicadores, não tem variância baixa) — é que a forma agregada de coletar
  esses dois indicadores hoje carrega pouca informação acionável

*Fonte: notebook 03 Q5, Q6 + `docs/decisions/0002-ips-sem-sinal-preditivo.md`.
Visual: gráfico de barras do IPP médio por categoria de defasagem.*

---

## Slide 7 — O que realmente move o ponteiro

**Título:** Ponto de virada e nota geral seguem o mesmo padrão: acadêmico + engajamento

- O que mais separa quem atinge o Ponto de Virada de quem não atinge: IDA
  (+2,0 pontos) e IEG (+1,3) — não é IPS
- O que mais separa o quartil de INDE mais alto do mais baixo: IDA (1,95
  desvio-padrão) e IEG (1,72) — IPS é o que menos diferencia (0,68)
- Leitura: os dois indicadores que a Passos Mágicos já monitora de perto
  (aprendizado e engajamento) são, de fato, os que mais explicam o resultado
  final do aluno

*Fonte: notebook 02 Q7 + Q8. Visual: os 2 gráficos de barra horizontal
(gap por indicador).*

---

## Slide 8 — Modelo preditivo: risco de defasagem

**Título:** Prevendo quem vai piorar, antes de piorar

- XGBoost treinado em 2022→2023, testado em 2023→2024 (sem vazamento de
  dados futuros) — ROC-AUC 0,83, PR-AUC 0,52
- Explicabilidade via SHAP: cada predição vem com o "driver dominante" —
  acadêmico, engajamento, psicossocial ou psicopedagógico — pra equipe saber
  **por quê**, não só **quem**
- 92% das predições de risco de defasagem têm o eixo acadêmico como driver
  principal — consistente com o Slide 7

*Fonte: notebook 01. Visual: barra de ROC-AUC (0,83 vs linha de 0,50).*

---

## Slide 9 — O diferencial: evasão e triagem operacional

**Título:** Além da nota: prever quem a gente pode perder

- Segundo modelo, não pedido no enunciado: risco de **evasão** — mais
  relevante pra sustentabilidade do programa do que uma queda pontual de
  nota. ROC-AUC 0,63 — mais fraco que o de defasagem, **de propósito
  reportado assim**: o PEDE mede desempenho, não mede os motivos reais de
  evasão (mudança de endereço, questão financeira da família)
- Dashboard Streamlit: lista dos 1.156 alunos ativos, ranqueada por risco
  combinado, com driver dominante e exportação em CSV — pensado pra virar
  rotina semanal da equipe pedagógica, não um app de consulta passiva
- Score é sinalizador pra priorização humana, não veredito automático

*Fonte: notebook 01 + `app/dashboard.py`. Visual: screenshot do dashboard.*

---

## Slide 10 — Recomendações

**Título:** O que a Passos Mágicos pode fazer com isso

1. Usar o dashboard de triagem como rotina semanal, priorizando quem tem
   `risco_evasao` alto e driver `engajamento` — é o grupo mais acionável
2. Revisar a forma de captar o indicador psicossocial (IPS) — hoje ele não
   carrega sinal preditivo, o que sugere rever a metodologia de coleta, não
   descartar o cuidado psicossocial em si
3. Investigar os 33% de casos onde IPP e IAN discordam — pode ser
   subnotificação da avaliação psicopedagógica
4. Tratar a queda de IPS no terço mais baixo como alerta precoce — sinal
   fraco, mas real, de risco de queda de aprendizado no ano seguinte

*Visual: nenhum gráfico — 4 bullets de ação, fechamento gerencial.*
