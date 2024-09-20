### `Options.py`
### ❄️ Template Generator
### Open-Source, hosted on https://github.com/SeriousBenEntertainment/Template_Generator
### Please reach out to benjamin.gross1@adesso.de for any questions
### Loading needed Python libraries
import streamlit as st
import pandas as pd
import ast
from io import StringIO
from Functions import list_objects

# Options content
def frontend_options(df, schema, minio_client):
    # Decrypting the dataframe
    paragraph_list = df["PARAGRAPH"].tolist()
    paragraph_title_list = df["PARAGRAPH_TITLE"].tolist()
    combined_list = [
                        f"{p:<6} - {t}" 
                        for p, t in zip(paragraph_list, paragraph_title_list)
                    ]

    # Importing options
    options_csv = minio_client.get_object(schema.lower().replace(' ', '-'), "options.csv")
    csv_data = options_csv.read().decode('utf-8')
    options = pd.read_csv(StringIO(csv_data), quotechar="'", delimiter=',')
    with st.form("Forms"):
        st.title("Konfiguration")
        st.write("Bitte fülle die folgenden Felder aus, um bestmöglich ein Template generieren zu können.")
        st.header("Optionen")
        st.write("Bitte fülle die folgenden Felder mit den fachlichen Informationen aus.")
        
        # Initialize variables
        options_output = pd.DataFrame(columns=["ANSWER", "PARAGRAPH", "FILES"])
        i, x, y, key = -1, 0, -1, 0
        cont, cont_y = [], []
        file_names = list_objects(minio_client, "templategenerator")
        file_names = [
                        file 
                        for file in file_names 
                        if file.endswith(('.pdf','docx'))
                    ]

        # Loop through options
        for _, option in options.iterrows():
            # Create helptext
            try:
                chapter_paragraph = ast.literal_eval(option['CHAPTER_PARAGRAPH'])
                chapters_paragraphs = [
                                        f"{p} {t}"
                                        for cp in chapter_paragraph
                                            for p, t in zip(paragraph_list, paragraph_title_list)
                                            if cp == p
                                    ]
                help_text = ", ".join(chapters_paragraphs)
            except:
                chapter_paragraph = []
                help_text = ""

            # Header
            if option['TYPE'] == 'HEADER':
                i += 1
                with st.expander(option['QUESTION']):
                    cont.append(st.container(border=True))
                    with cont[i]:
                        st.header(option['QUESTION'])
                        st.write(option['DEFAULT'])

            # Subheader
            if option['TYPE'] == 'SUBHEADER':
                with cont[i]:
                    y += 1
                    cont_y.append(st.container(border=True))
                    with cont_y[y]:
                        st.subheader(option['QUESTION'])
                        st.write(option['DEFAULT'])

            # Describing text
            if option['TYPE'] == 'DESC':
                with cont[i]:
                    with cont_y[y]:
                        st.markdown(f"**{option['QUESTION']}**")

            # Text input
            if option['TYPE'] == 'TEXT':
                with cont[i]:
                    with cont_y[y]:
                        key += 1
                        answer = st.text_input(option['QUESTION'], key=f"option_{key}", value=str(option['DEFAULT']))
                        paragraph = option['CHAPTER_PARAGRAPH']
                        if chapter_paragraph:
                            st.text(f"Zugehörige Absätze: {', '.join(chapter_paragraph)}", help=help_text)
                        x += 1
                        files = st.multiselect("Füge zusätzliche Informationen hinzu", placeholder='Wähle eine oder mehrere Datei(en) aus', options=file_names, key=f"multifiles_options_{x}", default=["20190531_FAQ_80.pdf"])
                        st.markdown("---")

            # Toogle input
            if option['TYPE'] == 'BOOL':
                with cont[i]:
                    with cont_y[y]:
                        key += 1
                        answer = st.toggle(option['QUESTION'], key=f"option_{key}", value=eval(option['DEFAULT']))
                        paragraph = option['CHAPTER_PARAGRAPH']
                        if chapter_paragraph:
                            st.text(f"Zugehörige Absätze: {', '.join(chapter_paragraph)}", help=help_text)
                        st.markdown("---")

            # Selectbox input
            if option['TYPE'] == 'SELECT':
                with cont[i]:
                    with cont_y[y]:
                        key += 1
                        options_selectbox = ast.literal_eval(option['DEFAULT'])[1:]
                        index_selectbox = ast.literal_eval(option['DEFAULT'])[0]
                        answer = st.selectbox(option['QUESTION'], options=options_selectbox, key=f"option_{key}", index=int(index_selectbox))
                        paragraph = option['CHAPTER_PARAGRAPH']
                        st.markdown("---")

            # Creating output
            if option['TYPE'] == 'SELECT' or option['TYPE'] == 'TEXT' or option['TYPE'] == 'BOOL':
                if option['TYPE'] == 'Text':
                    options_output = options_output._append({"ANSWER": answer, "PARAGRAPH": paragraph, "FILES": files}, ignore_index=True)
                else:
                    options_output = options_output._append({"ANSWER": answer, "PARAGRAPH": paragraph, "FILES": []}, ignore_index=True)
        print(options_output)

        # Template generation
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
                file_names = list_objects(minio_client, "templategenerator")
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
        submitted = st.form_submit_button("Template generieren")
    return submitted, chapters, table_of_contents, paragraph_of_summary, table_of_glossar, table_of_stakeholders, table_of_attachments, options_output