# 🩺 CALCULADORA MÉDICA INTERATIVA DE PLANTÃO (EDITION STREAMLIT 2026 - EXPANDIDA)
# Desenvolvida para consulta rápida em Plantões Médicos (UBS, UPA, PS, Enfermaria, UTI)
# Compatível com Streamlit Community Cloud e Embed via Notion

import streamlit as st
import math

st.set_page_config(
    page_title="Calculadora Médica de Plantão",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Calculadora Médica Prática de Plantão (2026)")
st.caption("Ferramenta clínica baseada nas Diretrizes SBD 2026, SBC 2025/2026, GINA 2026, GOLD 2026, ESETT e Ministério da Saúde.")

st.sidebar.header("📌 Módulos de Cálculo")
modulo = st.sidebar.radio(
    "Selecione o módulo:",
    [
        "1. Cetoacidose (CAD) & Estado Hiperosmolar (SHH)",
        "2. Infusão de Drogas Vasoativas (BIC)",
        "3. Função Renal (CKD-EPI 2021)",
        "4. Anestésicos Locais & Dose Máxima (Sutura)",
        "5. Correção de Hiponatremia (Adrogue & SALSA)",
        "6. Escore NIHSS (AVC Isquêmico)",
        "7. Risco Coronariano (HEART & TIMI Score)",
        "8. Gasometria Arterial & Ácido-Base",
        "9. Insulinoterapia Hospitalar (SBD 2026)",
        "10. Doses Pediátricas por Peso",
        "11. Escores Críticos (CURB-65 & qSOFA)",
        "12. Dengue - Manejo Volêmico (MS)",
        "13. Queimaduras (Regra de Parkland)"
    ]
)

# -----------------------------------------------------------------------------
# MÓDULO 1: CAD E SHH
# -----------------------------------------------------------------------------
if modulo == "1. Cetoacidose (CAD) & Estado Hiperosmolar (SHH)":
    st.header("🧪 Manejo de CAD & SHH (SBD 2026)")
    st.subheader("Cálculos Hidroeletrolíticos e Correções")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        glicemia = st.number_input("Glicemia Capilar/Plasmática (mg/dL)", min_value=10.0, max_value=2000.0, value=350.0, step=10.0)
        sodio = st.number_input("Sódio Sérico (Na+) (mEq/L)", min_value=100.0, max_value=200.0, value=135.0, step=1.0)
    with col2:
        potassio = st.number_input("Potássio Sérico (K+) (mEq/L)", min_value=1.0, max_value=10.0, value=4.0, step=0.1)
        cloro = st.number_input("Cloro Sérico (Cl-) (mEq/L)", min_value=50.0, max_value=150.0, value=100.0, step=1.0)
    with col3:
        hco3 = st.number_input("Bicarbonato (HCO3-) (mEq/L)", min_value=1.0, max_value=50.0, value=12.0, step=1.0)
        ureia = st.number_input("Ureia Plasmática (mg/dL)", min_value=5.0, max_value=400.0, value=50.0, step=5.0)

    # Lógica de Correção do Sódio
    if glicemia < 400:
        na_corrigido = sodio + 1.6 * ((glicemia - 100) / 100)
        fator_usado = "1,6 (Glicemia < 400 mg/dL)"
    else:
        na_corrigido = sodio + 2.4 * ((glicemia - 100) / 100)
        fator_usado = "2,4 (Glicemia >= 400 mg/dL)"
        
    osm_efetiva = 2 * sodio + (glicemia / 18)
    osm_total = 2 * sodio + (glicemia / 18) + (ureia / 2.8)
    anion_gap = sodio - (cloro + hco3)
    
    st.markdown("---")
    st.subheader("📊 Resultados Obtidos:")
    
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Na+ Corrigido", f"{na_corrigido:.1f} mEq/L", delta=f"Fator {fator_usado}")
    r2.metric("Osmolaridade Efetiva", f"{osm_efetiva:.1f} mOsm/kg", delta="Alvo SHH > 320")
    r3.metric("Anion Gap", f"{anion_gap:.1f} mEq/L", delta="Normal: 4 - 12")
    r4.metric("Osmolaridade Total", f"{osm_total:.1f} mOsm/kg")
    
    st.markdown("### ⚠️ Conduta Prática Recomendada:")
    if potassio < 3.3:
        st.error("🚨 **ATENÇÃO ABSOLUTA**: Potássio < 3,3 mEq/L. **NÃO INICIAR INSULINA!** Repor KCl 10 a 40 mEq/h até K+ > 3,3 mEq/L para evitar arritmia e PCR por hipocalemia grave.")
    elif potassio <= 5.2:
        st.success(f"✅ Potássio em {potassio} mEq/L. Pode iniciar Insulinoterapia EV (0,1 UI/kg/h na CAD ou 0,05 UI/kg/h na SHH). Associar 10-30 mEq de KCl por litro de solução de manutenção.")
    else:
        st.warning(f"⚠️ Potássio em {potassio} mEq/L (Hipercalemia). Iniciar Insulinoterapia EV, mas **NÃO repor KCl** no momento. Reavaliar K+ a cada 2 horas.")

# -----------------------------------------------------------------------------
# MÓDULO 2: DROGAS VASOATIVAS
# -----------------------------------------------------------------------------
elif modulo == "2. Infusão de Drogas Vasoativas (BIC)":
    st.header("💉 Calculadora de Drogas Vasoativas em Bomba de Infusão (BIC)")
    
    drogas = st.selectbox(
        "Selecione a medicação:",
        ["Noradrenalina", "Nitroglicerina (Tridil)", "Nitroprussiato de Sódio (Nipride)", "Dopamina", "Dobutamina"]
    )
    
    peso = st.number_input("Peso do Paciente (kg)", min_value=30.0, max_value=250.0, value=70.0, step=1.0)
    
    if drogas == "Noradrenalina":
        st.subheader("Noradrenalina (Ampolas de 4 mg / 4 mL)")
        diluicao = st.radio(
            "Selecione a diluição:",
            ["Padrão (1 amp = 4 mg + 250 mL SG5% -> 16 mcg/mL)",
             "Concentrada (2 amp = 8 mg + 250 mL SG5% -> 32 mcg/mL)",
             "Quadrupla (4 amp = 16 mg + 250 mL SG5% -> 64 mcg/mL)"]
        )
        
        if "16 mcg/mL" in diluicao:
            conc = 16.0
        elif "32 mcg/mL" in diluicao:
            conc = 32.0
        else:
            conc = 64.0
            
        dose_target = st.slider("Dose desejada (mcg/kg/min)", min_value=0.01, max_value=2.00, value=0.10, step=0.01)
        vazao_mlh = (dose_target * peso * 60) / conc
        
        st.success(f"📌 **Vazão na Bomba de Infusão:** **{vazao_mlh:.1f} mL/h**")
        st.info(f"Fórmula: (Dose {dose_target} mcg/kg/min × {peso} kg × 60) / {conc} mcg/mL = {vazao_mlh:.1f} mL/h")

    elif drogas == "Nitroglicerina (Tridil)":
        st.subheader("Nitroglicerina / Tridil (Ampolas de 25 mg / 5 mL)")
        st.write("Diluição padrão: 1 ampola (25 mg) + 245 mL SG5% (Total 250 mL -> 100 mcg/mL)")
        conc = 100.0
        dose_mcg_min = st.slider("Dose em mcg/min (Início 5 mcg/min, titular até 200 mcg/min)", min_value=5.0, max_value=200.0, value=10.0, step=5.0)
        vazao_mlh = (dose_mcg_min * 60) / conc
        st.success(f"📌 **Vazão na Bomba de Infusão:** **{vazao_mlh:.1f} mL/h**")

    elif drogas == "Nitroprussiato de Sódio (Nipride)":
        st.subheader("Nitroprussiato de Sódio / Nipride (Ampola 50 mg / 2 mL)")
        st.write("Diluição padrão: 1 ampola (50 mg) + 248 mL SG5% (Total 250 mL -> 200 mcg/mL) - *Proteger da luz!*")
        conc = 200.0
        dose_target = st.slider("Dose desejada (mcg/kg/min)", min_value=0.25, max_value=10.00, value=0.50, step=0.25)
        vazao_mlh = (dose_target * peso * 60) / conc
        st.success(f"📌 **Vazão na Bomba de Infusão:** **{vazao_mlh:.1f} mL/h**")
        if dose_target > 3.0:
            st.warning("⚠️ Risco de intoxicação cianídrica em doses > 3 mcg/kg/min por tempo prolongado.")

    elif drogas == "Dopamina":
        st.subheader("Dopamina (Ampolas de 50 mg / 10 mL)")
        st.write("Diluição padrão: 5 ampolas (250 mg) + 200 mL SG5% (Total 250 mL -> 1000 mcg/mL)")
        conc = 1000.0
        dose_target = st.slider("Dose desejada (mcg/kg/min)", min_value=2.0, max_value=20.0, value=5.0, step=0.5)
        vazao_mlh = (dose_target * peso * 60) / conc
        st.success(f"📌 **Vazão na Bomba de Infusão:** **{vazao_mlh:.1f} mL/h**")

    elif drogas == "Dobutamina":
        st.subheader("Dobutamina (Ampola de 250 mg / 20 mL)")
        st.write("Diluição padrão: 1 ampola (250 mg) + 230 mL SG5% (Total 250 mL -> 1000 mcg/mL)")
        conc = 1000.0
        dose_target = st.slider("Dose desejada (mcg/kg/min)", min_value=2.5, max_value=20.0, value=5.0, step=0.5)
        vazao_mlh = (dose_target * peso * 60) / conc
        st.success(f"📌 **Vazão na Bomba de Infusão:** **{vazao_mlh:.1f} mL/h**")

# -----------------------------------------------------------------------------
# MÓDULO 3: CKD-EPI 2021
# -----------------------------------------------------------------------------
elif modulo == "3. Função Renal (CKD-EPI 2021)":
    st.header("🫘 Estimativa de Taxa de Filtração Glomerular (CKD-EPI 2021)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sexo = st.radio("Sexo Biológico", ["Feminino", "Masculino"])
    with col2:
        idade = st.number_input("Idade (anos)", min_value=18, max_value=120, value=65)
    with col3:
        creatinina = st.number_input("Creatinina Sérica (mg/dL)", min_value=0.2, max_value=20.0, value=1.2, step=0.1)

    is_female = (sexo == "Feminino")
    k = 0.7 if is_female else 0.9
    alpha = -0.241 if is_female else -0.302
    
    scr_k = creatinina / k
    egfr = 142 * (min(scr_k, 1.0) ** alpha) * (max(scr_k, 1.0) ** -1.200) * (0.9938 ** idade)
    if is_female:
        egfr *= 1.012

    st.markdown("---")
    st.metric("TFGe (CKD-EPI 2021)", f"{egfr:.1f} mL/min/1,73m²")
    
    if egfr >= 90:
        estagio = "G1 (Normal ou Elevado)"
    elif egfr >= 60:
        estagio = "G2 (Ligeiramente Diminuído)"
    elif egfr >= 45:
        estagio = "G3a (Moderadamente Diminuído)"
    elif egfr >= 30:
        estagio = "G3b (Moderada a Severamente Diminuído)"
    elif egfr >= 15:
        estagio = "G4 (Severamente Diminuído)"
    else:
        estagio = "G5 (Falência Renal / Diálise)"

    st.info(f"**Estágio da Função Renal:** {estagio}")
    
    st.markdown("### 📋 Ajustes de Drogas Importantes:")
    if egfr < 30:
        st.warning("⚠️ **TFGe < 30 mL/min**: Contraindicada Metformina. Reduzir Enoxaparina para 1 mg/kg 1x/dia. Evitar AINEs.")
    if egfr < 20:
        st.warning("⚠️ **TFGe < 20 mL/min**: iSGLT2 não deve ser iniciado (manter se já em uso conforme diretrizes renais).")

# -----------------------------------------------------------------------------
# MÓDULO 4: ANESTÉSICOS LOCAIS (NOVO)
# -----------------------------------------------------------------------------
elif modulo == "4. Anestésicos Locais & Dose Máxima (Sutura)":
    st.header("🩹 Dose Máxima de Anestésicos Locais para Suturas / Procedimentos")
    st.caption("Prevenção da Síndrome de Intoxicação Sistêmica por Anestésicos Locais (LAST)")
    
    col1, col2 = st.columns(2)
    with col1:
        peso_anest = st.number_input("Peso do Paciente (kg)", min_value=5.0, max_value=200.0, value=70.0, step=1.0)
    with col2:
        anestesico = st.selectbox(
            "Anestésico Local & Apresentação:",
            [
                "Lidocaína 1% SEM Epinefrina (10 mg/mL) - Máx 4,5 mg/kg",
                "Lidocaína 2% SEM Epinefrina (20 mg/mL) - Máx 4,5 mg/kg",
                "Lidocaína 1% COM Epinefrina (10 mg/mL) - Máx 7,0 mg/kg",
                "Lidocaína 2% COM Epinefrina (20 mg/mL) - Máx 7,0 mg/kg",
                "Bupivacaína 0,5% SEM Epinefrina (5 mg/mL) - Máx 2,0 mg/kg",
                "Bupivacaína 0,5% COM Epinefrina (5 mg/mL) - Máx 2,5 mg/kg"
            ]
        )
        
    if "Lidocaína 1% SEM" in anestesico:
        dose_mg_kg = 4.5
        conc_mg_ml = 10.0
    elif "Lidocaína 2% SEM" in anestesico:
        dose_mg_kg = 4.5
        conc_mg_ml = 20.0
    elif "Lidocaína 1% COM" in anestesico:
        dose_mg_kg = 7.0
        conc_mg_ml = 10.0
    elif "Lidocaína 2% COM" in anestesico:
        dose_mg_kg = 7.0
        conc_mg_ml = 20.0
    elif "Bupivacaína 0,5% SEM" in anestesico:
        dose_mg_kg = 2.0
        conc_mg_ml = 5.0
    else:
        dose_mg_kg = 2.5
        conc_mg_ml = 5.0
        
    dose_total_mg = peso_anest * dose_mg_kg
    vol_max_ml = dose_total_mg / conc_mg_ml
    
    st.markdown("---")
    r1, r2, r3 = st.columns(3)
    r1.metric("Dose Máxima por Peso", f"{dose_mg_kg} mg/kg")
    r2.metric("Dose Máxima Total (mg)", f"{dose_total_mg:.0f} mg")
    r3.metric("Volume Máximo em mL", f"{vol_max_ml:.1f} mL")
    
    st.info(f"💡 **Orientações do Plantão:** Para um paciente de **{peso_anest} kg**, o limite de segurança é de **{vol_max_ml:.1f} mL** do anestésico selecionado. Sempre realizar aspiração prévia antes de injetar para evitar injeção intravascular inadvertida.")

# -----------------------------------------------------------------------------
# MÓDULO 5: ADROGUE & SALSA (HIPONATREMIA) (NOVO)
# -----------------------------------------------------------------------------
elif modulo == "5. Correção de Hiponatremia (Adrogue & SALSA)":
    st.header("🧂 Manejo Rápido da Hiponatremia & Fórmula de Adrogué-Madias")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sexo_h = st.radio("Sexo e Perfil", ["Homem Adulto", "Mulher Adulta / Homem Idoso", "Mulher Idosa", "Criança"])
        peso_h = st.number_input("Peso (kg)", min_value=10.0, max_value=200.0, value=70.0)
    with col2:
        na_paciente = st.number_input("Sódio Atual do Paciente (Na+) (mEq/L)", min_value=90.0, max_value=150.0, value=115.0)
        na_desejado = st.number_input("Sódio Alvo Desejado (mEq/L)", min_value=95.0, max_value=150.0, value=121.0)
    with col3:
        solucao = st.selectbox(
            "Solução de Infusão:",
            [
                "Salina 3% (513 mEq/L Na+)",
                "Soro Fisiológico 0,9% (154 mEq/L Na+)",
                "Ringer Lactato (130 mEq/L Na+)"
            ]
        )

    # Cálculo da Água Corporal Total (ACT)
    if sexo_h == "Homem Adulto":
        f_act = 0.6
    elif sexo_h == "Mulher Adulta / Homem Idoso":
        f_act = 0.5
    elif sexo_h == "Mulher Idosa":
        f_act = 0.45
    else:
        f_act = 0.6
        
    act = peso_h * f_act
    
    if "3%" in solucao:
        na_solucao = 513.0
    elif "0,9%" in solucao:
        na_solucao = 154.0
    else:
        na_solucao = 130.0
        
    # Fórmula Adrogué-Madias: Delta Na por 1L = (Na_solucao - Na_paciente) / (ACT + 1)
    delta_na_1L = (na_solucao - na_paciente) / (act + 1.0)
    variacao_desejada = na_desejado - na_paciente
    
    if delta_na_1L > 0:
        vol_necessario_l = variacao_desejada / delta_na_1L
        vol_necessario_ml = vol_necessario_l * 1000.0
    else:
        vol_necessario_ml = 0.0

    st.markdown("---")
    st.subheader("📊 Cálculo de Reposição Continuada (Adrogué-Madias):")
    c1, c2, c3 = st.columns(3)
    c1.metric("Água Corporal Total (ACT)", f"{act:.1f} L")
    c2.metric("Elevação de Na+ por 1L de Soro", f"+{delta_na_1L:.2f} mEq/L")
    c3.metric(f"Volume de {solucao} para +{variacao_desejada:.0f} mEq/L", f"{vol_necessario_ml:.0f} mL")

    st.markdown("### 🚨 Protocolo de Emergência (Estudo SALSA - Encefalopatia Hiponatrêmica):")
    st.error("• **Sintomas Graves (Convulsão, Coma, Torpor):** Administrar **Bolus Intermitente Rápido de Salina 3% (100 a 150 mL em 10-20 min)**.")
    st.write("• Pode repetir 1 a 2 vezes se mantiver sintomas graves ou até elevar Na+ em 4-6 mEq/L nas primeiras 1-2h.")
    st.warning("🛑 **LIMITE DE SEGURANÇA MÁXIMO:** **NÃO elevar mais de 8 a 10 mEq/L nas primeiras 24 horas** (ou < 6-8 mEq/L em pacientes de alto risco) para evitar a **Síndrome de Desmielinização Osmótica (Mielinólise Pontina)**.")
    st.info("💡 **Preparo Caseiro de SF 3% (500 mL):** 445 mL de Soro Fisiológico 0,9% + 55 mL de NaCl 20%.")

# -----------------------------------------------------------------------------
# MÓDULO 6: NIHSS (NOVO)
# -----------------------------------------------------------------------------
elif modulo == "6. Escore NIHSS (AVC Isquêmico)":
    st.header("🧠 Escore NIHSS Completo (Escala de AVC do NIH)")
    st.caption("Avaliador de gravidade do AVC Isquêmico para decisão de Trombólise com Alteplase")
    
    q1 = st.selectbox("1a. Nível de Consciência:", [0, 1, 2, 3], format_func=lambda x: f"{x} - " + ["Alerta", "Somnolento", "Torporoso/Estuporoso", "Coma/Riflexia"][x])
    q2 = st.selectbox("1b. Perguntas (Mês atual e Idade):", [0, 1, 2], format_func=lambda x: f"{x} - " + ["Acerta ambas", "Acerta uma", "Erra ambas"][x])
    q3 = st.selectbox("1c. Comandos (Abrir/fechar olhos, fechar mão):", [0, 1, 2], format_func=lambda x: f"{x} - " + ["Obedece ambos", "Obedece um", "Erra ambos"][x])
    q4 = st.selectbox("2. Olhar Conjugado:", [0, 1, 2], format_func=lambda x: f"{x} - " + ["Normal", "Paresia parcial", "Desvio forçado/Paresia total"][x])
    q5 = st.selectbox("3. Campos Visuais:", [0, 1, 2, 3], format_func=lambda x: f"{x} - " + ["Sem perda", "Hemianopsia parcial", "Hemianopsia completa", "Cegueira bilateral"][x])
    q6 = st.selectbox("4. Paralisia Facial:", [0, 1, 2, 3], format_func=lambda x: f"{x} - " + ["Normal", "Paresia mínima", "Paralisia parcial", "Paralisia completa"][x])
    q7 = st.selectbox("5. Motor Membro Superior (D e E):", [0, 1, 2, 3, 4], format_func=lambda x: f"{x} - " + ["Sem queda (10s)", "Queda sutil sem tocar leito", "Queda toca leito", "Sem força contra gravidade", "Sem movimento"][x])
    q8 = st.selectbox("6. Motor Membro Inferior (D e E):", [0, 1, 2, 3, 4], format_func=lambda x: f"{x} - " + ["Sem queda (5s)", "Queda sutil sem tocar leito", "Queda toca leito", "Sem força contra gravidade", "Sem movimento"][x])
    q9 = st.selectbox("7. Ataxia Apendicular (Dismetria):", [0, 1, 2], format_func=lambda x: f"{x} - " + ["Ausente", "Presente em 1 membro", "Presente em 2 membros"][x])
    q10 = st.selectbox("8. Sensibilidade (Estímulo doloroso):", [0, 1, 2], format_func=lambda x: f"{x} - " + ["Normal", "Perda leve/moderada", "Perda grave/Anestesia"][x])
    q11 = st.selectbox("9. Melhor Linguagem (Afasia):", [0, 1, 2, 3], format_func=lambda x: f"{x} - " + ["Sem afasia", "Afasia leve/moderada", "Afasia grave", "Muto/Afasia global"][x])
    q12 = st.selectbox("10. Disartria:", [0, 1, 2], format_func=lambda x: f"{x} - " + ["Normal", "Leve/moderada", "Grave/Anartria"][x])
    q13 = st.selectbox("11. Extinção e Inatenção (Negligência):", [0, 1, 2], format_func=lambda x: f"{x} - " + ["Sem negligência", "Negligência parcial (1 modalidade)", "Negligência profunda (> 1 modalidade)"][x])
    
    nihss_total = sum([q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13])
    
    st.markdown("---")
    st.metric("Pontuação Total NIHSS", f"{nihss_total} pontos")
    
    if nihss_total == 0:
        st.success("Exame neurológico normal.")
    elif nihss_total <= 4:
        st.info("AVC leve / Deficit mínimo. Avaliar se o déficit é incapacitante para indicar Trombólise.")
    elif nihss_total <= 15:
        st.warning("AVC moderado. Candidato a Trombólise se janela < 4h30 e sem contraindicações.")
    elif nihss_total <= 25:
        st.error("AVC moderadamente grave a grave. Indicada Trombólise e avaliação de Trombectomia Mecânica.")
    else:
        st.error("AVC muito grave (NIHSS > 25). Alto risco de transformação hemorrágica.")

# -----------------------------------------------------------------------------
# MÓDULO 7: RISCO CORONARIANO (HEART & TIMI) (NOVO)
# -----------------------------------------------------------------------------
elif modulo == "7. Risco Coronariano (HEART & TIMI Score)":
    st.header("🫀 Escores de Risco para Síndrome Coronariana Aguda (SCA)")
    
    escore_tipo = st.radio("Selecione o Escore:", ["HEART Score (Dor Torácica no PS)", "TIMI Risk Score (SCA sem Supra)"])
    
    if escore_tipo == "HEART Score (Dor Torácica no PS)":
        st.subheader("HEART Score para Estratificação no Pronto-Socorro")
        
        h = st.selectbox("H - História clínica:", [0, 1, 2], format_func=lambda x: ["0 - Pouco suspeita", "1 - Moderadamente suspeita", "2 - Altamente suspeita"][x])
        e = st.selectbox("E - Eletrocardiograma (ECG):", [0, 1, 2], format_func=lambda x: ["0 - Normal", "1 - Alteração de repolarização não específica", "2 - Infradesnível de ST acentuado / Isquemia"][x])
        a = st.selectbox("A - Idade (Age):", [0, 1, 2], format_func=lambda x: ["0 - < 45 anos", "1 - 45 a 64 anos", "2 - >= 65 anos"][x])
        r = st.selectbox("R - Fatores de Risco (HAS, DM, DLP, Tabagismo, Obesidade, HF):", [0, 1, 2], format_func=lambda x: ["0 - Nenhum fator de risco", "1 - 1 ou 2 fatores de risco", "2 - >= 3 fatores de risco ou Doença Aterosclerótica Prévia"][x])
        t = st.selectbox("T - Troponina inicial:", [0, 1, 2], format_func=lambda x: ["0 - Normal (<= limite)", "1 - 1 a 3x o limite superior", "2 - > 3x o limite superior"][x])
        
        heart_score = h + e + a + r + t
        st.markdown(f"**Pontuação HEART Score:** **{heart_score} pontos**")
        
        if heart_score <= 3:
            st.success("✅ **Baixo Risco (0 - 3 pontos):** Risco de MACE em 6 semanas < 2,5%. Candidato à alta hospitalar com acompanhamento ambulatorial.")
        elif heart_score <= 6:
            st.warning("⚠️ **Risco Intermediário (4 - 6 pontos):** Risco MACE ~ 12-20%. Observação, troponina seriada e ecocardiograma/estratificação pré-alta.")
        else:
            st.error("🚨 **Alto Risco (7 - 10 pontos):** Risco MACE > 50-65%. Internação em Unidade Coronariana / UTI e Cateterismo (ICP) de urgência.")

    else:
        st.subheader("TIMI Risk Score para SCA sem Supra de ST")
        t1 = st.checkbox("Idade >= 65 anos")
        t2 = st.checkbox(">= 3 Fatores de Risco para DAC (HAS, DM, DLP, Tabagismo, HF)")
        t3 = st.checkbox("Estenose Coronariana Prévia >= 50%")
        t4 = st.checkbox("Uso de AAS nos últimos 7 dias")
        t5 = st.checkbox(">= 2 episódios de Angina nas últimas 24 horas")
        t6 = st.checkbox("Infradesnível de ST >= 0,5 mm no ECG de entrada")
        t7 = st.checkbox("Marcadores de Necrose Miocárdica Elevados (Troponina positiva)")
        
        timi_score = sum([t1, t2, t3, t4, t5, t6, t7])
        st.markdown(f"**Pontuação TIMI Score:** **{timi_score} pontos**")
        
        if timi_score <= 2:
            st.success("✅ **Baixo Risco (0 - 2 pontos):** Mortalidade / IAM em 14 dias ~ 5-8%. Estratégia conservadora inicial.")
        elif timi_score <= 4:
            st.warning("⚠️ **Risco Intermediário (3 - 4 pontos):** Mortalidade / IAM em 14 dias ~ 13-20%. Estratégia invasiva precoce (< 24h).")
        else:
            st.error("🚨 **Alto Risco (5 - 7 pontos):** Mortalidade / IAM em 14 dias ~ 26-41%. Estratégia invasiva de urgência.")

# -----------------------------------------------------------------------------
# MÓDULO 8: GASOMETRIA ARTERIAL (NOVO)
# -----------------------------------------------------------------------------
elif modulo == "8. Gasometria Arterial & Ácido-Base":
    st.header("🫁 Interpretador de Gasometria Arterial & Resposta Compensatória")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        ph = st.number_input("pH Arterial", min_value=6.80, max_value=7.80, value=7.25, step=0.01)
        pco2 = st.number_input("pCO2 (mmHg)", min_value=10.0, max_value=120.0, value=28.0, step=1.0)
    with col2:
        hco3_g = st.number_input("HCO3- (mEq/L)", min_value=2.0, max_value=60.0, value=12.0, step=1.0)
        po2 = st.number_input("pO2 (mmHg)", min_value=20.0, max_value=500.0, value=85.0, step=1.0)
    with col3:
        sato2_g = st.number_input("SatO2 (%)", min_value=30.0, max_value=100.0, value=95.0, step=1.0)
        fio2 = st.number_input("FiO2 fornecida (%)", min_value=21.0, max_value=100.0, value=21.0, step=1.0)

    paO2_fio2 = po2 / (fio2 / 100.0)
    
    st.markdown("---")
    st.subheader("📊 Raciocínio Diagnóstico:")
    
    # 1. Distúrbio Primário
    if ph < 7.35:
        estado_ph = "ACIDEMIA"
    elif ph > 7.45:
        estado_ph = "ALCALEMIA"
    else:
        estado_ph = "pH NORMAL (ou Distúrbio Misto Compensado)"
        
    st.write(f"• **Status do pH:** **{estado_ph}** ({ph:.2f})")
    
    if ph < 7.35:
        if hco3_g < 22 and pco2 <= 40:
            disturbio = "Acidose Metabólica"
            pco2_esperada = (1.5 * hco3_g) + 8
            st.error(f"🔴 **Distúrbio Primário:** {disturbio}")
            st.info(f"💡 **Resposta Compensatória (Fórmula de Winter):** pCO2 esperada = **{pco2_esperada - 2:.1f} a {pco2_esperada + 2:.1f} mmHg**.")
            if pco2 < pco2_esperada - 2:
                st.warning("⚠️ pCO2 medida é MENOR que a esperada -> **Alcalose Respiratória Associada**.")
            elif pco2 > pco2_esperada + 2:
                st.warning("⚠️ pCO2 medida é MAIOR que a esperada -> **Acidose Respiratória Associada**.")
            else:
                st.success("✅ Resposta respiratória compensatória adequada.")
                
        elif pco2 > 45:
            disturbio = "Acidose Respiratória"
            st.error(f"🔴 **Distúrbio Primário:** {disturbio}")
            st.info("💡 Na acidose respiratória aguda, espera-se elevação de 1 mEq/L de HCO3 para cada 10 mmHg de pCO2 acima de 40.")

    elif ph > 7.45:
        if hco3_g > 26:
            disturbio = "Alcalose Metabólica"
            pco2_esp = hco3_g + 15
            st.error(f"🔵 **Distúrbio Primário:** {disturbio}")
            st.info(f"💡 pCO2 esperada ≈ HCO3 + 15 = **{pco2_esp - 2:.1f} a {pco2_esp + 2:.1f} mmHg**.")
        elif pco2 < 35:
            disturbio = "Alcalose Respiratória"
            st.error(f"🔵 **Distúrbio Primário:** {disturbio}")

    # PaO2 / FiO2
    st.write(f"• **Relação PaO2/FiO2:** **{paO2_fio2:.0f}**")
    if paO2_fio2 < 200:
        st.error("🚨 **Insuficiência Respiratória / SDRA Grave** (PaO2/FiO2 < 200). Indicada O2 alto fluxo ou VNI/IOT.")
    elif paO2_fio2 < 300:
        st.warning("⚠️ **Troca Gasosa Comprometida / SDRA Leve** (PaO2/FiO2 200-300).")

# -----------------------------------------------------------------------------
# MÓDULO 9: INSULINOTERAPIA HOSPITALAR (NOVO)
# -----------------------------------------------------------------------------
elif modulo == "9. Insulinoterapia Hospitalar (SBD 2026)":
    st.header("💉 Prescrição de Insulinoterapia Hospitalar & Correção (SBD 2026)")
    st.caption("Cálculo de Esquema Basal-Bolus e Correção Prandial para Enfermaria e CTI")
    
    col1, col2 = st.columns(2)
    with col1:
        peso_ins = st.number_input("Peso do Paciente (kg)", min_value=30.0, max_value=200.0, value=70.0)
        perfil_pac = st.selectbox("Perfil de Sensibilidade:", ["Sensível / Idoso / DRC (0,3 UI/kg/dia)", "Usual / Eutrófico (0,4 a 0,5 UI/kg/dia)", "Resistente / Obeso / Corticoide (0,6 UI/kg/dia)"])
    with col2:
        glicemia_hosp = st.number_input("Glicemia Capilar Atual (mg/dL)", min_value=40.0, max_value=600.0, value=240.0, step=10.0)
        opcao_calc = st.radio("Cálculo Pretendido:", ["Dose Total Diária Basal-Bolus", "Escala de Correção Prandial"])

    if "0,3 UI" in perfil_pac:
        fator_d = 0.3
    elif "0,4" in perfil_pac:
        fator_d = 0.45
    else:
        fator_d = 0.6
        
    dtd = peso_ins * fator_d
    dose_basal = dtd * 0.5
    dose_bolus_total = dtd * 0.5
    dose_refeicao = dose_bolus_total / 3.0

    if opcao_calc == "Dose Total Diária Basal-Bolus":
        st.markdown("---")
        st.subheader(f"📋 Esquema Inicial Basal-Bolus Calculado (DTD = {dtd:.0f} UI/dia):")
        
        st.success(f"1. **Insulina Basal (50% = {dose_basal:.0f} UI/dia):**")
        st.write(f"   • **Glargina U100:** **{dose_basal:.0f} UI** SC 1x/dia à noite.")
        st.write(f"   • **OU NPH:** **{dose_basal * 0.66:.0f} UI** de manhã + **{dose_basal * 0.33:.0f} UI** à noite (2/3 manhã, 1/3 noite).")
        
        st.info(f"2. **Insulina Prandial / Bolus (50% = {dose_bolus_total:.0f} UI/dia dividida em 3 refeições):**")
        st.write(f"   • **Lispro / Aspart / Regular:** **{dose_refeicao:.0f} UI** SC antes do Café, Almoço e Jantar.")

    else:
        st.markdown("---")
        st.subheader("📊 Fator de Sensibilidade & Correção de Hiperglicemia:")
        fs = 1800 / dtd if dtd > 0 else 40
        og = 130.0
        
        if glicemia_hosp > og:
            bolus_corr = (glicemia_hosp - og) / fs
        else:
            bolus_corr = 0.0
            
        c1, c2, c3 = st.columns(3)
        c1.metric("Fator de Sensibilidade (FS)", f"{fs:.0f} mg/dL por 1 UI")
        c2.metric("Glicemia Atual vs. Alvo (130)", f"{glicemia_hosp:.0f} mg/dL")
        c3.metric("Bolus de Correção Indicado", f"{bolus_corr:.1f} UI")
        
        st.info(f"💡 **Conduta:** Aplicar **{math.ceil(bolus_corr)} UI** de Insulina Rápida/Ultrarrápida SC para corrigir a glicemia atual de {glicemia_hosp:.0f} mg/dL.")

# -----------------------------------------------------------------------------
# MÓDULO 10: DOSES PEDIÁTRICAS
# -----------------------------------------------------------------------------
elif modulo == "10. Doses Pediátricas por Peso":
    st.header("👶 Calculadora de Prescrição Pediátrica Rápida")
    
    peso_ped = st.number_input("Peso da Criança (kg)", min_value=2.0, max_value=60.0, value=15.0, step=0.5)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Analgésicos / Antitérmicos")
        gotas_dipirona = int(round(peso_ped))
        st.write(f"• **Dipirona 500 mg/mL (Gotas):** **{gotas_dipirona} gotas** de 6/6h (se dor/febre).")
        gotas_ibu = int(round(peso_ped))
        st.write(f"• **Ibuprofeno 100 mg/mL (Gotas):** **{gotas_ibu} gotas** de 8/8h (máx 40 gotas).")
        gotas_para = int(round(peso_ped))
        st.write(f"• **Paracetamol 200 mg/mL (Gotas):** **{gotas_para} gotas** de 6/6h (máx 35 gotas).")

    with col2:
        st.subheader("Antibióticos & Corticoides")
        ml_amox = peso_ped / 3.0
        st.write(f"• **Amoxicilina 250 mg/5 mL:** **{ml_amox:.1f} mL** de 8/8h por 7 a 10 dias.")
        ml_pred = peso_ped / 3.0
        st.write(f"• **Prednisolona 3 mg/mL (Solução):** **{ml_pred:.1f} mL** 1x/dia pela manhã por 5 dias.")

# -----------------------------------------------------------------------------
# MÓDULO 11: ESCORES CRÍTICOS
# -----------------------------------------------------------------------------
elif modulo == "11. Escores Críticos (CURB-65 & qSOFA)":
    st.header("🧮 Escores de Risco e Severidade")
    
    st.subheader("1. CURB-65 (Pneumonia Adquirida na Comunidade)")
    c1 = st.checkbox("C - Confusão mental (GCS < 15)")
    c2 = st.checkbox("U - Ureia > 50 mg/dL (ou BUN > 19 mg/dL)")
    c3 = st.checkbox("R - Frequência Respiratória >= 30 irpm")
    c4 = st.checkbox("B - Pressão Arterial Sistólica < 90 mmHg ou Diastólica <= 60 mmHg")
    c5 = st.checkbox("65 - Idade >= 65 anos")
    
    curb_score = sum([c1, c2, c3, c4, c5])
    st.markdown(f"**Pontuação CURB-65:** **{curb_score} ponto(s)**")
    
    if curb_score <= 1:
        st.success("✅ Risco baixo (Mortalidade < 1,5%). Conduta: Tratamento Ambulatorial.")
    elif curb_score == 2:
        st.warning("⚠️ Risco moderado (Mortalidade ~ 9,2%). Conduta: Considerar Internação Hospitalar / Enfermaria.")
    else:
        st.error("🚨 Risco elevado (Mortalidade > 22%). Conduta: Internação Hospitalar (Avaliar UTI se score >= 4).")
        
    st.markdown("---")
    st.subheader("2. qSOFA (Triagem Rápida de Sepse)")
    q1 = st.checkbox("Frequência Respiratória >= 22 irpm")
    q2 = st.checkbox("Alteração do Nível de Consciência (GCS < 15)")
    q3 = st.checkbox("Pressão Arterial Sistólica <= 100 mmHg")
    
    qsofa_score = sum([q1, q2, q3])
    st.markdown(f"**Pontuação qSOFA:** **{qsofa_score} ponto(s)**")
    
    if qsofa_score >= 2:
        st.error("🚨 **qSOFA POSITIVO (>= 2 pontos)**: Alto risco de desfecho desfavorável/ICU. Coletar Lactato, Hemoculturas, iniciar Antibiótico na 1ª hora e volume de 30 mL/kg de cristaloide se hipotensão.")
    else:
        st.info("qSOFA < 2 pontos. Manter monitorização contínua e reavaliar se piora clínica.")

    st.markdown("---")
    st.subheader("3. NEWS2 (National Early Warning Score 2)")
    st.caption("Escala de alerta clínico baseada em sinais vitais. A Escala 2 de SpO₂ deve ser usada somente quando indicada pelo protocolo clínico para insuficiência respiratória hipercápnica.")

    news2_escala_spo2 = st.radio(
        "Escala de SpO₂ do NEWS2:",
        ["Escala 1 (padrão)", "Escala 2 (hipercapnia, se indicada)"],
        key="news2_escala_spo2"
    )

    news_col1, news_col2, news_col3 = st.columns(3)
    with news_col1:
        news2_fr = st.number_input("Frequência Respiratória (irpm)", min_value=1, max_value=80, value=16, step=1, key="news2_fr")
        news2_spo2 = st.number_input("SpO₂ (%)", min_value=50, max_value=100, value=98, step=1, key="news2_spo2")
    with news_col2:
        news2_o2 = st.selectbox("Oxigênio suplementar:", ["Não", "Sim"], key="news2_o2")
        news2_temp = st.number_input("Temperatura (°C)", min_value=25.0, max_value=45.0, value=36.5, step=0.1, key="news2_temp")
    with news_col3:
        news2_pas = st.number_input("Pressão Arterial Sistólica (mmHg)", min_value=40, max_value=300, value=120, step=1, key="news2_pas")
        news2_fc = st.number_input("Frequência Cardíaca (bpm)", min_value=20, max_value=250, value=80, step=1, key="news2_fc")

    news2_consciencia = st.selectbox(
        "Nível de consciência (ACVPU):",
        ["Alerta (A)", "Confusão nova (C)", "Responde à voz (V)", "Responde à dor (P)", "Não responde (U)"],
        key="news2_consciencia"
    )

    # Pontuação NEWS2 conforme os intervalos do RCP. Qualquer C, V, P ou U = 3 pontos.
    if news2_fr <= 8:
        news2_fr_score = 3
    elif news2_fr <= 11:
        news2_fr_score = 1
    elif news2_fr <= 20:
        news2_fr_score = 0
    elif news2_fr <= 24:
        news2_fr_score = 2
    else:
        news2_fr_score = 3

    if news2_escala_spo2 == "Escala 1 (padrão)":
        if news2_spo2 <= 91:
            news2_spo2_score = 3
        elif news2_spo2 <= 93:
            news2_spo2_score = 2
        elif news2_spo2 <= 95:
            news2_spo2_score = 1
        else:
            news2_spo2_score = 0
    else:
        if news2_spo2 <= 83:
            news2_spo2_score = 3
        elif news2_spo2 <= 85:
            news2_spo2_score = 2
        elif news2_spo2 <= 87:
            news2_spo2_score = 1
        elif news2_spo2 <= 92:
            news2_spo2_score = 0
        elif news2_spo2 <= 94:
            news2_spo2_score = 1
        elif news2_spo2 <= 96:
            news2_spo2_score = 2
        else:
            news2_spo2_score = 3

    news2_o2_score = 2 if news2_o2 == "Sim" else 0

    if news2_temp <= 35.0:
        news2_temp_score = 3
    elif news2_temp <= 36.0:
        news2_temp_score = 1
    elif news2_temp <= 38.0:
        news2_temp_score = 0
    elif news2_temp <= 39.0:
        news2_temp_score = 1
    else:
        news2_temp_score = 2

    if news2_pas <= 90:
        news2_pas_score = 3
    elif news2_pas <= 100:
        news2_pas_score = 2
    elif news2_pas <= 110:
        news2_pas_score = 1
    elif news2_pas <= 219:
        news2_pas_score = 0
    else:
        news2_pas_score = 3

    if news2_fc <= 40:
        news2_fc_score = 3
    elif news2_fc <= 50:
        news2_fc_score = 1
    elif news2_fc <= 90:
        news2_fc_score = 0
    elif news2_fc <= 110:
        news2_fc_score = 1
    elif news2_fc <= 130:
        news2_fc_score = 2
    else:
        news2_fc_score = 3

    news2_consciencia_score = 0 if news2_consciencia == "Alerta (A)" else 3
    news2_componentes = [
        news2_fr_score, news2_spo2_score, news2_o2_score,
        news2_temp_score, news2_pas_score, news2_fc_score,
        news2_consciencia_score
    ]
    news2_total = sum(news2_componentes)
    news2_maior_componente = max(news2_componentes)

    st.markdown(f"**Pontuação NEWS2:** **{news2_total} ponto(s)**")
    st.caption(
        f"Componentes: FR {news2_fr_score}, SpO₂ {news2_spo2_score}, O₂ {news2_o2_score}, "
        f"temperatura {news2_temp_score}, PAS {news2_pas_score}, FC {news2_fc_score}, "
        f"consciência {news2_consciencia_score}."
    )

    if news2_total >= 7:
        st.error("🚨 **NEWS2 alto (≥ 7):** necessidade de avaliação clínica imediata e escalonamento conforme protocolo institucional.")
    elif news2_total >= 5 or news2_maior_componente >= 3:
        st.warning("⚠️ **NEWS2 com risco aumentado:** realizar avaliação clínica urgente e aumentar a frequência de monitorização conforme protocolo.")
    elif news2_total >= 1:
        st.info("NEWS2 baixo, porém diferente de zero: manter vigilância e reavaliar a tendência dos sinais vitais.")
    else:
        st.success("NEWS2 = 0: sem alterações pontuáveis neste momento; manter avaliação clínica habitual.")

    st.markdown("---")
    st.subheader("4. MEWS (Modified Early Warning Score)")
    st.caption("Versão clínica de cinco parâmetros: PAS, frequência cardíaca, frequência respiratória, temperatura e escala AVPU. Faixas de conduta podem variar conforme o protocolo institucional.")

    mews_col1, mews_col2, mews_col3 = st.columns(3)
    with mews_col1:
        mews_pas = st.number_input("PAS (mmHg)", min_value=40, max_value=300, value=120, step=1, key="mews_pas")
        mews_fc = st.number_input("Frequência Cardíaca (bpm)", min_value=20, max_value=250, value=80, step=1, key="mews_fc")
    with mews_col2:
        mews_fr = st.number_input("Frequência Respiratória (irpm)", min_value=1, max_value=80, value=16, step=1, key="mews_fr")
        mews_temp = st.number_input("Temperatura (°C)", min_value=25.0, max_value=45.0, value=36.5, step=0.1, key="mews_temp")
    with mews_col3:
        mews_avpu = st.selectbox(
            "Nível de consciência (AVPU):",
            ["Alerta (A)", "Responde à voz (V)", "Responde à dor (P)", "Não responde (U)"],
            key="mews_avpu"
        )

    if mews_pas >= 200:
        mews_pas_score = 2
    elif mews_pas >= 101:
        mews_pas_score = 0
    elif mews_pas >= 81:
        mews_pas_score = 1
    elif mews_pas >= 71:
        mews_pas_score = 2
    else:
        mews_pas_score = 3

    if mews_fc < 40:
        mews_fc_score = 2
    elif mews_fc <= 50:
        mews_fc_score = 1
    elif mews_fc <= 100:
        mews_fc_score = 0
    elif mews_fc <= 110:
        mews_fc_score = 1
    elif mews_fc <= 129:
        mews_fc_score = 2
    else:
        mews_fc_score = 3

    if mews_fr < 9:
        mews_fr_score = 2
    elif mews_fr <= 14:
        mews_fr_score = 0
    elif mews_fr <= 20:
        mews_fr_score = 1
    elif mews_fr <= 29:
        mews_fr_score = 2
    else:
        mews_fr_score = 3

    if mews_temp < 35.0:
        mews_temp_score = 2
    elif mews_temp <= 38.4:
        mews_temp_score = 0
    else:
        mews_temp_score = 2

    mews_avpu_score = ["Alerta (A)", "Responde à voz (V)", "Responde à dor (P)", "Não responde (U)"].index(mews_avpu)
    mews_total = sum([mews_pas_score, mews_fc_score, mews_fr_score, mews_temp_score, mews_avpu_score])

    st.markdown(f"**Pontuação MEWS:** **{mews_total} ponto(s)**")
    st.caption(
        f"Componentes: PAS {mews_pas_score}, FC {mews_fc_score}, FR {mews_fr_score}, "
        f"temperatura {mews_temp_score}, AVPU {mews_avpu_score}."
    )

    if mews_total >= 5:
        st.error("🚨 **MEWS ≥ 5:** alto risco de deterioração clínica; avaliação imediata e escalonamento conforme protocolo institucional.")
    elif mews_total >= 3:
        st.warning("⚠️ **MEWS 3–4:** risco aumentado; reavaliar o paciente e intensificar a monitorização conforme protocolo.")
    else:
        st.success("MEWS 0–2: manter monitorização e reavaliar conforme a evolução clínica.")

# -----------------------------------------------------------------------------
# MÓDULO 12: DENGUE
# -----------------------------------------------------------------------------
elif modulo == "12. Dengue - Manejo Volêmico (MS)":
    st.header("🦟 Classificação e Hidratação na Dengue (Ministério da Saúde)")
    
    peso_dengue = st.number_input("Peso do Paciente (kg)", min_value=10.0, max_value=200.0, value=70.0, step=1.0)
    
    grupo = st.radio(
        "Selecione o Grupo de Risco:",
        ["Grupo A (Sem sinais de alarme, sem comorbidades)",
         "Grupo B (Sem sinais de alarme, COM comorbidades/gestante/idoso ou Prova do Laço +)",
         "Grupo C (COM SINAIS DE ALARME: dor abd. intensa, vômitos, hipotensão, hematócrito em elevação)",
         "Grupo D (CHOQUE / Sinais de gravidade: pulso fraco, TEC > 3s, hipotensão grave)"]
    )
    
    if "Grupo A" in grupo:
        st.success("✅ **Grupo A (Tratamento Ambulatorial):**")
        st.write(f"• Hidratação Oral: 60 mL/kg/dia (Total: **{peso_dengue * 60:.0f} mL/dia**), sendo 1/3 em Soro de Reidratação Oral (SRO) e 2/3 em líquidos caseiros.")
        st.write("• Sintomáticos: Dipirona ou Paracetamol. **PROSCRITO AINEs e Salicilatos!**")
        
    elif "Grupo B" in grupo:
        st.warning("⚠️ **Grupo B (Atendimento na Unidade com Leito de Observação):**")
        st.write("• Solicitar Hemograma de urgência.")
        st.write(f"• Iniciar hidratação oral supervisionada enquanto aguarda Htc (60 mL/kg/dia = **{peso_dengue * 60:.0f} mL/dia**).")
        st.write("• Se Htc normal: conduta do Grupo A com reavaliação diária.")
        st.write("• Se Htc elevado: iniciar hidratação parenteral como no Grupo C.")

    elif "Grupo C" in grupo:
        st.error("🚨 **Grupo C (INTERNAÇÃO HOSPITALAR / LEITO DE OBSERVAÇÃO):**")
        st.write("• **Fase de Expansão Volêmica EV:** Ringer Lactato ou SF 0,9%: **10 mg/kg na 1ª hora**.")
        fase1 = peso_dengue * 10
        st.write(f"👉 **Volume na 1ª hora:** **{fase1:.0f} mL EV**.")
        st.write("• Reavaliar clinicamente e repeti Htc em 2 horas. Repetir fase de expansão até 3 vezes se necessário.")

    elif "Grupo D" in grupo:
        st.error("🚨 **Grupo D (EMERGÊNCIA / LEITO DE UTI):**")
        st.write("• **Ressuscitação Volêmica Imediata:** Ringer Lactato ou SF 0,9%: **20 mL/kg em 20 minutos**.")
        fase_d = peso_dengue * 20
        st.write(f"👉 **Bolus imediato:** **{fase_d:.0f} mL EV em 20 minutos**.")
        st.write("• Repetir até 3 vezes conforme resposta hemodinâmica. Se refratário, iniciar Vasopressoria (Noradrenalina).")

# -----------------------------------------------------------------------------
# MÓDULO 13: QUEIMADURA
# -----------------------------------------------------------------------------
elif modulo == "13. Queimaduras (Regra de Parkland)":
    st.header("🔥 Hidratação no Paciente Queimado (Fórmula de Parkland)")
    
    peso_q = st.number_input("Peso do Paciente (kg)", min_value=10.0, max_value=200.0, value=70.0, step=1.0)
    scq = st.number_input("Superfície Corporal Queimada - SCQ (%)", min_value=1.0, max_value=100.0, value=20.0, step=1.0)
    
    vol_total = 4.0 * peso_q * scq
    vol_8h = vol_total / 2.0
    vol_16h = vol_total / 2.0
    
    st.markdown("---")
    st.metric("Volume Total de Ringer Lactato (24h)", f"{vol_total:.0f} mL")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"⏱️ **Primeiras 8 horas:** **{vol_8h:.0f} mL** (Vazão: **{vol_8h / 8.0:.1f} mL/h**)")
    with col2:
        st.info(f"⏱️ **Próximas 16 horas:** **{vol_16h:.0f} mL** (Vazão: **{vol_16h / 16.0:.1f} mL/h**)")
    
    st.caption("Nota: Contar as 8 horas a partir do momento do acidente, não da chegada ao hospital. Ajustar conforme diurese (alvo 0,5 a 1,0 mL/kg/h em adultos).")
