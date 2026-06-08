# Placeholder for future resume parsing logic
import pdfplumber


def extract_text_from_pdf(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_skills(resume_text, skills_list):

    found_skills = []

    resume_text = resume_text.lower()

    for skill in skills_list:

        if skill.lower() in resume_text:
            found_skills.append(skill)

    return found_skills