# Formulário Mentoria NextGen — Paula

Formulário Streamlit pra mentoria da Paula no Programa NextGen 2ª Edição, com identidade visual da marca.

## O que tem aqui

- `app.py` — código do formulário com 8 perguntas (4 blocos)
- `requirements.txt` — dependências
- `.streamlit/config.toml` — paleta visual NextGen (roxos)

## Como rodar localmente (pra testar antes de publicar)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abre em `http://localhost:8501`.

## Como publicar no Streamlit Community Cloud (grátis)

### Passo 1 — Criar repositório no GitHub

1. Vai em https://github.com/new
2. Nome sugerido: `nextgen-mentoria-paula`
3. Marca como **público** (necessário pro plano grátis do Streamlit)
4. Cria

### Passo 2 — Subir os arquivos

Pode fazer via interface web do GitHub:
1. No repositório novo, clica em **"uploading an existing file"**
2. Arrasta `app.py`, `requirements.txt` e a pasta `.streamlit` inteira
3. Commit

### Passo 3 — Publicar no Streamlit

1. Vai em https://share.streamlit.io
2. Faz login com sua conta do GitHub
3. Clica em **"New app"**
4. Seleciona o repositório `nextgen-mentoria-paula`
5. Main file path: `app.py`
6. Clica em **Deploy**

Em ~2 minutos sua app está no ar com um link tipo:
`https://nextgen-mentoria-paula.streamlit.app`

Esse é o link que você manda pra Paula.

## Como ver as respostas (modo admin)

Depois que a Paula responder, você acessa as respostas dela adicionando `?admin=elaine` no final do link:

```
https://nextgen-mentoria-paula.streamlit.app/?admin=elaine
```

Você vai ver todas as respostas organizadas + botão pra baixar em JSON.

## Como duplicar pro Klayton

Quando for fazer o do Klayton:
1. Copia esse projeto inteiro pra uma nova pasta
2. Ajusta as perguntas no `app.py`
3. Cria novo repositório (ex.: `nextgen-mentoria-klayton`)
4. Publica do mesmo jeito

## Observação importante

As respostas ficam salvas num arquivo JSON dentro do servidor do Streamlit Cloud.
Por padrão, **apenas 1 resposta por formulário** (foi feito pra isso — cada um responde uma vez).
Se a Paula tentar abrir de novo depois de responder, vê uma tela de "já respondi".
