# Datathon — Case Passos Mágicos (enunciado oficial, POSTECH FIAP Fase 5)

Transcrito de `POSTECH - Datathon - Fase 5.pdf`.

## Contexto do case

Associação Passos Mágicos, 35 anos de atuação (desde 1992, Embu-Guaçu),
fundada por Michelle Flues e Dimetri Ivanoff. Trabalha a transformação de
vida de crianças e jovens de baixa renda via educação de qualidade, auxílio
psicológico/psicopedagógico, ampliação de visão de mundo e protagonismo.
Virou projeto social/educacional formal em 2016.

Desafio: usar o dataset PEDE (2022-2024) pra responder dores de negócio em
formato de apresentação gerencial/analítica com storytelling, e desenvolver
um modelo preditivo.

## Perguntas para responder na análise

1. **Adequação do nível (IAN)** — Qual é o perfil geral de defasagem dos
   alunos (IAN) e como ele evolui ao longo do ano? (Ex.: quantos alunos
   estão moderadamente ou severamente defasados?)
2. **Desempenho acadêmico (IDA)** — O desempenho acadêmico médio (IDA) está
   melhorando, estagnado ou caindo ao longo das fases e anos?
3. **Engajamento nas atividades (IEG)** — O grau de engajamento dos alunos
   (IEG) tem relação direta com seus indicadores de desempenho (IDA) e do
   ponto de virada (IPV)?
4. **Autoavaliação (IAA)** — As percepções dos alunos sobre si mesmos (IAA)
   são coerentes com seu desempenho real (IDA) e engajamento (IEG)?
5. **Aspectos psicossociais (IPS)** — Há padrões psicossociais (IPS) que
   antecedem quedas de desempenho acadêmico ou de engajamento?
6. **Aspectos psicopedagógicos (IPP)** — As avaliações psicopedagógicas
   (IPP) confirmam ou contradizem a defasagem identificada pelo IAN?
7. **Ponto de virada (IPV)** — Quais comportamentos (acadêmicos, emocionais
   ou de engajamento) mais influenciam o IPV ao longo do tempo?
8. **Multidimensionalidade dos indicadores** — Quais combinações de
   indicadores (IDA + IEG + IPS + IPP) elevam mais a nota global do aluno
   (INDE)?
9. **Previsão de risco com Machine Learning** — Quais padrões nos
   indicadores permitem identificar alunos em risco antes de queda no
   desempenho ou aumento da defasagem? Construa um modelo preditivo que
   mostre uma probabilidade do aluno entrar em risco de defasagem.
10. **Efetividade do programa** — Os indicadores mostram melhora consistente
    ao longo do ciclo nas diferentes fases (Quartzo, Ágata, Ametista,
    Topázio), confirmando o impacto real do programa?
11. **Insights e criatividade** — Insights e pontos de vista não abordados
    nas perguntas acima, com sugestões de melhoria pra Passos Mágicos.

## Entrega

- Link do GitHub com os códigos de limpeza e análise
- Apresentação de storytelling em formato gerencial (PPT ou PDF)
- Notebook Python com o modelo preditivo de risco de defasagem (Q9):
  feature engineering, split treino/teste, modelagem, avaliação
- App Streamlit com o modelo treinado, deploy no Community Cloud
- Vídeo de até 5 minutos apresentando resultados e storytelling

## Correção em relação ao `plano-projeto.md`

O enunciado real numera as perguntas 1-11 (não "Q1-Q10" como o resumo
anterior tratava) — a Q9 é especificamente o modelo de risco de defasagem
(já construído), e a Q11 é o espaço aberto de "insights e criatividade"
onde o modelo de evasão e o dashboard de triagem se encaixam como
diferencial, não como resposta a uma pergunta numerada separada.
