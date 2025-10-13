# Import necessary packages
from flask import Flask, render_template, request
import os
from openai import OpenAI
from dotenv import load_dotenv
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with API key from .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/jd")
def jd():
    return render_template("jd.html")

@app.route("/jdresume")
def jdresume():
    return render_template("jdresume.html")

@app.route("/iqs")
def iqs():
    return render_template("iqs.html")

@app.route("/email")
def email():
    return render_template("email.html")

@app.route("/jd", methods=["POST"])
def jdform():
    try:
        jobposition = request.form.get("jobposition", "").strip()
        tone = request.form.get("tone", "").strip()
        skills = request.form.get("skills", "").strip()
        qualifications = request.form.get("qualifications", "").strip()

        if jobposition and tone and skills and qualifications:
            model = "gpt-4o-mini"
            prompt = (f"Can you please provide me with the job description for a {jobposition} "
                     f"role in a {tone} tone? The ideal candidate should have experience with "
                     f"{skills}, {qualifications}. Additionally, I'd like to know more about the "
                     f"company culture and any opportunities for growth within the organization. "
                     f"The output should be in a formatted way on a webpage that use HTML tags "
                     f"to structure the content. Thank you!")

            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000
            )
            answer = completion.choices[0].message.content
            return render_template("jd.html", result=answer)
        else:
            response = "All fields are mandatory. Please try again."
            return render_template("jd.html", result=response)
    except Exception as e:
        response = f"Something went wrong. Please try again.<br><br>Error is: {str(e)}"
        return render_template("jd.html", result=response)


@app.route("/iqs", methods=["POST"])
def iqsform():
    try:
        jobposition = request.form.get("jobposition", "").strip()
        tone = request.form.get("tone", "").strip()
        skills = request.form.get("skills", "").strip()
        experience = request.form.get("experience", "").strip()

        if jobposition and tone and skills and experience:
            model = "gpt-4o-mini"
            prompt = (f"Can you generate the top 10 to 15 interview questions that a hiring manager "
                     f"might ask a candidate for {jobposition} with {experience} years of experience? "
                     f"The questions should be tailored to the required skills such as {skills} for "
                     f"the job and should be asked in a {tone} that is appropriate for the company culture. "
                     f"The output should be in a formatted way on a webpage that use HTML tags to "
                     f"structure the content. Thank you!")

            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000
            )
            answer = completion.choices[0].message.content
            return render_template("iqs.html", result=answer)
        else:
            response = "All fields are mandatory. Please try again."
            return render_template("iqs.html", result=response)
    except Exception as e:
        response = f"Something went wrong. Please try again.<br><br>Error is: {str(e)}"
        return render_template("iqs.html", result=response)


@app.route("/email", methods=["POST"])
def emailform():
    try:
        emailtype = request.form.get("emailtype", "").strip()
        tone = request.form.get("tone", "").strip()
        opcom = request.form.get("opcom", "").strip()

        if emailtype and tone:
            model = "gpt-4o-mini"
            prompt = (f"Hello ChatGPT, I am looking to generate a customized email template for "
                     f"various job-related purposes. Can you please help me by providing an email "
                     f"template based on the following inputs: Email type as {emailtype} and Tone "
                     f"as {tone} and additional information such as {opcom} and other relevant "
                     f"information. The output should be in a formatted way on a webpage that use "
                     f"HTML tags to structure the content. Thank you!")

            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000
            )
            answer = completion.choices[0].message.content
            return render_template("email.html", result=answer)
        else:
            response = "Mandatory fields missing. Please try again."
            return render_template("email.html", result=response)
    except Exception as e:
        response = f"Something went wrong. Please try again.<br><br>Error is: {str(e)}"
        return render_template("email.html", result=response)


@app.route("/jdresume", methods=["POST"])
def jdresumeform():
    try:
        if request.method == 'POST':
            jdtext = request.form.get("jd", "").strip()
            resumetext = request.form.get("resume", "").strip()

            if jdtext and resumetext:
                # Download NLTK data (only downloads if not already present)
                nltk.download('stopwords', quiet=True)
                nltk.download('punkt', quiet=True)

                stop_words = set(stopwords.words('english'))

                # Tokenize and clean the text data
                jd_tokens = nltk.word_tokenize(jdtext)
                jd_tokens = [word.lower() for word in jd_tokens
                            if word.isalpha() and word.lower() not in stop_words]
                resume_tokens = nltk.word_tokenize(resumetext)
                resume_tokens = [word.lower() for word in resume_tokens
                                if word.isalpha() and word.lower() not in stop_words]

                # Use TF-IDF to extract important keywords and phrases
                tfidf = TfidfVectorizer(tokenizer=lambda x: x, preprocessor=lambda x: x)
                jd_tfidf = tfidf.fit_transform([jd_tokens])
                resume_tfidf = tfidf.transform([resume_tokens])

                # Calculate similarity score
                similarity_score = cosine_similarity(jd_tfidf, resume_tfidf)[0][0]

                model = "gpt-4o-mini"

                # Shorten the Job Description
                jdprompt = f"Please shorten the Job Description to less than 500 words. Here is the JD: {jdtext}"
                jdcompletion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": jdprompt}],
                    max_tokens=500
                )
                jdshort = jdcompletion.choices[0].message.content

                # Shorten the Resume
                resumeprompt = f"Please shorten the Resume to less than 500 words. Here is the Resume: {resumetext}"
                resumecompletion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": resumeprompt}],
                    max_tokens=500
                )
                resumeshort = resumecompletion.choices[0].message.content

                # JD and Resume Comparison
                prompt = (f"Hi ChatGPT, Here is Job Description: {jdshort} and Job Seeker Resume: {resumeshort}. "
                         f"Check for similarities and differences between the JD and Resume and briefly explain "
                         f"if there is a good match between these to the hiring manager in their own language. "
                         f"Please ensure the completion length is limited to 3000 tokens. The output should be "
                         f"in a formatted way on a webpage that use HTML tags to structure the content. Thank you!")
                completion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000
                )
                answer = completion.choices[0].message.content

                match_percentage = f"{similarity_score * 100:.2f}"
                return render_template("jdresume.html",
                                      result=f"Match Index: <b>{match_percentage} %</b>",
                                      jdresumebrief=answer)
            else:
                response = "Mandatory fields missing. Please try again."
                return render_template("jdresume.html", result=response)
    except Exception as e:
        response = f"Something went wrong. Please try again.<br><br>Error is: <br/>{str(e)}"
        return render_template("jdresume.html", result=response)


if __name__ == '__main__':
    app.run(debug=True, port=8080)