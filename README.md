# ClassTracker

A Streamlit application for tracking class attendance with notifications and AI assistance.

## Features

- **Attendance Tracking**: Easy attendance recording for professors
- **Smart Notifications**: Alerts for upcoming classes and attendance warnings
- **AI Policy Assistant**: Answers questions about attendance policies using university documents
- **Attendance Analytics**: Visual reporting of attendance patterns

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Miguelramirez004/ClassTracker.git
   cd ClassTracker
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   
   # For Windows
   venv\Scripts\activate
   
   # For macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

### Running the App

Run the application locally:

```
streamlit run app.py
```

The application will be available at http://localhost:8501

## Deployment on Streamlit Cloud

1. Push your repository to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Set up required secrets (API keys, etc.)
5. Deploy the application

## Project Structure

```
ClassTracker/
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
├── config.py
├── data/
├── components/
│   ├── authentication.py
│   ├── attendance.py
│   ├── notifications.py
│   └── chatbot.py
├── utils/
│   ├── email_sender.py
│   ├── pdf_processor.py
│   └── time_utils.py
├── pages/
│   ├── home.py
│   ├── professor_dashboard.py
│   ├── student_dashboard.py
│   ├── attendance_manager.py
│   └── settings.py
├── static/
│   ├── css/
│   └── images/
└── docs/
    └── university_policies/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.