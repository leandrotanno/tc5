# 0002 — IPS sem sinal preditivo (não é bug, é achado)

## Contexto
Em `notebooks/01_modelagem.ipynb`, o eixo `psicossocial` (SHAP, agrupado em
`src/tc5/explain.py`) nunca aparece como driver dominante em nenhum dos dois
modelos (defasagem, evasão), em nenhuma das 1874 linhas de teste. Investigado
em `notebooks/03_eda_psicossocial.ipynb`.

## O que foi descartado
- **Missingness**: IPS falta em 3,7% das linhas de `features.csv` — na mesma
  faixa de IDA/IEG/IAA. Quem realmente falta muito é IPP (49,9%, ausente em
  todo 2022), não IPS.
- **Baixa variância**: desvio-padrão de 1,90 (escala 0-10), comparável a IDA
  (1,85) e IAN (2,50). Não é uma variável travada num valor só.

## O que explica
Correlação de IPS com os dois targets é a mais fraca dos 6 indicadores:
r=0,007 com `evasao` e r=0,056 com `piora_defasagem` (IEG chega a r=-0,32 com
evasão; IAN a r=0,28 com piora de defasagem). A diferença de média entre
grupos (evadiu vs não, piorou vs não) pra IPS é quase zero, contra gaps de
quase 1 ponto em IDA/IEG.

Em `03_eda_psicossocial.ipynb` (Q5) aparece um sinal não-linear fraco — o
tercil mais baixo de IPS antecede queda de IDA no ano seguinte em 56% dos
casos vs 45% no tercil mais alto — real, mas pequeno demais pra competir com
os indicadores acadêmicos/de engajamento num modelo de árvore.

## Conclusão
O IPS, do jeito que é coletado hoje (nota agregada dos avaliadores), não
prediz evasão nem piora de defasagem nesta base. Não é problema de qualidade
de dado — é isso que os dados mostram. Duas leituras possíveis, não
excludentes: (1) o aspecto psicossocial de fato pesa menos nesses dois
desfechos específicos do que desempenho/engajamento, ou (2) a forma de
agregação do indicador (média das notas dos avaliadores) perde informação
que uma leitura mais fina (por avaliador, por dimensão avaliada) capturaria.
Não investigado a fundo por falta de granularidade nos dados — o dataset só
tem a nota agregada, não os itens que a compõem.
