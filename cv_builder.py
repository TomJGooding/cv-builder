import json

from latex import Document

CV_JSON_FILE = "cv.json"
CV_TEX_FILE = "cv.tex"


def load_data(filepath: str = CV_JSON_FILE) -> dict:
    with open(filepath, "r") as f:
        cv_data = json.load(f)
    return cv_data


if __name__ == "__main__":
    cv_data = load_data()
    cv_document = Document()

    cv_document.preamble.append("\\usepackage{geometry}")
    cv_document.preamble.append("\\geometry{a4paper, left=25mm, top=20mm}")
    cv_document.preamble.append("\\pagestyle{empty}")
    cv_document.preamble.append("\\setlength\\parindent{0pt}")
    cv_document.preamble.append("\\usepackage{enumitem}")

    cv_document.begin()

    profile_data = cv_data["profile"]
    profile = cv_document.create_section(profile_data["full_name"])
    profile.append(
        " $|$ ".join(
            [
                profile_data["location"],
                profile_data["phone"],
                profile_data["email"],
            ]
        )
    )
    cv_document.extend(profile)

    summary = cv_document.create_subsection("Summary")
    summary.append(cv_data["summary"])
    cv_document.extend(summary)

    experience = cv_document.create_subsection("Experience")
    for job_data in cv_data["experience"]:
        job = cv_document.create_subsubsection(job_data["job_title"])
        job.append(f"{job_data['company']}, {job_data['location']}\\newline")
        job.append(f"{job_data['from_month']} - {job_data['to_month']}\\par")
        job.append("\\vspace*{1em}")
        job.append(job_data["description"])
        experience.extend(job)
    cv_document.extend(experience)

    education = cv_document.create_subsection("Education")
    for edu_data in cv_data["education"]:
        course = cv_document.create_subsubsection(edu_data["course_title"])
        course.append(f"{edu_data['school']}, {edu_data['to_year']}")
        education.extend(course)
    cv_document.extend(education)

    skills = cv_document.create_subsection("Skills")
    skills.append("\\begin{itemize}[nosep]")
    for skill in cv_data["skills"]:
        skills.append(f"\\item {skill['description']} ({skill['competency']})")
    skills.append("\\end{itemize}")
    cv_document.extend(skills)

    references = cv_document.create_subsection("References")
    references.append("Available on request")
    cv_document.extend(references)

    cv_document.end()

    cv_document.generate_tex(filepath=CV_TEX_FILE)
