### `Template.py`
### ❄️ Template Generator
### Open-Source, hosted on https://github.com/SeriousBenEntertainment/Template_Generator
### Please reach out to benjamin.gross1@adesso.de for any questions
### Loading needed Python libraries
import streamlit as st
import pandas as pd
from Functions import list_objects

# Template generation content
def template_options(combined_list, schema, minio_client):
    with st.form("Form_Template"):
        st.header("Template")
        st.write("Bitte wähle die Einstellungen für das Word Dokument aus.")
        template = st.container(border=True)
        with template.container(border=True):
            st.subheader("Absätze")
            st.write("Bitte wähle die Absätze aus 📒")
            chapters = st.multiselect("Absätze", options=combined_list, default=combined_list)
            with st.expander("Zusätzliche Informationen", expanded=False):
                st.subheader("Auswahl zusätzlicher Informationen")
                st.write("Wähle zusätzliche Informationen zum jeweiligen Absatz aus")
                file_names = list_objects(minio_client, schema.lower().replace(' ', '-'))
                x = 0
                for chapter in chapters:
                    st.write(chapter)
                    x += 1
                    st.multiselect("Füge zusätzliche Informationen hinzu", placeholder='Wähle eine oder mehrere Datei(en) aus', options=file_names, key=f"multifiles_chapters_{x}")
            with st.expander("Weitere Absätze", expanded=False):
                table_of_contents = st.checkbox("Inhaltsverzeichnis hinzufügen?", value=True)
                #table_of_certs = st.checkbox("Zertifizierungen hinzufügen?", value=True)
                paragraph_of_summary = st.checkbox("Zusammenfassung hinzufügen?", value=True)
                table_of_glossar = st.checkbox("Glossar hinzufügen?", value=True)
                table_of_stakeholders = st.checkbox("Stakeholder hinzufügen?", value=True)
                table_of_attachments = st.checkbox("Anhänge hinzufügen?", value=True)
        checked_in = st.form_submit_button("Template generieren")
    return checked_in, chapters, table_of_contents, paragraph_of_summary, table_of_glossar, table_of_stakeholders, table_of_attachments