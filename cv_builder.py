import json

CV_JSON_FILE = "cv.json"
CV_TEX_FILE = "cv.tex"


def load_data(filepath: str = CV_JSON_FILE) -> dict:
    with open(filepath, "r") as f:
        cv_data = json.load(f)
    return cv_data


def begin_document(document: list[str]) -> None:
    document.append("\\begin{document}")


def end_document(document: list[str]) -> None:
    document.append("\\end{document}")


def create_section(title: str) -> list[str]:
    section: list[str] = []
    section.append(f"\\section*{{{title}}}")
    return section


def create_subsection(title: str) -> list[str]:
    section: list[str] = []
    section.append(f"\\subsection*{{{title}}}")
    return section


def create_subsubsection(title: str) -> list[str]:
    section: list[str] = []
    section.append(f"\\subsubsection*{{{title}}}")
    return section


def generate_tex_file(
    preamble: list[str],
    document: list[str],
    filepath: str = CV_TEX_FILE,
) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        for line in preamble:
            f.write(f"{line}\n")
        for line in document:
            f.write(f"{line}\n")


if __name__ == "__main__":
    cv_data = load_data()

    preamble: list[str] = []
    document: list[str] = []

    preamble.append("\\documentclass{article}")
    preamble.append("\\usepackage{geometry}")
    preamble.append("\\geometry{a4paper, left=25mm, top=20mm}")
    preamble.append("\\pagestyle{empty}")
    preamble.append("\\setlength\\parindent{0pt}")
    preamble.append("\\usepackage{enumitem}")

    begin_document(document)

    profile_data = cv_data["profile"]
    profile = create_section(profile_data["full_name"])
    profile.append(
        " $|$ ".join(
            [
                profile_data["location"],
                profile_data["phone"],
                profile_data["email"],
            ]
        )
    )
    document.extend(profile)

    summary = create_subsection("Summary")
    summary.append(cv_data["summary"])
    document.extend(summary)

    experience = create_subsection("Experience")
    for job_data in cv_data["experience"]:
        job = create_subsubsection(job_data["job_title"])
        job.append(f"{job_data['company']}, {job_data['location']}\\newline")
        job.append(f"{job_data['from_month']} - {job_data['to_month']}\\par")
        job.append("\\vspace*{1em}")
        job.append(job_data["description"])
        experience.extend(job)
    document.extend(experience)

    education = create_subsection("Education")
    for edu_data in cv_data["education"]:
        course = create_subsubsection(edu_data["course_title"])
        course.append(f"{edu_data['school']}, {edu_data['to_year']}")
        education.extend(course)
    document.extend(education)

    skills = create_subsection("Skills")
    skills.append("\\begin{itemize}[nosep]")
    for skill in cv_data["skills"]:
        skills.append(f"\\item {skill['description']} ({skill['competency']})")
    skills.append("\\end{itemize}")
    document.extend(skills)

    references = create_subsection("References")
    references.append("Available on request")
    document.extend(references)

    end_document(document)

    generate_tex_file(preamble, document)
