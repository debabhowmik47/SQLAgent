import mysql.connector
from dotenv import load_dotenv
import os
from typing import TypedDict, List, Optional

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found.")

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Debangshu2003",
        database="salesdb"
    )
    mycursor = mydb.cursor()
    print("Successfully connected to MySQL.")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit()


def run_query(sql):
    """Executes the given SQL query and returns the results."""
    try:
        print(f"Executing SQL: {sql}")
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return result
    except Exception as e:
        return f"SQL Error: {e}"

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=api_key)


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        input: The user's question.
        sql: The SQL query generated from the question.
        result: The result from executing the SQL query.
        output: The final natural language answer.
    """
    input: str
    sql: Optional[str]
    result: Optional[List]
    output: Optional[str]



def question_to_sql(state: GraphState):
    """Converts the natural language question to a SQL query using Gemini."""
    question = state['input']
    
    schema = """
    Table Name: data
    Columns: Rank (INT), Name (VARCHAR), Industry (VARCHAR), `Revenue [USD millions]` (INT), `Revenue growth` (VARCHAR), Employees (INT), Headquarters (VARCHAR)
    """

    prompt = f"""Given the following user question and database schema, generate a concise MySQL query that can answer the question.
Only return the SQL query and nothing else. Do not include any explanation or markdown formatting.

Schema:
{schema}

Question: {question}
SQL Query:"""

    response = llm.invoke(prompt)
    sql_query = response.content
    sql_cleaned = sql_query.strip().replace("```sql", "").replace("```", "").strip()

    print(f"Generated SQL: {sql_cleaned}")
    return {'sql': sql_cleaned}

def execute_sql(state: GraphState):
    """Executes the SQL query from the previous step."""
    sql = state['sql']
    result = run_query(sql)
    print(f"Raw SQL result: {result}")
    return {'result': result}

def summarize_result(state: GraphState):
    """Summarizes the SQL result into a natural language answer."""
    result = state['result']
    question = state['input']
    sql_query = state['sql'] 
    
    if isinstance(result, str):

        return {'output': result}
    

    prompt = f"""You are an intelligent assistant. Based on the following information, provide a concise, natural language answer.
    
    Original Question: "{question}"
    SQL Query Used: "{sql_query}"
    Query Result: {result}
    
    Answer:"""
    
    summary_response = llm.invoke(prompt)
    summary = summary_response.content
    
    return {'output': summary}

from langgraph.graph import StateGraph, END

builder = StateGraph(GraphState)
builder.add_node("question_to_sql", question_to_sql)
builder.add_node("execute_sql", execute_sql)
builder.add_node("summarize_result", summarize_result)

builder.set_entry_point("question_to_sql")
builder.add_edge("question_to_sql", "execute_sql")
builder.add_edge("execute_sql", "summarize_result")
builder.add_edge("summarize_result", END)

graph = builder.compile()

def chatbot():
    print(" Welcome to the SQL Chatbot Boss!")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")

        if question.lower() in ["exit", "quit"]:
            print(" Exiting chatbot Boss. ")
            break

        print(f"\n--- Running Graph for: '{question}' ---")
        try:
            result = graph.invoke({"input": question})
            print("\n--- Final Answer ---")
            print(result['output'])
        except Exception as e:
            print(" Error processing your question:", str(e))

# Start the chatbot
chatbot()
