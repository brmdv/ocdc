import datetime as dt
from textwrap import TextWrapper, indent

from . import ast

MAX_WIDTH = 90
INDENT = "  "

wrapper = TextWrapper(MAX_WIDTH, drop_whitespace=False)
item_wrapper = TextWrapper(MAX_WIDTH, initial_indent="- ", subsequent_indent=INDENT)


def wrap(text: str) -> str:
    return "\n".join(wrapper.fill(line) for line in text.splitlines())


def wrap_item(item: ast.ListItem) -> str:
    return indent(item_wrapper.fill(item.text), item.level * INDENT)


def render_markdown(c: ast.Changelog) -> str:
    text = ""

    if c.title:
        text += f"# {c.title}\n\n"

    if c.intro:
        text += wrap(c.intro) + "\n"

    for v in c.versions:
        text += f"\n\n## {v.number}"
        if v.date:
            text += f" - {v.date}"
        text += "\n"

        for type_, changes in v.changes.items():
            text += f"\n### {type_}\n\n"
            for item in changes.items:
                text += wrap_item(item) + "\n"
            if changes.footer:
                text += f"\n{changes.footer}\n"

    return text


def render_new_template() -> str:
    v = ast.Version(
        number="0.1.0",
        date=dt.date.today().isoformat(),
        changes={
            ast.ChangeType.Added.value: ast.Changes(
                items=[ast.ListItem(text="Initial version.")]
            )
        },
    )
    c = ast.Changelog(title="Changelog", intro=INTRO, versions=[v])
    return render_markdown(c)


INTRO = """
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
""".strip()
