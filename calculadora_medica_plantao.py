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
        "13. Queimaduras (Regra de Parkland)",
        "14. Prognóstico em UTI (APACHE IV / SAPS 3)",
        "15. Tromboembolismo Venoso (Caprini / Worcester)",
        "16. Abdome Agudo e Líquidos (GBS, pancreatite, Tokyo, Alvarado, Light, ADA, GASA)",
        "17. Acompanhamento Ambulatorial e Geriatria",
        "18. Resistência Antimicrobiana (Ambler e MRSA)",
        "19. Interpretação de Sorologias",
        "20. Injúria Renal Aguda — Urina e Eletrólitos",
        "21. Soro de Manutenção por Peso"
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
        st.subheader("Noradrenalina — selecione apresentação e diluição")
        apresentacao = st.selectbox("Apresentação disponível:", ["4 mg/4 mL", "8 mg/8 mL", "2 mg/2 mL"], key="nora_apresentacao")
        diluicao = st.selectbox("Diluição final:", ["1 ampola em 250 mL", "2 ampolas em 250 mL", "4 ampolas em 250 mL"], key="nora_diluicao")
        mg_amp = {"4 mg/4 mL": 4.0, "8 mg/8 mL": 8.0, "2 mg/2 mL": 2.0}[apresentacao]
        n_amp = {"1 ampola em 250 mL": 1, "2 ampolas em 250 mL": 2, "4 ampolas em 250 mL": 4}[diluicao]
        conc = (mg_amp * n_amp * 1000) / 250
        st.write(f"Concentração calculada: **{conc:.1f} mcg/mL** (confirmar volume final real da preparação).")
        dose_target = st.slider("Dose desejada (mcg/kg/min)", 0.01, 2.00, 0.10, 0.01, key="nora_dose")
        vazao_mlh = (dose_target * peso * 60) / conc
        st.success(f"📌 Vazão na bomba: **{vazao_mlh:.1f} mL/h**")

    elif drogas == "Nitroglicerina (Tridil)":
        st.subheader("Nitroglicerina — selecione apresentação e diluição")
        apresentacao = st.selectbox("Apresentação disponível:", ["25 mg/5 mL", "50 mg/10 mL"], key="tridil_apresentacao")
        volume_final = st.number_input("Volume final da seringa/bolsa (mL)", 50.0, 1000.0, 250.0, step=10.0, key="tridil_volume")
        mg_total = {"25 mg/5 mL": 25.0, "50 mg/10 mL": 50.0}[apresentacao]
        conc = mg_total * 1000 / volume_final
        st.write(f"Concentração calculada: **{conc:.1f} mcg/mL**. Proteger conforme protocolo do produto.")
        dose_mcg_min = st.slider("Dose desejada (mcg/min)", 5.0, 200.0, 10.0, 5.0, key="tridil_dose")
        vazao_mlh = (dose_mcg_min * 60) / conc
        st.success(f"📌 Vazão na bomba: **{vazao_mlh:.1f} mL/h**")

    elif drogas == "Nitroprussiato de Sódio (Nipride)":
        st.subheader("Nitroprussiato — selecione apresentação e diluição")
        apresentacao = st.selectbox("Apresentação disponível:", ["50 mg/2 mL", "50 mg/5 mL"], key="nipride_apresentacao")
        volume_final = st.number_input("Volume final da bolsa (mL)", 50.0, 1000.0, 250.0, step=10.0, key="nipride_volume")
        mg_total = 50.0
        conc = mg_total * 1000 / volume_final
        st.write(f"Concentração calculada: **{conc:.1f} mcg/mL**. Proteger da luz.")
        dose_target = st.slider("Dose desejada (mcg/kg/min)", 0.25, 10.00, 0.50, 0.25, key="nipride_dose")
        vazao_mlh = (dose_target * peso * 60) / conc
        st.success(f"📌 Vazão na bomba: **{vazao_mlh:.1f} mL/h**")
        if dose_target > 3.0:
            st.warning("Risco de toxicidade por cianeto/tiocianato em doses altas ou uso prolongado; monitorar conforme protocolo.")

    elif drogas == "Dopamina":
        st.subheader("Dopamina — selecione apresentação e diluição")
        apresentacao = st.selectbox("Apresentação disponível:", ["50 mg/10 mL", "200 mg/5 mL"], key="dopamina_apresentacao")
        volume_final = st.number_input("Volume final da bolsa (mL)", 50.0, 1000.0, 250.0, step=10.0, key="dopamina_volume")
        mg_total = {"50 mg/10 mL": 50.0, "200 mg/5 mL": 200.0}[apresentacao]
        ampolas = st.number_input("Número de ampolas/frascos", 1, 10, 5, key="dopamina_ampolas")
        conc = mg_total * ampolas * 1000 / volume_final
        st.write(f"Concentração calculada: **{conc:.1f} mcg/mL**.")
        dose_target = st.slider("Dose desejada (mcg/kg/min)", 2.0, 20.0, 5.0, 0.5, key="dopamina_dose")
        vazao_mlh = (dose_target * peso * 60) / conc
        st.success(f"📌 Vazão na bomba: **{vazao_mlh:.1f} mL/h**")

    elif drogas == "Dobutamina":
        st.subheader("Dobutamina — selecione apresentação e diluição")
        apresentacao = st.selectbox("Apresentação disponível:", ["250 mg/20 mL", "250 mg/5 mL", "100 mg/10 mL"], key="dobutamina_apresentacao")
        volume_final = st.number_input("Volume final da bolsa/seringa (mL)", 50.0, 1000.0, 250.0, step=10.0, key="dobutamina_volume")
        mg_total = {"250 mg/20 mL": 250.0, "250 mg/5 mL": 250.0, "100 mg/10 mL": 100.0}[apresentacao]
        ampolas = st.number_input("Número de ampolas/frascos", 1, 10, 1, key="dobutamina_ampolas")
        conc = mg_total * ampolas * 1000 / volume_final
        st.write(f"Concentração calculada: **{conc:.1f} mcg/mL**.")
        dose_target = st.slider("Dose desejada (mcg/kg/min)", 2.5, 20.0, 5.0, 0.5, key="dobutamina_dose")
        vazao_mlh = (dose_target * peso * 60) / conc
        st.success(f"📌 Vazão na bomba: **{vazao_mlh:.1f} mL/h**")

    st.warning("Conferir concentração, volume final, compatibilidade, via central/periférica, bomba, monitorização e protocolo institucional antes da administração. O cálculo não substitui checagem independente.")

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

    st.markdown("---")
    st.subheader("ABCD2 — risco após AIT")
    st.caption("Regra auxiliar em adultos; não deve definir alta ou urgência isoladamente. A investigação especializada de AIT não deve ser atrasada.")
    abcd_idade = st.number_input("Idade (anos)", min_value=1, max_value=120, value=65, key="abcd_idade")
    abcd_pas = st.number_input("PA sistólica inicial (mmHg)", min_value=40, max_value=300, value=140, key="abcd_pas")
    abcd_pad = st.number_input("PA diastólica inicial (mmHg)", min_value=20, max_value=200, value=90, key="abcd_pad")
    abcd_clinica = st.selectbox("Características clínicas", ["Sem fraqueza ou alteração da fala", "Alteração da fala sem fraqueza", "Fraqueza unilateral"], key="abcd_clinica")
    abcd_duracao = st.selectbox("Duração dos sintomas", ["<10 min", "10–59 min", "≥60 min"], key="abcd_duracao")
    abcd_diabetes = st.checkbox("Diabetes mellitus", key="abcd_diabetes")
    abcd_score = (1 if abcd_idade >= 60 else 0) + (1 if abcd_pas >= 140 or abcd_pad >= 90 else 0)
    abcd_score += 2 if abcd_clinica == "Fraqueza unilateral" else 1 if abcd_clinica == "Alteração da fala sem fraqueza" else 0
    abcd_score += 2 if abcd_duracao == "≥60 min" else 1 if abcd_duracao == "10–59 min" else 0
    abcd_score += 1 if abcd_diabetes else 0
    st.metric("ABCD2", f"{abcd_score}/7")
    st.info("Pontuação maior indica maior risco observado em coortes, mas o ABCD2 tem discriminação limitada e não substitui avaliação neurológica, imagem vascular, ECG e investigação etiológica.")

# -----------------------------------------------------------------------------
# MÓDULO 7: RISCO CORONARIANO (HEART & TIMI) (NOVO)
# -----------------------------------------------------------------------------
elif modulo == "7. Risco Coronariano (HEART & TIMI Score)":
    st.header("🫀 Escores de Risco para Síndrome Coronariana Aguda (SCA)")
    
    escore_tipo = st.radio("Selecione o Escore:", [
        "HEART Score (Dor Torácica no PS)",
        "TIMI Risk Score (SCA sem Supra)",
        "GRACE clássico (SCA - risco intra-hospitalar)"
    ])
    
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

    elif escore_tipo == "TIMI Risk Score (SCA sem Supra)":
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

    else:
        st.subheader("GRACE clássico de admissão (Global Registry of Acute Coronary Events)")
        st.caption("Modelo prognóstico publicado para SCA. Esta é a tabela clássica intra-hospitalar; não é GRACE 2.0, que usa funções não lineares e coeficientes específicos.")
        grace_col1, grace_col2, grace_col3 = st.columns(3)
        with grace_col1:
            grace_idade = st.number_input("Idade (anos)", min_value=18, max_value=120, value=65, key="grace_idade")
            grace_fc = st.number_input("Frequência cardíaca (bpm)", min_value=20, max_value=250, value=80, key="grace_fc")
        with grace_col2:
            grace_pas = st.number_input("Pressão arterial sistólica (mmHg)", min_value=40, max_value=300, value=120, key="grace_pas")
            grace_creat = st.number_input("Creatinina sérica (mg/dL)", min_value=0.1, max_value=20.0, value=1.0, step=0.1, key="grace_creat")
        with grace_col3:
            grace_killip = st.selectbox("Classe Killip", ["I - sem IC", "II - IC leve", "III - edema pulmonar", "IV - choque"], key="grace_killip")
            grace_parada = st.checkbox("Parada cardíaca na admissão", key="grace_parada")
            grace_st = st.checkbox("Desvio do segmento ST", key="grace_st")
            grace_biom = st.checkbox("Biomarcador cardíaco elevado", key="grace_biom")

        def grace_faixa(valor, faixas):
            for limite, pontos in faixas:
                if valor <= limite:
                    return pontos
            return faixas[-1][1]

        grace_pontos = 0
        grace_pontos += grace_faixa(grace_idade, [(29, 0), (39, 8), (49, 25), (59, 41), (69, 58), (79, 75), (89, 91), (120, 100)])
        grace_pontos += grace_faixa(grace_fc, [(49, 0), (69, 3), (89, 9), (109, 15), (149, 24), (199, 38), (250, 46)])
        grace_pontos += 58 if grace_pas < 80 else 53 if grace_pas < 100 else 43 if grace_pas < 120 else 34 if grace_pas < 140 else 24 if grace_pas < 160 else 10 if grace_pas < 200 else 0
        grace_pontos += 1 if grace_creat < 0.4 else 4 if grace_creat < 0.8 else 7 if grace_creat < 1.2 else 10 if grace_creat < 1.6 else 13 if grace_creat < 2.0 else 21 if grace_creat < 4.0 else 28
        grace_pontos += [0, 20, 39, 59][["I - sem IC", "II - IC leve", "III - edema pulmonar", "IV - choque"].index(grace_killip)]
        grace_pontos += 39 if grace_parada else 0
        grace_pontos += 28 if grace_st else 0
        grace_pontos += 14 if grace_biom else 0
        st.metric("GRACE clássico", f"{grace_pontos} pontos")
        if grace_pontos < 109:
            st.success("Baixo risco intra-hospitalar: mortalidade estimada tradicionalmente <1%. Não substitui ECG, troponina seriada ou julgamento clínico.")
        elif grace_pontos <= 140:
            st.warning("Risco intermediário: mortalidade estimada tradicionalmente em torno de 1–3%. Usar junto à avaliação completa da SCA.")
        else:
            st.error("Alto risco: mortalidade estimada tradicionalmente >3%; em NSTE-ACS, GRACE >140 pode apoiar estratégia invasiva precoce, sem atrasar cuidados emergentes.")
        st.info("Para GRACE 2.0, use uma calculadora validada: não é correto chamar esta soma clássica de GRACE 2.0.")

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

    # Ânion gap e delta gap para interpretação ácido-base
    st.markdown("### Ânion gap e interpretação")
    ag_na = st.number_input("Sódio para ânion gap (mEq/L)", min_value=80.0, max_value=200.0, value=140.0, key="ag_na")
    ag_cl = st.number_input("Cloro para ânion gap (mEq/L)", min_value=40.0, max_value=160.0, value=104.0, key="ag_cl")
    ag_hco3 = st.number_input("Bicarbonato para ânion gap (mEq/L)", min_value=2.0, max_value=60.0, value=24.0, key="ag_hco3")
    ag_albumina = st.number_input("Albumina (g/dL; opcional para correção)", min_value=1.0, max_value=6.0, value=4.0, step=0.1, key="ag_albumina")
    anion_gap_calc = ag_na - (ag_cl + ag_hco3)
    ag_corrigido = anion_gap_calc + 2.5 * (4.0 - ag_albumina)
    delta_ag = ag_corrigido - 12.0
    delta_hco3 = 24.0 - ag_hco3
    st.write(f"**Ânion gap:** {anion_gap_calc:.1f} mEq/L | **Corrigido pela albumina:** {ag_corrigido:.1f} mEq/L")
    if ag_corrigido > 12:
        st.warning("Ânion gap elevado: sugere acúmulo de ânions não mensurados. Correlacionar com lactato, cetonas, função renal, toxinas e evolução clínica.")
        if delta_ag - delta_hco3 > 6:
            st.info("Delta-delta alto: considerar alcalose metabólica concomitante.")
        elif delta_ag - delta_hco3 < -6:
            st.info("Delta-delta baixo: considerar acidose metabólica hiperclorêmica concomitante.")
    elif ag_corrigido < 8:
        st.info("Ânion gap baixo: considerar hipoalbuminemia, paraproteinemia, erro laboratorial ou outras causas.")
    else:
        st.success("Ânion gap dentro da faixa usual (interpretar conforme o laboratório e a albumina).")

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

    st.markdown("---")
    st.subheader("Outras medicações pediátricas comuns — referência por peso")
    st.warning("Use apenas como referência educacional. Confirmar idade, indicação, concentração, via, dose máxima, função renal/hepática e protocolo institucional antes de administrar.")
    ped_med = st.selectbox("Selecione a medicação", [
        "Paracetamol (10–15 mg/kg/dose)", "Ibuprofeno (5–10 mg/kg/dose; >6 meses)",
        "Ondansetrona (0,15 mg/kg/dose; máximo 8 mg)", "Dexametasona (0,15–0,6 mg/kg/dose)",
        "Ceftriaxona (50–75 mg/kg/dia; indicação dependente)", "Amoxicilina (40–90 mg/kg/dia; dividida)",
        "Salbutamol inalatório (seguir dispositivo/protocolo)", "Adrenalina IM na anafilaxia (0,01 mg/kg; máximo 0,5 mg)"
    ], key="ped_med")
    ped_ranges = {
        "Paracetamol (10–15 mg/kg/dose)": (10.0, 15.0, 75.0, "mg/dose"),
        "Ibuprofeno (5–10 mg/kg/dose; >6 meses)": (5.0, 10.0, 40.0, "mg/dose"),
        "Ondansetrona (0,15 mg/kg/dose; máximo 8 mg)": (0.15, 0.15, 8.0, "mg/dose"),
        "Dexametasona (0,15–0,6 mg/kg/dose)": (0.15, 0.6, 16.0, "mg/dose"),
        "Ceftriaxona (50–75 mg/kg/dia; indicação dependente)": (50.0, 75.0, 4000.0, "mg/dia"),
        "Amoxicilina (40–90 mg/kg/dia; dividida)": (40.0, 90.0, 4000.0, "mg/dia"),
        "Salbutamol inalatório (seguir dispositivo/protocolo)": (0.0, 0.0, 0.0, "não calcular sem apresentação"),
        "Adrenalina IM na anafilaxia (0,01 mg/kg; máximo 0,5 mg)": (0.01, 0.01, 0.5, "mg/dose")
    }
    ped_min, ped_max, ped_teto, ped_unidade = ped_ranges[ped_med]
    if ped_min > 0:
        ped_dose_min = min(peso_ped * ped_min, ped_teto)
        ped_dose_max = min(peso_ped * ped_max, ped_teto)
        st.info(f"Faixa calculada: **{ped_dose_min:.2f}–{ped_dose_max:.2f} {ped_unidade}** para {peso_ped:.1f} kg (teto considerado: {ped_teto:g}).")
    else:
        st.info("Para salbutamol, selecione a apresentação e siga a tabela/protocolo pediátrico local; não há uma dose única segura para todas as apresentações.")

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
# MÓDULO 14: PROGNÓSTICO EM UTI
# -----------------------------------------------------------------------------
elif modulo == "14. Prognóstico em UTI (APACHE IV / SAPS 3)":
    st.header("📈 Prognóstico em UTI")
    st.warning("APACHE IV completo é um modelo proprietário e complexo; esta interface não o chama de APACHE IV calculado. Use plataforma licenciada/validada para probabilidade de mortalidade.")
    prognostico_tipo = st.radio("Escolha o instrumento", ["SAPS 3 — cálculo global publicado", "APACHE IV — checklist de completude"], key="prognostico_tipo")
    if prognostico_tipo == "SAPS 3 — cálculo global publicado":
        st.caption("O SAPS 3 deve usar dados da admissão na UTI, aproximadamente na janela de ±1 hora, não os piores valores de 24 horas. A equação global abaixo é uma aproximação da publicação e precisa de validação local.")
        saps_idade = st.number_input("Idade (anos)", 18, 120, 65, key="saps_idade")
        saps_total = st.number_input("SAPS 3 total (20 variáveis preenchidas)", 0.0, 250.0, 50.0, step=1.0, key="saps_total")
        saps_logit = -32.6659 + 7.3068 * math.log(saps_total + 20.5958)
        saps_prob = 100 * math.exp(saps_logit) / (1 + math.exp(saps_logit)) if saps_logit < 700 else 100.0
        st.metric("Probabilidade global publicada de mortalidade hospitalar", f"{saps_prob:.1f}%")
        st.info("Para calcular o SAPS 3 total, preencher idade, comorbidades, localização e tempo pré-UTI, circunstâncias/diagnóstico da admissão e fisiologia. Não preencher dados ausentes com zero.")
        st.caption("A equação global pode perder calibração fora da população original. Registrar versão, janela temporal, completude e validação local.")
    else:
        st.subheader("Checklist de dados necessários para APACHE IV")
        apache_fields = [
            "APS completo com os piores valores do dia 1", "Diagnóstico principal/categoria de admissão", "Idade", "Saúde crônica", "Origem e tempo antes da UTI", "Cirurgia de emergência", "GCS e motivo de não avaliação", "PaO₂/FiO₂ e ventilação mecânica", "Terapia de substituição renal/dados laboratoriais", "Ramo específico para CABG, se aplicável"
        ]
        preenchidos = sum(st.checkbox(item, key="apache_" + str(i)) for i, item in enumerate(apache_fields))
        st.metric("Itens documentados", f"{preenchidos}/{len(apache_fields)}")
        if preenchidos == len(apache_fields):
            st.success("Checklist completo. Ainda assim, é necessário cálculo por implementação licenciada/validada do APACHE IV; esta tela não gera probabilidade APACHE IV.")
        else:
            st.info("Resultado não calculável como APACHE IV completo: faltam dados ou coeficientes oficiais.")

# -----------------------------------------------------------------------------
# MÓDULO 15: TROMBOEMBOLISMO VENOSO
# -----------------------------------------------------------------------------
elif modulo == "15. Tromboembolismo Venoso (Caprini / Worcester)":
    st.header("🩸 Escores de risco para tromboembolismo venoso")
    tv_tipo = st.radio("Selecione o instrumento", ["Caprini 2013", "Worcester perioperatório — ablação venosa"], key="tv_tipo")
    if tv_tipo == "Caprini 2013":
        st.caption("Versão cirúrgica 2013. Os rótulos de risco e a profilaxia dependem da população e do protocolo institucional.")
        caprini = 0
        caprini_1 = st.multiselect("Fatores de 1 ponto", ["Idade 41–60", "Cirurgia menor", "Cirurgia maior prévia no último mês", "Varizes", "DII", "Edema de pernas", "IMC ≥25", "IAM recente", "IC", "Infecção grave", "Doença pulmonar", "Repouso <72h", "Hormônio/anticoncepcional", "Gestação/puerpério", "Tabagismo", "Diabetes em insulina"], key="caprini_1")
        caprini_2 = st.multiselect("Fatores de 2 pontos", ["Idade 61–74", "Artroscopia", "Cirurgia maior >45 min", "Câncer atual/prévio", "Gesso imobilizante", "Cateter venoso central", "Imobilidade ≥72h"], key="caprini_2")
        caprini_3 = st.multiselect("Fatores de 3 pontos", ["Idade ≥75", "TVP/EP prévio", "História familiar de TVP/EP", "Trombofilia documentada"], key="caprini_3")
        caprini_5 = st.multiselect("Fatores de 5 pontos", ["Artroplastia eletiva de quadril/joelho", "Fratura de quadril/pelve/perna", "Trauma grave", "Lesão medular com paralisia", "AVC"], key="caprini_5")
        caprini = len(caprini_1) + 2*len(caprini_2) + 3*len(caprini_3) + 5*len(caprini_5)
        st.metric("Caprini 2013", f"{caprini} pontos")
        if caprini <= 1: st.success("Baixo risco na categorização 2013 (0–1).")
        elif caprini == 2: st.info("Risco moderado (2).")
        elif caprini <= 4: st.warning("Risco alto (3–4).")
        else: st.error("Risco muito alto (≥5). Usar protocolo institucional, incluindo avaliação de sangramento.")
        st.caption("Não usar para diagnosticar TVP/EP nem decidir anticoagulação isoladamente. Misturar versões ou omitir fatores invalida a interpretação.")
    else:
        st.caption("Este Worcester é o instrumento perioperatório publicado para ablação térmica endovenosa ambulatorial; não é um escore geral de internação.")
        worcester = 0
        worcester_2 = st.multiselect("Fatores de 2 pontos", ["TVP/EP prévio", "Trombofilia conhecida", "Imobilidade do membro-alvo", "Câncer, artrite inflamatória ou DII"], key="worcester_2")
        worcester_1 = st.multiselect("Fatores de 1 ponto", ["IMC >30", "Terapia hormonal relevante", "Trombose venosa superficial"], key="worcester_1")
        worcester = 2*len(worcester_2) + len(worcester_1)
        st.metric("Worcester perioperatório", f"{worcester} pontos")
        if worcester == 0: st.success("Baixo risco no estudo original.")
        elif worcester == 1: st.warning("Risco moderado no estudo original.")
        else: st.error("Alto risco no estudo original; requer validação independente e protocolo local.")

# -----------------------------------------------------------------------------
# MÓDULO 16: ABDOME AGUDO E LÍQUIDOS
# -----------------------------------------------------------------------------
elif modulo == "16. Abdome Agudo e Líquidos (GBS, pancreatite, Tokyo, Alvarado, Light, ADA, GASA)":
    st.header("🩺 Escores e critérios de abdome agudo e líquidos")
    abd_tipo = st.selectbox("Selecione o cálculo/critério", ["Glasgow-Blatchford (HDA)", "Duke-ISCVID (endocardite infecciosa)", "Marshall modificado / Atlanta (pancreatite)", "Balthazar / CTSI clássico", "Tokyo Guidelines — colecistite", "Tokyo Guidelines — colangite", "Alvarado (apendicite)", "Critérios de Light", "ADA em líquido", "GASA / SAAG"], key="abd_tipo")
    if abd_tipo == "Duke-ISCVID (endocardite infecciosa)":
        st.caption("Critérios Duke-ISCVID 2023: definição de caso, não um escore numérico. Resultado definitivo exige critérios completos e avaliação especializada.")
        patologia = st.checkbox("Critério patológico: microrganismo/histologia em vegetação, tecido, prótese, dispositivo ou êmbolo", key="duke_pat")
        micro = st.checkbox("Critério maior microbiológico", key="duke_micro")
        imagem = st.checkbox("Critério maior de imagem/cirurgia", key="duke_img")
        regurg = st.checkbox("Nova regurgitação valvar significativa", key="duke_regurg")
        predisposicao = st.checkbox("Predisposição: prótese, endocardite prévia, cardiopatia, dispositivo ou uso de drogas injetáveis", key="duke_pred")
        febre = st.checkbox("Febre ≥38°C", key="duke_febre")
        vascular = st.checkbox("Fenômeno vascular", key="duke_vasc")
        imunologico = st.checkbox("Fenômeno imunológico", key="duke_imune")
        micro_menor = st.checkbox("Evidência microbiológica menor", key="duke_micro_menor")
        maiores = sum([micro, imagem, regurg])
        menores = sum([predisposicao, febre, vascular, imunologico, micro_menor])
        if patologia or maiores >= 2 or (maiores >= 1 and menores >= 3) or menores >= 5:
            st.error("Endocardite infecciosa DEFINITIVA pelos critérios clínicos selecionados. Confirmar critérios completos, culturas e imagem.")
        elif (maiores >= 1 and menores >= 1) or menores >= 3:
            st.warning("Endocardite infecciosa POSSÍVEL pelos critérios clínicos selecionados.")
        else:
            st.info("Critérios selecionados não atingem endocardite possível; isso não exclui doença e não substitui avaliação especializada.")

    if abd_tipo == "Glasgow-Blatchford (HDA)":
        ureia = st.number_input("Ureia (mmol/L)", 0.0, 100.0, 7.0, key="gbs_ureia")
        hb = st.number_input("Hemoglobina (g/dL)", 2.0, 25.0, 13.0, key="gbs_hb")
        sexo_gbs = st.selectbox("Sexo", ["Homem", "Mulher"], key="gbs_sexo")
        pas_gbs = st.number_input("PAS (mmHg)", 40, 300, 120, key="gbs_pas")
        pulso_gbs = st.number_input("Pulso (bpm)", 20, 250, 80, key="gbs_pulso")
        melena = st.checkbox("Melena", key="gbs_melena"); sincope = st.checkbox("Síncope", key="gbs_sincope"); hepatopatia = st.checkbox("Doença hepática", key="gbs_hep"); ic = st.checkbox("Insuficiência cardíaca", key="gbs_ic")
        gbs = 0
        gbs += 0 if ureia < 6.5 else 2 if ureia < 8 else 3 if ureia < 10 else 4 if ureia < 25 else 6
        gbs += (0 if hb >= 13 else 1 if hb >= 12 else 3 if hb >= 10 else 6) if sexo_gbs == "Homem" else (0 if hb >= 12 else 1 if hb >= 10 else 6)
        gbs += 0 if pas_gbs >= 110 else 1 if pas_gbs >= 100 else 2 if pas_gbs >= 90 else 3
        gbs += 1 if pulso_gbs >= 100 else 0; gbs += 1 if melena else 0; gbs += 2 if sincope else 0; gbs += 2 if hepatopatia else 0; gbs += 2 if ic else 0
        st.metric("Glasgow-Blatchford", f"{gbs} pontos")
        if gbs <= 1: st.success("Muito baixo risco em coortes; pode ser candidato a manejo ambulatorial somente após avaliação e protocolo de HDA.")
        else: st.warning("Risco crescente: avaliação hospitalar, ressuscitação conforme necessidade e endoscopia conforme protocolo.")
    elif abd_tipo == "Marshall modificado / Atlanta (pancreatite)":
        pas_m = st.number_input("PAS (mmHg)", 40, 250, 120, key="marshall_pas"); resposta_fluidos = st.checkbox("PAS <90 responsiva a fluidos", key="marshall_resp"); nao_resp = st.checkbox("PAS <90 não responsiva a fluidos", key="marshall_nresp"); ph_m = st.number_input("pH (se PAS <90)", 6.5, 7.6, 7.35, key="marshall_ph")
        creat_m = st.number_input("Creatinina (mg/dL)", 0.1, 20.0, 1.0, key="marshall_creat"); pf_m = st.number_input("PaO₂/FiO₂", 50.0, 600.0, 400.0, key="marshall_pf")
        cardio = 0 if pas_m > 90 else 1 if resposta_fluidos else 2 if nao_resp and ph_m >= 7.3 else 3 if nao_resp and ph_m >= 7.2 else 4
        renal = 0 if creat_m < 1.4 else 1 if creat_m <= 1.8 else 2 if creat_m <= 3.6 else 3 if creat_m <= 4.9 else 4
        resp = 0 if pf_m > 400 else 1 if pf_m > 300 else 2 if pf_m > 200 else 3 if pf_m > 101 else 4
        st.write(f"Cardiovascular: {cardio} | Renal: {renal} | Respiratório: {resp}")
        st.metric("Maior disfunção orgânica", f"{max(cardio, renal, resp)} pontos")
        st.warning("Marshall ≥2 em qualquer sistema define falência orgânica. Persistência >48h corresponde a pancreatite aguda grave na Atlanta revisada; considerar tempo e contexto.")
    elif abd_tipo == "Balthazar / CTSI clássico":
        grau = st.selectbox("Grau morfológico de Balthazar", ["A — normal", "B — aumento", "C — inflamação", "D — uma coleção", "E — ≥2 coleções/gás"], key="balthazar_grau")
        necrose = st.selectbox("Necrose", ["Ausente", "<30%", "30–50%", ">50%"], key="balthazar_necrose")
        grau_pts = [0,1,2,3,4][["A — normal", "B — aumento", "C — inflamação", "D — uma coleção", "E — ≥2 coleções/gás"].index(grau)]
        nec_pts = [0,2,4,6][["Ausente", "<30%", "30–50%", ">50%"].index(necrose)]
        ctsi = grau_pts + nec_pts
        st.metric("CT Severity Index clássico", f"{ctsi}/10")
        st.info("0–3 leve, 4–6 moderado, 7–10 grave na categorização convencional. Não confundir com Atlanta nem com o índice modificado de Mortele.")
    elif abd_tipo == "Tokyo Guidelines — colecistite":
        a = st.checkbox("Sinal local: Murphy/dor ou massa em QSD", key="tokyo_c_a"); b = st.checkbox("Sinais sistêmicos: febre, PCR elevada ou leucocitose", key="tokyo_c_b"); c = st.checkbox("Imagem compatível", key="tokyo_c_c")
        grau2 = sum([st.checkbox("Leucócitos >18.000", key="tokyo_c_g1"), st.checkbox("Massa dolorosa em QSD", key="tokyo_c_g2"), st.checkbox("Sintomas >72h", key="tokyo_c_g3"), st.checkbox("Inflamação local marcada", key="tokyo_c_g4")])
        org = st.checkbox("Disfunção orgânica", key="tokyo_c_org")
        st.write("Diagnóstico: **definitivo**" if a and b and c else "suspeito" if a and b else "não preenchido")
        st.write(f"Gravidade Tokyo: **Grau III**" if org else "**Grau II**" if grau2 >= 1 else "**Grau I/indeterminado**")
    elif abd_tipo == "Tokyo Guidelines — colangite":
        infl = st.checkbox("Inflamação sistêmica", key="tokyo_ch_a"); colest = st.checkbox("Colestase", key="tokyo_ch_b"); imagem = st.checkbox("Imagem: dilatação/causa biliar", key="tokyo_ch_c")
        grau2 = sum([st.checkbox("Leucócitos <4.000 ou >12.000", key="tokyo_ch_g1"), st.checkbox("Febre ≥39°C", key="tokyo_ch_g2"), st.checkbox("Idade ≥75", key="tokyo_ch_g3"), st.checkbox("BT ≥5 mg/dL", key="tokyo_ch_g4"), st.checkbox("Albumina reduzida", key="tokyo_ch_g5")])
        org = st.checkbox("Disfunção orgânica", key="tokyo_ch_org")
        st.write("Diagnóstico: **definitivo**" if infl and colest and imagem else "suspeito" if infl and (colest or imagem) else "não preenchido")
        st.write(f"Gravidade Tokyo: **Grau III**" if org else "**Grau II**" if grau2 >= 2 else "**Grau I/indeterminado**")
    elif abd_tipo == "Alvarado (apendicite)":
        itens = [st.checkbox(label, key="alv_"+str(i)) for i, label in enumerate(["Migração da dor", "Anorexia", "Náuseas/vômitos", "Dor em FID", "Descompressão dolorosa", "Temperatura elevada", "Leucocitose", "Desvio à esquerda/neutrofilia"])]
        alvarado = sum([1,1,1,2,1,1,2,1][i] for i, marcado in enumerate(itens) if marcado)
        st.metric("Alvarado", f"{alvarado}/10")
        if alvarado <= 4: st.success("Baixa probabilidade; reavaliar e considerar diagnóstico diferencial/imagem.")
        elif alvarado <= 6: st.warning("Probabilidade intermediária; observação, reavaliação e imagem conforme contexto.")
        else: st.error("Alta probabilidade em estudos; não substitui avaliação cirúrgica/imagem.")
    elif abd_tipo == "Critérios de Light":
        pp = st.number_input("Proteína pleural (g/dL)", 0.0, 15.0, 3.0, key="light_pp"); ps = st.number_input("Proteína sérica (g/dL)", 0.0, 15.0, 6.0, key="light_ps"); ldp = st.number_input("LDH pleural (U/L)", 0.0, 5000.0, 200.0, key="light_ldp"); lds = st.number_input("LDH sérica (U/L)", 0.0, 5000.0, 300.0, key="light_lds"); ldsn = st.number_input("Limite superior normal da LDH sérica (U/L)", 1.0, 5000.0, 250.0, key="light_ldsn")
        criterios = [pp/ps > 0.5 if ps else False, ldp/lds > 0.6 if lds else False, ldp > (2/3)*ldsn]
        st.write(f"Razão proteína: {pp/ps if ps else 0:.2f} | Razão LDH: {ldp/lds if lds else 0:.2f} | LDH/LSN: {ldp/ldsn:.2f}")
        st.warning("Exsudato" if any(criterios) else "Transudato pelos critérios de Light")
        st.caption("Diuréticos podem gerar pseudoexsudato; interpretar com albumina sérica–pleural e contexto quando necessário.")
    elif abd_tipo == "ADA em líquido":
        ada = st.number_input("ADA (U/L)", 0.0, 300.0, 40.0, key="ada_valor"); compartimento = st.selectbox("Compartimento", ["Pleural", "Ascítico/peritoneal", "Outro"], key="ada_comp")
        st.metric("ADA", f"{ada:.1f} U/L")
        if compartimento == "Pleural" and ada >= 40: st.warning("ADA ≥40 U/L apoia TB pleural no contexto de exsudato linfocitário, mas não confirma isoladamente.")
        elif compartimento == "Pleural": st.info("ADA abaixo do limiar tradicional reduz a probabilidade, mas não exclui TB em imunossupressão ou doença precoce.")
        else: st.info("Não transferir automaticamente o limiar de 40 U/L para outros compartimentos; usar método, população e diretriz local.")
    else:
        alb_s = st.number_input("Albumina sérica (g/dL)", 0.0, 6.0, 2.5, step=0.1, key="saag_s"); alb_a = st.number_input("Albumina ascítica (g/dL)", 0.0, 6.0, 1.0, step=0.1, key="saag_a"); saag = alb_s - alb_a
        st.metric("GASA / SAAG", f"{saag:.2f} g/dL")
        if saag >= 1.1: st.success("≥1,1 g/dL: hipertensão portal é provável; correlacionar com proteína ascítica e etiologia.")
        else: st.warning("<1,1 g/dL: favorece causa sem hipertensão portal, como carcinomatose, TB ou pancreatite; não é diagnóstico isolado.")

# -----------------------------------------------------------------------------
# MÓDULO 17: ACOMPANHAMENTO AMBULATORIAL E GERIATRIA
# -----------------------------------------------------------------------------
elif modulo == "17. Acompanhamento Ambulatorial e Geriatria":
    st.header("🏠 Acompanhamento ambulatorial e avaliação geriátrica")
    amb_tipo = st.selectbox("Selecione o instrumento", ["CKD-EPI 2021", "Risco cardiovascular SBC/ERG", "PREVENT — dados e limites", "Mini-Mental por escolaridade", "MoCA — disponibilidade oficial", "Katz", "Pfeffer/FAQ", "Barthel", "Lawton", "FRAIL", "GDS"], key="amb_tipo")
    if amb_tipo == "CKD-EPI 2021":
        sexo_a = st.radio("Sexo biológico", ["Feminino", "Masculino"], key="amb_sexo")
        idade_a = st.number_input("Idade", 18, 120, 65, key="amb_idade")
        creat_a = st.number_input("Creatinina (mg/dL)", 0.2, 20.0, 1.2, step=0.1, key="amb_creat")
        k_a = 0.7 if sexo_a == "Feminino" else 0.9; alpha_a = -0.241 if sexo_a == "Feminino" else -0.302
        egfr_a = 142 * (min(creat_a/k_a, 1.0)**alpha_a) * (max(creat_a/k_a, 1.0)**-1.2) * (0.9938**idade_a)
        if sexo_a == "Feminino": egfr_a *= 1.012
        st.metric("TFGe CKD-EPI 2021", f"{egfr_a:.1f} mL/min/1,73m²")
        st.info("Uso ambulatorial exige tendência temporal, albuminúria e contexto clínico; TFGe isolada não define diagnóstico ou ajuste universal de fármacos.")
    elif amb_tipo == "Risco cardiovascular SBC/ERG":
        st.caption("Implementação educativa do Escore de Risco Global baseado em Framingham; o risco depende da equação/versão e deve ser conferido com a diretriz SBC vigente.")
        erg_sexo = st.selectbox("Sexo", ["Homem", "Mulher"], key="erg_sexo"); erg_idade = st.number_input("Idade", 20, 100, 55, key="erg_idade"); ct = st.number_input("Colesterol total (mg/dL)", 50.0, 500.0, 200.0, key="erg_ct"); hdl = st.number_input("HDL (mg/dL)", 10.0, 150.0, 50.0, key="erg_hdl"); pas = st.number_input("PAS (mmHg)", 60, 250, 130, key="erg_pas"); trata = st.checkbox("Usa anti-hipertensivo", key="erg_trata"); fuma = st.checkbox("Tabagismo atual", key="erg_fuma"); diab = st.checkbox("Diabetes", key="erg_diab")
        st.info("Campos registrados. Para evitar falsa precisão, use calculadora SBC/Framingham validada para converter esses dados em percentual; esta interface não substitui a equação oficial completa.")
    elif amb_tipo == "PREVENT — dados e limites":
        st.warning("PREVENT não é calculado por uma soma simples. A implementação fiel exige a equação/licença e testes da AHA, além de validação local; este painel não inventa uma probabilidade.")
        st.write("Registrar: sexo, idade 30–79 anos, colesterol total/HDL, PAS e tratamento, tabagismo, diabetes, IMC, TFGe e variáveis opcionais como albuminúria/HbA1c. Aplicável a prevenção primária, não a doença cardiovascular conhecida.")
    elif amb_tipo == "Mini-Mental por escolaridade":
        escolar = st.selectbox("Escolaridade", ["Analfabeto", "1–3 anos", "4–7 anos", "≥8 anos"], key="mm_escolar"); mm = st.number_input("Pontuação (0–30)", 0, 30, 24, key="mm_score")
        cortes = {"Analfabeto":21, "1–3 anos":22, "4–7 anos":23, "≥8 anos":24}
        st.metric("Mini-Mental", f"{mm}/30")
        st.warning(f"Abaixo do ponto de corte de referência ({cortes[escolar]}) — rastreio positivo, não diagnóstico." if mm < cortes[escolar] else "Acima do ponto de corte de referência; ainda requer avaliação clínica e funcional.")
    elif amb_tipo == "MoCA — disponibilidade oficial":
        st.error("O MoCA é protegido por direitos autorais. Use a versão oficial licenciada, com treinamento/certificação quando exigido; não reproduzir aqui um formulário não autorizado.")
    elif amb_tipo == "Katz":
        katz = st.multiselect("Atividades independentes", ["Banho", "Vestir-se", "Banheiro", "Transferência", "Continência", "Alimentação"], key="katz_itens")
        st.metric("Katz — itens independentes", f"{len(katz)}/6"); st.info("Descrever a versão e se a pontuação representa independência ou dependência; não há corte universal.")
    elif amb_tipo == "Pfeffer/FAQ":
        pfeffer = st.number_input("Pfeffer/FAQ (0–30; maior = maior dependência)", 0, 30, 0, key="pfeffer")
        st.metric("Pfeffer/FAQ", f"{pfeffer}/30"); st.info("Alguns protocolos usam ≥5/6 como alerta, mas o ponto de corte depende da versão e do contexto.")
    elif amb_tipo == "Barthel":
        barthel = st.number_input("Barthel (versão 0–100)", 0, 100, 100, key="barthel"); st.metric("Barthel", f"{barthel}/100"); st.info("Pontuação maior indica maior independência; declarar a versão utilizada.")
    elif amb_tipo == "Lawton":
        lawton = st.number_input("Lawton (versão 0–8)", 0, 8, 8, key="lawton"); st.metric("Lawton", f"{lawton}/8"); st.info("Avalia atividades instrumentais; tarefas nunca realizadas por contexto cultural não equivalem automaticamente a incapacidade.")
    elif amb_tipo == "FRAIL":
        frail = sum(st.checkbox(item, key="frail_"+str(i)) for i, item in enumerate(["Fadiga", "Dificuldade para subir um lance de escadas", "Dificuldade para caminhar uma quadra", "≥5 doenças", "Perda de peso >5%/ano"]))
        st.metric("FRAIL", f"{frail}/5"); st.info("0 robusto; 1–2 pré-frágil; 3–5 frágil, conforme a versão usual.")
    else:
        gds = st.number_input("GDS-15 (0–15)", 0, 15, 0, key="gds")
        st.metric("GDS-15", f"{gds}/15"); st.warning("GDS-15 ≥5 sugere rastreio positivo; confirmar por entrevista clínica, avaliar delirium, medicamentos e risco de suicídio.")

# -----------------------------------------------------------------------------
# MÓDULO 18: RESISTÊNCIA ANTIMICROBIANA
# -----------------------------------------------------------------------------
elif modulo == "18. Resistência Antimicrobiana (Ambler e MRSA)":
    st.header("🧫 Resistência antimicrobiana e stewardship")
    st.caption("Painel educacional baseado no PDF fornecido. Não prescreve automaticamente, não transforma fenótipo em gene e exige revisão de microbiologia/infectologia.")
    resist_tipo = st.radio("Selecione o painel", ["Classificação de Ambler", "Agente → mecanismos → estratégias", "Fatores de risco para MRSA"], key="resist_tipo")
    if resist_tipo == "Classificação de Ambler":
        ambler = st.selectbox("Classe molecular", ["A — ESBL/KPC", "B — MBL NDM/VIM/IMP", "C — AmpC/CMY", "D — OXA"], key="ambler_class")
        ambler_info = {
            "A — ESBL/KPC": "Serino-betalactamases. ESBLs hidrolisam cefalosporinas; KPC é carbapenemase. Atividade de inibidores depende da enzima e do antibiograma.",
            "B — MBL NDM/VIM/IMP": "Metalo-betalactamases dependentes de zinco. Não são inibidas por avibactam isolado; aztreonam pode ser inativado por ESBL/AmpC coproduzida.",
            "C — AmpC/CMY": "Cefalosporinases induzíveis/desreprimidas ou plasmidiais. Ceftriaxona pode selecionar resistência em organismos de risco; interpretação depende de espécie e suscetibilidade.",
            "D — OXA": "Oxacilinases. OXA-48 em Enterobacterales e OXA-23/24/58 em Acinetobacter têm perfis diferentes; não generalizar o efeito de avibactam."
        }
        st.info(ambler_info[ambler])
    elif resist_tipo == "Agente → mecanismos → estratégias":
        agente = st.selectbox("Agente", ["E. coli/Klebsiella — ESBL", "Enterobacter/Citrobacter/Serratia — AmpC", "Enterobacterales — KPC", "Enterobacterales — MBL", "Pseudomonas aeruginosa", "Acinetobacter baumannii", "Stenotrophomonas maltophilia", "Staphylococcus aureus — MRSA", "Enterococcus — VRE", "Haemophilus influenzae — BLNAR"], key="resist_agente")
        mecanismos_por_agente = {
            "E. coli/Klebsiella — ESBL": ["ESBL classe A (CTX-M/TEM/SHV)", "Porina/efluxo associado", "Mecanismo não confirmado"],
            "Enterobacter/Citrobacter/Serratia — AmpC": ["AmpC classe C induzível", "AmpC classe C desreprimida", "AmpC plasmidial CMY", "Mecanismo não confirmado"],
            "Enterobacterales — KPC": ["KPC classe A", "KPC + perda de porina", "Carbapenemase não tipada"],
            "Enterobacterales — MBL": ["NDM classe B", "VIM/IMP classe B", "MBL + ESBL/AmpC coproduzida", "Carbapenemase não tipada"],
            "Pseudomonas aeruginosa": ["AmpC classe C", "Perda de OprD", "Efluxo RND", "KPC", "MBL VIM/IMP/NDM", "Mecanismo combinado/não confirmado"],
            "Acinetobacter baumannii": ["OXA-23/24/58 classe D", "MBL NDM classe B", "Baixa permeabilidade/efluxo", "Mecanismo combinado/não confirmado"],
            "Stenotrophomonas maltophilia": ["L1 classe B", "L2 classe A", "Efluxo/porinas", "Mecanismo combinado/não confirmado"],
            "Staphylococcus aureus — MRSA": ["mecA/mecC → PBP2a", "VISA/espessamento de parede", "vanA/VRSA raro", "Mecanismo não confirmado"],
            "Enterococcus — VRE": ["vanA/vanB", "PBP5 de baixa afinidade", "Resistência de alto nível a aminoglicosídeo", "Mecanismo não confirmado"],
            "Haemophilus influenzae — BLNAR": ["PBP3 alterada (BLNAR)", "TEM-1 classe A", "Mecanismo não confirmado"]
        }
        mecanismo = st.selectbox("Mecanismo confirmado ou suspeito", mecanismos_por_agente[agente], key="resist_mecanismo")
        base = {
            "E. coli/Klebsiella — ESBL": "Classe A; resistência a penicilinas/cefalosporinas. Estratégia depende do foco, gravidade e suscetibilidade; carbapenêmico é opção importante em infecção invasiva.",
            "Enterobacter/Citrobacter/Serratia — AmpC": "Classe C, indução/desrepressão. Evitar assumir ceftriaxona como segura em infecção invasiva; cefepima ou carbapenêmico dependem do perfil e do foco.",
            "Enterobacterales — KPC": "Classe A carbapenemase. Considerar novos betalactâmicos/inibidores ativos conforme MIC e disponibilidade institucional.",
            "Enterobacterales — MBL": "Classe B. Avibactam isolado não inibe MBL; considerar estratégias com aztreonam combinado ou cefiderocol somente com revisão especializada e suscetibilidade.",
            "Pseudomonas aeruginosa": "Combinações de efluxo, perda de porina OprD, AmpC e carbapenemases. Direcionar por antibiograma/MIC e foco; não inferir mecanismo único.",
            "Acinetobacter baumannii": "OXA classe D, MBL, baixa permeabilidade e efluxo. Separar colonização de CRAB invasivo; opções dependem de disponibilidade e diretriz local.",
            "Stenotrophomonas maltophilia": "L1 classe B e L2 classe A; resistência intrínseca a vários betalactâmicos. Em doença grave, seleção de agentes ativos e combinação inicial dependem da diretriz e da suscetibilidade.",
            "Staphylococcus aureus — MRSA": "mecA/mecC e PBP2a. Betalactâmicos usuais não são ativos; vancomicina, daptomicina ou ceftarolina dependem do foco, MIC, função renal e monitorização.",
            "Enterococcus — VRE": "vanA/vanB alteram o alvo D-Ala-D-Ala. Linezolida ou daptomicina podem ser opções conforme foco e suscetibilidade; bacteremia/endocardite exigem especialista.",
            "Haemophilus influenzae — BLNAR": "PBP3 alterada sem betalactamase detectável; ampicilina pode falhar. Direcionar pelo antibiograma e foco."
        }
        st.write(f"**Mecanismo selecionado:** {mecanismo}")
        st.write(base[agente])
        st.warning("Antes de qualquer terapia: confirmar síndrome e foco, qualidade da amostra, MIC/antibiograma, função renal/hepática, alergias, gravidez, interações, controle de foco e epidemiologia local. Saída é apoio para revisão, não prescrição.")
    else:
        st.subheader("Fatores de risco para MRSA")
        mrsa_fatores = st.multiselect("Fatores presentes", ["Hospitalização recente/prolongada", "Instituição de longa permanência", "Cirurgia ou dispositivo médico", "Antibióticos de amplo espectro", "Doença grave/comorbidades", "Uso de drogas injetáveis", "Contato pele a pele/esporte de contato", "Ambiente lotado/baixa higiene", "Colonização ou MRSA prévio"], key="mrsa_fatores")
        st.metric("Fatores selecionados", len(mrsa_fatores))
        st.info("Fator de risco ou colonização não equivale a infecção. Correlacionar síndrome, cultura, antibiograma, necessidade de drenagem e epidemiologia local.")
        st.caption("O painel de tratamento não fornece dose automática. Para casos graves, endocardite, bacteremia, pneumonia, sepse, CRE/MBL, CRAB ou falha terapêutica, consultar infectologia/microbiologia.")

# -----------------------------------------------------------------------------
# MÓDULO 19: INTERPRETAÇÃO DE SOROLOGIAS
# -----------------------------------------------------------------------------
elif modulo == "19. Interpretação de Sorologias":
    st.header("🧪 Interpretação de Sorologias")
    st.caption("Painel de interpretação laboratorial. Resultado isolado não substitui confirmação, contexto clínico, avaliação de exposição, exame físico ou protocolo local.")
    sorologia = st.selectbox("Selecione a infecção/painel", [
        "Hepatite B", "Hepatite C", "Hepatite A", "Sífilis",
        "Toxoplasmose na gestação", "Citomegalovírus na gestação", "HIV"
    ], key="sorologia_tipo")

    def resultado(label, key):
        return st.selectbox(label, ["Negativo/não reagente", "Positivo/reagente", "Indeterminado/inconclusivo"], key=key)

    if sorologia == "Hepatite B":
        st.subheader("Hepatite B — HBsAg, anti-HBc e anti-HBs")
        st.caption("O painel de rastreio recomendado inclui HBsAg, anti-HBs e anti-HBc total. O anti-HBc IgM ajuda a identificar infecção recente; anti-HBc IgG é o componente persistente do anti-HBc total.")
        hbsag = resultado("HBsAg", "soro_hbsag")
        hbc_igm = resultado("Anti-HBc IgM", "soro_hbc_igm")
        hbc_igg = resultado("Anti-HBc IgG", "soro_hbc_igg")
        hbs = resultado("Anti-HBs", "soro_hbs")
        if hbsag.startswith("Positivo") and hbc_igm.startswith("Positivo"):
            st.error("Padrão compatível com hepatite B aguda recente. Solicitar avaliação clínica, ALT/AST, bilirrubinas e HBV-DNA conforme contexto; encaminhar para cuidado especializado e avaliar contatos/gestação.")
        elif hbsag.startswith("Positivo") and hbc_igg.startswith("Positivo") and hbc_igm.startswith("Negativo"):
            st.warning("Padrão compatível com infecção crônica ou fase não aguda. Confirmar duração do HBsAg, solicitar HBV-DNA/ALT e avaliar fibrose e necessidade de seguimento/tratamento.")
        elif hbsag.startswith("Negativo") and hbc_igg.startswith("Positivo") and hbs.startswith("Positivo"):
            st.success("Infecção passada resolvida, com imunidade. Documentar risco de reativação em imunossupressão.")
        elif hbsag.startswith("Negativo") and hbc_igg.startswith("Negativo") and hbs.startswith("Positivo"):
            st.success("Imunidade provável por vacinação, se houver série documentada; a vacina não produz anti-HBc.")
        elif hbsag.startswith("Negativo") and hbc_igg.startswith("Negativo") and hbs.startswith("Negativo"):
            st.info("Susceptível, sem evidência sorológica de infecção ou imunidade; avaliar vacinação conforme calendário e situação clínica.")
        elif hbsag.startswith("Negativo") and hbc_igg.startswith("Positivo") and hbs.startswith("Negativo"):
            st.warning("Anti-HBc isolado: pode representar infecção passada com perda do anti-HBs, janela imunológica, infecção oculta, falso-positivo ou variante. Repetir/confirmar painel e considerar HBV-DNA conforme risco.")
        else:
            st.warning("Padrão discordante ou inconclusivo. Repetir/confirmar o painel e considerar HBV-DNA, vacinação prévia, exposição recente e estado imunológico.")
        st.info("HBsAg positivo geralmente indica infecção e potencial infectividade, exceto positividade transitória após vacina. Em gestantes, HBsAg deve ser pesquisado em cada gestação; resultado positivo exige plano perinatal específico.")

    elif sorologia == "Hepatite C":
        st.subheader("Hepatite C — anti-HCV e RNA do HCV")
        anti_hcv = resultado("Anti-HCV", "soro_hcv")
        rna_hcv = st.selectbox("HCV-RNA por NAT/PCR", ["Não realizado", "Não detectável", "Detectável", "Indeterminado"], key="soro_hcv_rna")
        if anti_hcv.startswith("Negativo") and rna_hcv == "Não detectável":
            st.success("Sem evidência laboratorial de infecção atual. Se exposição ocorreu nos últimos 6 meses ou houver imunossupressão, considerar HCV-RNA e repetição no período de janela.")
        elif anti_hcv.startswith("Negativo") and rna_hcv == "Detectável":
            st.error("HCV-RNA detectável com anti-HCV negativo: compatível com infecção muito recente ou resposta sorológica ausente. Encaminhar para confirmação e cuidado especializado.")
        elif anti_hcv.startswith("Positivo") and rna_hcv == "Detectável":
            st.error("Infecção atual pelo HCV. Encaminhar para avaliação e tratamento antiviral, confirmar RNA em nova amostra antes da terapia conforme protocolo e avaliar coinfecções/função hepática.")
        elif anti_hcv.startswith("Positivo") and rna_hcv == "Não detectável":
            st.success("Sem infecção atual detectável: provável infecção passada resolvida/tratada ou falso-positivo biológico. Se a distinção for necessária, repetir com outro ensaio e considerar RNA conforme exposição.")
        else:
            st.warning("Resultado insuficiente ou discordante. Completar HCV-RNA por NAT/PCR; anti-HCV isolado não distingue infecção atual de passada.")
        st.caption("Não há vacina para hepatite C. Pessoas diagnosticadas devem ser avaliadas também para hepatite A, hepatite B e HIV.")

    elif sorologia == "Hepatite A":
        st.subheader("Hepatite A — anti-HAV IgM e IgG/total")
        hav_igm = resultado("Anti-HAV IgM", "soro_hav_igm")
        hav_igg = resultado("Anti-HAV IgG ou anti-HAV total", "soro_hav_igg")
        if hav_igm.startswith("Positivo"):
            st.error("Compatível com infecção atual/recente por HAV, mas correlacionar com sintomas e considerar falso-positivo/reação cruzada. Avaliar notificação e profilaxia pós-exposição de contatos conforme prazo e protocolo.")
        elif hav_igm.startswith("Negativo") and hav_igg.startswith("Positivo"):
            st.success("Imunidade por infecção passada ou vacinação; não indica hepatite A aguda isoladamente.")
        elif hav_igm.startswith("Negativo") and hav_igg.startswith("Negativo"):
            st.info("Sem evidência de infecção prévia ou imunidade detectável; considerar vacinação conforme indicação.")
        else:
            st.warning("Resultado inconclusivo: repetir/confirmar conforme sintomas, momento da exposição e método laboratorial.")
        st.caption("IgM anti-HAV deve ser solicitado principalmente quando há suspeita clínica; IgG/anti-HAV total isolado não diagnostica doença aguda.")

    elif sorologia == "Sífilis":
        st.subheader("Sífilis — algoritmo treponêmico e não treponêmico")
        st.caption("Interpretar teste treponêmico em conjunto com VDRL/RPR quantitativo, história de tratamento e exame clínico. Na gestação, pessoa soropositiva deve ser considerada infectada até que tratamento adequado esteja documentado.")
        algoritmo = st.radio("Algoritmo", ["Tradicional: VDRL/RPR primeiro", "Reverso: teste treponêmico primeiro"], key="sif_algoritmo")
        if algoritmo.startswith("Tradicional"):
            nao_trep = resultado("VDRL/RPR", "sif_nt_trad")
            trep = resultado("Teste treponêmico confirmatório (TP-PA/FTA-ABS/EIA)", "sif_t_trad")
            if nao_trep.startswith("Positivo") and trep.startswith("Positivo"):
                sif_result = "Compatível com sífilis atual ou previamente tratada; titular VDRL/RPR e determinar estágio/necessidade de tratamento."
            elif nao_trep.startswith("Positivo") and trep.startswith("Negativo"):
                sif_result = "Possível falso-positivo do VDRL/RPR ou infecção muito precoce; repetir/confirmar conforme risco e clínica."
            elif nao_trep.startswith("Negativo") and trep.startswith("Positivo"):
                sif_result = "Infecção passada tratada, sífilis latente ou fase muito precoce; revisar tratamento e considerar repetição se exposição recente."
            else:
                sif_result = "Sem evidência sorológica no painel atual; se suspeita recente, repetir conforme janela e avaliação clínica."
        else:
            trep = resultado("Teste treponêmico inicial (EIA/CIA/rápido)", "sif_t_rev")
            nao_trep = resultado("VDRL/RPR quantitativo", "sif_nt_rev")
            segundo_trep = resultado("Segundo teste treponêmico (preferencialmente TP-PA)", "sif_2t_rev")
            if trep.startswith("Positivo") and nao_trep.startswith("Positivo"):
                sif_result = "Compatível com sífilis atual ou previamente tratada; usar título quantitativo, clínica e histórico para estágio e seguimento."
            elif trep.startswith("Positivo") and nao_trep.startswith("Negativo") and segundo_trep.startswith("Positivo"):
                sif_result = "Infecção atual ou passada confirmada; sem tratamento adequado documentado, tratar conforme o estágio."
            elif trep.startswith("Positivo") and nao_trep.startswith("Negativo") and segundo_trep.startswith("Negativo"):
                sif_result = "Provável falso-positivo em baixo risco; repetir em até 4 semanas se seguimento for confiável ou tratar conforme estágio se seguimento não for garantido."
            else:
                sif_result = "Padrão não conclusivo; revisar método, janela, clínica e histórico de tratamento."
        st.warning(sif_result)
        sif_titulo = st.text_input("Título quantitativo VDRL/RPR, se disponível (ex.: 1:8)", key="sif_titulo")
        tratado = st.checkbox("Tratamento adequado previamente documentado e sem risco de reinfecção", key="sif_tratado")
        if trep.startswith("Positivo") and not tratado:
            st.error("Na ausência de tratamento adequado documentado, é necessário determinar o estágio e tratar com penicilina conforme protocolo. Na gestação, penicilina é o tratamento comprovadamente eficaz para prevenir infecção fetal; alergia exige dessensibilização.")
        st.info("Queda de quatro vezes do título é a referência usual de resposta; aumento sustentado de quatro vezes sugere reinfecção ou falha. O título isolado não define duração da infecção.")

    elif sorologia == "Toxoplasmose na gestação":
        st.subheader("Toxoplasmose na gestação — IgG, IgM e avidez")
        semanas = st.number_input("Idade gestacional (semanas)", 1.0, 42.0, 12.0, step=0.1, key="toxo_semanas")
        toxo_igg = resultado("Toxoplasma IgG", "toxo_igg")
        toxo_igm = resultado("Toxoplasma IgM", "toxo_igm")
        avidez = st.selectbox("Avidez do IgG", ["Não realizada", "Baixa", "Intermediária", "Alta"], key="toxo_avidez")
        if toxo_igg.startswith("Negativo") and toxo_igm.startswith("Negativo"):
            st.info("Gestante suscetível no momento: orientar prevenção e repetir conforme protocolo de pré-natal/local.")
        elif toxo_igg.startswith("Positivo") and toxo_igm.startswith("Negativo"):
            st.success("Infecção anterior provável, sem evidência sorológica de infecção recente; documentar e seguir protocolo obstétrico.")
        elif toxo_igg.startswith("Negativo") and toxo_igm.startswith("Positivo"):
            st.warning("IgM isolado pode ser falso-positivo ou infecção muito recente. Repetir em laboratório de referência, solicitar IgG em amostra pareada e discutir imediatamente com obstetrícia/infectologia.")
        elif toxo_igg.startswith("Positivo") and toxo_igm.startswith("Positivo"):
            if avidez == "Alta" and semanas < 18:
                st.success("Alta avidez antes de 18 semanas favorece infecção anterior à gestação, reduzindo a probabilidade de infecção primária recente. Correlacionar com data da coleta, método e histórico.")
            elif avidez == "Baixa" and semanas < 18:
                st.error("Baixa avidez antes de 18 semanas é compatível com infecção primária relativamente recente, mas não define sozinha a data. Encaminhar imediatamente para protocolo obstétrico, confirmação em referência e avaliação fetal.")
            elif semanas >= 18 and avidez == "Baixa":
                st.warning("Após 18 semanas, baixa avidez não data com segurança a infecção e pode persistir. Encaminhar para obstetrícia/infectologia; decisão de tratamento e investigação fetal depende do protocolo vigente.")
            elif semanas >= 18 and avidez == "Alta":
                st.info("Alta avidez após 18 semanas não exclui infecção ocorrida no início da gestação. Correlacionar com sorologias anteriores, ultrassonografia e protocolo especializado.")
            else:
                st.warning("IgG e IgM positivos com avidez não realizada/intermediária: resultado inconclusivo para datação. Repetir/confirmar em laboratório de referência e encaminhar.")
        else:
            st.warning("Resultado inconclusivo; repetir e discutir com o serviço de pré-natal de alto risco.")
        st.caption("A avidez deve ser interpretada pelo método e pelos limites do laboratório. Não iniciar, suspender ou trocar tratamento obstétrico somente por uma regra automática da calculadora.")

    elif sorologia == "Citomegalovírus na gestação":
        st.subheader("Citomegalovírus na gestação — IgG, IgM e avidez")
        cmv_igg = resultado("CMV IgG", "cmv_igg")
        cmv_igm = resultado("CMV IgM", "cmv_igm")
        cmv_avidez = st.selectbox("Avidez do CMV IgG", ["Não realizada", "Baixa", "Intermediária", "Alta"], key="cmv_avidez")
        if cmv_igg.startswith("Negativo") and cmv_igm.startswith("Negativo"):
            st.info("Sem evidência sorológica de infecção prévia; orientar prevenção de exposição e avaliação conforme protocolo obstétrico.")
        elif cmv_igg.startswith("Positivo") and cmv_igm.startswith("Negativo"):
            st.success("Infecção passada provável; IgG positivo isolado não informa quando ocorreu e não confirma infecção fetal.")
        elif cmv_igg.startswith("Negativo") and cmv_igm.startswith("Positivo"):
            st.warning("IgM isolado não diagnostica infecção primária: pode ser falso-positivo ou reação cruzada. Repetir IgG/IgM, considerar soroconversão em amostras pareadas e avaliação especializada.")
        elif cmv_igg.startswith("Positivo") and cmv_igm.startswith("Positivo") and cmv_avidez == "Baixa":
            st.error("IgM positivo associado a baixa avidez de IgG apoia infecção primária recente. Encaminhar para medicina fetal/infectologia; IgG/IgM não diagnosticam CMV congênito.")
        elif cmv_igg.startswith("Positivo") and cmv_igm.startswith("Positivo") and cmv_avidez == "Alta":
            st.info("IgM positivo com alta avidez favorece infecção não recente ou reativação, mas não exclui completamente infecção recente. Correlacionar com amostras anteriores e avaliação especializada.")
        else:
            st.warning("Padrão inconclusivo: repetir/confirmar em laboratório experiente e encaminhar conforme achados obstétricos.")
        st.caption("Para suspeita de CMV congênito, o diagnóstico neonatal é feito por PCR em saliva com confirmação em urina no período apropriado; sorologia materna isolada não diagnostica infecção congênita.")

    else:
        st.subheader("HIV — algoritmo laboratorial")
        hiv_agab = st.selectbox("Teste inicial HIV-1/2 Ag/Ab", ["Não reagente", "Reagente", "Indeterminado"], key="hiv_agab")
        hiv_diff = st.selectbox("Teste suplementar de diferenciação HIV-1/HIV-2", ["Não realizado", "HIV-1 positivo", "HIV-2 positivo", "Não reativo/indeterminado"], key="hiv_diff")
        hiv_rna = st.selectbox("HIV-1 RNA/NAT", ["Não realizado", "Detectável", "Não detectável", "Indeterminado"], key="hiv_rna")
        if hiv_agab == "Não reagente" and hiv_rna != "Detectável":
            st.success("Sem evidência laboratorial no momento pelo teste inicial. Se exposição recente, sintomas de infecção aguda ou PrEP, considerar janela diagnóstica e HIV-1 RNA/repetição.")
        elif hiv_agab == "Reagente" and hiv_diff in ["HIV-1 positivo", "HIV-2 positivo"]:
            st.error("Resultado compatível com infecção por HIV-1 ou HIV-2 após teste suplementar. Encaminhar imediatamente para confirmação conforme algoritmo local e início de cuidado; solicitar carga viral e avaliação clínica.")
        elif hiv_agab == "Reagente" and hiv_diff == "Não reativo/indeterminado" and hiv_rna == "Detectável":
            st.error("Padrão compatível com infecção aguda por HIV-1: Ag/Ab reagente, diferenciação negativa/indeterminada e RNA detectável. Encaminhamento urgente para confirmação e cuidado.")
        elif hiv_agab == "Reagente" and hiv_diff == "Não reativo/indeterminado" and hiv_rna == "Não detectável":
            st.warning("Padrão mais compatível com resultado inicial falso-reagente, mas seguir o algoritmo do laboratório e repetir se necessário; avaliar exposição recente e qualidade da amostra.")
        else:
            st.warning("Algoritmo incompleto ou inconclusivo: repetir/encaminhar para laboratório que realize Ag/Ab, diferenciação e RNA reflexo.")
        st.info("Teste positivo de triagem não deve ser comunicado como diagnóstico definitivo sem o algoritmo confirmatório. Resultado negativo não exclui infecção durante a janela diagnóstica.")

# -----------------------------------------------------------------------------
# MÓDULO 20: INJÚRIA RENAL AGUDA — INTERPRETAÇÃO LABORATORIAL
# -----------------------------------------------------------------------------
elif modulo == "20. Injúria Renal Aguda — Urina e Eletrólitos":
    st.header("🫘 Injúria Renal Aguda — interpretação laboratorial")
    st.caption("FENa, densidade urinária, ureia/creatinina e sedimento ajudam a formular hipóteses, mas não substituem avaliação volêmica, medicamentos, ultrassonografia e contexto clínico.")
    st.warning("Primeiro excluir causas reversíveis pré-renais e obstrução pós-renal. FENa e índices urinários são menos confiáveis em IRA não oligúrica, uso de diuréticos, DRC, sepse, contraste e algumas etiologias específicas.")

    st.subheader("1. FENa — Fração de Excreção de Sódio")
    fena_col1, fena_col2 = st.columns(2)
    with fena_col1:
        na_u = st.number_input("Sódio urinário (mEq/L)", 0.0, 300.0, 20.0, key="ira_na_u")
        cr_u = st.number_input("Creatinina urinária (mg/dL)", 1.0, 1000.0, 100.0, key="ira_cr_u")
    with fena_col2:
        na_s = st.number_input("Sódio sérico (mEq/L)", 80.0, 200.0, 140.0, key="ira_na_s")
        cr_s = st.number_input("Creatinina sérica (mg/dL)", 0.1, 20.0, 2.0, step=0.1, key="ira_cr_s")
    diuretico = st.checkbox("Uso recente de diurético de alça/tiazídico", key="ira_diuretico")
    fena = 100 * (na_u * cr_s) / (na_s * cr_u) if na_s > 0 and cr_u > 0 and cr_s > 0 else 0.0
    st.metric("FENa", f"{fena:.2f}%")
    if diuretico:
        st.warning("Diuréticos podem elevar falsamente a FENa; considerar FEUreia e o conjunto de dados clínicos.")
    elif fena < 1:
        st.info("FENa <1% favorece retenção de sódio/pré-renal, mas também pode ocorrer em IRA intrínseca precoce, glomerulonefrite, rabdomiólise, obstrução ou sepse.")
    elif fena > 2:
        st.warning("FENa >2% favorece lesão tubular intrínseca, mas sofre influência de DRC, sepse, contraste e outras situações.")
    else:
        st.info("FENa entre 1–2%: zona intermediária; correlacionar com sedimento, tendência da creatinina, volemia, fármacos e imagem.")
    st.code("FENa (%) = 100 × (Na urinário × creatinina sérica) / (Na sérico × creatinina urinária)")

    st.subheader("2. Densidade urinária")
    densidade = st.number_input("Densidade urinária", min_value=1.000, max_value=1.060, value=1.020, step=0.001, format="%.3f", key="ira_densidade")
    if densidade >= 1.020:
        st.info("Densidade ≥1,020 pode indicar urina concentrada e favorecer padrão pré-renal, desde que não haja glicosúria, proteinúria intensa ou contraste.")
    elif densidade <= 1.010:
        st.warning("Densidade próxima de 1,010/isostenúria sugere perda de concentração, podendo ocorrer em lesão tubular intrínseca ou DRC.")
    else:
        st.info("Densidade intermediária: interpretar com osmolaridade, glicose, proteínas e hidratação.")

    st.subheader("3. Razão ureia/creatinina")
    ureia_mg = st.number_input("Ureia sérica (mg/dL)", 1.0, 400.0, 80.0, key="ira_ureia")
    creat_mg = st.number_input("Creatinina sérica (mg/dL)", 0.1, 20.0, 2.0, step=0.1, key="ira_creat")
    razao = ureia_mg / creat_mg if creat_mg > 0 else 0.0
    st.metric("Ureia/creatinina", f"{razao:.1f}")
    if razao > 20:
        st.info("Razão >20 pode favorecer componente pré-renal, mas também ocorre em sangramento digestivo, catabolismo, corticoide e dieta hiperproteica.")
    elif razao < 10:
        st.warning("Razão <10 pode favorecer lesão renal intrínseca, mas não define etiologia isoladamente.")
    else:
        st.info("Razão 10–20: não define etiologia; usar evolução e demais achados.")
    st.caption("A razão usa ureia em mg/dL. Não misturar numericamente com BUN sem conversão.")

    st.subheader("4. Sedimento urinário")
    cilindros = st.selectbox("Cilindros granulosos castanhos (‘muddy brown’)", ["Ausentes", "Presentes", "Não avaliado"], key="ira_cilindros")
    eos_sangue = st.selectbox("Eosinofilia periférica", ["Ausente", "Presente", "Não avaliada"], key="ira_eos_sangue")
    eos_urina = st.selectbox("Eosinofilúria", ["Ausente", "Presente", "Não avaliada"], key="ira_eos_urina")
    if cilindros == "Presentes":
        st.error("Cilindros granulosos castanhos favorecem lesão tubular aguda, especialmente em choque, sepse, isquemia, nefrotoxinas ou pigmentos.")
    if eos_sangue == "Presente" or eos_urina == "Presente":
        st.warning("Eosinofilia/eosinofilúria podem apoiar nefrite intersticial aguda, mas têm baixa sensibilidade e especificidade e não confirmam nem excluem a doença.")
    if cilindros == "Ausentes" and eos_sangue == "Ausente" and eos_urina == "Ausente":
        st.info("A ausência desses achados não exclui IRA intrínseca. Procurar hemácias/cilindros hemáticos, proteinúria, leucócitos, cristais e achados de imagem conforme a hipótese.")

    st.subheader("5. Integração por padrão provável")
    padrao = st.selectbox("Padrão clínico-laboratorial predominante", ["Pré-renal", "Renal intrínseca — tubular", "Renal intrínseca — intersticial", "Renal intrínseca — glomerular", "Pós-renal/obstrutiva", "Indeterminado/misto"], key="ira_padrao")
    integracao = {
        "Pré-renal": "Procurar hipovolemia, baixo débito ou vasodilatação efetiva. FENa baixa, urina concentrada e razão ureia/creatinina elevada podem apoiar o padrão. Monitorar resposta hemodinâmica; não administrar volume automaticamente em congestão.",
        "Renal intrínseca — tubular": "Cilindros granulosos castanhos, perda de concentração e FENa frequentemente >2% favorecem lesão tubular aguda. Investigar isquemia, sepse, contraste, fármacos e pigmentos.",
        "Renal intrínseca — intersticial": "Considerar fármaco novo, infecção ou doença imune, com piúria, leucócitos/cilindros leucocitários, rash ou eosinofilia. Eosinofilúria é pouco confiável; discutir nefrologia.",
        "Renal intrínseca — glomerular": "Hematúria dismórfica, cilindros hemáticos, proteinúria e hipertensão sugerem glomerulonefrite. FENa baixa não exclui doença glomerular; considerar investigação imunológica e nefrologia.",
        "Pós-renal/obstrutiva": "Índices urinários variam com o tempo e não excluem obstrução. Procurar retenção, sintomas urinários e realizar ultrassonografia/resíduo pós-miccional com prioridade.",
        "Indeterminado/misto": "Não forçar uma etiologia. Reavaliar creatinina e diurese, medicamentos, volemia, sedimento, eletrólitos, ultrassonografia e causas sistêmicas; considerar nefrologia."
    }
    st.info(integracao[padrao])
    st.caption("Classificar IRA com critérios de creatinina e diurese, como KDIGO. A causa pode ser multifatorial, especialmente em pacientes hospitalizados.")

# -----------------------------------------------------------------------------
# MÓDULO 21: SORO DE MANUTENÇÃO POR PESO
# -----------------------------------------------------------------------------
elif modulo == "21. Soro de Manutenção por Peso":
    st.header("💧 Soro de Manutenção por Peso")
    st.caption("Cálculo conforme as metas informadas: 30 mL/kg/dia de água, 1 mEq/kg/dia de sódio, 1 mEq/kg/dia de potássio, 1 mEq/kg/dia de cloro e 100 g/kg/dia de glicose.")
    st.warning("A meta de glicose de 100 g/kg/dia foi mantida exatamente como solicitada, mas é uma quantidade extremamente alta para manutenção e pode causar hiperglicemia/complicações. Confirmar a unidade e o protocolo antes de administrar; muitas referências usam metas em kcal/kg/dia ou GIR em mg/kg/min, não 100 g/kg/dia.")
    peso_manut = st.number_input("Peso do paciente (kg)", min_value=0.5, max_value=300.0, value=70.0, step=0.1, key="manut_peso")
    frequencia = st.selectbox("Frequência de administração", ["6/6 horas", "8/8 horas", "12/12 horas", "24/24 horas"], key="manut_freq")
    tomadas_dia = {"6/6 horas": 4, "8/8 horas": 3, "12/12 horas": 2, "24/24 horas": 1}[frequencia]

    # Metas diárias solicitadas
    agua_dia = 30.0 * peso_manut
    sodio_dia = 1.0 * peso_manut
    potassio_dia = 1.0 * peso_manut
    cloro_meta_dia = 1.0 * peso_manut
    glicose_dia = 100.0 * peso_manut

    # Apresentações solicitadas: NaCl 20% = 3,4 mEq Na/mL; K 19,1% = 2,5 mEq K/mL; SG 5% = 0,05 g/mL
    nacl_m_eq_ml = 3.4
    kcl_m_eq_ml = 2.5
    sg5_g_ml = 0.05
    nacl_ml_dia = sodio_dia / nacl_m_eq_ml
    kcl_ml_dia = potassio_dia / kcl_m_eq_ml
    sg5_ml_dia = glicose_dia / sg5_g_ml
    cloro_da_nacl_dia = sodio_dia
    cloro_do_kcl_dia = potassio_dia
    cloro_total_dia = cloro_da_nacl_dia + cloro_do_kcl_dia
    cloro_excesso_dia = cloro_total_dia - cloro_meta_dia
    volume_total_dia = agua_dia
    volume_hora = volume_total_dia / 24.0

    st.subheader("Metas diárias")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Água", f"{agua_dia:.1f} mL/dia")
        st.metric("Sódio", f"{sodio_dia:.1f} mEq/dia")
    with col2:
        st.metric("Potássio", f"{potassio_dia:.1f} mEq/dia")
        st.metric("Cloro — meta", f"{cloro_meta_dia:.1f} mEq/dia")
    with col3:
        st.metric("Glicose solicitada", f"{glicose_dia:.1f} g/dia")
        st.metric("Velocidade hídrica", f"{volume_hora:.1f} mL/h")

    st.subheader("Volumes das apresentações")
    st.write(f"**NaCl 20%:** {nacl_ml_dia:.2f} mL/dia para fornecer {sodio_dia:.1f} mEq de sódio (3,4 mEq/mL).")
    st.write(f"**KCl 19,1%:** {kcl_ml_dia:.2f} mL/dia para fornecer {potassio_dia:.1f} mEq de potássio (2,5 mEq/mL).")
    st.write(f"**Soro glicosado 5%:** {sg5_ml_dia:.1f} mL/dia para fornecer {glicose_dia:.1f} g de glicose (0,05 g/mL).")
    st.write(f"**Volume hídrico de manutenção:** {volume_total_dia:.1f} mL/dia, equivalente a {volume_hora:.1f} mL/h.")

    st.subheader(f"Divisão por administração — {frequencia}")
    st.write(f"Número de administrações em 24 h: **{tomadas_dia}**")
    st.write(f"**Volume hídrico por administração:** {agua_dia / tomadas_dia:.1f} mL")
    st.write(f"**NaCl 20% por administração:** {nacl_ml_dia / tomadas_dia:.2f} mL")
    st.write(f"**KCl 19,1% por administração:** {kcl_ml_dia / tomadas_dia:.2f} mL")
    st.write(f"**SG 5% por administração:** {sg5_ml_dia / tomadas_dia:.1f} mL")
    st.write(f"**Sódio por administração:** {sodio_dia / tomadas_dia:.1f} mEq")
    st.write(f"**Potássio por administração:** {potassio_dia / tomadas_dia:.1f} mEq")
    st.write(f"**Glicose por administração:** {glicose_dia / tomadas_dia:.1f} g")

    st.error(f"Atenção ao cloro: NaCl e KCl fornecem juntos aproximadamente {cloro_total_dia:.1f} mEq/dia de cloro, enquanto a meta informada foi {cloro_meta_dia:.1f} mEq/dia. Excesso calculado: {cloro_excesso_dia:.1f} mEq/dia. Com apenas NaCl e KCl não é possível atingir simultaneamente 1 mEq/kg/dia de sódio, 1 mEq/kg/dia de potássio e 1 mEq/kg/dia de cloro; ajustar a composição conforme eletrólitos séricos, função renal e protocolo.")
    st.warning("Não adicionar KCl sem confirmar diurese, potássio sérico, função renal, compatibilidade, via e protocolo. O volume final real deve considerar o volume dos eletrólitos adicionados e a concentração final desejada. Este cálculo não substitui prescrição nem dupla checagem.")
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
