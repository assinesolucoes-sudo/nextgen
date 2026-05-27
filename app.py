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
# IDENTIDADE VISUAL — PALETA NEXTGEN
# ============================================================
st.markdown("""
<style>
    /* Reset e base */
    .stApp {
        background: linear-gradient(180deg, #faf9fc 0%, #f3eefa 100%);
    }

    /* Header personalizado */
    .nextgen-header {
        background: linear-gradient(135deg, #5D3A9B 0%, #8B5FBF 50%, #B47FE0 100%);
        padding: 40px 32px;
        border-radius: 20px;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(93, 58, 155, 0.15);
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
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
    }
    .nextgen-brand {
        color: rgba(255,255,255,0.85);
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
        position: relative;
    }
    .nextgen-title {
        color: white;
        font-size: 28px;
        font-weight: 600;
        margin: 0 0 12px 0;
        line-height: 1.2;
        position: relative;
    }
    .nextgen-subtitle {
        color: rgba(255,255,255,0.92);
        font-size: 15px;
        line-height: 1.6;
        margin: 0;
        position: relative;
    }

    /* Card de introdução */
    .intro-card {
        background: white;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        border-left: 4px solid #8B5FBF;
        box-shadow: 0 2px 12px rgba(93, 58, 155, 0.06);
    }
    .intro-card p {
        color: #444441;
        font-size: 14px;
        line-height: 1.7;
        margin: 0 0 12px 0;
    }
    .intro-card p:last-child { margin-bottom: 0; }

    /* Bloco temático */
    .block-header {
        margin: 36px 0 16px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid #E8DDF5;
    }
    .block-label {
        color: #8B5FBF;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .block-title {
        color: #2c2c2a;
        font-size: 19px;
        font-weight: 600;
        margin: 0 0 8px 0;
    }
    .block-desc {
        color: #5F5E5A;
        font-size: 13px;
        line-height: 1.6;
        margin: 0;
    }

    /* Estilo das perguntas */
    .stRadio > label, .stCheckbox > label, .stTextArea > label {
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #2c2c2a !important;
        margin-bottom: 8px !important;
    }

    /* Opções */
    .stRadio > div, .stCheckbox > div {
        background: white;
        padding: 16px 20px;
        border-radius: 12px;
        border: 1px solid #E8DDF5;
        margin-top: 8px;
    }

    div[data-testid="stRadio"] label {
        padding: 8px 0;
        font-size: 14px !important;
    }

    /* Textarea */
    .stTextArea textarea {
        background: white !important;
        border: 1px solid #E8DDF5 !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 14px !important;
        font-family: inherit !important;
    }
    .stTextArea textarea:focus {
        border-color: #8B5FBF !important;
        box-shadow: 0 0 0 3px rgba(139, 95, 191, 0.15) !important;
    }

    /* Input de texto */
    .stTextInput input {
        background: white !important;
        border: 1px solid #E8DDF5 !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
    }
    .stTextInput input:focus {
        border-color: #8B5FBF !important;
        box-shadow: 0 0 0 3px rgba(139, 95, 191, 0.15) !important;
    }

    /* Botão de envio */
    .stButton button, .stFormSubmitButton button {
        background: linear-gradient(135deg, #5D3A9B 0%, #8B5FBF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        width: 100% !important;
        margin-top: 24px !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 16px rgba(93, 58, 155, 0.25) !important;
    }
    .stButton button:hover, .stFormSubmitButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(93, 58, 155, 0.35) !important;
    }

    /* Sucesso */
    .success-card {
        background: linear-gradient(135deg, #5D3A9B 0%, #8B5FBF 100%);
        color: white;
        padding: 48px 32px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(93, 58, 155, 0.2);
    }
    .success-card h2 {
        color: white;
        font-size: 26px;
        font-weight: 600;
        margin: 16px 0 12px 0;
    }
    .success-card p {
        color: rgba(255,255,255,0.95);
        font-size: 15px;
        line-height: 1.6;
        margin: 0 0 8px 0;
    }
    .success-check {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: rgba(255,255,255,0.2);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        color: white;
        margin-bottom: 8px;
    }

    /* Esconde elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Container principal */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 760px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# ARMAZENAMENTO DE RESPOSTAS
# ============================================================
RESPOSTAS_DIR = Path("respostas")
RESPOSTAS_DIR.mkdir(exist_ok=True)
ARQUIVO_RESPOSTAS = RESPOSTAS_DIR / "paula_respostas.json"

def salvar_resposta(dados):
    """Salva resposta em arquivo JSON (uma resposta apenas, sobrescreve)"""
    payload = {
        "respondido_em": datetime.now().isoformat(),
        "respostas": dados
    }
    with open(ARQUIVO_RESPOSTAS, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def ja_respondeu():
    """Verifica se já existe resposta salva"""
    return ARQUIVO_RESPOSTAS.exists()

# ============================================================
# VERIFICAR MODO E ESTADO
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

        # Botão para baixar JSON
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
            st.success("Resposta apagada. O formulário está pronto pra ser respondido de novo.")
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
# FORMULÁRIO
# ============================================================
with st.form("formulario_paula", clear_on_submit=False):

    respostas = {}

    # ---------- BLOCO 1 ----------
    st.markdown("""
    <div class="block-header">
        <div class="block-label">Bloco 1 — Pra começar</div>
        <h2 class="block-title">Sobre você, agora</h2>
        <p class="block-desc">Algumas perguntas curtas baseadas no que você me contou. A ideia é aprofundar, não repetir.</p>
    </div>
    """, unsafe_allow_html=True)

    # Q1 — escolha única com Outro
    q1 = "Você se descreveu como dinâmica e falante. Em momentos de pressão no trabalho, você tende a:"
    opcoes_q1 = [
        "Falar mais e processar em voz alta",
        "Me recolher e processar internamente",
        "Buscar alguém pra dividir e pensar junto",
        "Acelerar a execução pra dar conta",
        "Outro"
    ]
    escolha_q1 = st.radio(q1, opcoes_q1, index=None, key="q1_radio")
    outro_q1_texto = ""
    if escolha_q1 == "Outro":
        outro_q1_texto = st.text_input("Conta aqui o que é:", key="q1_outro", placeholder="Escreva sua resposta...")
    if escolha_q1 == "Outro" and outro_q1_texto:
        respostas[q1] = f"Outro: {outro_q1_texto}"
    else:
        respostas[q1] = escolha_q1

    # Q2 — múltipla escolha com Outro
    q2 = "Você recusou a posição comercial pura. Pensando no que mais te incomoda em meta dura, marque o que pesa de verdade (pode marcar mais de uma):"
    st.markdown(f"<div style='font-size:15px; font-weight:500; color:#2c2c2a; margin-top:20px; margin-bottom:8px;'>{q2}</div>", unsafe_allow_html=True)
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
    # Checkbox "Outro" + campo de texto que só aparece quando marcado
    marcou_outro_q2 = st.checkbox("Outro", key="q2_outro_check")
    if marcou_outro_q2:
        outro_q2_texto = st.text_input("Conta aqui o que é:", key="q2_outro_text", placeholder="Escreva sua resposta...")
        if outro_q2_texto:
            selecionados_q2.append(f"Outro: {outro_q2_texto}")
    respostas[q2] = selecionados_q2

    # Q3 — escolha única com Outro
    q3 = "Quando uma análise sua não é usada por quem deveria usar, o que vem primeiro em você:"
    opcoes_q3 = [
        "Frustração com quem não usou",
        "Autocrítica — talvez eu não tenha apresentado bem",
        "Vontade de explicar melhor pra próxima",
        "Aceitação — faz parte do processo",
        "Cansaço — já vi esse filme antes",
        "Outro"
    ]
    escolha_q3 = st.radio(q3, opcoes_q3, index=None, key="q3_radio")
    outro_q3_texto = ""
    if escolha_q3 == "Outro":
        outro_q3_texto = st.text_input("Conta aqui o que é:", key="q3_outro", placeholder="Escreva sua resposta...")
    if escolha_q3 == "Outro" and outro_q3_texto:
        respostas[q3] = f"Outro: {outro_q3_texto}"
    else:
        respostas[q3] = escolha_q3

    # Q4 — múltipla escolha com Outro
    q4 = "O que mais te energiza no trabalho hoje (marca quantas quiser):"
    st.markdown(f"<div style='font-size:15px; font-weight:500; color:#2c2c2a; margin-top:20px; margin-bottom:8px;'>{q4}</div>", unsafe_allow_html=True)
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
    # Checkbox "Outro" + campo de texto que só aparece quando marcado
    marcou_outro_q4 = st.checkbox("Outro", key="q4_outro_check")
    if marcou_outro_q4:
        outro_q4_texto = st.text_input("Conta aqui o que é:", key="q4_outro_text", placeholder="Escreva sua resposta...")
        if outro_q4_texto:
            selecionados_q4.append(f"Outro: {outro_q4_texto}")
    respostas[q4] = selecionados_q4

    # ---------- BLOCO 2 ----------
    st.markdown("""
    <div class="block-header">
        <div class="block-label">Bloco 2 — Onde a gente vai</div>
        <h2 class="block-title">Temas pra aprofundar</h2>
        <p class="block-desc">Pensando na transição que você está vivendo — do RH pro comercial com pegada analítica — marca os temas que fazem mais sentido pra gente se aprofundar nos próximos meses. Pode marcar quantos quiser. Vou trazer pra mesa minha vivência de transição de carreira dentro do ecossistema da TBC, especialmente nas áreas comercial e controladoria.</p>
    </div>
    """, unsafe_allow_html=True)

    q5 = "Quais temas você quer aprofundar nas mentorias:"
    st.markdown(f"<div style='font-size:15px; font-weight:500; color:#2c2c2a; margin-bottom:8px;'>{q5}</div>", unsafe_allow_html=True)

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
        col1, col2 = st.columns([1, 20])
        with col1:
            marcado = st.checkbox("", key=f"tema_{tema}", label_visibility="collapsed")
        with col2:
            st.markdown(f"<div style='font-size:14px; font-weight:500; color:#2c2c2a; margin-top:2px;'>{tema}</div><div style='font-size:12px; color:#5F5E5A; line-height:1.5; margin-bottom:8px;'>{descricao}</div>", unsafe_allow_html=True)
        if marcado:
            selecionados_q5.append(tema)

    # Checkbox "Outro" + campo de texto que só aparece quando marcado
    marcou_outro_q5 = st.checkbox("Outro tema que eu deveria ter colocado e não coloquei", key="q5_outro_check")
    if marcou_outro_q5:
        outro_q5_texto = st.text_input("Conta aqui o tema:", key="q5_outro_text", placeholder="Escreva o tema...")
        if outro_q5_texto:
            selecionados_q5.append(f"Outro: {outro_q5_texto}")
    respostas[q5] = selecionados_q5

    # ---------- BLOCO 3 ----------
    st.markdown("""
    <div class="block-header">
        <div class="block-label">Bloco 3 — Como a gente vai</div>
        <h2 class="block-title">Formato dos encontros</h2>
        <p class="block-desc">Pensa em como VOCÊ aprende e troca melhor. Cada pessoa tem um jeito. Quais formatos funcionam mais pra você (sugiro marcar 2 ou 3):</p>
    </div>
    """, unsafe_allow_html=True)

    q6 = "Formatos de encontro que funcionam pra você:"
    st.markdown(f"<div style='font-size:15px; font-weight:500; color:#2c2c2a; margin-bottom:8px;'>{q6}</div>", unsafe_allow_html=True)

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
        col1, col2 = st.columns([1, 20])
        with col1:
            marcado = st.checkbox("", key=f"formato_{formato}", label_visibility="collapsed")
        with col2:
            st.markdown(f"<div style='font-size:14px; font-weight:500; color:#2c2c2a; margin-top:2px;'>{formato}</div><div style='font-size:12px; color:#5F5E5A; line-height:1.5; margin-bottom:8px;'>{descricao}</div>", unsafe_allow_html=True)
        if marcado:
            selecionados_q6.append(formato)
    respostas[q6] = selecionados_q6

    # ---------- BLOCO 4 ----------
    st.markdown("""
    <div class="block-header">
        <div class="block-label">Bloco 4 — Pra fechar</div>
        <h2 class="block-title">O que você quer me dizer</h2>
        <p class="block-desc">As duas últimas perguntas. Pode ser bem curto.</p>
    </div>
    """, unsafe_allow_html=True)

    q7 = "Em uma frase: qual é a SUA maior dor profissional hoje? (Não a do cliente, não a do time. A sua.)"
    respostas[q7] = st.text_area(
        q7,
        placeholder="Pode ser curto e direto. Uma frase basta.",
        height=100,
        key="q7"
    )

    q8 = "O que eu não te perguntei aqui e que você acha importante eu saber antes da gente continuar?"
    respostas[q8] = st.text_area(
        q8,
        placeholder="Espaço livre. Se não tiver nada, pode pular.",
        height=100,
        key="q8"
    )

    # ---------- BOTÃO ----------
    enviado = st.form_submit_button("Enviar respostas pra Elaine")

    if enviado:
        salvar_resposta(respostas)
        st.rerun()
