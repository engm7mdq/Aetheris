"""Aetheris entry point: streamlit run app.py

Unauthenticated sessions only get the sign-in page; the dashboard pages are not even registered
with the navigation, so typing a page URL cannot bypass the login. Every page additionally calls
``setup_page()``, which refuses to render without an authenticated session (defence in depth).
"""
import streamlit as st

import config
from src.i18n import t
from src.ui.common import (
    _bootstrap,
    apply_preferences,
    current_theme,
    current_user,
    footer,
    is_authenticated,
    mark_semester_selector,
    preference_controls,
    semester_selector,
    sign_out,
)
from src.ui.login import render_login

st.set_page_config(page_title=config.APP_FULL_TITLE, page_icon=str(config.FAVICON), layout="wide")
_bootstrap()

if not is_authenticated():
    apply_preferences(login=True)
    st.navigation([st.Page(render_login, title=t("nav.login"), url_path="login", default=True)],
                  position="hidden").run()
    st.stop()

apply_preferences()
pages = {
    t("nav.section.workspace"): [
        st.Page("pages/0_Overview.py", title=t("nav.overview"), icon=":material/dashboard:", default=True),
        st.Page("pages/1_Semesters.py", title=t("nav.semesters"), icon=":material/calendar_month:"),
        st.Page("pages/2_Dataset_Management.py", title=t("nav.dataset"), icon=":material/database:"),
    ],
    t("nav.section.scheduling"): [
        st.Page("pages/3_Exam_Scheduling.py", title=t("nav.scheduling"), icon=":material/smart_toy:"),
        st.Page("pages/4_Timetable.py", title=t("nav.timetable"), icon=":material/event_note:"),
        st.Page("pages/5_Analytics.py", title=t("nav.analytics"), icon=":material/monitoring:"),
        st.Page("pages/6_Historical_Results.py", title=t("nav.history"), icon=":material/history:"),
    ],
    t("nav.section.about"): [
        st.Page("pages/7_Methodology.py", title=t("nav.methodology"), icon=":material/school:"),
    ],
}
nav = st.navigation(pages)
logo = config.LOGO_DARK if current_theme() == "dark" else config.LOGO_LIGHT
st.logo(str(logo), size="large", icon_image=str(config.LOGO_MARK))

mark_semester_selector(False)
semester_selector()            # rendered once, at the top of the sidebar content
mark_semester_selector(True)   # pages reuse the selection
with st.sidebar.container():
    st.divider()
    st.markdown(t("auth.signed_in_as", user=current_user()))
    preference_controls(st.sidebar, key_suffix="_side")
    if st.button(t("auth.logout"), icon=":material/logout:", width="stretch", key="ae_logout"):
        sign_out()
        st.rerun()
    footer(st.sidebar)

try:
    nav.run()
finally:
    mark_semester_selector(False)
