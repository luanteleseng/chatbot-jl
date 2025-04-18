import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Agente do Luanzinho 😎")
st.write(
    "Pergunte qualquer coisa sobre Engenharia de Dados e eu posso te ajudar!"
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Coloca sua chave aqui", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
        # Adiciona system prompt na inicialização
        st.session_state.messages.append({
            "role": "system",
            "content": (
                "Você é um assistente especialista em Engenharia de Dados. "
                "Responda perguntas sobre ETL, pipelines, bancos de dados, BigQuery, Kafka, Spark, modelagem de dados, arquitetura de dados, e cloud (GCP, AWS, Azure). "
                "Seja claro, técnico, direto e sempre em português. Dê exemplos de código quando possível."
            )
        })

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue  # não exibe o system prompt
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Pergunte ou solicite alguma coisa"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        system_message = {
            "role": "system",
            "content": (
                "Você é um assistente especialista em Engenharia de Dados. "
                "Você responde perguntas sobre ETL, pipelines, bancos de dados, BigQuery, Kafka, Spark, modelagem de dados, arquitetura de dados, cloud (GCP, AWS, Azure), e boas práticas. "
                "Seja claro, objetivo e use exemplos quando possível. Responda em português, a menos que o usuário peça o contrário."
            )
        }
        
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[system_message] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
