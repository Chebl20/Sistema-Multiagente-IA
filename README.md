# 🌱 Sistema Multiagente de IA

**Atividade de Inteligência Artificial - Sistemas de Informação - 2025.01**  
**Projeto: Sistema Multiagente com 3 Agentes**

OBS.: Por favor cada equipe mexa apenas no seu próprio agente e faça seu pull request quando necessário.
---

## 🧠 Descrição do Ambiente

- O ambiente contém **20 plantas**.
- Cada planta possui dois **índices principais**:
  - **Umidade**
  - **Amadurecimento**
- As plantas devem ser **monitoradas**, **mantidas** e **colhidas**.
- As plantas possuem **fatores diferentes de perda de umidade** e **velocidade de crescimento**.
- Se uma planta chegar a **0% de umidade** ou permanecer por **muito tempo totalmente madura**, ela **morre**.

---

## 🎯 Objetivo Geral

- **Coletar o máximo de plantas possíveis**.
- **Minimizar a perda de plantas** por falta de cuidado ou colheita tardia.

---

## 🤖 Agentes do Sistema

### 🌧️ Agente IRRIGADOR → *Equipe ?*
**Objetivo:** Manter as plantas com umidade adequada para garantir seu crescimento saudável.  
**Funções:**  
- Identificar plantas com umidade baixa.  
- Irrigar seletivamente com base na prioridade.

---

### 🌾 Agente COLHEDOR → *Equipe ?*
**Objetivo:** Identificar e colher as plantas que atingiram total maturidade.  
**Funções:**  
- Monitorar o índice de amadurecimento.  
- Colher a planta antes de ela morrer por excesso de maturidade.

---

### 🧪 Agente SENSOR → *Equipe ?*
**Objetivo:** Monitorar e analisar os índices de umidade e amadurecimento de cada planta, compartilhando os dados com os demais agentes.  
**Funções:**  
- Observar periodicamente os valores das plantas.  
- Atualizar um painel ou memória compartilhada com os dados das plantas.
