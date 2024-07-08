class Document:
    def __init__(
        self,
        documentclass: str = "article",
    ) -> None:
        self.preamble: list[str] = []
        self._content: list[str] = []

        self.preamble.append(f"\\documentclass{{{documentclass}}}")

    def append(self, line: str) -> None:
        self._content.append(line)

    def extend(self, lines: list[str]) -> None:
        self._content.extend(lines)

    def begin(self) -> None:
        self.append("\\begin{document}")

    def end(self) -> None:
        self.append("\\end{document}")

    @staticmethod
    def create_section(title: str) -> list[str]:
        section: list[str] = []
        section.append(f"\\section*{{{title}}}")
        return section

    @staticmethod
    def create_subsection(title: str) -> list[str]:
        section: list[str] = []
        section.append(f"\\subsection*{{{title}}}")
        return section

    @staticmethod
    def create_subsubsection(title: str) -> list[str]:
        section: list[str] = []
        section.append(f"\\subsubsection*{{{title}}}")
        return section

    def generate_tex(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            for line in self.preamble:
                f.write(f"{line}\n")
            for line in self._content:
                f.write(f"{line}\n")
