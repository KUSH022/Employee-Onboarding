import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Constants
MODEL_NAME = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
POLICY_PDF = os.path.join("data", "policy.pdf")

class RAGPipeline:
    def __init__(self):
        self._llm = None
        self._embeddings = None
        self._vector_store = None
        self._initialize_resources()

    def _initialize_resources(self):
        try:
            self._llm = ChatGroq(
                model=MODEL_NAME,
                temperature=0.1,
                groq_api_key=os.getenv("GROQ_API_KEY")
            )
            self._embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            self._initialize_vector_store()
        except Exception as e:
            raise Exception(f"Failed to initialize AI resources: {str(e)}")

    def _initialize_vector_store(self):
        if not os.path.exists(POLICY_PDF):
            raise FileNotFoundError(f"Policy document not found at {POLICY_PDF}. Please ensure the PDF is uploaded to the data directory.")
        
        loader = PyPDFLoader(POLICY_PDF)
        docs = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = splitter.split_documents(docs)
        
        self._vector_store = FAISS.from_documents(chunks, self._embeddings)

    def get_response(self, query, chat_history, role="Employee", name="User"):
        try:
            # Similarity Search with Score
            docs_with_scores = self._vector_store.similarity_search_with_score(query, k=4)
            relevant_docs = [doc for doc, score in docs_with_scores if score < 1.5]
            
            if not relevant_docs:
                return f"I couldn't find any specific policies related to your question, {name}. Please contact HR at hr@company.com for role-specific guidance."
            
            context = "\n".join([doc.page_content for doc in relevant_docs])
            
            # Build memory-aware prompt
            history_str = ""
            for msg in chat_history[-6:]:
                role_label = "User" if msg["role"] == "user" else "Assistant"
                history_str += f"{role_label}: {msg['content']}\n"
            
            system_prompt = f"""You are a professional Enterprise HR Assistant.
Your goal is to answer the user's question based ONLY on the provided Context.
You must speak directly to the user (Name: {name}) and take their role (Role: {role}) into account.

Role-Based Guidance:
- If the user is a 'Manager', focus on leadership and oversight aspects within policies.
- If the user is an 'Engineer', focus on operational and technical execution aspects.

Context:
{context}

Recent Conversation:
{history_str}

User Question: {query}
Professional Response for {name} ({role}):"""

            response = self._llm.invoke(system_prompt)
            return response.content.strip()
            
        except Exception as e:
            print(f"RAG Error: {str(e)}")
            return "I apologize, but I'm having trouble connecting to my knowledge base right now. Please try again in a moment."
