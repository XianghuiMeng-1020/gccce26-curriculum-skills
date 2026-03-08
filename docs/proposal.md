# GenAI-Driven Curriculum Analytics: Mapping and Gap Analysis
## Case Study: BASc(SDS) vs. BSc(IM)

---

## 1. Executive Summary

This project employs **Generative AI (Large Language Models)** to perform a semantic analysis of university curriculum syllabi. By moving beyond traditional keyword matching to **semantic skill extraction**, we aim to construct a high-fidelity "Skill Graph" for two distinct programs:
* [cite_start]**BASc(SDS):** Bachelor of Arts and Sciences in Social Data Science [cite: 1]
* [cite_start]**BSc(IM):** Bachelor of Science in Information Management [cite: 559]

The objective is to visualize the **Skill Supply** provided by the university and analyze the distinctive identities, overlaps, and structural differences between the two disciplines.

---

## 2. Methodology & Workflow

The analysis pipeline consists of three phases: **Data Parsing**, **GenAI Extraction**, and **Quantitative Visualization**.

### Phase 1: Unstructured Data Parsing
We processed the raw PDF syllabus documents for the 2025-26 academic year. Using Python scripts, we sliced the documents into granular **Course Objects**, extracting the `Course Code`, `Title`, and `Description`.

* [cite_start]**Data Source A:** BASc(SDS) Regulations & Syllabuses (40+ courses including electives) [cite: 139]
* [cite_start]**Data Source B:** BSc(IM) Regulations & Syllabuses (19 core and elective courses) [cite: 692]

### Phase 2: GenAI Skill Extraction (Prompt Engineering)
To reduce "Hallucinations" and ensure structured data, we utilized a **Chain-of-Thought (CoT)** approach with a defined Taxonomy. We instructed the LLM (GPT-4o) to categorize skills into three distinct buckets.

#### The Prompt Design
We used a strict System Prompt to enforce the JSON output format and taxonomy adherence.

**System Instruction:**
```text
You are an expert Curriculum Analyst and Career Data Scientist. 
Your task is to analyze the provided course description and extract professional skills.

Step 1: Analyze the text to identify specific technical tools, hard theoretical concepts, and soft skills.
Step 2: Classify extracted terms into the following JSON structure:
    - "tools": [List of software, programming languages, platforms]
    - "hard_skills": [List of technical methodologies, domain knowledge]
    - "soft_skills": [List of interpersonal, management, or cognitive skills]

Rules:
1. Extract ONLY from the text provided. Do not hallucinate skills not implied.
2. Normalize terms (e.g., map "statistical analysis methods" to "Statistical Analysis").
3. Output strictly valid JSON.
```
**User Input Example:**
```text
Course: BSDS3003 Data processing and visualization
Description: This course provides an in-depth exploration of data processing... Basic knowledge of Python programming is needed.
```

### Phase 3: Post-Processing
The JSON outputs were flattened into a tabular dataset (DataFrame) for statistical analysis. We calculated Frequency (TF) and Distinctive Scores to compare the two programs.

**Table 1: GenAI Extraction Validation (Sample Results)**
*A comparison of raw syllabus text against the structured GenAI output, demonstrating the extraction logic.*

| Course Code | Raw Description Fragment (Source) | Extracted Tools | Extracted Hard Skills | Extracted Soft Skills |
| :--- | :--- | :--- | :--- | :--- |
| **BSDS3003** (SDS) | "...Basic knowledge of Python programming is needed... skills needed in exploring, analyzing..." | `Python` | `Data Processing`, `Data Visualization`, `Feature Engineering` | *(None listed in description)* |
| **BSIM4011** (IM) | "...General management and communication skills are explored... use project management software..." | *(Implied Software)* | `Project Management`, `Change Management`, `Planning` | `General Management`, `Communication` |
| **BSDS3001** (SDS) | "...Methods of inquiry and research... address social issues or challenges..." | *(None)* | `Data Analysis`, `Research Methods` | `Critical Thinking`, `Problem Solving` |

## 3. Results & Analysis
The following visualizations reconstruct the "Skill DNA" of each program.
### 3.1 Technical Architecture: The "Builder" vs. The "Manager"
![Top 15 Technical Tools Comparison](plot/analysis_1_top_tools.png)

**Table 2: Key Technical Stack Mapping (Evidence Chain)**
*Linking high-frequency tools directly to specific curriculum requirements found in the dataset.*

| Tool Category | Top Tool | Primary Program | Representative Courses (Evidence from JSON) |
| :--- | :--- | :--- | :--- |
| **Scripting & Modeling** | **Python** | **BASc(SDS)** | *SDST2604 Intro to R/Python*, *BSDS3003 Data Processing*, *BSDS3004 Intro to Statistics* |
| **Database & Query** | **SQL** | **BSc(IM)** | *BSIM3017 Database Systems* (Explicitly teaches Structured Query Language) |
| **System Design** | **UML** | **BSc(IM)** | *BSIM3014 User-based Systems Analysis* (Explicitly teaches Unified Modeling Language) |
| **Spatial Analysis** | **GIS / GPS** | **BASc(SDS)** | *GEOG2090 Intro to GIS*, *GEOG3417 Health, Wellbeing, Place and GIS* |
| **Visualization** | **Tableau/Power BI** | **Shared** | *BSIM4028 Principles and Practice of Data Visualization* |

#### Observation:
* **BASc(SDS) Dominance (Blue Bars):** The chart illustrates a distinct reliance on computational scripting and spatial analysis. **Python** is the most frequently mentioned tool (Frequency ≈ 3.0), followed by **GIS** (Geographic Information Systems) and **R**. [cite_start]This aligns directly with the curriculum's emphasis on building models from scratch, as seen in courses like *Introduction to R/Python programming* [cite: 301] [cite_start]and *Modern maps in the age of big data*[cite: 206].
* **BSc(IM) Dominance (Yellow Bars):** The IM program shares visualization tools like **Tableau**, **Qlik**, and **Power BI** with SDS, but uniquely emphasizes **Unified Modeling Language (UML)**. [cite_start]While **SQL** is present in both, the IM curriculum places a stronger structural focus on it within courses like *Database systems* [cite: 728] [cite_start]and *User-based systems analysis*[cite: 780], highlighting a focus on system architecture.

#### Theoretical Insight:
This visualization confirms the **"Builder vs. Manager"** structural distinction in the curriculum design:
* **SDS (The Builder):** Focuses on the "Creation Stack" (Python/R/GPS) to generate new insights, statistical models, and algorithms from raw data.
* **IM (The Manager):** Focuses on the "Management Stack" (UML/SQL/BI Tools), emphasizing the organization, storage, architectural design, and presentation of existing information assets.
---
### 3.2 Curriculum Convergence: The Shared Core
![Skill Set Overlap Venn Diagram](plot/analysis_2_skill_overlap.png)

**Table 3: The "Data Literacy Core" (Top Shared Skills)**
*The intersection of the two programs defines the universal requirements for data professionals as found in the syllabus data.*

| Shared Skill Dimension | Specific Skills | Context in BASc(SDS) | Context in BSc(IM) |
| :--- | :--- | :--- | :--- |
| **Communication** | Visualization, Reporting | *CAES9420 Academic English*: "Report writing and oral presentation" | *CAES9420 Academic English*: "Communication to an academic audience" |
| **Ethics & Governance** | Privacy, Security, Ethics | *MLIM7350 Data Curation*: "Legal and Ethical Considerations" | *BSIM4028 Data Visualization*: "Ethical Practice in Data Visualization" |
| **Execution** | Project Management | *BSDS4999 Project*: "Project Management" skills for research | *BSIM4011 Project Management*: "Project life cycle and techniques" |

#### Observation:
* **Unique Skills (Asymmetry in Scope):** The Venn diagram reveals a significant asymmetry in the curriculum breadth. **SDS (Blue area)** possesses a much larger set of unique skills (**132**), reflecting its broad interdisciplinary nature that draws from Social Sciences, Geography, Psychology, and Statistics (e.g., "Mental Health", "Global Economy"). In contrast, **IM (Yellow area)** is more specialized with **44** unique skills, focusing deeply on the domain of library and information sciences.
* **Intersection:** There are **56 shared skills** in the intersection, representing a substantial overlap in the foundational competencies.

#### Theoretical Insight:
The overlap represents the **"Data Literacy Core"** essential for any modern data professional. Regardless of whether a student is trained as an analyst (SDS) or a manager (IM), both programs recognize a foundational need for:
1.  **Data Visualization** (Communicating insights).
2.  **Ethics** (Responsible use of data and information).
3.  **Project Management** (Executing tasks in organizational settings).
This convergence suggests that while the "ends" (Policy vs. Curation) differ, the "means" (Basic Data Literacy) are shared.
---

### 3.3 Skill Composition: The Hard/Soft Balance
![Distribution of Skill Types](plot/analysis_3_skill_types.png)
#### Observation:
* **Hard Skills (Left Group):** Both programs are overwhelmingly technical, with Hard Skills comprising nearly **80%** of the extracted skill set. This validates the academic rigor of both degrees as Science-based programs, ensuring students possess deep substantive knowledge.
* **Soft Skills (Middle Group):** A key divergence appears here. **BSc(IM) (Yellow bar)** shows a noticeably higher proportion of Soft Skills (~20%) compared to SDS (~16%). This aligns with the IM curriculum's inclusion of courses like *Project management* and *Information behavior*, which focus on organizational dynamics.
* **Tools (Right Group):** SDS maintains a slightly higher emphasis on specific Tool usage, reinforcing its practical, hands-on nature in implementing computational models.

#### Theoretical Insight:
This supports the **"Human-in-the-Loop" Theory** of Information Management:
* **IM** places higher weight on **Soft Skills** because Information Management is inherently socio-technical—it involves understanding *User Needs*, *Leadership*, and *Communication* with stakeholders to ensure systems are actually adopted and used effectively.
* **SDS** prioritizes **methodological accuracy** (Hard Skills), focusing on the statistical validity and computational efficiency of models over the organizational context of their implementation.
---
### 3.4 Distinctive Competencies: Program Identity
![Most Distinctive Skills](plot/analysis_4_distinctive_skills.png)
#### Observation:
This diverging lollipop chart effectively isolates the "Genetic Difference" between the two programs by plotting the relative frequency difference of skills:
* **SDS Identity (Right Side, Blue):** The skills most unique to SDS are dominated by **Critical Thinking** (the largest outlier), followed by **Policy Analysis**, **Statistical Analysis**, and **Python**. This cluster combines high-level cognitive skills with the technical tools needed to execute them.
* **IM Identity (Left Side, Yellow):** The skills most unique to IM are dominated by **Information Management**, followed by **Communication**, **Project Management**, and **Metadata Implementation**. This cluster mixes broad management concepts with specific information governance techniques.

#### Theoretical Insight:
This analysis successfully isolates the **Core Value Proposition** of each degree:
* **SDS = "Interpretation & Inquiry":** The massive distinctiveness of *Critical Thinking* and *Policy Analysis* suggests that SDS uses data as a means to an end—specifically to interpret complex social behaviors and formulate policy interventions. The technical skills (Python, Stats) serve this analytical purpose.
* **IM = "Curation & Governance":** The focus on *Information Management*, *Metadata*, and *Communication* confirms that IM is dedicated to the infrastructure of knowledge. The goal is not just to analyze data, but to curate, organize, and manage the lifecycle of information assets to ensure they are accessible and usable by organizations.

---
## 4. Conclusion

The application of GenAI for semantic curriculum mapping has successfully decoded the underlying "Skill DNA" of the two programs, revealing a quantifiable structural distinction that extends far beyond surface-level course titles.

**Table 4: Strategic Competency Matrix**
*A final summary of the distinct identities revealed by the analysis.*

| Dimension | BASc(SDS): The Computational Interpreter | BSc(IM): The System Architect |
| :--- | :--- | :--- |
| **Primary Goal** | **Derive Meaning** from Data | **Manage Lifecycle** of Data |
| **Key Technical Stack** | Python, R, GIS, SPSS (Creation Stack) | SQL, UML, Tableau (Management Stack) |
| **Top Distinctive Hard Skill** | *Statistical Modeling* (`BSDS3005`) | *Information Retrieval* (`BSIM3004`) |
| **Top Distinctive Soft Skill** | *Critical Thinking* (`BSDS3001`, `POLI3039`) | *Communication / Leadership* (`BSIM3998`) |
| **Target Career Profile** | Data Analyst, Policy Researcher | Information Manager, Solution Architect |

**Theory Validation & Market Positioning:**
The empirical data supports a clear division of labor within the "Data Domain":

* **BASc(SDS) as the "Computational Interpreter":**
    By prioritizing **Python, Statistical Modeling, and Critical Thinking**, SDS supplies the market with **Analysts and Policymakers**. These graduates are equipped to build the algorithms required to *interpret* complex social behaviors and formulate evidence-based policies. They operate primarily in the "Creation Stack" of data science.

* **BSc(IM) as the "System Architect":**
    By prioritizing **SQL, Metadata, Project Management, and Communication**, IM supplies the market with **Managers and Information Architects**. These graduates are designed to *curate and govern* the information lifecycle, ensuring that data ecosystems are accessible, organized, and ethically managed. They operate primarily in the "Management Stack" of information infrastructure.

Ultimately, while both degrees share a foundational **Data Literacy Core**, they diverge to serve complementary roles: one builds the models to understand the world (SDS), while the other builds the systems to organize that understanding (IM).