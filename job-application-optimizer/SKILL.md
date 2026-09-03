---
name: job-application-optimizer
description: "Complete job application toolkit using the Maverick AI framework. Use this skill whenever a user is applying for a specific job and needs: resume optimization (audit, rewrite with XYZ formula, ATS testing), customized cover letter, interview preparation (company research, predicted questions with answers), and salary negotiation strategy. Triggers on phrases like 'help me apply for this job', 'optimize my resume for this role', 'I have an interview coming up', 'prepare me for this job', or when the user uploads both a resume and job description. Works with any resume format (Word, PDF, plain text) and job description format (same)."
---

# Job Application Optimizer

Complete job application toolkit powered by the Maverick AI framework. Automates resume optimization, cover letter generation, interview prep, and salary negotiation in one workflow.

## How This Works

This skill takes your resume and a specific job description, then runs them through a battle-tested framework that:

1. **Audits your resume** — Match score, missing keywords, red flags from ATS + hiring manager perspective
2. **Interviews you about the gaps** — Surfaces experience you have but didn't put on the resume
3. **Rewrites your experience** — Uses the Google XYZ formula (Accomplished X as measured by Y by doing Z)
4. **Tests the output** — ATS scan + hiring manager review
5. **Generates cover letter** — 30-second, targeted, gap-addressing
6. **Preps for interviews** — Company intel, predicted questions, sample answers
7. **Scripts salary negotiation** — Market data, counter-offer email, phone call script

All outputs are personalized to the specific role and company.

---

## Step 1: Gather Your Materials

The skill needs:

1. **Your resume** — Upload as .docx, .pdf, or paste plain text
2. **Job description** — Upload or paste the full job posting
3. **Target salary** — For the negotiation script (asked later)

**Important:** always start from the user's canonical base resume, not from a version rewritten for a previous job. Rewrites that compound across applications drift away from the user's actual experience. Each new application customizes from the original.

## Step 2: Resume Audit

First, the skill acts as a senior recruiter at the target company and analyzes your resume against the job description.

You'll receive:
- **Match score** (0-100)
- **Top 5 missing keywords** that the ATS scans for
- **3 red flags** a hiring manager spots in under 10 seconds
- **Strengths** in your resume
- **Weaknesses** to fix
- **Comparison** to what a strong candidate looks like

Be brutally honest here. The user would rather fix problems now than get ghosted later.

## Step 3: Interactive Gaps Interview

This is where the skill gets collaborative. **Just because something isn't on your resume doesn't mean you don't have the experience.**

Never assume the resume is complete. For each missing keyword or red flag from Step 2, ask probing questions before concluding anything is actually missing.

**Example Gap Questions:**

- **"You have RHEL/Oracle Linux experience. Do you have experience with Debian, Ubuntu, or other Debian-based Linux distributions? (Personal projects, older roles, cost-optimized production systems, etc.?)"**

- **"For [missing tool/skill], have you worked with this in any context — production, side projects, learning, previous roles you didn't emphasize?"**

- **"The role emphasizes hands-on [X]. On your resume, you talk more about designing/architecting systems. When you were at [your old company], were you personally doing hands-on work, or more delegating?"**

- **"Why didn't you include [experience] on your resume? Too old? Different context? Felt less important than other work?"**

For each missing keyword or red flag, work through:

1. **"Do you actually have experience with [X]? If so, where?"**
2. **"Why isn't it on your resume?"** — Too old? Different context? Passed over for higher-impact work?
3. **"How recent is this experience, and in what context?"** — This matters for credibility. "Ubuntu desktop in 2008" is different from "Debian in production last year."
4. **"Could we reframe this on your resume?"** — This turns buried experience into a selling point.

**The user's job**: Be honest and specific. Answer with yes/no, when and where, the context, and why it matters.

**The skill's job**: Take those answers and surface the hidden experience on the resume.

**Example**:
- User says: "I used Debian at gumi (2014-2016) for cost optimization. Also Ubuntu on my desktop in university."
- Skill reframes it: "Deployed and maintained Debian-based infrastructure at gumi Asia (500K+ DAU gaming platform), leveraging cost-optimized Linux distributions for edge compute and gaming servers."
- And revises the narrative: instead of "no Debian experience," the story becomes "I understand the cost/support tradeoffs between Debian-based and enterprise Linux distros, and I've used both in production and development contexts."

## Step 4: Experience Rewrite

Using the audit results *and the answers from the gaps interview*, rewrite the experience section with these rules:

1. Naturally include missing keywords (no forced insertions)
2. Fix every red flag identified
3. **Use the Google XYZ formula**: "Accomplished [X] as measured by [Y] by doing [Z]"
   - Example: Instead of "Managed a team of 5 engineers"
   - Rewrite as: "Reduced deployment time by 40% (measured by weekly release velocity) by restructuring the engineering team into cross-functional pods"
4. Start every bullet with a strong action verb. Never use "Responsible for" or "Helped with"
5. Add specific metrics and numbers. If the user didn't provide numbers, suggest realistic placeholders marked `[FILL IN]`
6. Keep bullets to 1-2 lines max
7. Order bullets by impact, not chronology. The most impressive result goes first

Rewrites should enhance and reposition the user's original experience — never invent it.

## Step 5: ATS + Hiring Manager Stress Test

Test the rewritten resume from two perspectives:

- **ATS filter**: Would it pass? Which keywords are present/missing? Any formatting issues that would confuse a parser (tables, columns, headers, special characters, images)?
- **Hiring manager scan** (reading 200 resumes in one sitting): Which sections would they skip, and why? What makes them stop scrolling? Yes/Maybe/No pile?

Rewrite any section that would get skipped so it actually stops the scroll.

The result: a final, optimized resume ready to submit.

**Output format**: PDF document with the complete rewritten resume

---

## Step 6: Cover Letter Generation

Generate a targeted cover letter with:

1. **First paragraph**: Company name, role, one specific thing about the company (a recent product launch, news article, or value that resonates). Do NOT be generic.
2. **Second paragraph**: The 2-3 requirements where the user's experience is strongest, each with one concrete result and numbers.
3. **Third paragraph**: Address the biggest gap head-on. Explain transferable or adjacent experience. Do not pretend the gap doesn't exist.
4. **Closing**: One sentence. Ask for the interview. No "I look forward to the opportunity to discuss."

**Total length**: Under 250 words. Confident, specific, human tone. Should not sound AI-written.

---

## Step 7: Interview Preparation

Research the company and prepare the user with:

### Company Intel
- What the company actually does (2 sentences, no PR speak)
- Recent news (last 90 days) worth referencing
- Their biggest challenge or competitor threat
- What Glassdoor/Blind reviews say about their interview process and culture

### Predicted Interview Questions (top 10)
For each question:
- The question they'll ask
- Why they're asking it (what they're testing)
- A sample answer using the user's actual resume experience, with specific metrics
- The likely follow-up question

Do **not** run a mock interview. Deliver predicted questions and answers.

### Questions the User Should Ask
5 questions that show deep research and business understanding — not generic "What's a typical day?" questions.

---

## Step 8: Salary Negotiation Script

Ask the user for their target salary; don't derive it from market data alone. Then:

### Market Data
- Current pay range for this role at this company (Levels.fyi, Glassdoor, Blind, Payscale)
- Where the user's target falls in that range

### Counter-Offer Strategy
- The exact email to send (grateful, confident, specific)
- References market data without being adversarial
- Asks for a specific number, not a range

### Phone Call Scripts
- Opening the conversation
- Stating the counter
- Handling "this is the best we can do"
- Negotiating non-salary items if base is firm (signing bonus, PTO, remote flexibility, relocation, start date)

### Walk-Away Analysis
- At what number should they accept?
- At what number should they walk away?
- What non-monetary factors make a lower offer worth taking?

---

## Important Notes

### Always Review and Personalize
The skill generates the structure and language. The user provides the substance:
- Add their own voice and stories
- Fill in any `[FILL IN]` placeholders with real data
- Adjust generic phrasing to match how they actually talk
- Review predicted questions and adjust for their specific experience

### Resume Customization Per Job
The same resume doesn't work for every role. The missing keywords and red flags change based on the job description.

Run this skill for each job applied to (about 15-20 minutes per application).

---

## Workflow Summary

```
1. Upload resume + job description (5 min setup)
   ↓
2. Resume audit (match score, missing keywords, red flags)
   ↓
3. Interactive gaps interview (Claude asks, user answers)
   ↓
4. Experience rewrite using XYZ formula + gap answers
   ↓
5. ATS + hiring manager stress test
   ↓
6. Final resume PDF output (download + submit)
   ↓
7. Cover letter generated
   ↓
8. Interview prep (company intel + predicted Qs)
   ↓
9. Salary negotiation script (when offer comes)
```

---

## Tips for Success

- **Don't skip the audit.** Understanding the gap is half the work.
- **Don't skip the gaps interview.** The audit only sees what's on the page, not what the candidate has done.
- **Use the XYZ formula religiously.** It's the difference between a task description and an accomplishment.
- **Include metrics.** Hiring managers care about impact, not effort.
- **Address gaps head-on in cover letters.** Confidence beats pretending.
- **Customize for every job.** The keywords change, so the bullets change.
- **Always negotiate the offer.** Almost every offer has room to move.
