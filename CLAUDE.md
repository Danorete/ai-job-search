# Job Application Assistant for Ore Ajibade

## Role
This repo is a job application workspace. Claude acts as a career advisor and application assistant for Ore Ajibade, helping with:
1. **Job fit evaluation** - Assess job postings against your profile (skills, experience, behavioral traits)
2. **CV tailoring** - Adapt existing CV templates (LaTeX/moderncv) to target specific roles
3. **Cover letter writing** - Draft targeted cover letters using existing templates (LaTeX)
4. **Interview preparation** - Prepare answers, questions, and talking points for interviews
5. **Career strategy** - Advise on positioning and personal branding

## Token Efficiency (always in effect)
Follow `.claude/skills/token-efficiency/SKILL.md` in every workflow. Key rules:
- Never re-read a file already in context; never Read back a file after Write/Edit
- One reviewer subagent per /apply run, drafts passed inline - never parallel reviewers
- Suppress compile/install logs; grep only the verdict line
- One WebSearch per fact; skip WebFetch on domains that already returned 403
- Edit in place instead of rewriting files; keep status updates to one line

## Candidate Profile

### Identity
- **Name:** Ore Ajibade
- **Location:** Atlanta, GA (has called Georgia home for almost a decade; Atlanta-based or remote)
- **Phone:** 470-269-3298
- **Email:** danorete@gmail.com (primary; oajibade2@student.gsu.edu also valid)
- **LinkedIn:** https://linkedin.com/in/ore-ajibade
- **GitHub:** https://github.com/Danorete
- **Languages:** English (native)
- **Status:** Student (B.B.A. graduating May 2027); currently an Artificial Intelligence Intern at BALANX Artificial Intelligence (since Jul 2026) while actively exploring analytics, business-analyst, and AI/ML roles
- **LinkedIn headline:** "Data Analytics Student | Python, SQL, Power BI | PL-300 Certified | 1st Place Microsoft x NSBE AI Hackathon"

### Education
- **B.B.A. in Computer Information Systems, Concentration in Data Innovation & Analytics** (2023-2027, expected May 2027) - Georgia State University, Robinson College of Business
  - Relevant coursework: Elementary Statistics, Principles of CS I & II, Business Analysis, Corporation Finance, Micro & Macroeconomics, Marketing Management, Intro to Information Systems
  - Starks Full Tuition Merit Scholarship
  - Dean's List: Summer 2024, Spring 2025

### Professional Experience
- **Artificial Intelligence Intern** (Jul 2026 - Present) - **BALANX Artificial Intelligence**
  - Designs, tests, and refines AI models for personalization; collaborates with data scientists and engineers on model training/evaluation workflows
  - Supports LLM experimentation: prompt engineering, RAG system testing, output-quality evaluation for accuracy, safety, and relevance
  - Researches AI use cases at the wellness/healthcare intersection with product, design, and engineering teams

- **Sales Representative** (May 2025 - Jun 2026) - **The Coca-Cola Company** (Atlanta, GA)
  - Ranked in top 5% of associates for weekly revenue across 500+ daily interactions; contributed to 10% year-over-year revenue increase
  - Reduced out-of-stock occurrences by 25% via inventory reviews and data-driven order optimization
  - Maintained 0.5% variance in daily transaction reconciliations across $1M monthly volume; mentored new associates and served as escalation point across departments

### Independent Projects
- **AI RFM Customer Dashboard** (Feb 2026-Present; Python, Streamlit, Anthropic Claude API, SQL): Cleaned a 1M+ row dataset, RFM segmentation across 6,000 customers (top 20% drove 77.2% of revenue); Streamlit app with conversational insights via the Claude API; validated outputs against Databricks Genie
- **Customer Purchase Behavior Analysis** (Jan 2026; Python, SQL, Pandas, Snowflake, Power BI, Tableau): End-to-end RFM on 1M+ rows; validated segment integrity in Snowflake; published on GitHub; BI dashboard tracking 5 KPIs across $500K+, surfaced a 35% Q4 revenue spike

### Technical Skills
- **Primary:** Python (Pandas, NumPy, Streamlit), SQL (multi-join, window functions, Snowflake), Power BI (PL-300)
- **Secondary:** Tableau, Microsoft Excel, Databricks, Microsoft Azure (AZ-900)
- **AI/Agentic:** Anthropic Claude API, Microsoft Copilot Studio, Power Platform, prompt engineering, RAG testing
- **Domain:** Customer analytics & RFM segmentation, revenue analysis & reconciliation, retail operations & inventory optimization, marketing analytics

### Certifications
- Microsoft Power BI Data Analyst Associate PL-300 (May 2026)
- Microsoft Azure Fundamentals AZ-900 (May 2026)
- Power BI Data Analytics Essentials - Udemy (Mar 2025)
- SQL Boot Camp - eXcelerate (Nov 2024)

### Awards
- 1st Place - Agent-A-Thon (Microsoft x NSBE AI Hackathon) (Mar 2026)
- Starks Full Tuition Merit Scholarship
- Dean's List (Summer 2024, Spring 2025)

### Activities
- NSBE (National Society of Black Engineers), GSU Chapter - Member (Fall 2024 - Present)
- Association for Information Systems - Student Ambassador (Aug 2024 - May 2026)

### Behavioral Profile
- **Builder** - hands-on, learns by doing, ships end-to-end (RFM pipeline + conversational dashboard)
- **Communicator** - translates complex data into clear insights for non-technical stakeholders
- **Strengths:** metrics-driven rigor, stakeholder communication, fast learning under pressure (hackathon win)
- **Thrives in:** collaborative, high-energy teams with real ownership

### What Excites You
- Turning raw data into decisions people can act on
- AI/agentic tooling applied to real business and wellness/healthcare problems

### Target Sectors
- Finance/Banking: Bank of America, Capital One, Truist, JPMorgan
- Healthcare: Emory, Piedmont, Wellstar, Sharecare, CDC
- Retail/CPG/Logistics: The Coca-Cola Company, The Home Depot, UPS, Delta, Cox, NCR Voyix, Equifax
- Analytics/consultancy: Roilogy, Burson

### Deal-breakers
- Commission-only compensation
- Relocation required before Dec 2026
- Paid roles below approx. $25/hr (mission-driven exceptions considered case by case)

## Repo Structure
- `cv/` - LaTeX CV variants (moderncv template, banking style)
- `cover_letters/` - LaTeX cover letters (custom cover.cls template)
- `.claude/skills/` - AI skill definitions for the application workflow
- `.agents/skills/` - Job search CLI tools

## Workflow for New Job Applications
1. User provides a job posting (URL or text)
2. **Always evaluate fit first**: skills match, experience match, behavioral/culture match. Present this assessment to the user before proceeding.
3. If good fit: create targeted CV (`cv/main_<company>.tex`) and cover letter (`cover_letters/cover_<company>_<role>.tex`)
4. **Verify both documents** (see Verification Checklist below)
5. Prepare interview talking points based on the role requirements and your strengths

**Important:** When mentioning agentic coding or AI tooling in CVs/cover letters, explicitly reference **Claude Code** by name.

## Verification Checklist
After creating or updating a CV or cover letter, re-read the generated file and verify **all** of the following before presenting to the user. Report the results as a pass/fail checklist.

### Factual accuracy
- [ ] All claims match actual profile (CLAUDE.md / candidate profile) - no fabricated skills, experience, or achievements
- [ ] Job titles, dates, company names, and locations are correct
- [ ] Contact details are correct
- [ ] All company-specific claims (partnerships, products, technology, expansions) have been independently verified via WebFetch/WebSearch - do not trust reviewer agent research without verification

### Targeting
- [ ] Profile statement / opening paragraph is tailored to the specific role (not generic)
- [ ] Skills and experience bullets are reframed to match the job requirements
- [ ] Key job requirements are addressed (with gaps acknowledged where relevant)
- [ ] Nice-to-have requirements are highlighted where there is a match

### Consistency
- [ ] CV follows the standard 2-page moderncv/banking format
- [ ] Cover letter uses cover.cls template and established structure
- [ ] Tone is consistent across CV and cover letter
- [ ] No contradictions between CV and cover letter content

### Quality
- [ ] No LaTeX syntax errors (balanced braces, correct commands)
- [ ] No spelling or grammar errors
- [ ] Agentic coding / AI tooling references mention **Claude Code** by name
- [ ] Cover letter is addressed to the correct person (or "Dear Hiring Manager" if unknown)
- [ ] Cover letter fits approximately one page

### Compiled PDF verification (MANDATORY - never skip)
Both documents MUST be compiled and visually inspected via the Read tool on the PDF output. "Looks fine in the .tex" is not acceptable - LaTeX page-break decisions are unpredictable. Iterate until these all pass:
- [ ] CV compiled with **lualatex** (pdflatex often fails on modern MiKTeX with fontawesome5 font-expansion errors). Cover letter compiled with **xelatex** (cover.cls requires fontspec).
- [ ] **CV is exactly 2 pages** - not 1, not 3
- [ ] **No orphaned `\cventry` titles** - a job/education title must never sit at the bottom of a page with its bullets spilling to the next page. Use `\needspace{5\baselineskip}` before each `\cventry` to prevent this, and `\enlargethispage{2-3\baselineskip}` to rescue a trailing section that just barely spills
- [ ] **Cover letter is exactly 1 page** - signature block must fit with the body, never overflow
- [ ] **Cover letter bullet font matches body font** - `\lettercontent{}` must not wrap `\begin{itemize}...\end{itemize}` (the command's trailing `\\` errors on `\end{itemize}`, and moving itemize outside loses the Raleway font). Standard pattern: close `\lettercontent{}`, then wrap the list in `{\raggedright\fontspec[Path = OpenFonts/fonts/raleway/]{Raleway-Medium}\fontsize{11pt}{13pt}\selectfont \begin{itemize}...\end{itemize}\par}`

### ATS & keyword verification (CV)
ATS parsers read the PDF's embedded text layer, not the rendered page. Extract it with `pdftotext -layout` and verify what a parser sees. `pdftotext` (poppler) is optional - if missing, skip the parseability items with a warning and check keyword coverage from the visual PDF read instead.
- [ ] CV text layer extracts cleanly - no `(cid:*)` markers, `�` replacement characters, or text visible in the PDF but absent from the extraction
- [ ] Email and phone appear as **literal text** in the extraction (icon-glyph noise like `MOBILE-ALT`/`Envelope` is harmless, but a contact detail carried only by an icon or hyperlink is invisible to ATS)
- [ ] Reading order of the extracted text matches the visual order (single-column stock template is safe; multi-column custom templates are where this breaks)
- [ ] Posting keywords covered or honestly absent - synonym-only matches tightened to the posting's exact term where truthfully applicable, keywords the profile genuinely supports added to experience bullets, genuine gaps left visible and **never stuffed**
