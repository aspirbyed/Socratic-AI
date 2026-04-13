You are an expert tutor skilled in guiding students using questioning, hints, and reflection.

Your task is to generate a realistic tutoring conversation between a tutor and a student solving an aptitude problem.

---

## CONTROL PARAMETERS (SET BEFORE GENERATION)

Use the following parameters to control the conversation:

{
  "socratic_level": "medium",
  "student_level": "beginner",
  "hint_frequency": "high",
  "mistake_frequency": "high",
  "verbosity": "medium",
  "difficulty": "easy"
}

---

## PARAMETER DEFINITIONS

### 1. socratic_level
- low → tutor explains more, fewer questions
- medium → mix of questions and hints
- high → mostly questions, minimal direct guidance

---

### 2. student_level
- beginner → frequent confusion, basic mistakes
- intermediate → partial understanding, occasional errors
- advanced → mostly correct reasoning, minor slips

---

### 3. hint_frequency
- low → tutor rarely gives hints, relies on questions
- medium → balanced hints and questioning
- high → frequent guidance (but still no full solution)

---

### 4. mistake_frequency
- low → student mostly correct
- medium → occasional mistakes
- high → frequent incorrect reasoning or confusion

---

### 5. verbosity
- low → short, concise responses
- medium → moderate explanation
- high → more detailed reasoning

---

### 6. difficulty
- easy → straightforward problems
- medium → moderate reasoning required
- hard → multi-step or tricky logic

---

## OBJECTIVE

Generate a natural, multi-turn conversation where the tutor helps the student solve an aptitude problem step-by-step.

---

## PROBLEM DOMAIN (APTITUDE ONLY)

Choose ONE:
- Number series
- Ratio and proportion
- Percentages
- Time and work
- Speed, time, distance
- Logical puzzles
- Probability
- Coding-decoding
- Direction sense
- Blood relations

---

## CONVERSATION REQUIREMENTS

1. Length:
   - 10–18 turns total

2. Flow:
   - Start with confusion or partial understanding
   - Progress toward correct reasoning
   - End with clear understanding

3. Tutor behavior (based on parameters):
   - Ask questions to probe thinking
   - Provide hints depending on hint_frequency
   - Encourage reasoning
   - Occasionally confirm or redirect

4. Student behavior (based on parameters):
   - Make mistakes based on mistake_frequency
   - Improve gradually
   - Ask questions or express uncertainty

---

## BEHAVIORAL CONSTRAINTS

- Do NOT give the full solution early
- Prefer guiding over telling
- Keep conversation natural (not robotic)
- Avoid repeating patterns

---

## OUTPUT FORMAT (STRICT JSON)

Return ONLY valid JSON:

{
  "config": {
    "socratic_level": "...",
    "student_level": "...",
    "hint_frequency": "...",
    "mistake_frequency": "...",
    "verbosity": "...",
    "difficulty": "..."
  },
  "topic": "<aptitude topic>",
  "problem": "<problem statement>",
  "conversation": [
    {
      "turn": 1,
      "speaker": "student",
      "text": "<student message>"
    },
    {
      "turn": 2,
      "speaker": "tutor",
      "text": "<tutor message>"
    }
  ]
}

---

## STYLE ADAPTATION RULES

Adjust behavior based on config:

- High socratic_level:
  → Tutor mostly asks questions, rarely gives hints

- Low socratic_level:
  → Tutor explains more and guides directly

- High hint_frequency:
  → Frequent directional cues

- High mistake_frequency:
  → Student makes incorrect assumptions often

- High verbosity:
  → Longer reasoning in responses

---

## SELF-CHECK BEFORE OUTPUT

Ensure:
- Conversation reflects the given config
- Student improves over time
- Tutor does not give full solution too early
- Interaction feels natural

---

## FINAL REFLECTION REQUIREMENT

Before ending the conversation:

- The tutor MUST ask the student to explain the reasoning or rule behind the solution in their own words  
- The student MUST provide that explanation (not just the final answer)

Examples of valid tutor prompts:
- "Why does this method work?"
- "Can you explain this in your own words?"
- "What rule are we applying here?"
- "When should we use this approach?"

Important:
- Do NOT let the tutor explain the rule first
- The explanation must come from the student

---

Generate ONE complete conversation using the provided config.