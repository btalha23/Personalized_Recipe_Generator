import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tracers.run_collector import RunCollectorCallbackHandler
from langchain_core.tracers.context import collect_runs
from langsmith import traceable
from langsmith import Client
import streamlit as st
from streamlit_feedback import streamlit_feedback
from dotenv import load_dotenv, find_dotenv
import os
import time


# # Database connection details
server = 'rag_application_server'
prg_database_name = 'personalized_recipe_generator'
user = 'root'
password = 'root'
host="localhost"
port="3306"

def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
  db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
  return SQLDatabase.from_uri(db_uri)

# # Now, you can interact with this table using LangChain's SQLDatabase
db = init_database(
  user=user,
  password=password,
  host=host,
  port=port,
  database=prg_database_name
  )
st.session_state.db = db
# Verify by printing the list of tables in the database
print(db.dialect)
print(db.get_usable_table_names())  # This should list the newly created table

def get_sql_chain_prg(db: SQLDatabase, model_choice: str):

    model=model_choice.split('/')[-1]
    print(f"selected LLM model: {model}")

    template = """
        You are a world's renowned chef, who can create a dish with any ingredients that are given to you.
        You have a tremendous experience in a varitey of cuisines, like for example continental, indian, mexican,
        chinese, vetnamise, thai, middle eastern, turkish, lebanese, italian, spanish, french, japanese, british, 
        and the list continues.
        You have expertize in making both vegetarian and non-vegetarian dishes. Expert meat as well as fish and seafood cook.
        You are well versed about different how to cater for gluten free or lactose free diets.

        Use all the knowledge you have to create a new, delicious recipe from the ingredients chosen by the user.

        Based on the table schema below, write a SQL query that would answer the user's question. 
        Take the conversation history into account.

        <SCHEMA>{schema}</SCHEMA>

        Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, 
        not even backticks.

        For example:
        Question: Need a recipe using chicken, tomato, basil
        SQL Query: SELECT * 
                FROM recipe_knowledge_base 
                WHERE NER LIKE CONCAT('%', 'chicken', '%') 
                AND NER LIKE CONCAT('%', 'tomato', '%') 
                AND NER LIKE CONCAT('%', 'basil', '%');
        Question: Do you have recipes for chicken?
        SQL Query: SELECT * 
                FROM recipe_knowledge_base 
                WHERE NER LIKE '%chicken%';
        Question: Name 10 dishes
        SQL Query: SELECT name FROM recipe_knowledge_base LIMIT 10;

        Your turn:

        Question: {question}
        SQL Query:
    """

    prompt = ChatPromptTemplate.from_template(template)
  
    llm = ChatOpenAI(temperature=0, 
                 model=model) # "gpt-4o-mini"
    
    def get_schema(_):
        return db.get_table_info()
        
    # sql_chain = (
    #     RunnablePassthrough.assign(schema=get_schema)
    #     | prompt
    #     | llm.bind(stop=["\SQL Result:"])
    #     | StrOutputParser()
    # )
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm.bind(stop=["\nSQL Result:"])
        | StrOutputParser()
    )


def get_response(user_query: str, model_choice: str, db: SQLDatabase, chat_history: list):
    
    sql_query_chain = get_sql_chain_prg(db, model_choice)
    print(f"generated SQL query: {sql_query_chain}")

    model=model_choice.split('/')[-1]
    print(f"selected LLM model: {model}")

    full_chain_template = """
        You are a world's renowned chef, who can create a dish with any ingredients that are given to you.
        You have a tremendous experience in a varitey of cuisines, like for example continental, indian, mexican,
        chinese, vetnamise, thai, middle eastern, turkish, lebanese, italian, spanish, french, japanese, british, 
        and the list continues.
        You have expertize in making both vegetarian and non-vegetarian dishes. Expert meat as well as fish and seafood cook.
        You are well versed about different how to cater for gluten free or lactose free diets.

        Use all the knowledge you have to create a new, delicious recipe from the ingredients chosen by the user.
        There are going to be 8 or less ingredients given to you by the user. You also have access to some pantry staples like
        cream, eggs, butter, milk, vinegar, sugar and flour. 
        You are allowed to mix and match steps, thoughts, and ideas from your knowledge. Do not copy and paste 
        the recipe directly from the database. Show innovation and creativity in the final dish.
        
        Based on the table schema below, question, sql query, and sql response, write a natural language response.
        The natural language response should not have any mention of SQL response and SQL query.

        <SCHEMA>{schema}</SCHEMA>
    
        SQL Query: <SQL>{query}</SQL>
        User Question: {question}
        SQL Response: {response}
        """
    
    prompt = ChatPromptTemplate.from_template(full_chain_template)
    
    llm = ChatOpenAI(temperature=0, 
                    model=model) # "gpt-4o-mini"
    chain = (
        RunnablePassthrough.assign(query=sql_query_chain).assign(
        schema=lambda _: db.get_table_info(),
        response=lambda vars: db.run(vars["query"])
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.invoke({
        "question": user_query
    })

st.title("Personalized Recipe Generator")

load_dotenv(find_dotenv())
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "PRG RAG App Eval Experiments"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
client = Client()

# Model selection
model_choice = st.sidebar.selectbox(
    "Select a model:",
    ["openai/gpt-3.5-turbo", "openai/gpt-4o-mini"],
)
print(f"User selected model: {model_choice}")

if "chat_history" not in st.session_state:
  st.session_state.chat_history = [
    AIMessage(content="""Hello, I am a chef to assist you with your meal today.
              Give me 8 or less ingredients so that I can provide you with 
              the most delicious dish you have ever tasted. 
              Lets start cooking.""")
  ]

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

last_ai_message = ""
user_query = st.chat_input("Type a message...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
        
    with st.chat_message("AI"):
        # response = get_response_loyalty_customer(user_query, st.session_state.db, st.session_state.chat_history)
        with collect_runs() as runs_cb:
            response = get_response(user_query, model_choice, 
                                    st.session_state.db, 
                                    st.session_state.chat_history)
            st.markdown(response)
            st.session_state.last_run = runs_cb.traced_runs[0].id
        
    st.session_state.chat_history.append(AIMessage(content=response))
    
@st.cache_data(ttl="2h", show_spinner=False)
def get_run_url(run_id):
    time.sleep(1)
    return client.read_run(run_id).url


if st.session_state.get("last_run"):
    run_url = get_run_url(st.session_state.last_run)
    st.sidebar.markdown(f"[Latest Trace: 🛠️]({run_url})")
    feedback = streamlit_feedback(
        feedback_type="faces",
        optional_text_label="[Optional] Please provide an explanation",
        key=f"feedback_{st.session_state.last_run}",
    )
    if feedback:
        scores = {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0}
        client.create_feedback(
            st.session_state.last_run,
            feedback["type"],
            score=scores[feedback["score"]],
            comment=feedback.get("text", None),
        )
        st.toast("Feedback recorded!", icon="📝")