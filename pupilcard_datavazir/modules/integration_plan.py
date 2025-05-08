# === Intégration dans pupil_report_card.py ===
# 1. Ajouter en haut :
from modules import interpretation

# 2. Dans display_student_profile(), après génération des scores :
if scores_egra is not None and scores_egma is not None:
    rule_message = interpretation.generate_rule_based_interpretation(scores_egra, scores_egma)
    prompt = interpretation.create_llm_prompt(rule_message, scores_egra, scores_egma)
    llm_message = interpretation.generate_llm_message(prompt)

    st.markdown("### 🧠 Interprétation (système hybride)")
    st.markdown("**Analyse systématique :**")
    st.info(rule_message)
    st.markdown("**Synthèse enrichie :**")
    st.success(llm_message)

# 3. Dans export_to_word() (après les graphiques) :
doc.add_heading("Interpretation & Recommendations", level=1)
doc.add_paragraph("Analyse systématique :")
doc.add_paragraph(rule_message)
doc.add_paragraph("Synthèse enrichie :")
doc.add_paragraph(llm_message)


# === Intégration dans class_comparative.py ===
# 1. Ajouter en haut :
from modules import interpretation

# 2. Après fig_egma :
summary_text = interpretation.generate_group_summary(class_means, level='class')
prompt = interpretation.create_group_prompt(summary_text)
llm_summary = interpretation.generate_llm_message(prompt)

st.subheader("🧠 Class Insights")
st.markdown("**Systematic Summary**")
st.info(summary_text)
st.markdown("**LLM Interpretation**")
st.success(llm_summary)


# === Intégration dans school_comparative.py ===
# 1. Ajouter en haut :
from modules import interpretation

# 2. Après calcul de school_means :
summary_text = interpretation.generate_group_summary(school_means, level='school')
prompt = interpretation.create_group_prompt(summary_text)
llm_summary = interpretation.generate_llm_message(prompt)

st.subheader("🧠 School Insights")
st.markdown("**Systematic Summary**")
st.info(summary_text)
st.markdown("**LLM Interpretation**")
st.success(llm_summary)


# === Optionnel : Ajouter les interprétations dans export_comparison_to_word ===
doc.add_heading("Interpretation & Recommendations", level=1)
doc.add_paragraph("Systematic Summary:")
doc.add_paragraph(summary_text)
doc.add_paragraph("LLM Interpretation:")
doc.add_paragraph(llm_summary)
