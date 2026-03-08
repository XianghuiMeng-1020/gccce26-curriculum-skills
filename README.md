# Curriculum Skill Extraction (GCCCE 26)

This repository contains data and code for the semantic skill extraction and comparison of two degree programs from official course descriptions. It supports transparency and reproducibility for the associated paper.

## Repository structure

```
.
├── data/                          # Input and derived data
│   ├── course_skills_extracted.json
│   └── pdf_data.json
├── scripts/                       # Python pipelines and generators
│   ├── step1_batch.py             # Batch skill extraction (LLM)
│   ├── step2_analy.py             # Analysis and publication plots
│   ├── step2_analy_update.py      # Variant with labeled plots
│   ├── generate_distinct_skill_labels.py
│   ├── table1_metrics.py
│   └── tools.py
├── docs/                          # Project documentation
│   └── proposal.md
├── plot/                          # Generated figures (created by scripts)
├── distinct_skill_labels.md       # Distinct skill labels by program (for GitHub)
├── distinct_skill_labels.csv      # Same data in CSV format
├── table1_metrics.csv             # Optional: Table 1 metrics (run table1_metrics.py)
└── README.md
```

## Skill labels for transparency

- **`distinct_skill_labels.md`** — Markdown list of all distinct extracted skill labels for Program 1 and Program 2, with a short note on extraction and normalization.
- **`distinct_skill_labels.csv`** — Same content in CSV (columns: Program, Program name, Label) for reuse and checking.

Labels are normalized within each program by lowercasing and stripping whitespace; they are derived from official course descriptions only. Program 1 corresponds to BASc(SDS), Program 2 to BSc(IM).

### Regenerating the skill label lists

From the repository root:

```bash
python scripts/generate_distinct_skill_labels.py
# Or with a custom input file:
python scripts/generate_distinct_skill_labels.py data/course_skills_extracted.json
```

Outputs are written to the repo root: `distinct_skill_labels.md` and `distinct_skill_labels.csv`.

## Running the pipeline

All scripts assume they are run from the **repository root** (paths are relative to it).

1. **Extract skills** (requires API/tools in `tools.py`):
   ```bash
   python scripts/step1_batch.py
   ```
   Reads `data/pdf_data.json`, writes `data/course_skills_extracted.json`.

2. **Table 1 metrics**:
   ```bash
   python scripts/table1_metrics.py
   ```
   Reads `data/course_skills_extracted.json`, writes `table1_metrics.csv` to repo root.

3. **Plots**:
   ```bash
   python scripts/step2_analy.py
   # or
   python scripts/step2_analy_update.py
   ```
   Reads `data/course_skills_extracted.json`, writes figures to `plot/`.

## Manuscript reference

For the paper, you may refer readers to the repository as follows:

> The complete list of distinct extracted skill labels for Program 1 and Program 2, together with the normalization rules used, is available in the project repository (files `distinct_skill_labels.md` and `distinct_skill_labels.csv`) to support transparency and verification of the reported results.

Replace “the project repository” with your actual GitHub URL (e.g. `https://github.com/yourusername/your-repo`).

## License

See repository or paper for license and citation details.
