import streamlit as st
from modules import pupil_report_card, class_comparison, school_comparison
from modules import language

def main():
    # Set page config
    st.set_page_config(page_title=language.t("app_title"), layout="wide")
    
    # Initialize language
    language.init_language()
    
    # Add language selector in sidebar
    language.language_selector()
    
    # Navigation
    st.sidebar.title(language.t("navigation"))
    app_mode = st.sidebar.selectbox(
        language.t("choose_application"),
        [language.t("pupil_report_card"), language.t("class_comparison"), language.t("school_comparison")]
    )

    if app_mode == language.t("pupil_report_card"):
        pupil_report_card.main()
    elif app_mode == language.t("class_comparison"):
        class_comparison.main()
    elif app_mode == language.t("school_comparison"):
        school_comparison.main()

if __name__ == '__main__':
    main()