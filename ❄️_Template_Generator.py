### `❄️_Template_Generator.py`
### ❄️ Template Generator
### Open-Source, hosted on https://github.com/SeriousBenEntertainment/Template_Generator
### Please reach out to benjamin.gross1@adesso.de for any questions
### Loading needed Python libraries
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import sys
from io import StringIO, BytesIO
from minio.error import S3Error
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from textwrap import wrap
sys.path.insert(1, "pages/functions/")
from Options import frontend_options
from Functions import connect_to_minio, list_buckets, list_objects, upload_files, create_session, load_data, write_data, export_doc, web_scraper

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
    minio = st.toggle("MinIO", True)
    snowflake = st.toggle("Snowflake", False)
    kunde = st.text_input("Kunde:", value="GWQ ServicePlus AG")
    web = st.toggle("Webscraper", True)
    if web:
        kunde_url = st.text_input("Kunden-Webseite (z.B. `Über uns`):", value="https://www.gwq-serviceplus.de/ueber-uns")
        kunde_info = web_scraper(kunde_url)
    cloud = st.selectbox("Cloud:", options=["AWS", "Azure", "Google Cloud"], index=2)
    service_1 = 'Google Cloud Vision'
    service_2 = 'Google Translate'
    on = st.toggle("OpenAI ChatGPT", False)
    if not on:
        st.markdown("Local Server Configuration")
        url = st.text_input("URL:", value="http://localhost")
        port = st.number_input("Port:", value=1234, min_value=1, max_value=65535)
    system = st.text_input("System:", value = f"Du erstellst einzelne Absätze einer Anzeige beim Bundesamt für Soziale Sicherung über die Verarbeitung von Sozialdaten im Auftrag (AVV) nach § 80 Zehntes Sozialgesetzbuch (SGB X). Tausche die Platzhalter (z.B. <Kunde>) durch die entsprechenden Inhalte aus und gebe nur den verbesserten Text in einer sachlichen und formellen Form aus und verzichte auf Phrasen wie z.B. 'Vielen Dank für die Informationen. Hier sind die angepassten Absätze für die Anzeige beim Bundesamt für Soziale Sicherung:'.")

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
        minio_client = connect_to_minio("localhost:9000", st.secrets['MinIO']['user'], st.secrets['MinIO']['pass'])
        if minio_client:
            st.success("Connected to MinIO")

            # Loading database tables from csv files
            df_csv = minio_client.get_object("templategenerator", "anzeige_pre.csv")
            csv_data = df_csv.read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_data), quotechar="'", delimiter=',')
            paragraphs_csv = minio_client.get_object("templategenerator", "anzeige_paragraphs.csv")
            csv_data = paragraphs_csv.read().decode('utf-8')
            paragraphs = pd.read_csv(StringIO(csv_data), quotechar="'", delimiter=',')

            # Upload files
            uploaded_files = st.file_uploader("Datei(en) hochladen", accept_multiple_files=True, type=['csv', 'pdf', 'docx'])
            if uploaded_files:
                try:
                    upload_files(minio_client, "templategenerator", uploaded_files)
                    st.success("Datei(en) erfolgreich hochgeladen.")
                except S3Error as e:
                    st.error(f"Error: {e}")

            # Display buckets
            st.subheader("Buckets")
            buckets = list_buckets(minio_client)
            if buckets:
                selected_bucket = st.selectbox("Wähle ein Bucket", buckets)

                # Display objects in selected bucket
                st.write(f"Objects in {selected_bucket}")
                objects = list_objects(minio_client, selected_bucket)
                filtered_objects = [
                                        object
                                        for object in objects
                                        if object.endswith(('.pdf', '.docx'))
                                    ]
                selected_object = st.selectbox("Wähle ein Objekt", filtered_objects)
                if selected_object:
                    try:
                        # Download the selected file and display it
                        data = minio_client.get_object(selected_bucket, selected_object)
                        if selected_object.endswith('.pdf'):
                            pdf_viewer(data.read(), height=800)
                        if selected_object.endswith('.docx'):
                            pdf_viewer(convert_docx_to_pdf(data.read()), height=800)
                    except S3Error as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Keine Buckets gefunden.")
        else:
            st.error("Keine Verbindung zum MinIO Data Lake möglich.")

# Snowflake connection
if snowflake:
    with st.expander("Datenbankinhalt"):
        # Establish Snowflake session
        session = create_session()
        if session:
            st.success("Datenbankverbindung erfolgreich hergestellt.")
            st.write(f"Streamlit Version: {st.__version__}")
            st.write(f"Python Version: {sys.version}")

            df = load_data(session, 'OPENAI_DATABASE.PUBLIC.ANZEIGE_PRE')
            st.dataframe(df)
            paragraphs = load_data(session, 'OPENAI_DATABASE.PUBLIC.ANZEIGE_PARAGRAPHS')
            st.dataframe(paragraphs)
            #options = load_data(session, 'OPENAI_DATABASE.PUBLIC.ANZEIGE_OPTIONS')
            #st.dataframe(options)
        else:
            st.error("Keine Verbindung zu Snowflake möglich.")


# Show ChatBot
pg.run()

# Show options
submitted, chapters, table_of_contents, paragraph_of_summary, table_of_glossar, table_of_stakeholders, table_of_attachments, options = frontend_options(df, minio_client)

if submitted:
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
        server_url = f"{url}:{str(port)}/v1"
        chain = prompt | ChatOpenAI(
            base_url=server_url,
            model="llama-3-8b-chat-doctor-Q4_K_M_v2",
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
                    for option in options['DESC']: 
                        prompt = prompt.replace(f"<{option}>", str(options[options['DESC'] == option].drop(columns=options.columns[:1]).to_string(index=False, header=False)))

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
        write_data(session, anzeige_temp, table_name='ANZEIGE_TEMP', database='OPENAI_DATABASE', schema='PUBLIC')
    with st.expander("Datenbankinhalt", expanded=False):
        if snowflake:
            df = load_data(session, 'OPENAI_DATABASE.PUBLIC.ANZEIGE_TEMP')
            st.dataframe(df)

    # Export to Word
    export_doc(anzeige_temp, cloud, service_1, service_2, last_chapter, paragraph_of_summary, table_of_glossar, table_of_stakeholders, table_of_attachments, table_of_contents)
