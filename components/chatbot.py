import os
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from datetime import datetime

class AttendancePolicyAssistant:
    """A streamlined RAG-based chatbot for answering questions about attendance policy."""
    
    def __init__(self, policy_dir="docs/university_policies"):
        """Initialize the chatbot with policies from the specified directory."""
        self.policy_dir = policy_dir
        self.model = None
        self.memory = None
        self.is_initialized = False
        
        # System prompt template for the assistant
        self.system_prompt = """You are an intelligent attendance policy assistant for a university.
        You help students and faculty understand attendance policies and rules.
        Your goal is to provide accurate, helpful information based on the university's official attendance policy.
        
        Current date and time: {current_time}"""
        
        # User prompt template with policy context
        self.user_prompt = """
        Attendance Policy:
        {policy_data}
        
        Chat History:
        {chat_history}
        
        User Question: {question}
        
        Please provide a clear, specific answer based on the attendance policy.
        If the policy doesn't address the question, acknowledge that and provide general guidance.
        Make sure to cite specific sections of the policy when relevant (e.g., "According to Section 3.1...").
        """
    
    def initialize(self):
        """Initialize the LLM and memory."""
        try:
            # Check if OpenAI API key is available
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return False, "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
            
            # Initialize the LLM
            self.model = ChatOpenAI(
                api_key=api_key,
                model_name="gpt-3.5-turbo",
                temperature=0.0
            )
            
            # Initialize conversation memory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            self.is_initialized = True
            return True, "Assistant initialized successfully!"
        
        except Exception as e:
            return False, f"Error initializing assistant: {str(e)}"
    
    def _load_policy_document(self):
        """Load the attendance policy document."""
        try:
            # Look for attendance policy files
            if os.path.exists(self.policy_dir):
                for filename in os.listdir(self.policy_dir):
                    if "attendance" in filename.lower() and filename.endswith((".txt", ".md")):
                        file_path = os.path.join(self.policy_dir, filename)
                        with open(file_path, "r", encoding="utf-8") as file:
                            return file.read()
            
            # Fallback to hardcoded policy if file isn't found
            return """
            UNIVERSITY ATTENDANCE POLICY

            1. General Attendance Requirements

            Regular attendance is required for all courses. Students are expected to attend all classes for the courses in which they are registered.

            2. Absence Limits

            2.1 Each course syllabus will specify the number of allowed absences (typically 3-4 for a semester-long course).

            2.2 Exceeding the allowed number of absences may result in automatic failure of the course.

            3. Excused Absences

            3.1 Absences may be excused for the following reasons:
            - Illness (with medical documentation)
            - Religious observances
            - University-sponsored activities
            - Family emergencies
            - Legal obligations

            3.2 Documentation must be provided to the instructor within one week of the absence.

            4. Late Arrivals and Early Departures

            4.1 Arriving more than 15 minutes late or leaving more than 15 minutes early may be counted as an absence.

            4.2 Three late arrivals or early departures may be counted as one absence.

            5. Make-up Work

            5.1 Students with excused absences are responsible for arranging to make up missed work.

            5.2 Make-up work must be completed within one week of returning to class.

            6. Appeals

            6.1 Students may appeal attendance-related decisions to the department chair and then to the dean of the college.
            """
        except Exception as e:
            print(f"Error loading policy document: {str(e)}")
            return self._get_fallback_policy()
    
    def _get_fallback_policy(self):
        """Return a fallback policy text in case of errors."""
        return """
        UNIVERSITY ATTENDANCE POLICY

        1. General Attendance Requirements
        Regular attendance is required for all courses.

        2. Absence Limits
        Exceeding the allowed number of absences (typically 3-4) may result in failure.

        3. Excused Absences
        Absences may be excused with proper documentation (medical, religious, etc.).

        4. Late Arrivals
        Excessive lateness may count as absences.

        5. Make-up Work
        Students with excused absences can make up missed work.

        6. Appeals
        Students may appeal attendance decisions through proper channels.
        """
    
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
            
            # Load policy text
            policy_text = self._load_policy_document()
            
            # Create the prompt with ChatPromptTemplate
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("human", self.user_prompt)
            ])
            
            # Format the prompt with our context
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_prompt = prompt.format(
                current_time=current_time,
                policy_data=policy_text,
                chat_history=str(self.memory.chat_memory.messages) if self.memory and hasattr(self.memory, 'chat_memory') else "",
                question=question
            )
            
            # Get the response from the model
            response = self.model.invoke(formatted_prompt)
            
            # Update memory
            if self.memory:
                self.memory.chat_memory.add_user_message(question)
                self.memory.chat_memory.add_ai_message(response.content)
            
            return response.content
        
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
