import streamlit as st
import requests

def corrigir_texto(texto):
    url = "https://api.languagetoolplus.com/v2/check"
    data = {
        "text": texto,
        "language": "pt-BR"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        return texto
    result = response.json()
    texto_corrigido = texto
    # Aplica as correções sugeridas (do fim para o começo)
    for match in sorted(result.get("matches", []), key=lambda m: -m["offset"]):
        if match["replacements"]:
            replacement = match["replacements"][0]["value"]
            start = match["offset"]
            end = start + match["length"]
            texto_corrigido = texto_corrigido[:start] + replacement + texto_corrigido[end:]
    return texto_corrigido

def gerar_projeto(respostas):
    return f"""
Meu Projeto de Vida

Eu sou movido por {respostas['motivacoes']}.
Meus pontos fortes incluem {respostas['pontos_fortes']}, mas reconheço que preciso desenvolver {respostas['pontos_fracos']}.
No momento, {respostas['situacao_atual']}.

Quando penso no futuro, sonho em {respostas['sonhos_ambicoes']}.
Para alcançar esses sonhos, estabeleci metas: {respostas['metas_claras']}.
Em cerca de {respostas['visao_longo_prazo_anos']} anos, me vejo {respostas['visao_longo_prazo_detalhe']}.

Dividi meus objetivos em etapas menores: {respostas['etapas']}.
Minhas prioridades são: {respostas['prioridades']}.
Para isso, vou precisar de {respostas['recursos']}.
Reconheço que desafios podem surgir, como {respostas['obstaculos']}, e pretendo {respostas['como_superar_obstaculos']}.

Pretendo revisar meu plano {respostas['avaliacao_frequencia']}, ajustando metas conforme necessário.
Acredito que {respostas['persistencia']} serão essenciais para seguir em frente, mesmo diante dos obstáculos.

Este é o meu compromisso comigo mesmo e com meu futuro.
""".strip()

st.title("Projeto de Vida — Geração Automática")

with st.form("projeto_form"):
    motivacoes = st.text_area("O que te move? (valores, paixões, motivações)")
    pontos_fortes = st.text_area("Quais são seus pontos fortes?")
    pontos_fracos = st.text_area("Quais áreas você precisa desenvolver?")
    situacao_atual = st.text_area("Onde você está agora? (conquistas e desafios atuais)")
    sonhos_ambicoes = st.text_area("Quais seus sonhos e ambições?")
    metas_claras = st.text_area("Defina metas claras (específicas, mensuráveis, atingíveis, relevantes e com prazo - SMART)")
    visao_longo_prazo_anos = st.text_input("Visão de longo prazo: em quantos anos?")
    visao_longo_prazo_detalhe = st.text_area("Como você imagina sua vida nesse tempo?")
    etapas = st.text_area("Divida grandes objetivos em etapas menores")
    prioridades = st.text_area("O que precisa ser feito primeiro? (prioridades)")
    recursos = st.text_area("Quais recursos você precisa? (tempo, dinheiro, conhecimento, ajuda)")
    obstaculos = st.text_area("Quais obstáculos podem surgir?")
    como_superar_obstaculos = st.text_area("Como pretende superar esses obstáculos?")
    avaliacao_frequencia = st.text_area("Com que frequência vai revisar seu plano?")
    persistencia = st.text_area("O que te faz persistir mesmo diante de desafios?")

    corrigir = st.form_submit_button("Corrigir Gramática e Ortografia")
    gerar = st.form_submit_button("Gerar Projeto de Vida")

    # Guardar respostas
    respostas = {
        "motivacoes": motivacoes,
        "pontos_fortes": pontos_fortes,
        "pontos_fracos": pontos_fracos,
        "situacao_atual": situacao_atual,
        "sonhos_ambicoes": sonhos_ambicoes,
        "metas_claras": metas_claras,
        "visao_longo_prazo_anos": visao_longo_prazo_anos,
        "visao_longo_prazo_detalhe": visao_longo_prazo_detalhe,
        "etapas": etapas,
        "prioridades": prioridades,
        "recursos": recursos,
        "obstaculos": obstaculos,
        "como_superar_obstaculos": como_superar_obstaculos,
        "avaliacao_frequencia": avaliacao_frequencia,
        "persistencia": persistencia,
    }

if corrigir:
    for campo in respostas:
        respostas[campo] = corrigir_texto(respostas[campo])
    st.success("Respostas corrigidas! Agora clique em 'Gerar Projeto de Vida'.")

if gerar:
    st.markdown("#### Seu Projeto de Vida:")
    st.text_area("Projeto de Vida Gerado", gerar_projeto(respostas), height=320)

st.info("Este app utiliza a API do LanguageTool para correção gramatical e ortográfica.")
