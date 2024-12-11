# AT - Desenvolvimento de Data-Driven Apps com Python

## Descrição e Objetivo

A aplicação visa entregar ao usuário as estatísticas e resumos de diversas partidas de futebol, além de permitir que o usuário faça consultas personalizadas a uma IA especializada.

## Exemplos de recursos disponíveis

- Visualizar resumos de partidas com diferentes tipos de narração
- Comparar jogadores de uma mesma partida
- Ver as estatísticas das partidas disponíveis
- Perguntar para uma IA mais detalhes da partida

## Utilização

A aplicação pode ser acessada diretamente em ambiente web quanto utilizá-la localmente:

### Ambiente web
Acesse: <Endereço da aplicação publicada>
Documentação da API: <Endereço Docs da api publicada>

### Ambiente local
1. Crie ou ative um ambiente Python no terminal
2. Instale as dependências no arquivo requirements.txt 
3. Inicie a API com o comando <uvicorn api.main:api --reload --port 8000>
4. Inicie a aplicação com o comando <streamlit run app\main.py>
5. Acesse a api no endereço <http://127.0.0.1:8000/>
6. Acesse a aplicação no endereço <http://localhost:8501/>

## Problemas conhecidos

- Erro exporádico de índice de liste "langchain\chains\base.py", line 516
- Erro exporádico em "langchain_community\utilities\google_finance.py", line 79