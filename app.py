import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import json

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Mentoria NextGen — Klayton",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# IDENTIDADE VISUAL
# ============================================================
st.markdown("""
<style>
    /* ===== BASE ===== */
    .stApp {
        background: linear-gradient(180deg, #faf9fc 0%, #f3eefa 100%);
    }
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 820px !important;
    }
    #MainMenu, footer, header { visibility: hidden; }

    /* ===== HEADER PRINCIPAL ===== */
    .nextgen-header {
        background: linear-gradient(135deg, #4A2D85 0%, #5D3A9B 40%, #8B5FBF 100%);
        padding: 48px 40px;
        border-radius: 24px;
        margin-bottom: 32px;
        box-shadow: 0 12px 40px rgba(93, 58, 155, 0.20);
        position: relative;
        overflow: hidden;
    }
    .nextgen-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 60%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, transparent 70%);
    }
    .nextgen-brand {
        color: rgba(255,255,255,0.85);
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 12px;
        position: relative;
    }
    .nextgen-title {
        color: white;
        font-size: 32px;
        font-weight: 700;
        margin: 0 0 14px 0;
        line-height: 1.15;
        position: relative;
        letter-spacing: -0.5px;
    }
    .nextgen-subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 16px;
        line-height: 1.65;
        margin: 0;
        position: relative;
        max-width: 600px;
    }

    /* ===== BARRA DE PROGRESSO ===== */
    .progress-container {
        background: white;
        padding: 16px 24px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 2px 12px rgba(93, 58, 155, 0.06);
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .progress-text {
        color: #5D3A9B;
        font-size: 13px;
        font-weight: 600;
        white-space: nowrap;
    }
    .progress-bar-bg {
        flex: 1;
        height: 8px;
        background: #f0e8f9;
        border-radius: 20px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #5D3A9B 0%, #B47FE0 100%);
        border-radius: 20px;
        transition: width 0.5s ease;
    }

    /* ===== INTRODUÇÃO ===== */
    .intro-card {
        background: white;
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 32px;
        border-left: 5px solid #8B5FBF;
        box-shadow: 0 4px 20px rgba(93, 58, 155, 0.08);
    }
    .intro-card p {
        color: #3a3a38;
        font-size: 15px;
        line-height: 1.75;
        margin: 0 0 12px 0;
    }
    .intro-card p:last-child { margin-bottom: 0; }
    .intro-card strong { color: #5D3A9B; }

    /* ===== FAIXA DE BLOCO ===== */
    .block-strip {
        background: linear-gradient(135deg, #5D3A9B 0%, #8B5FBF 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 16px;
        margin: 40px 0 8px 0;
        box-shadow: 0 6px 24px rgba(93, 58, 155, 0.15);
        position: relative;
        overflow: hidden;
    }
    .block-strip::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 200px;
        height: 100%;
        background: radial-gradient(circle at right, rgba(255,255,255,0.15) 0%, transparent 70%);
    }
    .block-strip-label {
        color: rgba(255,255,255,0.85);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
        position: relative;
    }
    .block-strip-title {
        color: white;
        font-size: 22px;
        font-weight: 700;
        margin: 0 0 8px 0;
        position: relative;
        letter-spacing: -0.3px;
    }
    .block-strip-desc {
        color: rgba(255,255,255,0.92);
        font-size: 14px;
        line-height: 1.65;
        margin: 0;
        position: relative;
        max-width: 95%;
    }

    /* ===== CARD VISUAL VIA STREAMLIT CONTAINER ===== */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: white !important;
        border-radius: 18px !important;
        padding: 20px 28px !important;
        margin: 16px 0 !important;
        box-shadow: 0 4px 20px rgba(93, 58, 155, 0.07) !important;
        border: 1px solid #f0e8f9 !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 8px 28px rgba(93, 58, 155, 0.12) !important;
    }

    /* ===== TÍTULO DA PERGUNTA ===== */
    .pergunta-titulo {
        color: #2c2c2a;
        font-size: 18px;
        font-weight: 600;
        line-height: 1.5;
        margin: 0 0 18px 0;
        letter-spacing: -0.2px;
    }
    .pergunta-titulo .sub {
        font-weight: 400;
        font-size: 14px;
        color: #5F5E5A;
    }

    /* ===== RADIO E CHECKBOX — TEXTOS BEM VISÍVEIS ===== */
    div[data-testid="stRadio"] > div {
        background: transparent !important;
        padding: 0 !important;
        border: none !important;
        gap: 6px !important;
    }
    div[data-testid="stRadio"] label p {
        font-size: 15px !important;
        color: #2c2c2a !important;
        margin: 0 !important;
    }
    div[data-testid="stRadio"] label {
        padding: 12px 16px !important;
        background: #faf9fc !important;
        border-radius: 12px !important;
        border: 1.5px solid transparent !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: #f0e8f9 !important;
        border-color: #d4c3e8 !important;
    }

    div[data-testid="stCheckbox"] {
        background: #faf9fc !important;
        padding: 12px 16px !important;
        border-radius: 12px !important;
        margin: 6px 0 !important;
        border: 1.5px solid transparent !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stCheckbox"]:hover {
        background: #f0e8f9 !important;
        border-color: #d4c3e8 !important;
    }
    div[data-testid="stCheckbox"] label p {
        font-size: 15px !important;
        color: #2c2c2a !important;
        margin: 0 !important;
    }

    /* ===== TEXTAREA ===== */
    .stTextArea textarea {
        background: #faf9fc !important;
        border: 1.5px solid #E8DDF5 !important;
        border-radius: 14px !important;
        padding: 16px !important;
        font-size: 15px !important;
        font-family: inherit !important;
        line-height: 1.6 !important;
        color: #2c2c2a !important;
    }
    .stTextArea textarea:focus {
        border-color: #8B5FBF !important;
        box-shadow: 0 0 0 4px rgba(139, 95, 191, 0.12) !important;
        background: white !important;
    }

    /* ===== TEXT INPUT ===== */
    .stTextInput input {
        background: white !important;
        border: 1.5px solid #d4c3e8 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        color: #2c2c2a !important;
    }
    .stTextInput input:focus {
        border-color: #8B5FBF !important;
        box-shadow: 0 0 0 4px rgba(139, 95, 191, 0.12) !important;
    }
    .stTextInput label p {
        font-size: 13px !important;
        color: #5D3A9B !important;
        font-weight: 600 !important;
    }

    /* ===== BOTÃO ENVIAR ===== */
    .stButton button {
        background: linear-gradient(135deg, #4A2D85 0%, #5D3A9B 50%, #8B5FBF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 18px 32px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100% !important;
        margin-top: 32px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 24px rgba(93, 58, 155, 0.3) !important;
        letter-spacing: 0.3px !important;
    }
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 32px rgba(93, 58, 155, 0.4) !important;
    }

    /* ===== SUCESSO ===== */
    .success-card {
        background: linear-gradient(135deg, #4A2D85 0%, #5D3A9B 40%, #8B5FBF 100%);
        color: white;
        padding: 56px 40px;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 12px 40px rgba(93, 58, 155, 0.25);
        position: relative;
        overflow: hidden;
    }
    .success-card::before {
        content: '';
        position: absolute;
        top: -30%;
        right: -10%;
        width: 50%;
        height: 160%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
    }
    .success-card h2 {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin: 20px 0 14px 0;
        position: relative;
    }
    .success-card p {
        color: rgba(255,255,255,0.95);
        font-size: 16px;
        line-height: 1.65;
        margin: 0 0 10px 0;
        position: relative;
    }
    .success-check {
        width: 72px;
        height: 72px;
        border-radius: 50%;
        background: rgba(255,255,255,0.22);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 38px;
        color: white;
        position: relative;
    }

    /* ===== TEMA/FORMATO COM DESCRIÇÃO ===== */
    .opcao-titulo {
        font-size: 15px;
        font-weight: 600;
        color: #2c2c2a;
        margin: 0;
        line-height: 1.4;
    }
    .opcao-desc {
        font-size: 13px;
        color: #5F5E5A;
        line-height: 1.55;
        margin: 4px 0 0 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# ARMAZENAMENTO
# ============================================================
RESPOSTAS_DIR = Path("respostas")
RESPOSTAS_DIR.mkdir(exist_ok=True)
ARQUIVO_RESPOSTAS = RESPOSTAS_DIR / "klayton_respostas.json"

def salvar_resposta(dados):
    payload = {
        "respondido_em": datetime.now().isoformat(),
        "respostas": dados
    }
    with open(ARQUIVO_RESPOSTAS, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def ja_respondeu():
    return ARQUIVO_RESPOSTAS.exists()

# ============================================================
# MODOS
# ============================================================
query_params = st.query_params
modo_admin = query_params.get("admin") == "elaine"
modo_preview = query_params.get("preview") == "true"

# ----- MODO ADMIN -----
if modo_admin:
    st.markdown("""
    <div class="nextgen-header">
        <div class="nextgen-brand">Modo Administrador</div>
        <h1 class="nextgen-title">Respostas — Klayton</h1>
    </div>
    """, unsafe_allow_html=True)

    if ja_respondeu():
        with open(ARQUIVO_RESPOSTAS, "r", encoding="utf-8") as f:
            dados = json.load(f)

        data_formatada = datetime.fromisoformat(dados["respondido_em"]).strftime("%d/%m/%Y às %H:%M")
        st.markdown(f"**Respondido em {data_formatada}**")
        st.markdown("---")

        for pergunta, resposta in dados["respostas"].items():
            st.markdown(f"**{pergunta}**")
            if isinstance(resposta, list):
                if len(resposta) == 0:
                    st.markdown("_(não respondido)_")
                else:
                    for item in resposta:
                        st.markdown(f"- {item}")
            else:
                if not resposta:
                    st.markdown("_(em branco)_")
                else:
                    st.markdown(f"{resposta}")
            st.markdown("")

        st.download_button(
            label="⬇ Baixar respostas (JSON)",
            data=json.dumps(dados, ensure_ascii=False, indent=2),
            file_name=f"klayton_respostas_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

        st.markdown("---")
        st.markdown("##### Limpar resposta (pra resetar antes de enviar pro Klayton)")
        if st.button("🗑 Apagar resposta atual"):
            ARQUIVO_RESPOSTAS.unlink()
            st.success("Resposta apagada. Formulário pronto pra ser respondido de novo.")
            st.rerun()
    else:
        st.info("Nenhuma resposta recebida ainda.")
    st.stop()

# ----- MODO RESPONDIDO -----
if ja_respondeu() and not modo_preview:
    st.markdown("""
    <div class="success-card">
        <div class="success-check">✓</div>
        <h2>Você já respondeu!</h2>
        <p>Valeu, Klayton. Vou ler com calma e a gente conversa no nosso próximo encontro.</p>
        <p style="margin-top: 20px; opacity: 0.85; font-size: 14px;">— Elaine</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============================================================
# HEADER E INTRODUÇÃO
# ============================================================
st.markdown("""
<div class="nextgen-header">
    <div class="nextgen-brand">Programa NextGen — 2ª Edição</div>
    <h1 class="nextgen-title">Pra a gente se aprofundar</h1>
    <p class="nextgen-subtitle">
        Klayton, esse formulário não é pesquisa de RH. É uma conversa por escrito,
        pra eu te apoiar melhor nos próximos meses da mentoria.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="intro-card">
    <p>Você manda bem em IA pra desenvolver — ChatGPT, Claude, Gemini. Então não é por aí que eu vou te ajudar; isso você já domina.</p>
    <p><strong>Importante, pra gente já começar alinhado:</strong> eu não vou te ajudar a programar — não é minha praia, e você não precisa de mim pra isso. O que eu trago é o que fica em volta do código: como você organiza, documenta, apresenta e faz o que cria ser reconhecido. É aí que eu somo.</p>
    <p>Quase tudo aqui é só marcar opção — pra não tomar muito seu tempo. Tem 1 pergunta escrita só no final. Cada pergunta veio do que você me contou no nosso primeiro encontro, no dia 13/05.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# PROGRESSO
# ============================================================
def contar_progresso():
    total = 7
    respondidas = 0

    # Q1 radio
    if st.session_state.get("q1_radio") is not None:
        if st.session_state.get("q1_radio") != "Outro" or st.session_state.get("q1_outro", "").strip():
            respondidas += 1

    # Q2 checkbox
    opcoes_q2_list = ["Mergulho sozinho até sair", "Jogo na IA pra destravar",
        "Testo direto e vejo o que acontece", "Chamo alguém da equipe pra pensar junto",
        "Paro e vou fazer outra coisa"]
    if any(st.session_state.get(f"q2_{op}", False) for op in opcoes_q2_list) or \
       (st.session_state.get("q2_outro_check") and st.session_state.get("q2_outro_text", "").strip()):
        respondidas += 1

    # Q3 checkbox
    opcoes_q3_list = ["Explicar de novo algo que já resolvi antes", "Parar o que estou fazendo no meio",
        "Gosto, me energiza ajudar", "Sinto que vira só comigo, não fica registrado"]
    if any(st.session_state.get(f"q3_{op}", False) for op in opcoes_q3_list) or \
       (st.session_state.get("q3_outro_check") and st.session_state.get("q3_outro_text", "").strip()):
        respondidas += 1

    # Q4 checkbox
    opcoes_q4_list = ["Criar uma ferramenta do zero", "Ver alguém usando algo que eu fiz",
        "Resolver um problema difícil", "Ajudar um colega a destravar",
        "Aprender uma tecnologia nova", "Ter autonomia pra fazer do meu jeito"]
    if any(st.session_state.get(f"q4_{op}", False) for op in opcoes_q4_list) or \
       (st.session_state.get("q4_outro_check") and st.session_state.get("q4_outro_text", "").strip()):
        respondidas += 1

    # Q5 checkbox (temas)
    temas_lista = ["Fazer minhas ferramentas chegarem mais longe na TBC",
        "Ter um jeito de validar antes de subir pro cliente",
        "Registrar o que descubro pra não ficar só na minha cabeça",
        "Explicar o valor do que faço pra quem não é técnico",
        "Estruturar uma ideia minha pra ela ser levada a sério"]
    if any(st.session_state.get(f"tema_{t}", False) for t in temas_lista) or \
       (st.session_state.get("q5_outro_check") and st.session_state.get("q5_outro_text", "").strip()):
        respondidas += 1

    # Q6 checkbox (formatos)
    formatos_lista = ["Pegar uma ferramenta real sua e trabalhar em cima dela",
        "Eu penso em voz alta e a gente constrói um material junto",
        "Estudo de caso concreto", "Conversa direta sobre um problema específico",
        "Eu te observo numa entrega real e te dou retorno",
        "Você me observa em algo meu e conversamos depois"]
    if any(st.session_state.get(f"formato_{f}", False) for f in formatos_lista):
        respondidas += 1

    # Q7 escrita
    if st.session_state.get("q7", "").strip():
        respondidas += 1

    return respondidas, total

respondidas, total = contar_progresso()
porcentagem = int((respondidas / total) * 100)
st.markdown(f"""
<div class="progress-container">
    <div class="progress-text">{respondidas} de {total} respondidas</div>
    <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="width: {porcentagem}%;"></div>
    </div>
    <div class="progress-text">{porcentagem}%</div>
</div>
""", unsafe_allow_html=True)

respostas = {}

# ============================================================
# BLOCO 1
# ============================================================
st.markdown("""
<div class="block-strip">
    <div class="block-strip-label">Bloco 1 — Como você trabalha</div>
    <h2 class="block-strip-title">Do jeito que as coisas acontecem</h2>
    <p class="block-strip-desc">Algumas perguntas curtas a partir do que você me contou. Sem certo ou errado — é pra eu entender como você funciona.</p>
</div>
""", unsafe_allow_html=True)

# Q1
with st.container(border=True):
    st.markdown('<p class="pergunta-titulo">Você me contou que às vezes vai direto na DEV do cliente — "melhor feito que mal feito". Quando você faz isso, o que mais pesa na decisão?</p>', unsafe_allow_html=True)
    q1_texto = 'Você me contou que às vezes vai direto na DEV do cliente — "melhor feito que mal feito". Quando você faz isso, o que mais pesa na decisão?'
    opcoes_q1 = ["A pressa de resolver logo", "Confiança de que vai dar certo",
                 "Não ter um ambiente meu pra testar antes", "Prefiro ver quebrar e corrigir na hora", "Outro"]
    escolha_q1 = st.radio("Q1", opcoes_q1, index=None, key="q1_radio", label_visibility="collapsed")
    if escolha_q1 == "Outro":
        outro_q1 = st.text_input("Conta aqui o que é:", key="q1_outro", placeholder="Escreva sua resposta...")
        respostas[q1_texto] = f"Outro: {outro_q1}" if outro_q1 else "Outro"
    elif escolha_q1:
        respostas[q1_texto] = escolha_q1

# Q2
with st.container(border=True):
    st.markdown('<p class="pergunta-titulo">Quando um problema técnico trava e não destrava fácil, o que você faz primeiro? <span class="sub">(marque o que mais acontece)</span></p>', unsafe_allow_html=True)
    q2_texto = "Quando um problema técnico trava e não destrava fácil, o que você faz primeiro? (marque o que mais acontece)"
    opcoes_q2 = ["Mergulho sozinho até sair", "Jogo na IA pra destravar",
                 "Testo direto e vejo o que acontece", "Chamo alguém da equipe pra pensar junto",
                 "Paro e vou fazer outra coisa"]
    selecionados_q2 = []
    for opcao in opcoes_q2:
        if st.checkbox(opcao, key=f"q2_{opcao}"):
            selecionados_q2.append(opcao)
    if st.checkbox("Outro", key="q2_outro_check"):
        outro_q2 = st.text_input("Conta aqui o que é:", key="q2_outro_text", placeholder="Escreva sua resposta...")
        selecionados_q2.append(f"Outro: {outro_q2}" if outro_q2 else "Outro")
    respostas[q2_texto] = selecionados_q2

# Q3
with st.container(border=True):
    st.markdown('<p class="pergunta-titulo">Você é referência pra equipe no SCC — ajuda os consultores e os colegas. Quando te procuram, o que mais te pega? <span class="sub">(pode marcar mais de uma)</span></p>', unsafe_allow_html=True)
    q3_texto = "Você é referência pra equipe no SCC — ajuda os consultores e os colegas. Quando te procuram, o que mais te pega? (pode marcar mais de uma)"
    opcoes_q3 = ["Explicar de novo algo que já resolvi antes", "Parar o que estou fazendo no meio",
                 "Gosto, me energiza ajudar", "Sinto que vira só comigo, não fica registrado"]
    selecionados_q3 = []
    for opcao in opcoes_q3:
        if st.checkbox(opcao, key=f"q3_{opcao}"):
            selecionados_q3.append(opcao)
    if st.checkbox("Outro", key="q3_outro_check"):
        outro_q3 = st.text_input("Conta aqui o que é:", key="q3_outro_text", placeholder="Escreva sua resposta...")
        selecionados_q3.append(f"Outro: {outro_q3}" if outro_q3 else "Outro")
    respostas[q3_texto] = selecionados_q3

# ============================================================
# BLOCO 2
# ============================================================
st.markdown("""
<div class="block-strip">
    <div class="block-strip-label">Bloco 2 — Onde a gente vai</div>
    <h2 class="block-strip-title">O que faria diferença pra você</h2>
    <p class="block-strip-desc">Você já cria ferramentas e leva pra TBC. O que eu trago aqui é o que fica em volta disso — apresentar, documentar, dar visibilidade. Marca o que mais faz sentido pra gente trabalhar. Pode marcar quantos quiser.</p>
</div>
""", unsafe_allow_html=True)

# Q4
with st.container(border=True):
    st.markdown('<p class="pergunta-titulo">O que mais te dá energia no trabalho hoje? <span class="sub">(marca quantas quiser)</span></p>', unsafe_allow_html=True)
    q4_texto = "O que mais te dá energia no trabalho hoje? (marca quantas quiser)"
    opcoes_q4 = ["Criar uma ferramenta do zero", "Ver alguém usando algo que eu fiz",
                 "Resolver um problema difícil", "Ajudar um colega a destravar",
                 "Aprender uma tecnologia nova", "Ter autonomia pra fazer do meu jeito"]
    selecionados_q4 = []
    for opcao in opcoes_q4:
        if st.checkbox(opcao, key=f"q4_{opcao}"):
            selecionados_q4.append(opcao)
    if st.checkbox("Outro", key="q4_outro_check"):
        outro_q4 = st.text_input("Conta aqui o que é:", key="q4_outro_text", placeholder="Escreva sua resposta...")
        selecionados_q4.append(f"Outro: {outro_q4}" if outro_q4 else "Outro")
    respostas[q4_texto] = selecionados_q4

# Q5 (temas)
with st.container(border=True):
    st.markdown('<p class="pergunta-titulo">Você falou que cria ferramentas e leva pra TBC, e que quer construir uma API de comunicação dentro do Winthor. Pensando nisso, o que faria mais diferença pra você nos próximos meses? <span class="sub">(marca quantos quiser)</span></p>', unsafe_allow_html=True)
    q5_texto = "Você falou que cria ferramentas e leva pra TBC, e que quer construir uma API de comunicação dentro do Winthor. Pensando nisso, o que faria mais diferença pra você nos próximos meses? (marca quantos quiser)"
    temas = [
        ("Fazer minhas ferramentas chegarem mais longe na TBC", "Não programar junto — mas construir a forma de apresentar o valor delas pra quem decide."),
        ("Ter um jeito de validar antes de subir pro cliente", "Um ritual seu de checagem — processo, não código."),
        ("Registrar o que descubro pra não ficar só na minha cabeça", "Um jeito leve de documentar o que você resolve. Terreno de processo, não de desenvolvimento."),
        ("Explicar o valor do que faço pra quem não é técnico", "Traduzir a entrega técnica em impacto que gestor e cliente entendem."),
        ("Estruturar uma ideia minha pra ela ser levada a sério", "Organizar a narrativa e a apresentação do projeto — não o desenvolvimento técnico dele.")
    ]
    selecionados_q5 = []
    for tema, descricao in temas:
        label_completa = f"**{tema}**  \n_{descricao}_"
        if st.checkbox(label_completa, key=f"tema_{tema}"):
            selecionados_q5.append(tema)
    if st.checkbox("**Outro que eu deveria ter colocado e não coloquei**", key="q5_outro_check"):
        outro_q5 = st.text_input("Conta aqui o que é:", key="q5_outro_text", placeholder="Escreva...")
        selecionados_q5.append(f"Outro: {outro_q5}" if outro_q5 else "Outro")
    respostas[q5_texto] = selecionados_q5

# ============================================================
# BLOCO 3
# ============================================================
st.markdown("""
<div class="block-strip">
    <div class="block-strip-label">Bloco 3 — Como a gente vai</div>
    <h2 class="block-strip-title">Formato dos encontros</h2>
    <p class="block-strip-desc">Pensa em como VOCÊ troca melhor. Cada um tem um jeito. Quais formatos funcionam pra você (sugiro marcar 2 ou 3):</p>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<p class="pergunta-titulo">Formatos de encontro que funcionam pra você:</p>', unsafe_allow_html=True)
    q6_texto = "Formatos de encontro que funcionam pra você:"
    formatos = [
        ("Pegar uma ferramenta real sua e trabalhar em cima dela", "Você traz algo que criou e a gente trabalha em cima — concreto, não teórico."),
        ("Eu penso em voz alta e a gente constrói um material junto", "Ex: como documentar algo, como apresentar uma ferramenta. Material de comunicação, não código."),
        ("Estudo de caso concreto", "A gente pega uma situação real e destrincha junto."),
        ("Conversa direta sobre um problema específico", "Você chega com um problema pontual e a gente foca nele."),
        ("Eu te observo numa entrega real e te dou retorno", "Acompanho você numa entrega sua e dou devolutiva depois."),
        ("Você me observa em algo meu e conversamos depois", "Você me vê numa situação real minha (apresentação, reunião) e conversamos.")
    ]
    selecionados_q6 = []
    for formato, descricao in formatos:
        label_completa = f"**{formato}**  \n_{descricao}_"
        if st.checkbox(label_completa, key=f"formato_{formato}"):
            selecionados_q6.append(formato)
    respostas[q6_texto] = selecionados_q6

# ============================================================
# BLOCO 4
# ============================================================
st.markdown("""
<div class="block-strip">
    <div class="block-strip-label">Bloco 4 — Pra fechar</div>
    <h2 class="block-strip-title">Uma coisa só, no seu terreno</h2>
    <p class="block-strip-desc">A última. Pode ser curto e direto.</p>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<p class="pergunta-titulo">Me descreve em 2-3 linhas uma ferramenta que você criou e levou pra TBC. O que ela resolve, e quem usa?</p>', unsafe_allow_html=True)
    q7_texto = "Me descreve em 2-3 linhas uma ferramenta que você criou e levou pra TBC. O que ela resolve, e quem usa?"
    respostas[q7_texto] = st.text_area("Q7", placeholder="Pode ser direto. O nome dela, o que faz, e quem usa no dia a dia.",
                                       height=110, key="q7", label_visibility="collapsed")

# ============================================================
# BOTÃO
# ============================================================
if st.button("Enviar respostas pra Elaine"):
    salvar_resposta(respostas)
    st.rerun()
