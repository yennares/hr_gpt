# HRGPT - AI-Powered HR Assistant

A Flask-based web application that leverages OpenAI's GPT-4o-mini model to assist with various HR-related tasks.

## Features

- **Job Description Generator**: Create professional job descriptions based on role, tone, skills, and qualifications
- **Interview Questions Generator**: Generate tailored interview questions based on job position and required skills
- **Email Template Generator**: Create customized email templates for various job-related purposes
- **Resume-JD Matcher**: Compare resumes against job descriptions and calculate match percentage using TF-IDF and cosine similarity

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd hrgpt
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up your OpenAI API key using `.env` file:
   - Copy `.env.example` to `.env`:
     - Windows:
       ```bash
       copy .env.example .env
       ```
     - macOS/Linux:
       ```bash
       cp .env.example .env
       ```
   - Open `.env` file and add your actual OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-actual-api-key-here
     ```
   - **Important**: Never commit your `.env` file to Git! It's already included in `.gitignore`

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:8080
```

3. Use the web interface to:
   - Generate job descriptions
   - Create interview questions
   - Generate email templates
   - Match resumes with job descriptions

## Dependencies

- **Flask**: Web framework for the application
- **OpenAI**: Official OpenAI API client (v1.0.0+)
- **python-dotenv**: Load environment variables from `.env` file
- **NLTK**: Natural language processing toolkit
- **scikit-learn**: Machine learning utilities (TF-IDF and cosine similarity)
- **NumPy, Pandas, SciPy**: Data processing libraries

## Project Structure

```
hrgpt/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables file
├── .env                  # Your actual environment variables (not committed to Git)
├── .gitignore            # Git ignore file
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html
│   ├── jd.html
│   ├── iqs.html
│   ├── email.html
│   └── jdresume.html
└── venv/                 # Virtual environment (not committed to Git)
```

## Security Notes

- ⚠️ **Never commit your `.env` file or expose your API key**
- The `.env` file is automatically gitignored
- Always use `.env` file for sensitive configuration
- Keep your OpenAI API key secure and rotate it if exposed

## Contributing

This is a personal project for learning and demonstration purposes. Feel free to fork and modify for your own use.

## License

This project is for educational and personal use.
