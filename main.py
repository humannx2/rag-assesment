import duckdb
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# SQL prompt
sql_prompt = PromptTemplate.from_template("""
You are an assistant that converts natural language observability questions into SQL.
Use the table `telemetry` with the columns: `timestamp`, `server`, `cpu`, `memory`, `disk`.

Question: {query}
SQL:
""")
sql_chain = sql_prompt | llm

# Summary prompt
summary_prompt = PromptTemplate.from_template("""
You are an assistant that summarizes SQL query results into human-readable insights.

SQL Result:
{result}

Summary:
""")
summary_chain = summary_prompt | llm

# execution functions

def run_sql(sql: str):
    try:
        con = duckdb.connect("telemetry.duckdb")
        result_df = con.execute(sql).fetchdf()
        return result_df.to_markdown(index=False)
    except Exception as e:
        return f"Error executing SQL: {e}"

def answer_query(user_query):
    print(f"Question: {user_query}")

    # convert to SQL
    sql_message = sql_chain.invoke({"query": user_query})
    sql = sql_message.content.strip()
    
    # removing markdown code blocks if present
    if "```" in sql:
        parts = sql.split("```")
        if len(parts) >= 3:  # proper markdown format with start and end ticks
            sql_part = parts[1]
            # Remove the "sql" language identifier incase llm adds it
            if sql_part.startswith("sql"):
                sql = sql_part[3:].strip()
            else:
                sql = sql_part.strip()
    
    print(f"\n SQL Output:\n{sql}")

    # run SQL
    result = run_sql(sql)
    print(f"\n SQL Result:\n{result}")

    # result into summary
    summary_message = summary_chain.invoke({"result": result})
    summary = summary_message.content
    print(f"\n Final Answer:\n{summary}")

# main loop

if __name__ == "__main__":
    print(" RAG Observability Assistant")
    print("Ask a question, or type 'exit' to quit.\n")

    while True:
        query = input(">> You: ")
        if query.lower() in ["exit", "quit"]:
            break
        answer_query(query)
