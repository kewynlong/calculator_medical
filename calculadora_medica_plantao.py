import streamlit as st
import math

st.set_page_config(
    page_title="Calculadora Médica de Plantão",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Calculadora Médica Prática de Plantão (2026)")
st.caption("Ferramenta clínica baseada nas Diretrizes SBD 2026, SBC, GINA 2026, GOLD 2026, Surviving Sepsis Campaign (SSC 2024/2026) e Ministério da Saúde.")

st.sidebar.header("📌 Módulos de Cálculo")
modulo = st.sidebar.radio(
    "Selecione o módulo:",
    [
        "1. Cetoacidose (CAD) & Estado Hiperosmolar (SHH)",
        "2. Infusão de Drogas Vasoativas (BIC)",
        "3. Função Renal (CKD-EPI 2021)",
        "4. Doses Pediátricas por Peso",
        "5. Escores Críticos (NEWS2, CURB-65 & qSOFA)",
        "6. Dengue - Manejo Volêmico (MS)",
        "7. Queimaduras (Regra de Parkland)"
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
        ["Noradrenalina", "Nitroglicerina (Tridil)", "Nitroprussiato de Sódio (Nipride)", "Dopamina"]
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
# MÓDULO 4: DOSES PEDIÁTRICAS
# -----------------------------------------------------------------------------
elif modulo == "4. Doses Pediátricas por Peso":
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
# MÓDULO 5: ESCORES CRÍTICOS (NEWS2, CURB-65 & qSOFA)
# -----------------------------------------------------------------------------
elif modulo == "5. Escores Críticos (NEWS2, CURB-65 & qSOFA)":
    st.header("🧮 Escores de Risco e Severidade Clínica")
    
    tabs = st.tabs(["🏥 1. NEWS 2 (National Early Warning Score)", "🫁 2. CURB-65 (PAC)", "🚨 3. qSOFA (Triagem Sepse)"])
    
    # -------------------------------------------------------------------------
    # TAB 1: NEWS 2
    # -------------------------------------------------------------------------
    with tabs[0]:
        st.subheader("National Early Warning Score 2 (NEWS2 - Royal College of Physicians)")
        st.caption("Ferramenta padrão ouro para detecção precoce de deterioração clínica e triagem de Sepse hospitalar/pré-hospitalar (Recomendado sobre o qSOFA pela Surviving Sepsis Campaign 2024/2026).")
        
        col_n1, col_n2 = st.columns(2)
        
        with col_n1:
            fr_news = st.number_input("Frequência Respiratória (irpm)", min_value=4, max_value=60, value=16, step=1, key="news_fr")
            
            escala_spo2 = st.radio(
                "Escala de Saturação de O₂ (SpO₂):",
                ["Escala 1 (Padrão Geral)", "Escala 2 (Insuficiência Hipercápnica / DPOC - Alvo 88-92%)"],
                key="news_escala"
            )
            
            spo2_news = st.number_input("Saturação de O₂ (%)", min_value=50, max_value=100, value=97, step=1, key="news_spo2")
            o2_supl = st.radio("Uso de Oxigênio Suplementar?", ["Não (Ar Ambiente)", "Sim"], key="news_o2")
            pas_news = st.number_input("Pressão Arterial Sistólica (PAS em mmHg)", min_value=40, max_value=260, value=120, step=5, key="news_pas")

        with col_n2:
            fc_news = st.number_input("Frequência Cardíaca / Pulso (bpm)", min_value=20, max_value=220, value=75, step=5, key="news_fc")
            
            consciencia_news = st.selectbox(
                "Nível de Consciência (ACVPU):",
                [
                    "A - Alerta (Preservado)",
                    "C - Nova Confusão Mental / Delirium Agudo",
                    "V - Responde à Voz",
                    "P - Responde à Dor",
                    "U - Inconsciente / Sem Resposta"
                ],
                key="news_consciencia"
            )
            
            temp_news = st.number_input("Temperatura Corporal (°C)", min_value=30.0, max_value=43.0, value=36.8, step=0.1, key="news_temp")

        # CÁLCULO DE PONTUAÇÃO DO NEWS2
        pts_fr = 0
        if fr_news <= 8:
            pts_fr = 3
        elif 9 <= fr_news <= 11:
            pts_fr = 1
        elif 12 <= fr_news <= 20:
            pts_fr = 0
        elif 21 <= fr_news <= 24:
            pts_fr = 2
        else: # >= 25
            pts_fr = 3

        pts_spo2 = 0
        if "Escala 1" in escala_spo2:
            if spo2_news <= 91:
                pts_spo2 = 3
            elif 92 <= spo2_news <= 93:
                pts_spo2 = 2
            elif 94 <= spo2_news <= 95:
                pts_spo2 = 1
            else:
                pts_spo2 = 0
        else: # Escala 2 (DPOC / Hipercápnico)
            if spo2_news <= 83:
                pts_spo2 = 3
            elif 84 <= spo2_news <= 85:
                pts_spo2 = 2
            elif 86 <= spo2_news <= 87:
                pts_spo2 = 1
            elif 88 <= spo2_news <= 92:
                pts_spo2 = 0
            elif 93 <= spo2_news <= 94 and o2_supl == "Sim":
                pts_spo2 = 1
            elif 95 <= spo2_news <= 96 and o2_supl == "Sim":
                pts_spo2 = 2
            elif spo2_news >= 97 and o2_supl == "Sim":
                pts_spo2 = 3
            elif spo2_news >= 93 and o2_supl == "Não (Ar Ambiente)":
                pts_spo2 = 0

        pts_o2 = 2 if o2_supl == "Sim" else 0

        pts_pas = 0
        if pas_news <= 90:
            pts_pas = 3
        elif 91 <= pas_news <= 100:
            pts_pas = 2
        elif 101 <= pas_news <= 110:
            pts_pas = 1
        elif 111 <= pas_news <= 219:
            pts_pas = 0
        else: # >= 220
            pts_pas = 3

        pts_fc = 0
        if fc_news <= 40:
            pts_fc = 3
        elif 41 <= fc_news <= 50:
            pts_fc = 1
        elif 51 <= fc_news <= 90:
            pts_fc = 0
        elif 91 <= fc_news <= 110:
            pts_fc = 1
        elif 111 <= fc_news <= 130:
            pts_fc = 2
        else: # >= 131
            pts_fc = 3

        pts_consciencia = 0 if "A - Alerta" in consciencia_news else 3

        pts_temp = 0
        if temp_news <= 35.0:
            pts_temp = 3
        elif 35.1 <= temp_news <= 36.0:
            pts_temp = 1
        elif 36.1 <= temp_news <= 38.0:
            pts_temp = 0
        elif 38.1 <= temp_news <= 39.0:
            pts_temp = 1
        else: # >= 39.1
            pts_temp = 2

        score_news2 = pts_fr + pts_spo2 + pts_o2 + pts_pas + pts_fc + pts_consciencia + pts_temp
        red_score = any(p == 3 for p in [pts_fr, pts_spo2, pts_pas, pts_fc, pts_consciencia, pts_temp])

        st.markdown("---")
        st.subheader(f"📊 Pontuação Total NEWS2: **{score_news2} ponto(s)**")
        
        # Detalhamento de cada item
        st.caption(f"Detalhamento: FR ({pts_fr}p) | SpO₂ ({pts_spo2}p) | O₂ Supl. ({pts_o2}p) | PAS ({pts_pas}p) | FC ({pts_fc}p) | Consciência ({pts_consciencia}p) | Temp ({pts_temp}p)")

        st.markdown("### 🚦 Estratificação de Risco & Resposta Clínica:")
        if score_news2 >= 7:
            st.error("🚨 **RISCO ALTO / EMERGÊNCIA CLÍNICA (≥ 7 pontos)**")
            st.write("• **Conduta Imediata:** Resposta clínica emergencial imediata.")
            st.write("• **Ações:** Acionar Equipe de Resposta Rápida (ERR) / Médico Intensivista. Avaliar transferência imediata para leito de UTI / Sala Vermelha.")
            st.write("• **Monitorização:** Instalar monitorização contínua de sinais vitais.")
            st.write("• **Suspeita de Infecção?** Iniciar protocolo de Sepse imediatamente (Coletar Hemoculturas, Lactato, Antibiótico em < 1h, Cristaloide 30 mL/kg).")

        elif score_news2 >= 5 or red_score:
            st.warning("⚠️ **RISCO MODERADO (5-6 pontos ou Parâmetro Único = 3 [Red Score])**")
            st.write("• **Conduta Imediata:** Avaliação médica urgente pelo plantonista do setor.")
            st.write("• **Ações:** Incrementar frequência de monitorização dos sinais vitais para no mínimo de 1/1h a 2/2h.")
            st.write("• **THINK SEPSIS:** Se houver suspeita infecciosa, realizar triagem ativa para Sepse conforme as diretrizes Surviving Sepsis Campaign (SSC 2024/2026).")

        else:
            st.success("✅ **RISCO BAIXO (0 a 4 pontos)**")
            st.write("• **Conduta:** Monitorização de rotina pela enfermagem (a cada 4 a 12 horas). Manter plano terapêutico habitual.")

    # -------------------------------------------------------------------------
    # TAB 2: CURB-65
    # -------------------------------------------------------------------------
    with tabs[1]:
        st.subheader("Escore CURB-65 (Pneumonia Adquirida na Comunidade - PAC)")
        c1 = st.checkbox("C - Confusão mental (GCS < 15 ou rebaixamento agudo)", key="c1")
        c2 = st.checkbox("U - Ureia > 50 mg/dL (ou BUN > 19 mg/dL)", key="c2")
        c3 = st.checkbox("R - Frequência Respiratória >= 30 irpm", key="c3")
        c4 = st.checkbox("B - Pressão Arterial Sistólica < 90 mmHg ou Diastólica <= 60 mmHg", key="c4")
        c5 = st.checkbox("65 - Idade >= 65 anos", key="c5")
        
        curb_score = sum([c1, c2, c3, c4, c5])
        st.markdown(f"**Pontuação CURB-65:** **{curb_score} ponto(s)**")
        
        if curb_score <= 1:
            st.success("✅ Risco baixo (Mortalidade < 1,5%). Conduta: Tratamento Ambulatorial.")
        elif curb_score == 2:
            st.warning("⚠️ Risco moderado (Mortalidade ~ 9,2%). Conduta: Considerar Internação Hospitalar em Enfermaria.")
        else:
            st.error("🚨 Risco elevado (Mortalidade > 22%). Conduta: Internação Hospitalar (Avaliar UTI se score >= 3-4).")

    # -------------------------------------------------------------------------
    # TAB 3: qSOFA
    # -------------------------------------------------------------------------
    with tabs[2]:
        st.subheader("quickSOFA (qSOFA - Triagem Rápida)")
        st.caption("Nota de atualização SSC 2024/2026: Devido à baixa sensibilidade do qSOFA (~23%), o NEWS2 é fortemente recomendado sobre o qSOFA como ferramenta de triagem única de sepse hospitalar.")
        q1 = st.checkbox("Frequência Respiratória >= 22 irpm", key="q1")
        q2 = st.checkbox("Alteração do Nível de Consciência (GCS < 15)", key="q2")
        q3 = st.checkbox("Pressão Arterial Sistólica <= 100 mmHg", key="q3")
        
        qsofa_score = sum([q1, q2, q3])
        st.markdown(f"**Pontuação qSOFA:** **{qsofa_score} ponto(s)**")
        
        if qsofa_score >= 2:
            st.error("🚨 **qSOFA POSITIVO (>= 2 pontos)**: Alto risco de deterioração / UTI. Coletar Lactato, Hemoculturas, iniciar Antibiótico na 1ª hora e volume de 30 mL/kg de cristaloide se hipotensão.")
        else:
            st.info("qSOFA < 2 pontos. Manter monitorização contínua e reavaliar se piora clínica (usar NEWS2 se disponível).")

# -----------------------------------------------------------------------------
# MÓDULO 6: DENGUE
# -----------------------------------------------------------------------------
elif modulo == "6. Dengue - Manejo Volêmico (MS)":
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
# MÓDULO 7: QUEIMADURA
# -----------------------------------------------------------------------------
elif modulo == "7. Queimaduras (Regra de Parkland)":
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
