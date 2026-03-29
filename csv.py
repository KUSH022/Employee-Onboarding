import os
import httpx
import pandas as pd
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# ------------------ CONFIG ------------------
BASE_DIR = "data/employees"
os.makedirs(BASE_DIR, exist_ok=True)

FILE_PATH = os.path.join(BASE_DIR, "employees.csv")

# ------------------ LLM SETUP ------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)


# ------------------ PROMPT ------------------
num_records = 50

prompt = f"""
Generate {num_records} rows of realistic employee data for a corporate company.

Rules:
- Output ONLY CSV format
- Columns: Employee ID, Name, Role, Department
- Employee ID should be numeric and unique
- Roles should include: Intern, Engineer, Senior Engineer, Manager, HR, Director
- Departments should include: IT, HR, Finance, Sales, Operations
- Names should be realistic Indian names
- Do NOT include any explanation

Example format:
Employee ID,Name,Role,Department
101,Rahul Sharma,Engineer,IT
102,Priya Singh,Manager,HR
"""

# ------------------ GENERATE ------------------
print("Generating employee data using LLM...")

response = llm.invoke(prompt)

csv_text = response.content.strip()

# ------------------ CLEAN OUTPUT ------------------
# Remove accidental markdown formatting if any
if "```" in csv_text:
    csv_text = csv_text.split("```")[1]
    if csv_text.startswith("csv"):
        csv_text = csv_text[3:]

# ------------------ SAVE ------------------
with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(csv_text)

print(f"✅ Employee data saved at: {FILE_PATH}")

# ------------------ VALIDATION ------------------
try:
    df = pd.read_csv(FILE_PATH)
    print("\nSample Data:")
    print(df.head())
except Exception as e:
    print("⚠️ Error reading CSV:", e)

