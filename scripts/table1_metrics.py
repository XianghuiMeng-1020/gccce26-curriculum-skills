"""
Table 1 metrics: program-level statistics for the paper.
Computes: Courses, Total extracted items, Mean items per course,
Unique labels, Singleton share, Courses naming tools.

Data source: course_skills_extracted.json (same as step2_analy*.py).

----------------------------------------------------------------------
AUDIT TABLE (formula, count basis, unit)
----------------------------------------------------------------------
| Metric                    | Formula                          | Count basis      | Unit    |
|---------------------------|----------------------------------|------------------|---------|
| Courses                    | count(course records per program) | 1 per course     | courses |
| Total extracted items      | sum(tools + hard_skills + soft_skills) | occurrence       | items   |
| Mean items per course      | Total extracted items / Courses  | occurrences/course | items/course |
| Unique labels              | len(unique labels in program)    | unique label     | labels  |
| Singleton share (%)        | (labels with freq=1) / unique labels * 100 | unique labels  | %       |
| Courses naming tools (%)   | (courses with ≥1 tool) / Courses * 100 | course (binary) | %       |

- Unique labels: pooled Tools + Hard Skills + Soft Skills; dedup within program.
  By default: strip + lower before counting (set NORMALIZE_FOR_UNIQUE_LABELS).
- Singleton: unique labels that appear exactly once in the program (occurrence count = 1).
- Total extracted items: occurrence-based (same label in two courses counts twice).
----------------------------------------------------------------------
MANUSCRIPT-READY DEFINITIONS (one sentence each)
----------------------------------------------------------------------
1. Courses: Number of course descriptions (one per course) assigned to that program.
2. Total extracted items: Sum of all skill-item occurrences (tools, hard skills, soft skills)
   extracted from course descriptions for that program.
3. Mean items per course: Total extracted items for the program divided by its course count.
4. Unique labels: Number of distinct skill labels in the program after stripping whitespace
   and lowercasing, with tools, hard skills, and soft skills pooled and deduplicated within program.
5. Singleton share: Proportion (as %) of unique labels that appear exactly once in the program.
6. Courses naming tools: Proportion (as %) of courses in the program with at least one extracted tool.
"""
import json
import os
from collections import defaultdict

# ---------------------------------------------------------------------------
# Configuration (for paper audit: what is counted and how)
# ---------------------------------------------------------------------------
NORMALIZE_FOR_UNIQUE_LABELS = True   # True = strip + lower before counting unique (recommended for paper)
COUNT_CASE_SENSITIVE = False         # If False, unique/singleton use normalized labels

def _repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_INPUT = os.path.join(_repo_root(), "data", "course_skills_extracted.json")
DEFAULT_OUTPUT_CSV = os.path.join(_repo_root(), "table1_metrics.csv")

# ---------------------------------------------------------------------------
# Load data (same structure as step2: list of {code, title, desc, program, skills})
# ---------------------------------------------------------------------------
def load_course_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        raise ValueError(f"No records in {filepath}")
    return data


def normalize_label(s, do_normalize=True):
    """For unique-label and singleton counts: strip; optionally lower."""
    t = (s or "").strip()
    if do_normalize:
        t = t.lower()
    return t


# ---------------------------------------------------------------------------
# Per-program aggregates (one pass over courses)
# ---------------------------------------------------------------------------
def compute_program_metrics(courses, normalize_unique=NORMALIZE_FOR_UNIQUE_LABELS):
    """
    Returns dict: program -> {
        'courses', 'total_items', 'mean_items_per_course',
        'unique_labels', 'singleton_count', 'singleton_share',
        'courses_naming_tools', 'courses_naming_tools_share'
    }
    """
    by_program = defaultdict(lambda: {
        "course_count": 0,
        "total_items": 0,
        "courses_with_tools": 0,
        "label_counts": defaultdict(int),  # normalized or raw label -> count (over the program)
    })

    for rec in courses:
        program = (rec.get("program") or "").strip()
        if not program:
            continue
        skills = rec.get("skills") or {}
        tools = skills.get("tools") or []
        hard = skills.get("hard_skills") or []
        soft = skills.get("soft_skills") or []

        # Normalize for extraction counts: we count occurrences; strip is applied when storing label
        def add_items(lst, key_prefix=""):
            for x in lst:
                label = (x or "").strip()
                if not label:
                    continue
                by_program[program]["total_items"] += 1
                norm = normalize_label(label, normalize_unique)
                if norm:
                    by_program[program]["label_counts"][norm] += 1

        add_items(tools)
        add_items(hard)
        add_items(soft)

        by_program[program]["course_count"] += 1
        if len(tools) > 0:
            by_program[program]["courses_with_tools"] += 1

    # Build final metrics
    result = {}
    for program, agg in by_program.items():
        n_courses = agg["course_count"]
        total_items = agg["total_items"]
        unique_labels = len(agg["label_counts"])
        singleton_count = sum(1 for c in agg["label_counts"].values() if c == 1)
        mean_items = total_items / n_courses if n_courses else 0
        singleton_share = (singleton_count / unique_labels * 100.0) if unique_labels else 0.0
        courses_naming_tools_pct = (agg["courses_with_tools"] / n_courses * 100.0) if n_courses else 0.0

        result[program] = {
            "courses": n_courses,
            "total_extracted_items": total_items,
            "mean_items_per_course": round(mean_items, 2),
            "unique_labels": unique_labels,
            "singleton_count": singleton_count,
            "singleton_share_pct": round(singleton_share, 1),
            "courses_naming_tools": agg["courses_with_tools"],
            "courses_naming_tools_share_pct": round(courses_naming_tools_pct, 1),
        }
    return result


# ---------------------------------------------------------------------------
# Table 1 output: CSV + print
# ---------------------------------------------------------------------------
def table1_to_rows(metrics_by_program):
    """Rows for Table 1 (program as row)."""
    rows = []
    for program, m in sorted(metrics_by_program.items()):
        rows.append({
            "Program": program,
            "Courses": m["courses"],
            "Total extracted items": m["total_extracted_items"],
            "Mean items per course": m["mean_items_per_course"],
            "Unique labels": m["unique_labels"],
            "Singleton share (%)": m["singleton_share_pct"],
            "Courses naming tools": m["courses_naming_tools"],
            "Courses naming tools (%)": m["courses_naming_tools_share_pct"],
        })
    return rows


def print_audit(metrics_by_program):
    """Print formulas and exact counts for paper audit."""
    print("\n--- Table 1 audit (exact counts) ---")
    for program, m in sorted(metrics_by_program.items()):
        print(f"\n{program}:")
        print(f"  Courses = {m['courses']}")
        print(f"  Total extracted items = {m['total_extracted_items']}")
        print(f"  Mean items per course = {m['total_extracted_items']} / {m['courses']} = {m['mean_items_per_course']}")
        print(f"  Unique labels = {m['unique_labels']} (pooled Tools+Hard+Soft, normalized: strip+lower)")
        print(f"  Singleton share = {m['singleton_count']} / {m['unique_labels']} = {m['singleton_share_pct']}%")
        print(f"  Courses naming tools = {m['courses_naming_tools']} / {m['courses']} = {m['courses_naming_tools_share_pct']}%")


def save_csv(rows, filepath):
    import csv
    if not rows:
        return
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def main():
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TABLE1_INPUT", DEFAULT_INPUT)
    output_path = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("TABLE1_OUTPUT", DEFAULT_OUTPUT_CSV)
    if not os.path.isabs(input_path):
        input_path = os.path.join(_repo_root(), input_path)

    if not os.path.isfile(input_path):
        print(f"Input not found: {input_path}")
        print("Usage: python table1_metrics.py [course_skills_extracted.json]")
        return 1

    courses = load_course_data(input_path)
    metrics = compute_program_metrics(courses, normalize_unique=NORMALIZE_FOR_UNIQUE_LABELS)

    rows = table1_to_rows(metrics)
    print_audit(metrics)

    # Print Table 1 (markdown-style)
    print("\n--- Table 1 (paper) ---")
    headers = ["Program", "Courses", "Total extracted items", "Mean items per course",
               "Unique labels", "Singleton share (%)", "Courses naming tools (%)"]
    col_widths = [max(len(str(h)), 8) for h in headers]
    for i, r in enumerate(rows):
        for j, k in enumerate(headers):
            key = k if k in r else k.replace(" (%)", "")
            col_widths[j] = max(col_widths[j], len(str(r.get(key, ""))))
    fmt = " | ".join(f"{{:<{w}}}" for w in col_widths)
    print(fmt.format(*headers))
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
    for r in rows:
        vals = [r.get("Program"), r.get("Courses"), r.get("Total extracted items"),
                r.get("Mean items per course"), r.get("Unique labels"),
                r.get("Singleton share (%)"), r.get("Courses naming tools (%)")]
        print(fmt.format(*[str(v) for v in vals]))

    save_csv(rows, output_path)
    print(f"\nSaved: {output_path}")
    return 0


if __name__ == "__main__":
    exit(main())
