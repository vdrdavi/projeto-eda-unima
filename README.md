# Documento de Requisitos de Produto (PRD)

---

## 1. Especificações do projeto

| Item | Detalhe |
|------|---------|
| **Participantes** | Davi Vasconcelos  <br>Danilo Lima  <br>Emylle Rayssa |
| **Status** | Levantamento de requisitos em andamento |
| **Lançamento alvo** | Junho / 2025 – versão final jogável submetida no repositório público |

---

## 2. Metas da equipe e objetivos de negócio

* **Meta acadêmica:** demonstrar domínio de **estruturas de dados avançadas**
* **Meta de usabilidade:** interface intuitiva e acessível, garantindo uma experiência fluida para os jogadores
* **Meta de qualidade:** estabilidade sem bugs críticos na entrega; código revisado e validado por todos os integrantes do grupo

---

## 3. Contexto e enquadramento estratégico

O jogo é o projeto final da disciplina **Estrutura de Dados Avançada**. Utilizar árvores geradas proceduralmente e um inventário com número limitado de slots promove a aplicação prática dos conceitos estudados em aula, além de gerar um artefato tangível para portfólio.

---

## 4. Suposições

| #  | Suposição                                                                                                                                                                             | Como validar                                                                                   |
| -- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| S1 | O público-alvo jogará em desktop usando teclado (WASD ou setas) como método principal de entrada.                                                                                     | Sessões de teste com usuários-alvo na Sprint 2; coletar feedback sobre controles alternativos. |
| S2 | O jogo manterá um desempenho fluido e estável nas condições de uso esperadas pelos membros da equipe.                                                                                 | Testes práticos de jogabilidade em diferentes máquinas durante a Sprint 1.                     |
| S3 | Todos os elementos de interface necessários (grade de inventário, menus básicos) podem ser implementados exclusivamente com recursos nativos do **Pygame**, sem bibliotecas externas. | Prova de conceito rápida na Sprint 1 para montar a grade e abrir/fechar o inventário.          |


---

## 5. Histórias de usuário (vinculadas às issues)

| ID | História | Critérios de aceite | Issue |
|----|----------|--------------------|-------|
| US‑01 | *Como jogador,* quero mover meu personagem com WASD/setas para explorar o mapa | Delay de input ≤ 100 ms; colisão com paredes | #2 |
| US‑02 | *Como jogador,* quero coletar itens ao tocar neles para progredir | Item some do mundo e aparece no inventário | #3 |
| US‑03 | *Como jogador,* quero ver meus itens em um inventário em grade para gerenciar recursos | Abre com **E**; impede coleta se cheio | #4 |
| US‑04 | *Como jogador,* quero um mapa coerente de áreas interligadas para sentir exploração | Algoritmo gera ≥ 10 nós conectados | #5 |
| US‑05 | *Como jogador,* preciso de feedback visual/sonoro ao coletar itens para perceber ação | SFX + animação em ≤ 0,3 s | #7, #8 |
| US‑06 | *Como desenvolvedor,* quero publicar o jogo como executável para facilitar avaliação | Binário + README de execução | #1 |

---

## 6. Interação do usuário e design

- **Visão 2D top‑down** simples (Pygame).
- **UI**: barra de status (HP, itens) + inventário modal em grade (4 × 4).
- **Feedbacks**:
  - Visual: flash no item + fade‑out.
  - Sonoro: *pickup.wav* curto, volume -6 dB.
- **Layout de teclado**: WASD / setas, **E** (inventário), **Esc** (pause).

---

## 7. Perguntas em aberto

| P  | Questão                                                                                 | Deadline          |
| -- | --------------------------------------------------------------------------------------- | ----------------- |
| P1 | Limite ideal de slots do inventário? 12 ou 16?                                          | Sprint 2 planning |
| P2 | Quais efeitos visuais mínimos são necessários para tornar a coleta perceptível e clara? | Sprint 2          |
| P3 | Precisamos de um objetivo final definido (ex: coletar tudo ou chegar a um destino)?     | Sprint 3 planning |
| P4 | Qual será a estratégia de balanceamento entre desafio e acessibilidade para jogadores?  | Sprint 3          |

---

## 8. Fora de escopo (por ora)

- Multiplayer ou rede.  
- Salvar/Carregar progresso.  
- Suporte a mobile/joystick.  
- Efeitos de partículas avançados.

---

## Métricas de sucesso

1. **Experiência:** 80 % dos play‑testers finalizam em < 10 min.  
2. **Desempenho:** média > 60 FPS em máquina de referência.  
3. **Qualidade:** testes unitários ≥ 90 % cobertura; zero bugs “críticos” abertos na entrega.

---

### Próximos passos

1. Criar branches de desenvolvimento para cada funcionalidade principal (movimentação, coleta, inventário, etc.).
2. Implementar a movimentação do personagem e a geração do mapa com árvore (Sprint 1).
3. Testar o desempenho do jogo em diferentes máquinas da equipe.
4. Criar um layout simples para a interface (grade do inventário e HUD básica).
5. Validar o inventário com protótipo funcional e iniciar coleta de itens (Sprint 2).

---
