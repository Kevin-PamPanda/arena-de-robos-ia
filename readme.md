# 🤖 ARIA – Arena de Robôs IA  
**Simulador de batalhas automáticas entre robôs usando IA, FastAPI, React e Python.**

Este projeto foi desenvolvido por **Kevin Minervino** como parte dos meus estudos em:
- Programação  
- Desenvolvimento Web  
- APIs com Python (FastAPI)  
- Frontend moderno (React + Vite)  
- Arquitetura cliente-servidor  
- Deploy profissional com Render e Vercel  

O ARIA é um projeto educacional / de portfólio, criado com foco em aprendizado, boas práticas e exploração de lógica de IA para jogos.

---

## 🚀 Demonstração Online

### **Frontend (React – Vercel)**  
👉 https://arena-de-robos-ia.vercel.app

### **API Backend (FastAPI – Render)**  
👉 https://arena-de-robos-ia.onrender.com/docs

---

## 🎮 Sobre o Projeto

O ARIA é um jogo de batalha automática entre dois robôs em uma arena 2D.  
O jogador escolhe um robô inicial, dá comandos estratégicos e acompanha os turnos acontecendo automaticamente.  

A cada turno, o backend calcula:
- movimento
- esquiva
- ataque
- decisões da IA adversária
- logs da batalha

O frontend exibe:
- estado dos robôs
- arena em formato de grid
- HP, atributos e posições
- logs atualizados em tempo real

---

## 🧠 Tecnologias Usadas

### **Backend – FastAPI (Python)**
- FastAPI  
- Uvicorn  
- Pydantic  
- Arquitetura modular (`core/models.py`, `core/engine.py`)  
- Sistema de IA simples para comportamento do robô adversário  

### **Frontend – React (Vite)**
- React + Hooks  
- Atualização automática a cada 2 segundos via `setInterval`  
- UI responsiva  
- Grid visual da arena  
- Deploy na Vercel  

### **Deploy**
- **API:** Render  
- **Frontend:** Vercel  

---

## 🏗️ Arquitetura do Sistema

Frontend (Vercel)
|
| -> Requisições REST (fetch)
|
Backend (FastAPI - Render)
|
| -> Engine de batalha (core/engine.py)
|
Arena e Robôs (core/models.py)

Frontend (Vercel)
|
| -> Requisições REST (fetch)
|
Backend (FastAPI - Render)
|
| -> Engine de batalha (core/engine.py)
|
Arena e Robôs (core/models.py)


O frontend envia comandos para a API, que processa a lógica da batalha e retorna o estado atualizado para ser exibido na interface.

---

## 🔧 Como rodar localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/Kevin-PamPanda/arena-de-robos-ia.git
cd arena-de-robos-ia

2. Criar ambiente virtual

python -m venv .venv

3. Instalar dependências

pip install -r requirements.txt

4. Rodar o backend

uvicorn api.main:app --reload
Acesse:
👉 http://127.0.0.1:8000/docs

5. Rodar o frontend

cd frontend
npm install
npm run dev
Acesse:
👉 http://localhost:5173

📝 Status do Projeto

✔ Batalha automática funcionando

✔ Turnos executados automaticamente

✔ Arena visual

✔ Logs em tempo real

✔ Deploy completo (API + Frontend)

⏳ Próximo passo: Modo Campanha Web

⏳ Futuro: Melhorias visuais e animações

👤 Autor

Kevin de Freitas Minervino
Desenvolvedor iniciante explorando IA, Python, automação e criação de jogos.
GitHub: https://github.com/Kevin-PamPanda
LinkedIn: https://www.linkedin.com/in/kevin-de-freitras-minervino-5480b931b/

⚠️ Aviso

Este projeto é 100% educacional, criado com o objetivo de estudo e composição de portfólio.
Não possui fins comerciais.

🧡 Agradecimentos

As minhas filhas que testaram cada etapa e gostam!

Projeto desenvolvido com suporte do ChatGPT, explorando conceitos de IA aplicada a jogos, backend e frontend modernos.

11/12/2025