from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.parser import extract_text_from_pdf, extract_skills

app = Flask(__name__)

SKILLS = [
    "python",
    "aws",
    "azure",
    "docker",
    "jenkins",
    "git",
    "github",
    "linux",
    "sql",
    "mysql",
    "sqlite",
    "html",
    "css",
    "javascript",
    "node.js",
    "pandas",
    "numpy",
    "matplotlib",
    "scikit-learn",
    "machine learning",
    "llm",
    "rag",
    "render",
    "netlify",
    "vercel"
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['resume']
    job_description = request.form['job_description']

    resume_text = extract_text_from_pdf(file)

    found_skills = extract_skills(
        resume_text,
        SKILLS
    )

    job_description_lower = job_description.lower()

    required_skills = []

    for skill in SKILLS:
        if skill.lower() in job_description_lower:
            required_skills.append(skill)

    missing_skills = []

    for skill in required_skills:
        if skill not in found_skills:
            missing_skills.append(skill)

    documents = [
        resume_text,
        job_description
    ]

    cv = CountVectorizer()

    matrix = cv.fit_transform(documents)

    similarity = cosine_similarity(matrix)

    match_percentage = round(
        similarity[0][1] * 100,
        2
    )

    suggestions = []

    if match_percentage < 50:
        suggestions.append(
            "Resume needs significant improvement for this role."
        )

    if len(missing_skills) > 0:
        suggestions.append(
            "Add missing skills relevant to the job description."
        )

    if "project" not in resume_text.lower():
        suggestions.append(
            "Add project experience section."
        )

    if "certification" not in resume_text.lower():
        suggestions.append(
            "Add certifications to strengthen profile."
        )

    return render_template(
        'result.html',
        score=match_percentage,
        skills=found_skills,
        missing_skills=missing_skills,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)