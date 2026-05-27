import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import json

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Mentoria NextGen — Paula",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# IDENTIDADE VISUAL — REDESIGN ELEGANTE
# ============================================================
st.markdown("""
<style>
    /* ===== BASE ===== */
    .stApp {
        background: linear-gradient(180deg, #faf9fc 0%, #f3eefa 100%);
    }

    /* Container principal mais largo */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 820px !important;
    }

    /* Esconde elementos padrão */
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
    .nextgen-header::after {
        content: '';
        position: absolute;
        bottom: -40%;
        left: -10%;
        width: 50%;
        height: 150%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
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

    /* ===== CARD DE INTRODUÇÃO ===== */
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

    /* ===== FAIXA DE BLOCO ===== */
    .block-strip {
        background: linear-gradient(135deg, #5D3A9B 0%, #8B5FBF 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 16px;
        margin: 48px 0 24px 0;
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
        color: rgba(255,255,255,0.8);
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
        max-width: 90%;
    }

    /* ===== CARD DE PERGUNTA ===== */
    .pergunta-card {
        background: white;
        border-radius: 18px;
        padding: 28px 32px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(93, 58, 155, 0.07);
        border: 1px solid #f0e8f9;
        transition: all 0.3s ease;
    }
    .pergunta-card:hover {
        box-shadow: 0 8px 28px rgba(93, 58, 155, 0.12);
        transform: translateY(-2px);
    }
    .pergunta-titulo {
        color: #2c2c2a;
        font-size: 18px !important;
        font-weight: 600 !important;
        line-height: 1.5;
        margin: 0 0 18px 0;
        letter-spacing: -0.2px;
    }
    .pergunta-sub {
        color: #5F5E5A;
        font-size: 13px;
        font-style: italic;
        margin: -10px 0 16px 0;
    }

    /* ===== OVERRIDE STREAMLIT — RADIO E CHECKBOX ===== */
    /* Esconde labels duplicados do Streamlit */
    div[data-testid="stRadio"] > label, 
    div[data-testid="stCheckbox"] > label {
        display: none !important;
    }

    /* Container dos radios sem o card branco extra */
    div[data-testid="stRadio"] > div {
        background: transparent !important;
        padding: 0 !important;
        border: none !important;
        gap: 4px !important;
    }

    /* Cada opção de radio */
    div[data-testid="stRadio"] label {
        padding: 14px 18px !important;
        background: #faf9fc !important;
        border-radius: 12px !important;
        margin: 4px 0 !important;
        border: 1.5px solid transparent !important;
        transition: all 0.2s ease !important;
        font-size: 15px !important;
        color: #2c2c2a !important;
        cursor: pointer !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: #f0e8f9 !important;
        border-color: #d4c3e8 !important;
    }

    /* Cada opção de checkbox */
    div[data-testid="stCheckbox"] {
        background: #faf9fc !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        margin: 6px 0 !important;
        border: 1.5px solid transparent !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stCheckbox"]:hover {
        background: #f0e8f9 !important;
        border-color: #d4c3e8 !important;
    }
    div[data-testid="stCheckbox"] label {
        font-size: 15px !important;
        color: #2c2c2a !important;
    }

    /* ===== CARD DE TEMA/FORMATO (com descrição) ===== */
    .opcao-rica {
        background: #faf9fc;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 8px 0;
        border: 1.5px solid transparent;
        transition: all 0.2s ease;
    }
    .opcao-rica:hover {
        background: #f0e8f9;
        border-color: #d4c3e8;
    }
    .opcao-titulo {
        font-size: 15px;
        font-weight: 600;
        color: #2c2c2a;
        margin: 0;
    }
    .opcao-desc {
        font-size: 13px;
        color: #5F5E5A;
        line-height: 1.55;
        margin: 4px 0 0 0;
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
    .stTextArea label {
        display: none !important;
    }

    /* ===== TEXT INPUT (campo "Outro") ===== */
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
    .stTextInput label {
        font-size: 13px !important;
        color: #5D3A9B !important;
        font-weight: 600 !important;
        margin-bottom: 6px !important;
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
    .stButton button:active {
        transform: translateY(-1px) !important;
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
        backdrop-filter: blur(10px);
    }

    /* ===== DIVISOR ENTRE PERGUNTAS ===== */
    .pergunta-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #E8DDF5, transparent);
        margin: 0;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# ARMAZENAMENTO
# ============================================================
RESPOSTAS_DIR = Path("respostas")
RESPOSTAS_DIR.mkdir(exist_ok=True)
ARQUIVO_RESPOSTAS = RESPOSTAS_DIR / "paula_respostas.json"

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
        <h1 class="nextgen-title">Respostas — Paula</h1>
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
            file_name=f"paula_respostas_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

        st.markdown("---")
        st.markdown("##### Limpar resposta (pra resetar antes de enviar pra Paula)")
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
        <p>Obrigada, Paula. Vou ler com calma e a gente conversa no nosso próximo encontro.</p>
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
        Paula, esse formulário não é uma pesquisa. É uma conversa por escrito,
        pra eu te apoiar melhor nos próximos meses da mentoria.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="intro-card">
    <p>Cada pergunta aqui veio do que você me contou no nosso primeiro encontro, no dia 15/05. A ideia é a gente ir mais fundo, não voltar pra trás.</p>
    <p>A maioria é só marcar opção — pra não tomar muito seu tempo. Tem 2 perguntas escritas curtas no final.</p>
    <p>Responde com calma, no seu tempo. Quando terminar, é só clicar em enviar lá embaixo.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# INICIALIZA RESPOSTAS NO SESSION STATE
# ============================================================
if 'respostas_dict' not in st.session_state:
    st.session_state.respostas_dict = {}

respostas = {}

# ============================================================
# FUNÇÕES AUXILIARES PRA CONTAR PROGRESSO
# ============================================================
def contar_progresso():
    """Conta quantas perguntas têm resposta válida (de 8)"""
    total = 8
    respondidas = 0

    # Q1
    if st.session_state.get("q1_radio") is not None:
        if st.session_state.get("q1_radio") != "Outro" or st.session_state.get("q1_outro", "").strip():
            respondidas += 1

    # Q2
    q2_alguma = any(st.session_state.get(f"q2_{op}", False) for op in [
        "A pressão por número mês a mês", "A competição entre colegas",
        "O relacionamento com cliente ficar transacional", "A sensação de não controlar o resultado",
        "A exposição em rankings e dashboards", "Ter que defender produto sem acreditar"
    ])
    if q2_alguma or (st.session_state.get("q2_outro_check") and st.session_state.get("q2_outro_text", "").strip()):
        respondidas += 1

    # Q3
    if st.session_state.get("q3_radio") is not None:
        if st.session_state.get("q3_radio") != "Outro" or st.session_state.get("q3_outro", "").strip():
            respondidas += 1

    # Q4
    q4_alguma = any(st.session_state.get(f"q4_{op}", False) for op in [
        "Resolver um problema complexo", "Ver alguém usando o que entreguei",
        "Aprender algo novo", "Conexão com pessoas",
        "Antecipar algo que ninguém viu", "Ter autonomia pra decidir",
        "Ser reconhecida pelo que faço"
    ])
    if q4_alguma or (st.session_state.get("q4_outro_check") and st.session_state.get("q4_outro_text", "").strip()):
        respondidas += 1

    # Q5
    temas_lista = [
        "Ler o cliente por trás do CRM",
        "A ponte entre Inteligência Comercial e operação",
        "Posicionamento de quem vem do RH em ambiente técnico-comercial",
        "Tradução de análise preditiva em recomendação executiva",
        "Uso estratégico de IA na rotina analítica",
        "Desenhar o lugar profissional ideal dentro da TBC",
        "Leitura de negócio do cliente final",
        "Carreira como projeto — pensar profissão com mentalidade de produto"
    ]
    q5_alguma = any(st.session_state.get(f"tema_{t}", False) for t in temas_lista)
    if q5_alguma or (st.session_state.get("q5_outro_check") and st.session_state.get("q5_outro_text", "").strip()):
        respondidas += 1

    # Q6
    formatos_lista = [
        "Conversa aberta com pauta solta", "Estudo de caso real",
        "Análise conjunta de uma entrega sua", "Simulação",
        "Shadowing reverso (você me observa)", "Shadowing direto (eu te observo)",
        "Sessão de provocação", "Co-construção de material"
    ]
    if any(st.session_state.get(f"formato_{f}", False) for f in formatos_lista):
        respondidas += 1

    # Q7
    if st.session_state.get("q7", "").strip():
        respondidas += 1

    # Q8
    if st.session_state.get("q8", "").strip():
        respondidas += 1

    return respondidas, total

# ============================================================
# BARRA DE PROGRESSO
# ============================================================
progresso_placeholder = st.empty()

def renderizar_progresso():
    respondidas, total = contar_progresso()
    porcentagem = int((respondidas / total) * 100)
    progresso_placeholder.markdown(f"""
    <div class="progress-container">
        <div class="progress-text">{respondidas} de {total} respondidas</div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: {porcentagem}%;"></div>
        </div>
        <div class="progress-text">{porcentagem}%</div>
    </div>
    """, unsafe_allow_html=True)

renderizar_progresso()

# ============================================================
# BLOCO 1
# ============================================================
st.markdown("""
<div class="block-strip">
    <div class="block-strip-label">Bloco 1 — Pra começar</div>
    <h2 class="block-strip-title">Sobre você, agora</h2>
    <p class="block-strip-desc">Algumas perguntas curtas baseadas no que você me contou. A ideia é aprofundar, não repetir.</p>
</div>
""", unsafe_allow_html=True)

# ---- Q1 ----
st.markdown('<div class="pergunta-card">', unsafe_allow_html=True)
st.markdown('<p class="pergunta-titulo">Você se descreveu como dinâmica e falante. Em momentos de pressão no trabalho, você tende a:</p>', unsafe_allow_html=True)
q1_texto = "Você se descreveu como dinâmica e falante. Em momentos de pressão no trabalho, você tende a:"
opcoes_q1 = [
    "Falar mais e processar em voz alta",
    "Me recolher e processar internamente",
    "Buscar alguém pra dividir e pensar junto",
    "Acelerar a execução pra dar conta",
    "Outro"
]
escolha_q1 = st.radio("Q1", opcoes_q1, index=None, key="q1_radio", label_visibility="collapsed")
if escolha_q1 == "Outro":
    outro_q1 = st.text_input("Conta aqui o que é:", key="q1_outro", placeholder="Escreva sua resposta...")
    if outro_q1:
        respostas[q1_texto] = f"Outro: {outro_q1}"
    else:
        respostas[q1_texto] = "Outro"
elif escolha_q1:
    respostas[q1_texto] = escolha_q1
st.markdown('</div>', unsafe_allow_html=True)

# ---- Q2 ----
st.markdown('<div class="pergunta-card">', unsafe_allow_html=True)
st.markdown('<p class="pergunta-titulo">Você recusou a posição comercial pura. Pensando no que mais te incomoda em meta dura, marque o que pesa de verdade (pode marcar mais de uma):</p>', unsafe_allow_html=True)
q2_texto = "Você recusou a posição comercial pura. Pensando no que mais te incomoda em meta dura, marque o que pesa de verdade (pode marcar mais de uma):"
opcoes_q2 = [
    "A pressão por número mês a mês",
    "A competição entre colegas",
    "O relacionamento com cliente ficar transacional",
    "A sensação de não controlar o resultado",
    "A exposição em rankings e dashboards",
    "Ter que defender produto sem acreditar"
]
selecionados_q2 = []
for opcao in opcoes_q2:
    if st.checkbox(opcao, key=f"q2_{opcao}"):
        selecionados_q2.append(opcao)
marcou_outro_q2 = st.checkbox("Outro", key="q2_outro_check")
if marcou_outro_q2:
    outro_q2 = st.text_input("Conta aqui o que é:", key="q2_outro_text", placeholder="Escreva sua resposta...")
    if outro_q2:
        selecionados_q2.append(f"Outro: {outro_q2}")
    else:
        selecionados_q2.append("Outro")
respostas[q2_texto] = selecionados_q2
st.markdown('</div>', unsafe_allow_html=True)

# ---- Q3 ----
st.markdown('<div class="pergunta-card">', unsafe_allow_html=True)
st.markdown('<p class="pergunta-titulo">Quando uma análise sua não é usada por quem deveria usar, o que vem primeiro em você:</p>', unsafe_allow_html=True)
q3_texto = "Quando uma análise sua não é usada por quem deveria usar, o que vem primeiro em você:"
opcoes_q3 = [
    "Frustração com quem não usou",
    "Autocrítica — talvez eu não tenha apresentado bem",
    "Vontade de explicar melhor pra próxima",
    "Aceitação — faz parte do processo",
    "Cansaço — já vi esse filme antes",
    "Outro"
]
escolha_q3 = st.radio("Q3", opcoes_q3, index=None, key="q3_radio", label_visibility="collapsed")
if escolha_q3 == "Outro":
    outro_q3 = st.text_input("Conta aqui o que é:", key="q3_outro", placeholder="Escreva sua resposta...")
    if outro_q3:
        respostas[q3_texto] = f"Outro: {outro_q3}"
    else:
        respostas[q3_texto] = "Outro"
elif escolha_q3:
    respostas[q3_texto] = escolha_q3
st.markdown('</div>', unsafe_allow_html=True)

# ---- Q4 ----
st.markdown('<div class="pergunta-card">', unsafe_allow_html=True)
st.markdown('<p class="pergunta-titulo">O que mais te energiza no trabalho hoje (marca quantas quiser):</p>', unsafe_allow_html=True)
q4_texto = "O que mais te energiza no trabalho hoje (marca quantas quiser):"
opcoes_q4 = [
    "Resolver um problema complexo",
    "Ver alguém usando o que entreguei",
    "Aprender algo novo",
    "Conexão com pessoas",
    "Antecipar algo que ninguém viu",
    "Ter autonomia pra decidir",
    "Ser reconhecida pelo que faço"
]
selecionados_q4 = []
for opcao in opcoes_q4:
    if st.checkbox(opcao, key=f"q4_{opcao}"):
        selecionados_q4.append(opcao)
marcou_outro_q4 = st.checkbox("Outro", key="q4_outro_check")
if marcou_outro_q4:
    outro_q4 = st.text_input("Conta aqui o que é:", key="q4_outro_text", placeholder="Escreva sua resposta...")
    if outro_q4:
        selecionados_q4.append(f"Outro: {outro_q4}")
    else:
        selecionados_q4.append("Outro")
respostas[q4_texto] = selecionados_q4
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# BLOCO 2
# ============================================================
st.markdown("""
<div class="block-strip">
    <div class="block-strip-label">Bloco 2 — Onde a gente vai</div>
    <h2 class="block-strip-title">Temas pra aprofundar</h2>
    <p class="block-strip-desc">Pensando na transição que você está vivendo — do RH pro comercial com pegada analítica — marca os temas que fazem mais sentido pra gente se aprofundar nos próximos meses. Pode marcar quantos quiser. Vou trazer pra mesa minha vivência de transição de carreira dentro do ecossistema da TBC, especialmente nas áreas comercial e controladoria.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="pergunta-card">', unsafe_allow_html=True)
st.markdown('<p class="pergunta-titulo">Quais temas você quer aprofundar nas mentorias:</p>', unsafe_allow_html=True)
q5_texto = "Quais temas você quer aprofundar nas mentorias:"

temas = [
    ("Ler o cliente por trás do CRM", "Ir além do dado: o que faz uma conta fechar ou travar, o que está por trás dos números."),
    ("A ponte entre Inteligência Comercial e operação", "Como o consultor de campo recebe (ou ignora) o que você entrega. Por que análise vira ação ou vira slide."),
    ("Posicionamento de quem vem do RH em ambiente técnico-comercial", "Construir autoridade sem perder o jeito acolhedor. Sair do lugar de 'a menina simpática' pra 'a referência analítica'."),
    ("Tradução de análise preditiva em recomendação executiva", "Pegar o que você entrega no operacional e transformar em insumo que muda decisão de gestor."),
    ("Uso estratégico de IA na rotina analítica", "Trocar fluxos, testar abordagens, pensar onde IA agrega e onde vira ruído. Conversa entre duas pessoas que já usam."),
    ("Desenhar o lugar profissional ideal dentro da TBC", "Mapear juntas qual carreira combina seus 3 mundos (psicologia + tecnologia + comercial) sem virar comercial puro nem voltar pro RH."),
    ("Leitura de negócio do cliente final", "Como uma empresa-cliente realmente usa (ou não usa) o que a TBC entrega — pelo olhar de quem está hoje do lado do cliente."),
    ("Carreira como projeto — pensar profissão com mentalidade de produto", "Ler oportunidade, se posicionar, pensar carreira com a mesma estratégia que se pensa um produto.")
]

selecionados_q5 = []
for tema, descricao in temas:
    col1, col2 = st.columns([1, 22])
    with col1:
        marcado = st.checkbox(" ", key=f"tema_{tema}", label_visibility="collapsed")
    with col2:
        st.markdown(f'<div class="opcao-titulo">{tema}</div><div class="opcao-desc">{descricao}</div>', unsafe_allow_html=True)
    if marcado:
        selecionados_q5.append(tema)

marcou_outro_q5 = st.checkbox("Outro tema que eu deveria ter colocado e não coloquei", key="q5_outro_check")
if marcou_outro_q5:
    outro_q5 = st.text_input("Conta aqui o tema:", key="q5_outro_text", placeholder="Escreva o tema...")
    if outro_q5:
        selecionados_q5.append(f"Outro: {outro_q5}")
    else:
        selecionados_q5.append("Outro")
respostas[q5_texto] = selecionados_q5
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# BLOCO 3
# ============================================================
st.markdown("""
<div class="block-strip">
    <div class="block-strip-label">Bloco 3 — Como a gente vai</div>
    <h2 class="block-strip-title">Formato dos encontros</h2>
    <p class="block-strip-desc">Pensa em como VOCÊ aprende e troca melhor. Cada pessoa tem um jeito. Quais formatos funcionam mais pra você (sugiro marcar 2 ou 3):</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="pergunta-card">', unsafe_allow_html=True)
st.markdown('<p class="pergunta-titulo">Formatos de encontro que funcionam pra você:</p>', unsafe_allow_html=True)
q6_texto = "Formatos de encontro que funcionam pra você:"

formatos = [
    ("Conversa aberta com pauta solta", "A gente combina o tema e deixa fluir, sem roteiro rígido."),
    ("Estudo de caso real", "Você traz uma situação concreta (uma conta, uma análise, uma reunião) e a gente destrincha juntas."),
    ("Análise conjunta de uma entrega sua", "Você me mostra algo que entregou e a gente olha juntas: o que funcionou, o que poderia ser diferente."),
    ("Simulação", "Eu faço o papel de um gestor/cliente/consultor e você pratica como apresentar, argumentar, posicionar."),
    ("Shadowing reverso (você me observa)", "Você me observa em alguma situação real minha (apresentação, reunião) e a gente conversa depois."),
    ("Shadowing direto (eu te observo)", "Eu observo você em alguma entrega real sua e te dou devolutiva."),
    ("Sessão de provocação", "Eu trago 3-4 perguntas duras sobre um tema, você responde. Bom pra sair do automático."),
    ("Co-construção de material", "A gente senta junta e constrói algo concreto (one-pager, narrativa, apresentação) que você vai usar de verdade.")
]

selecionados_q6 = []
for formato, descricao in formatos:
    col1, col2 = st.columns([1, 22])
    with col1:
        marcado = st.checkbox(" ", key=f"formato_{formato}", label_visibility="collapsed")
    with col2:
        st.markdown(f'<div class="opcao-titulo">{formato}</div><div class="opcao-desc">{descricao}</div>', unsafe_allow_html=True)
    if marcado:
        selecionados_q6.append(formato)
respostas[q6_texto] = selecionados_q6
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# BLOCO 4
# ============================================================
st.markdown("""
<div class="block-strip">
    <div class="block-strip-label">Bloco 4 — Pra fechar</div>
    <h2 class="block-strip-title">O que você quer me dizer</h2>
    <p class="block-strip-desc">As duas últimas perguntas. Pode ser bem curto.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="pergunta-card">', unsafe_allow_html=True)
st.markdown('<p class="pergunta-titulo">Em uma frase: qual é a SUA maior dor profissional hoje? (Não a do cliente, não a do time. A sua.)</p>', unsafe_allow_html=True)
q7_texto = "Em uma frase: qual é a SUA maior dor profissional hoje? (Não a do cliente, não a do time. A sua.)"
respostas[q7_texto] = st.text_area(
    "Q7",
    placeholder="Pode ser curto e direto. Uma frase basta.",
    height=110,
    key="q7",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="pergunta-card">', unsafe_allow_html=True)
st.markdown('<p class="pergunta-titulo">O que eu não te perguntei aqui e que você acha importante eu saber antes da gente continuar?</p>', unsafe_allow_html=True)
q8_texto = "O que eu não te perguntei aqui e que você acha importante eu saber antes da gente continuar?"
respostas[q8_texto] = st.text_area(
    "Q8",
    placeholder="Espaço livre. Se não tiver nada, pode pular.",
    height=110,
    key="q8",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# Atualiza progresso final
renderizar_progresso()

# ============================================================
# BOTÃO ENVIAR
# ============================================================
if st.button("Enviar respostas pra Elaine"):
    salvar_resposta(respostas)
    st.rerun()
