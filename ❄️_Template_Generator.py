### `❄️_Template_Generator.py`
### ❄️ Template Generator
### Open-Source, hosted on https://github.com/SeriousBenEntertainment/Template_Generator
### Please reach out to ben@seriousbenentertainment.org for any questions
### Loading needed Python libraries
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
pd.set_option('display.max_colwidth', None)
import sys
import logging
import warnings
warnings.filterwarnings(
    action='ignore',
    category=UserWarning,
    module='snowflake.connector'
)
import sys
import time
import os
import fnmatch
from typing import List
from io import StringIO, BytesIO
from minio.error import S3Error
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader, Docx2txtLoader, CSVLoader, PyPDFLoader, TextLoader
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_snowrag.embedding import SnowflakeEmbeddings
from langchain_snowrag.llms import Cortex
from langchain_snowrag.vectorstores import SnowflakeVectorStore
from langchain_openai import ChatOpenAI
from snowflake.snowpark.types import *
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from textwrap import wrap
from Options import frontend_options
from Template import template_options
from Functions import connect_to_minio, list_buckets, list_objects, upload_files, create_session, list_stages, list_files, load_data, write_data, uploading_files, export_doc, web_scraper, Cortex

# Define session states
if 'options_setup' not in st.session_state:
    st.session_state.options_setup = False
if 'combined_list' not in st.session_state:
    st.session_state['combined_list'] = []
if 'options' not in st.session_state:
    st.session_state['options'] = {}
    
# Set Vectorization details
MODEL_LLM = "mistral-large"
MODEL_EMBEDDINGS = "multilingual-e5-large"
VECTOR_LENGTH = 1024

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
            minio_client = connect_to_minio(st.secrets['MinIO']['url'], st.secrets['MinIO']['user'], st.secrets['MinIO']['pass'], st.secrets['MinIO']['secure'])

            # Select Schema
            schema = st.selectbox("Wähle die passende Konfiguration", options=list_buckets(minio_client))

            # Importing presets
            presets_csv = minio_client.get_object(schema.lower().replace(' ', '-'), "presets.csv")
            csv_data = presets_csv.read().decode('utf-8')
            presets = pd.read_csv(StringIO(csv_data), quotechar="'", delimiter=',')
        except S3Error as e:
            st.error(f"Keine Verbindung zu MinIO möglich: {e}")
    snowflake = st.toggle("Snowflake", False)
    if snowflake:
        snowflake_rag = st.toggle("Snowflake RAG", False)
        if snowflake_rag:
            folder = os.path.abspath(os.path.join(os.getcwd(), '..'))
            options_offline_resources = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
            st.session_state.option_offline_resources = st.selectbox("Offline Resources", options_offline_resources)
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
            st.session_state.kunde_url = st.text_input("Kunden-Webseite (z.B. `Über uns`):", value=presets['DEFAULT'][presets['OPTION'] == 'WebUrl'].to_string(index=False))
            kunde_info = web_scraper(st.session_state.kunde_url)
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
st.write('Dieses Tool erstellt ein Template-Word-Dokument.')

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
                st.dataframe(df)
                paragraphs_csv = minio_client.get_object(schema.lower().replace(' ', '-'), "anzeige_paragraphs.csv")
                csv_data = paragraphs_csv.read().decode('utf-8')
                paragraphs = pd.read_csv(StringIO(csv_data), quotechar="'", delimiter=',')
                st.dataframe(paragraphs)

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

                # Snowflake RAG
                if snowflake_rag:
                    with st.spinner("Processing documents..."):
                        if "vector" not in st.session_state:
                            class CustomDirectoryLoader:
                                def __init__(self, urls, directory_path: str, glob_pattern: str = "*.*"):
                                    """
                                    Initialize the loader with a directory path and a glob pattern.
                                    :param directory_path: Path to the directory containing files to load.
                                    :param glob_pattern: Glob pattern to match files within the directory.
                                    :param mode: Mode to use with UnstructuredFileLoader ('single', 'elements', or 'paged').
                                    """
                                    self.urls = urls
                                    self.directory_path = directory_path
                                    self.glob_pattern = glob_pattern

                                def load(self) -> List[Document]:
                                    """
                                    Load all files matching the glob pattern in the directory using UnstructuredFileLoader.
                                    :return: List of Document objects loaded from the files.
                                    """
                                    documents = []
                                    patterns = self.glob_pattern.split('|')

                                    # Iterate over all files matched by the glob pattern using os.walk and fnmatch
                                    for root, dirs, files in os.walk(self.directory_path):
                                        st.markdown("**Documents**")
                                        for filename in files:
                                            for pattern in patterns:
                                                if fnmatch.fnmatch(filename, pattern):
                                                    file_path = os.path.join(root, filename)
                                                    if file_path.endswith(".docx"):
                                                        loader = Docx2txtLoader(file_path=file_path)
                                                    if file_path.endswith(".csv"):
                                                        loader = CSVLoader(file_path=file_path)
                                                    if file_path.endswith(".pdf"):
                                                        loader = PyPDFLoader(file_path=file_path)
                                                    if file_path.endswith(".txt"):
                                                        loader = TextLoader(file_path=file_path)
                                                    st.markdown(f"{os.path.basename(file_path)}")
                                                    docs = loader.load()
                                                    documents.extend(docs)
                                    if isinstance(self.urls, str):
                                        self.urls = [self.urls]
                                    st.markdown("**Online**")
                                    if len(self.urls[0]) > 0:
                                        for url in self.urls:
                                            st.write(url.strip())
                                            loader = WebBaseLoader(url)
                                            docs = loader.load()
                                            documents.extend(docs)
                                    return documents

                            st.session_state.start = time.time()
                            st.session_state.embeddings = SnowflakeEmbeddings(
                                connection=session.connection, model=MODEL_EMBEDDINGS
                            )
                            folder = os.path.abspath(os.path.join(os.getcwd(), '..', st.session_state.option_offline_resources))
                            urls = st.session_state.kunde_url.split(',')
                            st.session_state.loader = CustomDirectoryLoader(urls=urls, directory_path=folder, glob_pattern="*.docx|*.pdf|*.csv|*.txt")

                            st.session_state.docs = st.session_state.loader.load()

                            st.session_state.text_splitter = RecursiveCharacterTextSplitter(
                                chunk_size=1000, chunk_overlap=200
                            )
                            st.session_state.documents = st.session_state.text_splitter.split_documents(
                                st.session_state.docs
                            )
                            st.session_state.vector = SnowflakeVectorStore.from_documents(
                                st.session_state.documents,
                                st.session_state.embeddings,
                                vector_length=VECTOR_LENGTH,
                            )
                            st.success(f"Documents processed in {int(time.time() - st.session_state.start)} seconds!")

                    llm = Cortex(connection=session.connection, model=MODEL_LLM)
                    prompt = ChatPromptTemplate.from_template(
                        """
                        {system}
                        <context>
                        {context}
                        </context>

                        Zusätzliche Informationen: {input}"""
                    )

                    document_chain = create_stuff_documents_chain(llm, prompt)

                    retriever = st.session_state.vector.as_retriever()
                    retrieval_chain = create_retrieval_chain(retriever, document_chain)

                    # Then pass the prompt to the LLM
                    system = st.text_input("System Message", value="Du bist ein Rechtsanwalt. Denke Schritt um Schritt.")
                    prompt = st.text_input("Frage")
                    if prompt:
                        st.session_state.start  = time.time()
                        input_data = {
                            "system": system,
                            "input": prompt
                        }
                        response = retrieval_chain.invoke(input_data)
                        st.write(f"{response['answer']} (processed in {int(time.time() - st.session_state.start)} seconds.)")

                        # Find the relevant chunks
                        st.markdown("**Quellen**")
                        for i, doc in enumerate(response["context"]):
                            st.write(doc.page_content)
                            st.write("--------------------------------")

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
#pg.run()

# Show options
st.title("Konfiguration")
try:
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

            # Setting the LLMs
            # ChatGPT gpt-4o-mini
            if on:
                chain = prompt | ChatOpenAI(
                    model="gpt-4o-mini-2024-07-18",
                    api_key=st.secrets["openai"]["key"],
                    streaming=False,
                )

            # Cortex AI
            #mistral-large
            if snowflake:
                chain = prompt | Cortex(
                    session=session, 
                    model="llama3.1-8b"
                )

            # Local LLM Server
            # model="llama-3.1-8b-chat-doctor-Q4_K_M_v2",
            if not snowflake and not on:
                server_url = f"{url}:{str(port)}/v1"
                chain = prompt | ChatOpenAI(
                    base_url=server_url,
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
                        if snowflake:
                            st.chat_message("ai").write(response)
                        else:
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
except Exception as e:
    st.error(e)