import streamlit as st
import sys
import os
from datetime import datetime, timedelta
import pandas as pd
from streamlit_option_menu import option_menu

# Import config and placeholder data
from config import DEMO_STUDENTS, DEMO_PROFESSORS, DEMO_COURSES

# Configure page
st.set_page_config(
    page_title="ClassTracker Demo",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_path = os.path.join('static', 'css', 'style.css')
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Create a basic CSS file if it doesn't exist
        os.makedirs(os.path.join('static', 'css'), exist_ok=True)
        with open(os.path.join('static', 'css', 'style.css'), 'w') as f:
            f.write("""
            .stApp {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .main-header {
                background-color: #f0f2f6;
                padding: 1rem;
                margin-bottom: 1rem;
                border-radius: 5px;
            }
            
            .attendance-card {
                background-color: white;
                border-radius: 5px;
                padding: 1rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
            }
            
            .notification-item {
                border-left: 3px solid #ff4b4b;
                padding-left: 10px;
                margin-bottom: 10px;
            }
            
            .warning-threshold {
                color: #ff4b4b;
                font-weight: bold;
            }
            """)
        with open(css_path, 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    # Initialize session state for demo
    if 'role' not in st.session_state:
        st.session_state.role = None
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    # Try to load CSS
    try:
        load_css()
    except Exception as e:
        st.error(f"Error loading CSS: {e}")
    
    # Sidebar for role selection
    with st.sidebar:
        st.title("ClassTracker Demo")
        st.caption("A Streamlit Attendance Tracking App")
        
        # Role selector
        role_options = ["Choose Role", "Student", "Professor"]
        selected_role = st.selectbox("Select Role", role_options, index=0)
        
        if selected_role == "Student":
            st.session_state.role = "student"
            student_options = [f"{student['name']} ({student['student_id']})" for student in DEMO_STUDENTS]
            selected_student = st.selectbox("Select Student", student_options)
            student_idx = student_options.index(selected_student)
            st.session_state.user_id = DEMO_STUDENTS[student_idx]['id']
            st.session_state.user_name = DEMO_STUDENTS[student_idx]['name']
            st.session_state.user_details = DEMO_STUDENTS[student_idx]
        
        elif selected_role == "Professor":
            st.session_state.role = "professor"
            professor_options = [f"{professor['name']} ({professor['department']})" for professor in DEMO_PROFESSORS]
            selected_professor = st.selectbox("Select Professor", professor_options)
            professor_idx = professor_options.index(selected_professor)
            st.session_state.user_id = DEMO_PROFESSORS[professor_idx]['id']
            st.session_state.user_name = DEMO_PROFESSORS[professor_idx]['name']
            st.session_state.user_details = DEMO_PROFESSORS[professor_idx]
        
        else:
            st.session_state.role = None
            st.session_state.user_id = None
    
    # Main content area
    if st.session_state.role is None:
        show_welcome_screen()
    else:
        show_navigation()

def show_welcome_screen():
    """Display welcome screen with app info"""
    st.title("Welcome to ClassTracker")
    
    st.markdown("""
    ### All-in-One Attendance Tracking Solution
    
    ClassTracker is a comprehensive platform that simplifies attendance management for educational institutions.
    
    #### Key Features:
    - 📋 **Attendance Tracking**: Easy attendance recording for professors
    - 🔔 **Smart Notifications**: Alerts for upcoming classes and attendance warnings
    - 💬 **AI Policy Assistant**: Answers questions about attendance policies
    - 📊 **Attendance Analytics**: Visual reporting of attendance patterns
    
    #### Getting Started:
    Select a role from the sidebar to explore the demo.
    """)
    
    # Feature showcase with columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("For Students")
        st.markdown("""
        - View class schedule
        - Check-in to classes
        - Track attendance status
        - Get reminders for classes
        - Ask questions about policies
        """)
    
    with col2:
        st.subheader("For Professors")
        st.markdown("""
        - Track attendance easily
        - Generate attendance reports
        - Monitor student participation
        - Send notifications
        - Access attendance analytics
        """)
    
    with col3:
        st.subheader("For Administrators")
        st.markdown("""
        - Centralized attendance data
        - Compliance monitoring
        - Custom policy configuration
        - Integration with LMS
        - Institution-wide analytics
        """)

def show_navigation():
    """Show navigation menu and handle page routing"""
    # User info display
    st.markdown(f"<div class='main-header'><h2>Welcome, {st.session_state.user_name}</h2><p>Role: {st.session_state.role.capitalize()}</p></div>", unsafe_allow_html=True)
    
    # Navigation menu
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Attendance", "Schedule", "AI Assistant", "Settings"],
        icons=["house", "check-circle", "calendar3", "chat", "gear"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )
    
    # Display different content based on selection
    if selected == "Dashboard":
        if st.session_state.role == "student":
            show_student_dashboard()
        else:
            show_professor_dashboard()
    
    elif selected == "Attendance":
        if st.session_state.role == "student":
            show_student_attendance()
        else:
            show_professor_attendance()
    
    elif selected == "Schedule":
        show_schedule()
    
    elif selected == "AI Assistant":
        show_ai_assistant()
    
    elif selected == "Settings":
        show_settings()

def show_student_dashboard():
    """Display the student dashboard"""
    st.title("Student Dashboard")
    
    # Create layout
    col1, col2 = st.columns([7, 3])
    
    with col1:
        # Upcoming classes
        st.subheader("Today's Classes")
        
        # Generate dummy class data for today
        now = datetime.now()
        today_classes = []
        
        for course_id in st.session_state.user_details['courses']:
            course = next((c for c in DEMO_COURSES if c['id'] == course_id), None)
            if course:
                start_time = now.replace(hour=9 + course_id*2, minute=0)
                end_time = now.replace(hour=10 + course_id*2, minute=30)
                
                # Only show classes that haven't ended yet
                if end_time > now:
                    today_classes.append({
                        "course_code": course['code'],
                        "title": course['title'],
                        "start_time": start_time,
                        "end_time": end_time,
                        "location": f"Building {course_id}, Room {101 + course_id*10}",
                        "status": "Upcoming" if start_time > now else "In Progress"
                    })
        
        if today_classes:
            for cls in today_classes:
                time_format = "%I:%M %p"  # 12-hour format with AM/PM
                start = cls["start_time"].strftime(time_format)
                end = cls["end_time"].strftime(time_format)
                
                status_color = "#FFA500" if cls["status"] == "In Progress" else "#4CAF50"
                
                st.markdown(f"""
                <div class="attendance-card">
                    <h3>{cls['course_code']}: {cls['title']}</h3>
                    <p><strong>Time:</strong> {start} - {end}</p>
                    <p><strong>Location:</strong> {cls['location']}</p>
                    <p><strong>Status:</strong> <span style="color:{status_color}">{cls['status']}</span></p>
                    
                    <div style="display:flex;justify-content:flex-end">
                        <button style="background-color:#4CAF50;color:white;border:none;padding:10px 15px;border-radius:5px;cursor:pointer;">
                            Check-in
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No more classes scheduled for today.")
        
        # Attendance overview
        st.subheader("Attendance Overview")
        
        # Generate dummy attendance data
        attendance_data = []
        
        for course_id in st.session_state.user_details['courses']:
            course = next((c for c in DEMO_COURSES if c['id'] == course_id), None)
            if course:
                # Random attendance data for demo
                import random
                total_classes = 15
                attended = random.randint(int(total_classes * 0.7), total_classes)
                absences = total_classes - attended
                attendance_rate = (attended / total_classes) * 100
                
                attendance_data.append({
                    "Course": course['code'],
                    "Course Name": course['title'],
                    "Attended": attended,
                    "Absences": absences,
                    "Total Classes": total_classes,
                    "Attendance Rate": attendance_rate,
                    "Max Absences": course['max_absences']
                })
        
        # Create a DataFrame and display
        import pandas as pd
        df = pd.DataFrame(attendance_data)
        
        # Custom styles based on absence warning
        def highlight_absences(row):
            absences = row['Absences']
            max_absences = row['Max Absences']
            
            if absences >= max_absences:
                return ['background-color: #FFCCCB'] * len(row)
            elif absences >= max_absences * 0.75:
                return ['background-color: #FFFFCC'] * len(row)
            return [''] * len(row)
        
        # Apply styling and display
        styled_df = df.style.apply(highlight_absences, axis=1)
        st.dataframe(
            styled_df,
            column_config={
                "Course": st.column_config.TextColumn("Course Code"),
                "Course Name": st.column_config.TextColumn("Course Name"),
                "Attended": st.column_config.NumberColumn("Classes Attended"),
                "Absences": st.column_config.NumberColumn("Absences"),
                "Total Classes": st.column_config.NumberColumn("Total Classes"),
                "Attendance Rate": st.column_config.ProgressColumn(
                    "Attendance Rate", 
                    format="%.1f%%",
                    min_value=0,
                    max_value=100
                ),
                "Max Absences": st.column_config.NumberColumn("Max Allowed")
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Show warning if approaching absence limit
        for idx, row in df.iterrows():
            if row['Absences'] >= row['Max Absences'] * 0.75:
                warn_class = "warning-threshold" if row['Absences'] >= row['Max Absences'] else ""
                st.markdown(f"""
                <div class="notification-item">
                    <p class="{warn_class}">Warning: You have {row['Absences']} absences in {row['Course']} ({row['Course Name']}). 
                    Maximum allowed: {row['Max Absences']}.</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        # Notifications section
        st.subheader("Notifications")
        
        # Generate dummy notifications
        now = datetime.now()
        notifications = [
            {
                "id": 1,
                "title": "Class Reminder",
                "message": f"Your {DEMO_COURSES[0]['code']} class starts in 30 minutes.",
                "time": now - timedelta(minutes=30),
                "read": False
            },
            {
                "id": 2,
                "title": "Attendance Warning",
                "message": f"You have missed 2 classes in {DEMO_COURSES[1]['code']}. Maximum allowed: 4.",
                "time": now - timedelta(days=1),
                "read": True
            },
            {
                "id": 3,
                "title": "Professor Announcement",
                "message": f"Tomorrow's {DEMO_COURSES[2]['code']} class will be held online.",
                "time": now - timedelta(days=2),
                "read": False
            }
        ]
        
        # Display notifications
        for notification in notifications:
            read_status = "" if notification['read'] else "🔵 "
            time_str = notification['time'].strftime("%m/%d %I:%M %p")
            
            with st.container():
                st.markdown(f"""
                <div class="notification-item" style="opacity: {'0.7' if notification['read'] else '1.0'}">
                    <h4>{read_status}{notification['title']}</h4>
                    <p>{notification['message']}</p>
                    <small>{time_str}</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Quick access to AI assistant
        st.subheader("Ask About Attendance Policy")
        policy_question = st.text_input("Type your question here...")
        if st.button("Ask"):
            st.info("This is a demo. In the full version, the AI would answer your question about attendance policies using the university's documents.")

def show_professor_dashboard():
    """Display the professor dashboard"""
    st.title("Professor Dashboard")
    
    # Get courses taught by this professor
    professor_courses = []
    for course_id in st.session_state.user_details['courses']:
        course = next((c for c in DEMO_COURSES if c['id'] == course_id), None)
        if course:
            professor_courses.append(course)
    
    # Create layout
    col1, col2 = st.columns([7, 3])
    
    with col1:
        # Course selection
        if professor_courses:
            selected_course = st.selectbox(
                "Select Course",
                options=[f"{c['code']}: {c['title']}" for c in professor_courses]
            )
            course_id = professor_courses[0]['id']  # Just use the first course for the demo
            
            # Today's class
            st.subheader("Today's Class")
            
            # Generate dummy class data
            now = datetime.now()
            start_time = now.replace(hour=9 + course_id*2, minute=0)
            end_time = now.replace(hour=10 + course_id*2, minute=30)
            
            st.markdown(f"""
            <div class="attendance-card">
                <h3>{professor_courses[0]['code']}: {professor_courses[0]['title']}</h3>
                <p><strong>Time:</strong> {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}</p>
                <p><strong>Location:</strong> Building {course_id}, Room {101 + course_id*10}</p>
                <p><strong>Students Enrolled:</strong> {len([s for s in DEMO_STUDENTS if course_id in s['courses']])}</p>
                
                <div style="display:flex;justify-content:flex-end">
                    <button style="background-color:#4CAF50;color:white;border:none;padding:10px 15px;border-radius:5px;cursor:pointer;margin-right:10px;">
                        Take Attendance
                    </button>
                    <button style="background-color:#2196F3;color:white;border:none;padding:10px 15px;border-radius:5px;cursor:pointer;">
                        View Roster
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Attendance analytics
            st.subheader("Attendance Analytics")
            
            # Generate dummy attendance data for chart
            import pandas as pd
            import plotly.express as px
            
            # Students in this course
            course_students = [s for s in DEMO_STUDENTS if course_id in s['courses']]
            
            # Create dummy data - attendance percentage for last 5 sessions
            class_dates = [(now - timedelta(days=i*7)).strftime('%m/%d') for i in range(5)]
            class_dates.reverse()  # Chronological order
            
            # Attendance data
            attendance_data = []
            
            # Overall attendance per session (dummy data)
            import random
            attendance_rates = [random.uniform(0.7, 1.0) for _ in range(5)]
            
            for i, date in enumerate(class_dates):
                attendance_data.append({
                    "Date": date,
                    "Attendance Rate": attendance_rates[i] * 100
                })
            
            df = pd.DataFrame(attendance_data)
            
            # Create chart
            fig = px.line(
                df, 
                x="Date", 
                y="Attendance Rate",
                markers=True,
                title="Class Attendance Trend"
            )
            fig.update_layout(yaxis_range=[50, 100])
            st.plotly_chart(fig, use_container_width=True)
            
            # Students at risk
            st.subheader("Students at Risk")
            
            # Generate dummy data for students with attendance issues
            at_risk_data = []
            for student in course_students:
                # Random attendance data
                absences = random.randint(0, 5)
                if absences >= professor_courses[0]['max_absences'] * 0.75:
                    at_risk_data.append({
                        "Student ID": student['student_id'],
                        "Name": student['name'],
                        "Absences": absences,
                        "Max Allowed": professor_courses[0]['max_absences'],
                        "Last Attended": (now - timedelta(days=random.randint(1, 14))).strftime('%m/%d/%Y')
                    })
            
            if at_risk_data:
                st.dataframe(
                    at_risk_data,
                    column_config={
                        "Student ID": st.column_config.TextColumn("Student ID"),
                        "Name": st.column_config.TextColumn("Student Name"),
                        "Absences": st.column_config.NumberColumn("Current Absences"),
                        "Max Allowed": st.column_config.NumberColumn("Maximum Allowed"),
                        "Last Attended": st.column_config.TextColumn("Last Attended")
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Action buttons
                col_a, col_b = st.columns(2)
                with col_a:
                    st.button("Send Warning Notifications")
                with col_b:
                    st.button("Contact Students")
            else:
                st.success("No students at risk for this course!")
        else:
            st.info("No courses assigned to this professor in the demo.")
    
    with col2:
        # Quick actions
        st.subheader("Quick Actions")
        st.button("Take Attendance")
        st.button("Generate Attendance Report")
        st.button("Send Class Announcement")
        st.button("Schedule Special Session")
        
        # Upcoming schedule
        st.subheader("Upcoming Schedule")
        
        # Generate dummy schedule for the week
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
        for i, day in enumerate(weekdays):
            has_class = i % 2 == 0  # Classes on alternating days for demo
            
            if has_class and professor_courses:
                course = professor_courses[0]
                st.markdown(f"""
                <div style="padding:10px;margin-bottom:10px;border-left:3px solid #2196F3;">
                    <strong>{day}:</strong> {course['code']} at {9 + i}:00 AM
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="padding:10px;margin-bottom:10px;border-left:3px solid #dddddd;color:#888888;">
                    <strong>{day}:</strong> No classes scheduled
                </div>
                """, unsafe_allow_html=True)

def show_student_attendance():
    """Display student attendance page"""
    st.title("My Attendance")
    
    # Get courses for this student
    student_courses = []
    for course_id in st.session_state.user_details['courses']:
        course = next((c for c in DEMO_COURSES if c['id'] == course_id), None)
        if course:
            student_courses.append(course)
    
    # Course selection
    if student_courses:
        selected_course = st.selectbox(
            "Select Course",
            options=[f"{c['code']}: {c['title']}" for c in student_courses]
        )
        course_idx = [f"{c['code']}: {c['title']}" for c in student_courses].index(selected_course)
        course = student_courses[course_idx]
        
        # Display attendance summary for selected course
        st.subheader(f"Attendance Summary: {course['code']}")
        
        # Generate dummy attendance data
        import random
        
        total_classes = 15
        attended = random.randint(int(total_classes * 0.7), total_classes)
        absences = total_classes - attended
        attendance_rate = (attended / total_classes) * 100
        
        # Create metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Classes Attended", attended)
        col2.metric("Absences", absences)
        col3.metric("Attendance Rate", f"{attendance_rate:.1f}%")
        col4.metric("Max Allowed Absences", course['max_absences'])
        
        # Warning if needed
        if absences >= course['max_absences'] * 0.75:
            if absences >= course['max_absences']:
                st.error(f"⚠️ You have reached the maximum allowed absences ({course['max_absences']}) for this course!")
            else:
                st.warning(f"⚠️ Warning: You have {absences} absences. Maximum allowed is {course['max_absences']}.")
        
        # Attendance history
        st.subheader("Attendance History")
        
        # Generate dummy attendance records
        now = datetime.now()
        attendance_records = []
        
        for i in range(total_classes):
            class_date = now - timedelta(days=i*7)
            
            # Determine status (mostly present, but some absences)
            if i < absences:
                status = "Absent"
            else:
                status = "Present"
            
            attendance_records.append({
                "Date": class_date.strftime('%m/%d/%Y'),
                "Day": class_date.strftime('%A'),
                "Time": f"{9 + (course['id']*2)}:00 AM - {10 + (course['id']*2)}:30 AM",
                "Status": status,
                "Notes": "" if status == "Present" else "Unexcused absence"
            })
        
        # Sort by date (newest first)
        attendance_records.reverse()
        
        # Display as table
        st.dataframe(
            attendance_records,
            column_config={
                "Date": st.column_config.TextColumn("Date"),
                "Day": st.column_config.TextColumn("Day"),
                "Time": st.column_config.TextColumn("Time"),
                "Status": st.column_config.TextColumn("Status"),
                "Notes": st.column_config.TextColumn("Notes"),
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Request absence excuse
        st.subheader("Request Absence Excuse")
        
        absence_date = st.date_input("Absence Date", value=datetime.now())
        reason = st.text_area("Reason for Absence")
        upload_file = st.file_uploader("Upload Supporting Document (optional)", type=["pdf", "jpg", "png"])
        
        if st.button("Submit Request"):
            st.success("This is a demo. In a real app, your absence excuse request would be submitted to your professor.")
    else:
        st.info("No courses available in the demo for this student.")

def show_professor_attendance():
    """Display professor attendance taking page"""
    st.title("Attendance Management")
    
    # Get courses taught by this professor
    professor_courses = []
    for course_id in st.session_state.user_details['courses']:
        course = next((c for c in DEMO_COURSES if c['id'] == course_id), None)
        if course:
            professor_courses.append(course)
    
    # Course selection
    if professor_courses:
        selected_course = st.selectbox(
            "Select Course",
            options=[f"{c['code']}: {c['title']}" for c in professor_courses]
        )
        course_idx = [f"{c['code']}: {c['title']}" for c in professor_courses].index(selected_course)
        course = professor_courses[course_idx]
        
        # Session selection/creation
        st.subheader("Class Session")
        
        session_option = st.radio(
            "Session",
            options=["Today's Session", "Past Session", "Future Session"]
        )
        
        if session_option == "Today's Session":
            session_date = datetime.now()
        elif session_option == "Past Session":
            session_date = st.date_input("Select Date", value=datetime.now() - timedelta(days=7))
        else:
            session_date = st.date_input("Select Date", value=datetime.now() + timedelta(days=7))
        
        # Format the date for display
        formatted_date = session_date.strftime('%A, %B %d, %Y')
        
        # Session details
        st.markdown(f"""
        <div class="attendance-card">
            <h3>Class Session: {formatted_date}</h3>
            <p><strong>Course:</strong> {course['code']}: {course['title']}</p>
            <p><strong>Time:</strong> {9 + course['id']}:00 AM - {10 + course['id']}:30 AM</p>
            <p><strong>Location:</strong> Building {course['id']}, Room {101 + course['id']*10}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get students in this course
        course_students = [s for s in DEMO_STUDENTS if course['id'] in s['courses']]
        
        # Generate QR code for check-in
        import io
        import qrcode
        from PIL import Image
        
        # Create a method tab interface
        attendance_method = st.radio(
            "Attendance Method",
            ["Manual Roll Call", "QR Code Check-in", "Geolocation Check-in"]
        )
        
        if attendance_method == "QR Code Check-in":
            # Generate QR code data
            qr_data = f"classtrack:checkin:{course['id']}:{formatted_date}"
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # Display
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img_byte_arr, caption=f"QR Code for {course['code']} attendance", width=200)
            
            with col2:
                st.markdown("""
                ### QR Code Check-in Instructions
                
                1. Display this QR code to your students
                2. Students can scan with the ClassTracker mobile app
                3. Check-ins are recorded automatically
                4. You can still manually update attendance below
                """)
        
        elif attendance_method == "Geolocation Check-in":
            st.markdown("""
            ### Geolocation Check-in
            
            Students within the specified radius of the class location can check in using the app.
            
            **Current Settings:**
            - Check-in radius: 100 meters
            - Classroom location: Set based on course schedule
            - Time window: 15 minutes before and after class start
            """)
            
            # Map placeholder
            st.image("https://via.placeholder.com/800x400?text=Campus+Map+(Demo)", use_column_width=True)
        
        # Attendance roster
        st.subheader("Attendance Roster")
        
        # Create attendance form
        with st.form("attendance_form"):
            # Generate existing attendance data or defaults
            attendance_data = []
            
            # For demo purposes, generate random attendance
            import random
            
            for student in course_students:
                # Default to present for today, random for other days
                if session_option == "Today's Session":
                    status = "Present"
                else:
                    statuses = ["Present", "Absent", "Late", "Excused"]
                    weights = [0.8, 0.1, 0.05, 0.05]  # 80% chance of present
                    status = random.choices(statuses, weights=weights, k=1)[0]
                
                attendance_data.append({
                    "student_id": student['student_id'],
                    "name": student['name'],
                    "status": status,
                    "notes": ""
                })
            
            # Create columns for layout
            col1, col2, col3, col4 = st.columns([3, 3, 2, 4])
            
            with col1:
                st.markdown("### Student ID")
                for student in attendance_data:
                    st.text(student['student_id'])
            
            with col2:
                st.markdown("### Name")
                for student in attendance_data:
                    st.text(student['name'])
            
            with col3:
                st.markdown("### Status")
                status_options = ["Present", "Absent", "Late", "Excused"]
                student_statuses = {}
                
                for i, student in enumerate(attendance_data):
                    key = f"status_{student['student_id']}"
                    student_statuses[key] = st.selectbox(
                        "",
                        options=status_options,
                        index=status_options.index(student['status']),
                        key=key
                    )
            
            with col4:
                st.markdown("### Notes")
                student_notes = {}
                
                for student in attendance_data:
                    key = f"note_{student['student_id']}"
                    student_notes[key] = st.text_input("", key=key)
            
            # Submit button
            submit = st.form_submit_button("Save Attendance")
            
            if submit:
                st.success("Attendance saved successfully! (Demo - no actual data is saved)")
                
                # In a real app, this would save to the database
                st.balloons()
        
        # Attendance statistics
        st.subheader("Course Attendance Statistics")
        
        # Generate attendance stats by student (dummy data)
        stats_data = []
        
        for student in course_students:
            # Random attendance stats for demo
            total_sessions = 15
            present_count = random.randint(int(total_sessions * 0.6), total_sessions)
            absent_count = total_sessions - present_count
            late_count = random.randint(0, min(3, absent_count))
            absent_count -= late_count
            excused_count = random.randint(0, min(2, absent_count))
            absent_count -= excused_count
            
            # Calculate attendance rate
            attendance_rate = ((present_count + late_count + excused_count) / total_sessions) * 100
            
            stats_data.append({
                "Student ID": student['student_id'],
                "Name": student['name'],
                "Present": present_count,
                "Absent": absent_count,
                "Late": late_count,
                "Excused": excused_count,
                "Attendance Rate": attendance_rate
            })
        
        # Create DataFrame
        import pandas as pd
        stats_df = pd.DataFrame(stats_data)
        
        # Display statistics
        st.dataframe(
            stats_df,
            column_config={
                "Student ID": st.column_config.TextColumn("Student ID"),
                "Name": st.column_config.TextColumn("Student Name"),
                "Present": st.column_config.NumberColumn("Present"),
                "Absent": st.column_config.NumberColumn("Absent"),
                "Late": st.column_config.NumberColumn("Late"),
                "Excused": st.column_config.NumberColumn("Excused"),
                "Attendance Rate": st.column_config.ProgressColumn(
                    "Attendance Rate",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Export options
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "Export to CSV",
                data=stats_df.to_csv(index=False),
                file_name=f"{course['code']}_attendance_stats.csv",
                mime="text/csv"
            )
        with col2:
            st.button("Email Report to Department")
    else:
        st.info("No courses available in the demo for this professor.")

def show_schedule():
    """Display class schedule page"""
    st.title("Class Schedule")
    
    # Get courses for current user
    user_courses = []
    if st.session_state.role == "student":
        for course_id in st.session_state.user_details['courses']:
            course = next((c for c in DEMO_COURSES if c['id'] == course_id), None)
            if course:
                user_courses.append(course)
    else:  # professor
        for course_id in st.session_state.user_details['courses']:
            course = next((c for c in DEMO_COURSES if c['id'] == course_id), None)
            if course:
                user_courses.append(course)
    
    # Tab view for different schedules
    tab1, tab2, tab3 = st.tabs(["Weekly Schedule", "Monthly View", "Academic Calendar"])
    
    with tab1:
        st.subheader("Weekly Schedule")
        
        # Create a weekly schedule table
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        time_slots = ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", 
                       "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
        
        # Generate empty schedule grid
        schedule_data = []
        
        for time_slot in time_slots:
            row_data = {"Time": time_slot}
            for day in weekdays:
                row_data[day] = ""
            schedule_data.append(row_data)
        
        # Fill in courses (for demo purposes)
        for course in user_courses:
            # Assign each course to specific days and times
            days = []
            if course['id'] == 1:  # CS101
                days = ["Monday", "Wednesday", "Friday"]
                time_index = 1  # 9:00 AM
            elif course['id'] == 2:  # MATH201
                days = ["Tuesday", "Thursday"]
                time_index = 3  # 11:00 AM
            elif course['id'] == 3:  # ENG105
                days = ["Monday", "Wednesday"]
                time_index = 6  # 2:00 PM
            
            # Add course to schedule
            for day in days:
                schedule_data[time_index][day] = f"{course['code']}\n{course['title']}"
                
                # Classes are 1.5 hours long (cover next slot too)
                if time_index + 1 < len(time_slots):
                    schedule_data[time_index + 1][day] = f"{course['code']} (cont.)"
        
        # Convert to DataFrame
        import pandas as pd
        schedule_df = pd.DataFrame(schedule_data)
        
        # Apply custom formatting with HTML
        st.markdown("""
        <style>
        .schedule-table td {
            text-align: center;
            padding: 10px;
            border: 1px solid #ddd;
        }
        .schedule-table th {
            text-align: center;
            background-color: #f2f2f2;
            padding: 10px;
            border: 1px solid #ddd;
        }
        .class-cell {
            background-color: #e6f7ff;
            border-radius: 5px;
            padding: 5px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display the schedule
        st.dataframe(
            schedule_df,
            column_config={
                "Time": st.column_config.TextColumn("Time")
            },
            hide_index=True,
            use_container_width=True
        )
    
    with tab2:
        st.subheader("Monthly View")
        
        # Display a simple calendar view
        st.markdown("### May 2025")
        
        # Calendar placeholder
        current_month = [
            ["", "", "", "1", "2", "3", "4"],
            ["5", "6", "7", "8", "9", "10", "11"],
            ["12", "13", "14", "15", "16", "17", "18"],
            ["19", "20", "21", "22", "23", "24", "25"],
            ["26", "27", "28", "29", "30", "31", ""]
        ]
        
        # Convert to DataFrame
        calendar_df = pd.DataFrame(
            current_month,
            columns=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        )
        
        # Display calendar
        st.dataframe(
            calendar_df,
            hide_index=True,
            use_container_width=True
        )
        
        # Display events for the month
        st.subheader("Events This Month")
        
        events = [
            {"date": "May 8", "event": "Midterm Exams Begin"},
            {"date": "May 12", "event": "Midterm Exams End"},
            {"date": "May 15", "event": "Course Registration Opens for Next Semester"},
            {"date": "May 25", "event": "Memorial Day (No Classes)"},
            {"date": "May 30", "event": "Last Day to Drop Classes"}
        ]
        
        for event in events:
            st.markdown(f"**{event['date']}**: {event['event']}")
    
    with tab3:
        st.subheader("Academic Calendar")
        
        # Display key academic dates
        academic_calendar = [
            {"period": "Spring Semester", "start_date": "January 15, 2025", "end_date": "May 30, 2025"},
            {"period": "Spring Break", "start_date": "March 10, 2025", "end_date": "March 14, 2025"},
            {"period": "Final Exams", "start_date": "June 2, 2025", "end_date": "June 13, 2025"},
            {"period": "Summer Session", "start_date": "June 24, 2025", "end_date": "August 15, 2025"},
            {"period": "Fall Semester", "start_date": "September 2, 2025", "end_date": "December 19, 2025"}
        ]
        
        # Convert to DataFrame
        calendar_df = pd.DataFrame(academic_calendar)
        
        # Display calendar
        st.dataframe(
            calendar_df,
            column_config={
                "period": st.column_config.TextColumn("Academic Period"),
                "start_date": st.column_config.TextColumn("Start Date"),
                "end_date": st.column_config.TextColumn("End Date")
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Download option
        st.download_button(
            "Download Academic Calendar",
            data=calendar_df.to_csv(index=False),
            file_name="academic_calendar_2025.csv",
            mime="text/csv"
        )

def show_ai_assistant():
    """Display AI assistant for policy questions"""
    st.title("AI Policy Assistant")
    
    st.markdown("""
    ### University Attendance Policy Assistant
    
    Ask any questions about the university's attendance policies, and our AI will provide answers based on official policy documents.
    """)
    
    # Mock policy document display
    with st.expander("View University Attendance Policy"):
        st.markdown("""
        ## University Attendance Policy (Sample)
        
        ### 1. General Attendance Requirements
        
        Regular attendance is required for all courses. Students are expected to attend all classes for the courses in which they are registered.
        
        ### 2. Absence Limits
        
        **2.1** Each course syllabus will specify the number of allowed absences (typically 3-4 for a semester-long course).
        
        **2.2** Exceeding the allowed number of absences may result in automatic failure of the course.
        
        ### 3. Excused Absences
        
        **3.1** Absences may be excused for the following reasons:
        - Illness (with medical documentation)
        - Religious observances
        - University-sponsored activities
        - Family emergencies
        - Legal obligations
        
        **3.2** Documentation must be provided to the instructor within one week of the absence.
        
        ### 4. Late Arrivals and Early Departures
        
        **4.1** Arriving more than 15 minutes late or leaving more than 15 minutes early may be counted as an absence.
        
        **4.2** Three late arrivals or early departures may be counted as one absence.
        
        ### 5. Make-up Work
        
        **5.1** Students with excused absences are responsible for arranging to make up missed work.
        
        **5.2** Make-up work must be completed within one week of returning to class.
        
        ### 6. Appeals
        
        **6.1** Students may appeal attendance-related decisions to the department chair and then to the dean of the college.
        """)
    
    # Chat interface
    st.subheader("Ask a Question")
    
    # Chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
            <div style="background-color:#e6f7ff;padding:10px;border-radius:5px;margin-bottom:10px;text-align:right;">
                <p style="margin:0;">{message['content']}</p>
                <small>You</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color:#f0f0f0;padding:10px;border-radius:5px;margin-bottom:10px;">
                <p style="margin:0;">{message['content']}</p>
                <small>AI Assistant</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Input for new question
    user_question = st.text_input("Type your question here...")
    
    if st.button("Send") and user_question:
        # Add user message to chat history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_question
        })
        
        # Generate mock AI response
        if "absence" in user_question.lower() and "excuse" in user_question.lower():
            ai_response = """
            According to the university attendance policy, absences may be excused for illness (with medical documentation), religious observances, university-sponsored activities, family emergencies, and legal obligations.
            
            To get an absence excused, you must provide documentation to your instructor within one week of the absence. For medical absences, a doctor's note is required.
            """
        elif "late" in user_question.lower():
            ai_response = """
            According to Section 4.1 of the attendance policy, arriving more than 15 minutes late to class or leaving more than 15 minutes early may be counted as an absence.
            
            Additionally, Section 4.2 states that three late arrivals or early departures may be counted as one absence. This is at the discretion of your instructor and should be detailed in your course syllabus.
            """
        elif "fail" in user_question.lower() or "grade" in user_question.lower():
            ai_response = """
            According to Section 2.2 of the university attendance policy, exceeding the allowed number of absences may result in automatic failure of the course.
            
            The specific number of allowed absences is typically 3-4 for a semester-long course, but this can vary. Check your course syllabus for the exact number allowed in your specific course.
            """
        elif "appeal" in user_question.lower():
            ai_response = """
            If you want to appeal an attendance-related decision, Section 6.1 of the policy states that you may appeal to the department chair first, and then to the dean of the college if needed.
            
            It's recommended to prepare documentation supporting your case before initiating an appeal process.
            """
        elif "make" in user_question.lower() and "up" in user_question.lower():
            ai_response = """
            According to Section 5 of the attendance policy, students with excused absences are responsible for arranging to make up missed work with their instructors.
            
            Make-up work must be completed within one week of returning to class. It's best to contact your instructor as soon as possible to make these arrangements.
            """
        else:
            ai_response = """
            Based on the university's attendance policy, regular attendance is required for all courses. Each course syllabus specifies the number of allowed absences (typically 3-4 for a semester).
            
            For more specific information, please refer to your course syllabus or ask a more specific question about the attendance policy.
            """
        
        # Add AI response to chat history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': ai_response
        })
        
        # Rerun to update the display
        st.experimental_rerun()
    
    # Sample questions
    st.subheader("Sample Questions")
    sample_questions = [
        "What counts as an excused absence?",
        "How many absences am I allowed?",
        "What happens if I'm late to class?",
        "Can I appeal an attendance decision?",
        "What if I miss a test due to illness?"
    ]
    
    cols = st.columns(len(sample_questions))
    for i, col in enumerate(cols):
        if col.button(sample_questions[i]):
            # Add sample question to chat history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': sample_questions[i]
            })
            
            # Generate response based on question index
            responses = [
                "According to Section 3.1 of the policy, absences may be excused for: illness (with medical documentation), religious observances, university-sponsored activities, family emergencies, and legal obligations. You must provide documentation within one week of the absence.",
                
                "The university policy typically allows 3-4 absences for a semester-long course, but the exact number is specified in your course syllabus. Exceeding this limit may result in automatic failure of the course according to Section 2.2.",
                
                "According to Section 4.1, arriving more than 15 minutes late or leaving more than 15 minutes early may be counted as an absence. Section 4.2 states that three late arrivals or early departures may count as one absence.",
                
                "Yes, Section 6.1 of the policy allows you to appeal attendance-related decisions. First appeal to the department chair, and if needed, you can then appeal to the dean of the college.",
                
                "If you miss a test due to an excused absence like illness, Section 5 states you are responsible for arranging to make up missed work. You'll need medical documentation, and the make-up work must be completed within one week of returning to class."
            ]
            
            # Add AI response to chat history
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': responses[i]
            })
            
            # Rerun to update the display
            st.experimental_rerun()

def show_settings():
    """Display settings page"""
    st.title("Settings")
    
    # Create tabs for different settings
    tab1, tab2, tab3 = st.tabs(["Notification Settings", "Display Settings", "Account Settings"])
    
    with tab1:
        st.subheader("Notification Settings")
        
        # Email notifications
        st.checkbox("Email Notifications", value=True)
        st.slider("Email Notification Frequency", min_value=1, max_value=24, value=6, 
                 help="How many hours between email notifications")
        
        # Push notifications
        st.checkbox("Push Notifications", value=True)
        st.multiselect("Push Notification Types", 
                      ["Class Reminders", "Attendance Warnings", "Professor Announcements", "Schedule Changes"],
                      default=["Class Reminders", "Attendance Warnings"])
        
        # Advanced settings
        with st.expander("Advanced Notification Settings"):
            st.number_input("Class Reminder Lead Time (minutes)", min_value=5, max_value=120, value=30,
                          help="How many minutes before class to send a reminder")
            st.checkbox("Notify on Weekends", value=False)
            st.checkbox("Quiet Hours", value=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.time_input("Quiet Hours Start", value=datetime.strptime("22:00", "%H:%M"))
            with col2:
                st.time_input("Quiet Hours End", value=datetime.strptime("07:00", "%H:%M"))
        
        st.button("Save Notification Settings")
    
    with tab2:
        st.subheader("Display Settings")
        
        # Theme setting
        theme = st.selectbox("Theme", ["Light", "Dark", "System Default"])
        
        # Layout
        layout = st.selectbox("Default View", ["Calendar View", "List View"])
        
        # Other settings
        st.checkbox("Compact Mode", value=False)
        st.checkbox("High Contrast Mode", value=False)
        st.slider("Font Size", min_value=1, max_value=5, value=3)
        
        # Preview
        st.subheader("Preview")
        st.info("Theme preview would be displayed here in the full version.")
        
        st.button("Save Display Settings")
    
    with tab3:
        st.subheader("Account Settings")
        
        # Personal info
        st.text_input("Name", value=st.session_state.user_name)
        st.text_input("Email", value=f"{st.session_state.user_name.lower().replace(' ', '.')}@university.edu")
        
        # Change password
        with st.expander("Change Password"):
            st.text_input("Current Password", type="password")
            st.text_input("New Password", type="password")
            st.text_input("Confirm New Password", type="password")
            st.button("Update Password")
        
        # Integrations
        with st.expander("Calendar Integration"):
            st.checkbox("Sync with Google Calendar", value=True)
            st.checkbox("Sync with Outlook Calendar", value=False)
            st.checkbox("Sync with Apple Calendar", value=False)
            st.button("Configure Calendar Integration")
        
        # Data export
        with st.expander("Export Data"):
            st.radio("Export Format", ["CSV", "Excel", "JSON"])
            col1, col2 = st.columns(2)
            with col1:
                st.button("Export Attendance Data")
            with col2:
                st.button("Export All Data")
        
        # Delete account
        with st.expander("Delete Account"):
            st.warning("Deleting your account will remove all your data from the system. This action cannot be undone.")
            st.text_input("Type 'DELETE' to confirm", key="delete_confirmation")
            st.button("Delete Account")

if __name__ == "__main__":
    main()