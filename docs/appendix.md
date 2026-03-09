# Appendix: Metric Definitions and Equations

This appendix gives the exact equations used to compute each metric reported in the paper. All metrics are computed **per program** over the set of course descriptions assigned to that program.

---

## 1. Courses analyzed

**Definition.** Number of course descriptions (one per course) assigned to the program.

**Equation:**

$$
\text{Courses analyzed} = \bigl| \{ c : c \in \text{program} \} \bigr|
$$

where each \(c\) is a course record. Equivalently, the count of course records with that program label.

---

## 2. Total extracted skill items

**Definition.** Sum of all skill-item *occurrences* extracted from course descriptions for that program (tools, hard skills, and soft skills). The same label appearing in two courses is counted twice.

**Equation:**

$$
\text{Total extracted skill items} = \sum_{c \in \text{program}} \Bigl( \bigl| \text{tools}(c) \bigr| + \bigl| \text{hard\_skills}(c) \bigr| + \bigl| \text{soft\_skills}(c) \bigr| \Bigr)
$$

---

## 3. Mean extracted skill item per course

**Definition.** Total extracted skill items for the program divided by the number of courses in that program.

**Equation:**

$$
\text{Mean extracted skill item per course} = \frac{\text{Total extracted skill items}}{\text{Courses analyzed}}
$$

---

## 4. Distinct extracted skill labels

**Definition.** Number of *distinct* skill labels in the program after normalizing: labels are pooled from tools, hard skills, and soft skills; within the program, text is lowercased and stripped of leading/trailing whitespace before counting unique labels.

**Equation:**

$$
\text{Distinct extracted skill labels} = \Bigl| \bigcup_{c \in \text{program}} \bigl\{ \text{normalize}(\ell) : \ell \in \text{tools}(c) \cup \text{hard\_skills}(c) \cup \text{soft\_skills}(c) \bigr\} \Bigr|
$$

where $\text{normalize}(\ell) = \text{lowercase}(\text{strip}(\ell))$.

---

## 5. Singleton share (%)

**Definition.** Proportion (as a percentage) of distinct labels that appear **exactly once** in the program (i.e., in only one course).

**Equation:**

$$
\text{Singleton share (\%)} = \frac{\bigl| \{ \ell : \text{count}(\ell) = 1 \} \bigr|}{\text{Distinct extracted skill labels}} \times 100
$$

with the convention that if the denominator is 0, the share is 0%.

---

## 6. Courses with at least one tool (%)

**Definition.** Proportion (as a percentage) of courses in the program that have at least one extracted tool (software, language, or framework).

**Equation:**

$$
\text{Courses with at least one tool (\%)} = \frac{\bigl| \{ c \in \text{program} : \bigl| \text{tools}(c) \bigr| \geq 1 \} \bigr|}{\text{Courses analyzed}} \times 100
$$

---

## Implementation

These metrics are computed in this repository by the script `scripts/table1_metrics.py`, using the data file `data/course_skills_extracted.json`. The same normalization (strip + lowercase) is used for the distinct skill labels listed in `distinct_skill_labels.md` and `distinct_skill_labels.csv`.
