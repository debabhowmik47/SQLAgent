# SQL Chatbot Boss (LangGraph + Gemini + MySQL)

This project is a command-line chatbot that answers questions about a MySQL database.  
It uses:

- **Google Gemini (via `langchain-google-genai`)** to:
  - Convert natural language questions into SQL.
  - Summarize SQL results into human-readable answers.
- **MySQL** as the data source.
- **LangGraph** to define a simple 3-step workflow:
  1. `question_to_sql`
  2. `execute_sql`
  3. `summarize_result`

---

## Features

- Ask natural language questions about your `salesdb.data` table.
- Automatically generates valid MySQL queries using Gemini.
- Executes SQL against your local MySQL database.
- Returns a concise, natural language answer.

---

## Project Structure

```text
.
├─ main.py              # Your chatbot code (the script in this repo)
├─ requirements.txt     # Python dependencies
├─ .env                 # Environment variables (Google API key, etc.) - NOT committed
└─ README.md            # Project documentation
