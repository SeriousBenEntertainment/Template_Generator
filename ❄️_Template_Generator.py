### `❄️_Template_Generator.py`
### ❄️ Template Generator
### Open-Source, hosted on https://github.com/SeriousBenEntertainment/Template_Generator
### Please reach out to benjamin.gross1@adesso.de for any questions
### Loading needed Python libraries
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
pd.set_option('display.max_colwidth', None)
import sys
import warnings
warnings.filterwarnings(
    action='ignore',
    category=UserWarning,
    module='snowflake.connector'
)
from io import StringIO, BytesIO
from minio.error import S3Error
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_snowpoc.llms import Cortex
import snowflake.connector
from snowflake.snowpark.types import *
import pandas as pd
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from textwrap import wrap
sys.path.insert(1, "pages/functions/")
from Options import frontend_options
from Template import template_options
from Functions import connect_to_minio, list_buckets, list_objects, upload_files, create_session, list_stages, list_files, load_data, write_data, uploading_files, export_doc, web_scraper

# Define session states
if 'options_setup' not in st.session_state:
    st.session_state.options_setup = False
if 'combined_list' not in st.session_state:
    st.session_state['combined_list'] = []
if 'options' not in st.session_state:
    st.session_state['options'] = {}

# Define the pages
pages = {
    "Home": [
        st.Page("🤖_OpenAI.py", title="❄️ Template Generator", icon="🤖"),
    ]
}

# Show the main page and sidebar
pg = st.navigation(pages, position="sidebar")

# Sidebar
sidebar = st.sidebar
with sidebar:
    st.subheader("Template Generator")
    st.image('images/header.png', width=200)
    minio = st.toggle("MinIO", False)
    if minio:
        try:
            # Establish MinIO session
            minio_client = connect_to_minio("localhost:9000", st.secrets['MinIO']['user'], st.secrets['MinIO']['pass'])

            # Select Schema
            schema = st.selectbox("Wähle die passende Konfiguration", options=list_buckets(minio_client))

            # Importing presets
            presets_csv = minio_client.get_object(schema.lower().replace(' ', '-'), "presets.csv")
            csv_data = presets_csv.read().decode('utf-8')
            presets = pd.read_csv(StringIO(csv_data), quotechar="'", delimiter=',')
        except S3Error as e:
            st.error(f"Keine Verbindung zu MinIO möglich: {e}")
    snowflake = st.toggle("Snowflake", True)
    if snowflake:
        try:
            # Establish Snowflake session
            session = create_session()

            # Select Schema
            schema = st.selectbox("Wähle die passende Konfiguration", options=list_stages(session))

            # Importing Schema
            csv_data = session.read.options({"FIELD_DELIMITER": ",", "FIELD_OPTIONALLY_ENCLOSED_BY": "'", "SKIP_HEADER": 1}).csv(f"@{schema.upper().replace(' ', '_')}/presets.csv")
            presets = csv_data.to_pandas()
            presets.columns = ["OPTION", "DEFAULT"]

        except Exception as e:
            st.error(f"Keine Verbindung zu Snowflake möglich: {e}")
    try:
        kunde = st.text_input("Kunde:", value=presets['DEFAULT'][presets['OPTION'] == 'Kunde'].to_string(index=False))
        web = st.toggle("Webscraper", value=eval(presets['DEFAULT'][presets['OPTION'] == 'Webscraper'].to_string(index=False)))
        if web:
            kunde_url = st.text_input("Kunden-Webseite (z.B. `Über uns`):", value=presets['DEFAULT'][presets['OPTION'] == 'WebUrl'].to_string(index=False))
            kunde_info = web_scraper(kunde_url)
        cloud = st.selectbox("Cloud:", options=["AWS", "Azure", "Google Cloud"], index=int(presets['DEFAULT'][presets['OPTION'] == 'Cloud'].to_string(index=False)))
        on = st.toggle("OpenAI ChatGPT", value=eval(presets['DEFAULT'][presets['OPTION'] == 'OpenAI'].to_string(index=False)))
        if not on:
            st.markdown("Local Server Configuration")
            url = st.text_input("URL:", value=presets['DEFAULT'][presets['OPTION'] == 'LLMUrl'].to_string(index=False))
            port = st.number_input("Port:", value=int(presets['DEFAULT'][presets['OPTION'] == 'LLMPort'].to_string(index=False)), min_value=1, max_value=65535)
        system = st.text_input("System:", value =presets['DEFAULT'][presets['OPTION'] == 'System'].to_string(index=False))
    except:
        st.error("Keine Konfiguration geladen.")

# Convert DOCX to PDF
def convert_docx_to_pdf(docx_content):
    # Creating a BytesIO object for the input file
    input_stream = BytesIO(docx_content)
    
    # Load the DOCX document
    document = Document(input_stream)

    # Creating a BytesIO object for the output file
    output_stream = BytesIO()

    # Creating the PDF document
    pdf = canvas.Canvas(output_stream, pagesize=letter)
    width, height = letter
    margin = 1 * inch
    y_position = height - margin
    line_height = 12
    max_line_width = width - 2 * margin

    # Inserting the paragraphs into the PDF
    for para in document.paragraphs:
        text = para.text
        wrapped_lines = wrap(text, width=int(max_line_width / 6))  # Estimate the number of characters per line
        for wrapped_line in wrapped_lines:
            if y_position < margin + line_height:
                pdf.showPage()
                y_position = height - margin
            pdf.drawString(margin, y_position, wrapped_line)
            y_position -= line_height
        y_position -= line_height
    pdf.save()
    
    # Relocating the pointer to the beginning of the output stream
    output_stream.seek(0)
    return output_stream.read()

# Title
st.title('❄️ Template Generator')
st.write('Dieses Tool erstellt ein Template-Dokument zu einer BAS-Anzeige zum Thema Sozialdatenverarbeitung.')

# Minio connection
if minio:
    with st.expander("MinIO Data Lake Inhalt"):
        try:
            if minio_client:
                st.success("Datenbankverbindung erfolgreich hergestellt.")
                st.write(f"Streamlit Version: {st.__version__}")
                st.write(f"Python Version: {sys.version}")

                # Loading database tables from csv files
                df_csv = minio_client.get_object(schema.lower().replace(' ', '-'), "anzeige_pre.csv")
                csv_data = df_csv.read().decode('utf-8')
                df = pd.read_csv(StringIO(csv_data), quotechar="'", delimiter=',')
                paragraphs_csv = minio_client.get_object(schema.lower().replace(' ', '-'), "anzeige_paragraphs.csv")
                csv_data = paragraphs_csv.read().decode('utf-8')
                paragraphs = pd.read_csv(StringIO(csv_data), quotechar="'", delimiter=',')

                #Files
                st.subheader("Dateien")
                uploaded_files = st.file_uploader("Datei(en) hochladen", accept_multiple_files=True, type=['csv', 'pdf', 'docx'])
                if uploaded_files:
                    try:
                        upload_files(minio_client, schema, uploaded_files)
                        st.success("Datei(en) erfolgreich hochgeladen.")
                    except S3Error as e:
                        st.error(f"Error: {e}")

                # Display objects in selected bucket
                st.write(f"Objekte in {schema}-Schema")
                objects = list_objects(minio_client, schema)
                filtered_objects = [
                                        object
                                        for object in objects
                                        if object.endswith(('.pdf', '.docx'))
                                    ]
                selected_object = st.selectbox("Wähle ein Objekt", filtered_objects)
                if selected_object:
                    try:
                        # Download the selected file and display it
                        data = minio_client.get_object(schema.lower().replace(' ', '-'), selected_object)
                        if selected_object.endswith('.pdf'):
                            pdf_content = data.read()
                        if selected_object.endswith('.docx'):
                            pdf_content = convert_docx_to_pdf(data.read())
                        pdf_viewer(pdf_content, height=800)
                    except S3Error as e:
                        st.error(f"Error: {e}")
            else:
                st.error("Keine Verbindung zum MinIO möglich.")
        except S3Error as e:
            st.error(f"Keine Verbindung zu MinIO möglich: {e}")

# Snowflake connection
if snowflake:
    with st.expander("Datenbankinhalt"):
        try:
            if session:
                st.success("Datenbankverbindung erfolgreich hergestellt.")
                st.write(f"Streamlit Version: {st.__version__}")
                st.write(f"Python Version: {sys.version}")

                # Loading database tables from csv files
                df_csv = session.read.options({"FIELD_DELIMITER": ",", "FIELD_OPTIONALLY_ENCLOSED_BY": "'", "SKIP_HEADER": 1}).csv(f"@{schema.upper().replace(' ', '_')}/anzeige_pre.csv")
                df = df_csv.to_pandas()
                df.columns = ["PARAGRAPH","PARAGRAPH_TITLE","PARAGRAPH_TEXT"]
                #df = load_data(session, 'DB_BG_HEALTH.PUBLIC.ANZEIGE_PRE')
                st.dataframe(df)
                paragraphs_csv = session.read.options({"FIELD_DELIMITER": ",", "FIELD_OPTIONALLY_ENCLOSED_BY": "'", "SKIP_HEADER": 1}).csv(f"@{schema.upper().replace(' ', '_')}/anzeige_paragraphs.csv")
                paragraphs = paragraphs_csv.to_pandas()
                paragraphs.columns = ["PARAGRAPH","PARAGRAPH_DESC","PARAGRAPH_URL"]
                #paragraphs = load_data(session, 'DB_BG_HEALTH.PUBLIC.ANZEIGE_PRE')
                st.dataframe(paragraphs)

                # Files
                st.subheader("Dateien")
                uploaded_files = st.file_uploader("Datei(en) hochladen", accept_multiple_files=True, type=['csv', 'pdf', 'docx'])
                if uploaded_files:
                    try:
                        uploading_files(session, schema, uploaded_files)
                        st.success("Datei(en) erfolgreich hochgeladen.")
                    except S3Error as e:
                        st.error(f"Error: {e}")
                st.write(f"Objekte in {schema}-Schema")
                objects = list_files(session, schema)
                filtered_objects = [
                                        object
                                        for object in objects
                                        if object.endswith(('.pdf', '.docx'))
                                    ]
                selected_object = st.selectbox("Wähle ein Objekt", filtered_objects)
                if selected_object:
                    try:
                        # Download the selected file and display it
                        data = session.file.get_stream(f"@{schema.upper().replace(' ', '_')}/{selected_object}")
                        if selected_object.endswith('.pdf'):
                            pdf_content = data.read()
                        if selected_object.endswith('.docx'):
                            pdf_content = convert_docx_to_pdf(data.read())
                        pdf_viewer(pdf_content, height=800)
                            
                    except S3Error as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Keine Verbindung zu Snowflake möglich.")
        except Exception as e:
            st.error(f"Keine Verbindung zu Snowflake möglich: {e}")

# Show ChatBot
pg.run()

# Show options
st.title("Konfiguration")
#try:
if not st.session_state['options_setup']:
    if minio:
        submitted, combined_list, options = frontend_options(df, schema, minio_client)
    if snowflake:
        submitted, combined_list, options = frontend_options(df, schema, session)
    if submitted:
        st.session_state['options_setup'] = True
        st.session_state['combined_list'] = combined_list
        st.session_state['options'] = options
if st.session_state['options_setup']:
    if minio:
        checked_in, chapters, table_of_contents, paragraph_of_summary, table_of_glossar, table_of_stakeholders, table_of_attachments = template_options(st.session_state['combined_list'], schema, minio_client)
    if snowflake:
        checked_in, chapters, table_of_contents, paragraph_of_summary, table_of_glossar, table_of_stakeholders, table_of_attachments = template_options(st.session_state['combined_list'], schema, session)
    if checked_in:
        # Erase previous messages
        st.session_state.pop("langchain_messages", None)
        
        # Set up memory
        msgs = StreamlitChatMessageHistory(key="langchain_messages")
        if len(msgs.messages) == 0:
            msgs.add_ai_message(f"""Ich schreibe den Text in einer sachlichen und formellen
                                    Form um und ersetze <Kunde> mit {kunde}, 
                                    <Cloud-Anbieter> mit {cloud}.""")

        # Set up the LangChain, passing in Message History
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", f"{system}"),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}"),
            ]
        )

        # Setting the LLM
        if on:
            chain = prompt | ChatOpenAI(
                model="gpt-4o-mini",
                api_key=st.secrets["openai"]["key"]
            )
        else:
            if snowflake:
                # Cortex AI
                #snowflake_connection = snowflake.connector.connect(
                #    connection_name="snowflake",
                #)
                llm = Cortex(model="mistral-7b", session=session)

                #llm = ChatSnowflakeCortex(connection=session, model="mistral-7b", snowflake_username="bengross", snowflake_password="adesso_2024", snowflake_account="sv04740.west-europe.azure", snowflake_role="HEALTH_DEV", snowflake_warehouse="COMPUTE_WH", snowflake_database="DB_BG_HEALTH", snowflake_schema="PUBLIC")
                output_parser = StrOutputParser()
                # create a chain
                chain = prompt | llm | output_parser
                #chain = prompt | Complete(
                #                    model="mistral-7b",
                #                    session=session,
                #                    stream=False) | output_parser
                #result = session.sql("SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large', 'Wie kann ich meine Daten in der Cloud sicher speichern?');").collect()
                #st.text(result[0][0])
            else:
                # Local Server
                server_url = f"{url}:{str(port)}/v1"
                chain = prompt | ChatOpenAI(
                    base_url=server_url,
                    model="llama-3.1-8b-chat-doctor-Q4_K_M_v2",
                    temperature=0.5,
                    max_tokens=4000,
                    api_key="lm-studio"
            )

        chain_with_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: msgs,
            input_messages_key="question",
            history_messages_key="history",
        )

        # Render current messages from StreamlitChatMessageHistory
        view_messages = st.status("Anzeige wird generiert...")
        with view_messages:
            for msg in msgs.messages:
                st.chat_message(msg.type).write(msg.content)

            # If user inputs a new prompt, generate and draw a new response
            chosen_chapters = []
            for chapter in chapters:
                # Erasing the first 9 letters
                last_chapter = chapter[0]
                chapter = chapter[9:]
                chosen_chapters.append(chapter)

            for text in df["PARAGRAPH_TEXT"]:
                if df["PARAGRAPH_TITLE"][df["PARAGRAPH_TEXT"] == text].to_string(index=False, header=False) in chosen_chapters:
                    if '<Kundeninfo>' in text and web:
                        prompt = text.replace('<Kunde>', str(kunde)).replace('<Cloud-Anbieter>', str(cloud)).replace('<Kundeninfo>', str(kunde_info))
                    else:
                        prompt = text.replace('<Kunde>', str(kunde)).replace('<Cloud-Anbieter>', str(cloud))
                    if '<§' or '<Art.' in prompt:
                        for paragraph in paragraphs["PARAGRAPH"]:
                            # Checking for matching paragraph
                            if paragraph in prompt:
                                prompt = prompt.replace(f"<{paragraph}>", paragraphs[paragraphs['PARAGRAPH'] == paragraph].drop(columns=paragraphs.columns[-1]).to_string(index=False, header=False))
                                paragraph_info = web_scraper(paragraphs[paragraphs['PARAGRAPH'] == paragraph].drop(columns=paragraphs.columns[:2]).to_string(index=False, header=False))
                                paragraph_info = paragraph_info.replace('\n', ' ')
                                prompt += paragraph_info
                    if '<option_' in prompt:
                        for option in st.session_state['options'].get('DESC', []):
                            prompt = prompt.replace(f"<{option}>", str(st.session_state['options'][st.session_state['options']['DESC'] == option].drop(columns=st.session_state['options'].columns[:1]).to_string(index=False, header=False)))

                    st.chat_message("human").write(prompt)

                    # Note: new messages are saved to history automatically by Langchain during run
                    config = {"configurable": {"session_id": "any"}}
                    response = chain_with_history.invoke({"question": prompt}, config)
                    st.chat_message("ai").write(response.content)

        # Draw the messages at the end, so newly generated ones show up immediately
        view_chat_messages = st.expander("Zeige die Daten des Chatbots.")
        with view_chat_messages:
            """
            Message History initialized with:
            ```python
            msgs = StreamlitChatMessageHistory(key="langchain_messages")
            ```

            Contents of `st.session_state.langchain_messages`:
            """
            view_chat_messages.json(st.session_state.langchain_messages)

        # Convert to dataframe
        messages = st.session_state.langchain_messages
        anzeige_temp = pd.DataFrame(columns=['PARAGRAPH', 'PARAGRAPH_TITLE', 'PARAGRAPH_TEXT'])
        counter = -1
        paragraph = -1
        for index, message in enumerate(messages):
            for key, value in message:
                if key == "content":
                    counter += 1
                    if counter > 0 and counter % 2 == 0:
                        paragraph += 1
                        anzeige_temp = anzeige_temp._append(pd.DataFrame([{
                                                                            'PARAGRAPH': df['PARAGRAPH'][paragraph],
                                                                            'PARAGRAPH_TITLE': df['PARAGRAPH_TITLE'][paragraph],
                                                                            'PARAGRAPH_TEXT': value
                                                                        }]), 
                                                            ignore_index=True)

        st.dataframe(anzeige_temp)
        if snowflake:
            write_data(session, anzeige_temp, table_name='ANZEIGE_TEMP', database=st.secrets.snowflake['database'], schema=st.secrets.snowflake['schema'])
        with st.expander("Datenbankinhalt", expanded=False):
            if snowflake:
                df = load_data(session, f"{st.secrets.snowflake['database']}.{st.secrets.snowflake['schema']}.ANZEIGE_TEMP")
                st.dataframe(df)

        # Export to Word
        export_doc(anzeige_temp, cloud, last_chapter, paragraph_of_summary, table_of_glossar, table_of_stakeholders, table_of_attachments, table_of_contents)
        st.session_state['options_setup'] = False
#except:
#    st.error("Keine Konfiguration geladen.")