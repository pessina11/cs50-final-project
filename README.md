# Simulador de Finanças Pessoais

#### Video Demo: https://youtu.be/LhLmGeTtNs8

#### Descrição:

Este projeto é o trabalho final do curso **CS50x – Introduction to Computer Science**, da Universidade Harvard, e consiste em um **Simulador de Finanças Pessoais** desenvolvido com **Python (Flask)**, **SQLite**, e interface web usando **HTML, Jinja2, CSS (Bulma)** e **JavaScript (Chart.js)**.

---

## 🔍 Funcionalidades

- **Cadastro e login de usuários**, com validação de campos e armazenamento seguro das senhas (hash com `werkzeug.security`).
- **Adição de transações financeiras**, com categorias e tipos (receita ou despesa).
- **Histórico completo das transações** realizadas.
- **Relatório mensal agrupado por mês e categoria**, com totais de receitas e despesas.
- **Gráficos interativos (Chart.js)** para visualização clara das finanças.
- **Dashboard inicial** com resumo financeiro: saldo atual, total de receitas e total de despesas.
- Exportação de relatório financeiro no formato **CSV**.

---

## 🗂 Estrutura dos Arquivos

- `app.py` – Lógica principal da aplicação: rotas Flask, controle de sessões, autenticação, manipulação do banco de dados e renderização de páginas.
- `templates/` – Arquivos HTML com herança via Jinja2:
  - `layout.html` – Layout base de todas as páginas.
  - `register.html` – Página de cadastro.
  - `login.html` – Página de login.
  - `dashboard.html` – Painel inicial com resumo financeiro.
  - `add.html` – Formulário de nova transação.
  - `history.html` – Histórico completo de transações.
  - `report.html` – Relatório mensal com gráficos.
- `static/` – Estilos personalizados e bibliotecas externas (como Chart.js e Bulma).
- `finance.db` – Banco de dados SQLite com as tabelas `users` e `transactions`.

---

## 🧱 Banco de Dados

- `users`: guarda o ID, nome de usuário e hash da senha.
- `transactions`: armazena as transações financeiras dos usuários, com campos:
  - `id`, `user_id`, `type` (income/expense), `category`, `amount`, `date`.

---

## 💡 Decisões de Design

- Utilizei SQLite por simplicidade e portabilidade, sem necessidade de servidor de banco externo.
- A lógica de agrupamento de transações por mês e categoria foi feita via SQL e Python, separando receitas de despesas para facilitar a visualização e os gráficos.
- A interface foi construída com foco em clareza e praticidade, usando o framework Bulma CSS e ícones simples.
- Os gráficos foram feitos com Chart.js, para que os dados mensais possam ser visualizados dinamicamente.
- Ao adicionar o dashboard, o fluxo inicial do usuário após login se tornou mais intuitivo.

---

## 🚀 Como usar

1. Clone o repositório no ambiente CS50.
2. Certifique-se de ter ativado o ambiente virtual.
3. Execute `flask run` com `app.py` como ponto de entrada.
4. Acesse o navegador no endereço fornecido.
5. Cadastre um usuário, faça login e utilize todas as funções!

---

## 📦 Melhorias Futuras (caso o projeto evolua)

- Adicionar autenticação via e-mail com confirmação.
- Inserir limites de orçamento por categoria.
- Implementar metas financeiras e alertas automáticos.
- Adicionar suporte para múltiplas moedas.
- Criar interface mobile responsiva ou app.

---

Este projeto foi uma excelente oportunidade para aplicar os conhecimentos de lógica, Python, web development e banco de dados aprendidos durante o CS50.

