"""
Generate distinct_skill_labels.md and distinct_skill_labels.csv for GitHub.
Uses same data and normalization (strip + lower) as table1_metrics.py.
"""
import json
import os
import csv
import sys

MD_PATH = "distinct_skill_labels.md"
CSV_PATH = "distinct_skill_labels.csv"


def _repo_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


DEFAULT_INPUT = os.path.join(_repo_root(), "data", "course_skills_extracted.json")


def load_course_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(s):
    return (s or "").strip().lower()


def get_distinct_labels_by_program(courses):
    """Return dict: program_name -> sorted list of distinct normalized labels."""
    by_program = {}
    for rec in courses:
        program = (rec.get("program") or "").strip()
        if not program:
            continue
        if program not in by_program:
            by_program[program] = set()
        skills = rec.get("skills") or {}
        for lst in (skills.get("tools") or [], skills.get("hard_skills") or [], skills.get("soft_skills") or []):
            for x in lst:
                label = normalize(x)
                if label:
                    by_program[program].add(label)
    return {p: sorted(by_program[p]) for p in by_program}


def write_md(program_labels, program_order, out_path):
    lines = [
        "# Distinct Extracted Skill Labels by Program",
        "",
        "- These labels were extracted from official course descriptions.",
        "- Within each program, labels were normalized by lowercasing and stripping whitespace.",
        "- The lists are provided to support transparency and checking of the paper results.",
        "",
    ]
    if not program_order:
        program_order = ["Program 1", "Program 2"]
        program_labels = {p: [] for p in program_order}
    for i, program in enumerate(program_order, start=1):
        labels = program_labels.get(program, [])
        section = f"Program {i}" if len(program_order) > 1 else program
        lines.append(f"## {section}")
        lines.append("")
        lines.append(f"**Total distinct skill labels:** {len(labels)}")
        lines.append("")
        if labels:
            for label in labels:
                lines.append(f"- {label}")
        else:
            lines.append("- *(none)*")
        lines.append("")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_csv(program_labels, program_order, out_path):
    rows = []
    for i, program in enumerate(program_order, start=1):
        section = f"Program {i}" if len(program_order) > 1 else program
        for label in program_labels.get(program, []):
            rows.append({"Program": section, "Program name": program, "Label": label})
    if not rows:
        for section in ["Program 1", "Program 2"]:
            rows.append({"Program": section, "Program name": "", "Label": ""})
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["Program", "Program name", "Label"])
        w.writeheader()
        w.writerows(rows)


def main():
    repo_root = _repo_root()
    input_path = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("DISTINCT_INPUT", DEFAULT_INPUT)
    if not os.path.isabs(input_path):
        try_path = os.path.join(repo_root, input_path)
        if os.path.isfile(try_path):
            input_path = try_path
    if not os.path.isfile(input_path):
        print(f"Input not found: {input_path}. Writing empty structure to {MD_PATH} and {CSV_PATH}.")
        program_labels = {}
        program_order = []
    else:
        courses = load_course_data(input_path)
        program_labels = get_distinct_labels_by_program(courses)
        program_order = sorted(program_labels.keys())
    out_dir = repo_root
    write_md(program_labels, program_order, os.path.join(out_dir, MD_PATH))
    write_csv(program_labels, program_order, os.path.join(out_dir, CSV_PATH))
    print(f"Wrote {MD_PATH} and {CSV_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
