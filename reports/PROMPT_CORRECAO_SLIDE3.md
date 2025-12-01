# Instruções para Correção do Slide 3 - Análise de Features e Correlação

## Contexto

A apresentação está excelente visualmente. Precisamos expandir o conteúdo do **Slide 3** para incluir uma análise mais completa das correlações, mostrando os Top 5 fatores positivos e Top 5 fatores negativos com o target (MEDV), além de manter a legenda completa das features.

## Slides a Manter (Sem Alterações)

- Slides 1 a 2: Manter exatamente como estão.
- Slides 4 a 12: Manter exatamente como estão.

## Correções Necessárias

### Slide 3: Análise de Features e Correlação

**Problema:** O slide atualmente mostra apenas 3 variáveis determinantes (LSTAT, RM, PTRATIO), mas seria mais informativo e visualmente rico mostrar os Top 5 correlações positivas e Top 5 negativas.

**Correção:**

1. **Manter a seção "Legenda das Features"** (todas as 13 features + target)

2. **Substituir a seção "Variáveis Determinantes"** por:

   **Top 5 Correlações Positivas com MEDV:**
   
   1. **RM (+0.70):** Número médio de quartos (Fator positivo mais forte)
   2. **ZN (+0.36):** Proporção de terrenos residenciais zoneados
   3. **B (+0.33):** Proporção de negros por cidade
   4. **DIS (+0.25):** Distância ponderada aos centros de emprego
   5. **CHAS (+0.18):** Limita com rio Charles (binária)
   
   **Top 5 Correlações Negativas com MEDV:**
   
   1. **LSTAT (-0.74):** % de população de baixa renda (Fator negativo mais forte)
   2. **PTRATIO (-0.51):** Razão aluno-professor por cidade
   3. **INDUS (-0.48):** Proporção de acres comerciais não-varejo
   4. **TAX (-0.47):** Taxa de imposto sobre propriedade
   5. **NOX (-0.43):** Concentração de óxidos de nitrogênio

3. **Manter a seção "Interpretação do Mapa de Correlação"** (cores vermelho/azul/branco)

4. **Adicionar um insight adicional** (opcional, se houver espaço):
   - "**Insight:** As correlações mais fortes (RM e LSTAT) explicam a maior parte da variância do preço. Features socioeconômicas (LSTAT, PTRATIO, INDUS) têm impacto negativo consistente."

5. **Manter o "Ponto de Atenção"** sobre escassez de dados

6. **Manter a indicação da imagem** da matriz de correlação

## Dados Corretos para Referência

**Top 5 Positivas (ordem decrescente):**
- RM: +0.70
- ZN: +0.36
- B: +0.33
- DIS: +0.25
- CHAS: +0.18

**Top 5 Negativas (ordem crescente, mais negativas primeiro):**
- LSTAT: -0.74
- PTRATIO: -0.51
- INDUS: -0.48
- TAX: -0.47
- NOX: -0.43

## Instrução Final

- Manter todo o layout visual, cores e estilo inalterados
- Preservar a legenda completa das features (já está boa)
- A seção de correlações pode ser apresentada em duas colunas (Top 5 Positivas à esquerda, Top 5 Negativas à direita) ou em lista vertical
- O objetivo é tornar o slide mais informativo sem sobrecarregar visualmente
- Manter a imagem da matriz de correlação no final

---

**Fim das Instruções**

