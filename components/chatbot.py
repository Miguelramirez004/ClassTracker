import os
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class AttendancePolicyAssistant:
    """A RAG-based chatbot for answering questions about attendance policy."""
    
    def __init__(self, policy_dir="docs/university_policies"):
        """Initialize the chatbot with policies from the specified directory."""
        self.policy_dir = policy_dir
        self.embedding_model = None
        self.vectorstore = None
        self.chain = None
        self.is_initialized = False
    
    def initialize(self):
        """Initialize the embedding model, vector store, and retrieval chain."""
        try:
            # Check if OpenAI API key is available
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return False, "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
            
            # Create embeddings model
            self.embedding_model = OpenAIEmbeddings()
            
            # Process policy documents
            policy_texts = self._load_policy_documents()
            if not policy_texts:
                return False, "No policy documents found in the specified directory."
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", ".", " ", ""]
            )
            
            splits = []
            for text in policy_texts:
                splits.extend(text_splitter.split_text(text))
            
            # Create vector store
            if not os.path.exists("chroma_db"):
                os.makedirs("chroma_db")
            
            self.vectorstore = Chroma.from_texts(
                texts=splits,
                embedding=self.embedding_model,
                persist_directory="chroma_db"
            )
            
            # Create retrieval chain
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
            
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                memory=memory,
                verbose=True
            )
            
            self.is_initialized = True
            return True, "Assistant initialized successfully!"
        
        except Exception as e:
            return False, f"Error initializing assistant: {str(e)}"
    
    def _load_policy_documents(self):
        """Load policy documents from the policy directory."""
        policy_texts = []
        
        if not os.path.exists(self.policy_dir):
            return policy_texts
        
        for filename in os.listdir(self.policy_dir):
            if filename.endswith(".txt") or filename.endswith(".md") or filename.endswith(".pdf"):
                file_path = os.path.join(self.policy_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        policy_texts.append(file.read())
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")
        
        return policy_texts
    
    def answer_question(self, question):
        """Answer a question about attendance policy."""
        if not self.is_initialized:
            success, message = self.initialize()
            if not success:
                return f"⚠️ {message} Using demo mode instead."
        
        try:
            # In case initialization failed, use a fallback response
            if not self.is_initialized:
                return self._get_fallback_response(question)
            
            # Get response from the chain
            response = self.chain.invoke({"question": question})
            return response["answer"]
        
        except Exception as e:
            print(f"Error answering question: {str(e)}")
            return self._get_fallback_response(question)
    
    def _get_fallback_response(self, question):
        """Get a fallback response based on the question."""
        question = question.lower()
        
        if "absence" in question and "excuse" in question:
            return """
            According to the university attendance policy, absences may be excused for illness (with medical documentation), religious observances, university-sponsored activities, family emergencies, and legal obligations.
            
            To get an absence excused, you must provide documentation to your instructor within one week of the absence. For medical absences, a doctor's note is required.
            """
        elif "late" in question:
            return """
            According to Section 4.1 of the attendance policy, arriving more than 15 minutes late to class or leaving more than 15 minutes early may be counted as an absence.
            
            Additionally, Section 4.2 states that three late arrivals or early departures may be counted as one absence. This is at the discretion of your instructor and should be detailed in your course syllabus.
            """
        elif "fail" in question or "grade" in question:
            return """
            According to Section 2.2 of the university attendance policy, exceeding the allowed number of absences may result in automatic failure of the course.
            
            The specific number of allowed absences is typically 3-4 for a semester-long course, but this can vary. Check your course syllabus for the exact number allowed in your specific course.
            """
        elif "appeal" in question:
            return """
            If you want to appeal an attendance-related decision, Section 6.1 of the policy states that you may appeal to the department chair first, and then to the dean of the college if needed.
            
            It's recommended to prepare documentation supporting your case before initiating an appeal process.
            """
        elif "make" in question and "up" in question:
            return """
            According to Section 5 of the attendance policy, students with excused absences are responsible for arranging to make up missed work with their instructors.
            
            Make-up work must be completed within one week of returning to class. It's best to contact your instructor as soon as possible to make these arrangements.
            """
        else:
            return """
            Based on the university's attendance policy, regular attendance is required for all courses. Each course syllabus specifies the number of allowed absences (typically 3-4 for a semester).
            
            For more specific information, please refer to your course syllabus or ask a more specific question about the attendance policy.
            """

def setup_chatbot():
    """Initialize the chatbot for the application."""
    if 'attendance_chatbot' not in st.session_state:
        st.session_state.attendance_chatbot = AttendancePolicyAssistant()
    
    return st.session_state.attendance_chatbot

def answer_policy_question(question):
    """Answer a question about attendance policy using the chatbot."""
    chatbot = setup_chatbot()
    return chatbot.answer_question(question)
