def _options_dict_to_str(options_dict: dict) -> str:
    return ", ".join(f"{key}={value}" for key, value in options_dict.items())


class Preamble:
    def __init__(self) -> None:
        self._content: list[str] = []

    def append(self, line: str) -> None:
        self._content.append(line)

    def extend(self, lines: list[str]) -> None:
        self._content.extend(lines)

    def usepackage(self, name: str, options: dict | None = None) -> None:
        self.append(f"\\usepackage{{{name}}}")
        if options:
            options_str = _options_dict_to_str(options)
            self.append(f"\\{name}{{{options_str}}}")

    def dumps(self) -> str:
        return "\n".join(self._content)


class Document:
    def __init__(
        self,
        *,
        documentclass: str = "article",
        pagestyle: str | None = None,
        indent: bool = True,
        geometry_options: dict | None = None,
    ) -> None:
        self.preamble = Preamble()
        self._content: list[str] = []

        self.preamble.append(f"\\documentclass{{{documentclass}}}")

        if pagestyle:
            self.preamble.append(f"\\pagestyle{{{pagestyle}}}")

        if not indent:
            self.preamble.usepackage("parskip")

        if geometry_options:
            self.preamble.usepackage("geometry", geometry_options)

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

    def dumps(self) -> str:
        preamble_dumps = self.preamble.dumps()
        document_dumps = "\n".join(self._content)
        return preamble_dumps + "\n\n" + document_dumps

    def generate_tex(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.dumps())
