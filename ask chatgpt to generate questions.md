Generate my daily ESAT practice set as **two separate files**:

1. a JSON question deck for my ESATPlayer app
2. a Markdown solutions file containing the fastest useful solution to each question

## 1. Question deck requirements

Generate a valid JSON file using exactly this structure:

```json
{
  "title": "Daily ESAT Set - <date>",
  "questions": [
    {
      "id": null,
      "subject": "m1 / m2 / phys",
      "difficulty": "easy / medium / hard",
      "question": "Question text here",
      "choices": [
        "choice 1",
        "choice 2",
        "choice 3",
        "choice 4"
      ],
      "correct_answer": "A / B / C etc..."
    }
  ]
}
```

Use the following field rules.

### `id`
Always set:

```json
"id": null
```

Do not generate UUIDs. ESATPlayer assigns persistent UUIDs itself when the deck is first loaded.

Interpret difficulty approximately as:

- `easy`: should normally be solvable quickly once the correct observation is made
- `medium`: requires one or two meaningful steps or a less obvious recognition
- `hard`: genuinely challenging under ESAT time pressure, but still appropriate for ESAT rather than olympiad mathematics

### `question`
Use plain English mixed with LaTeX where appropriate.

Use:

```text
$...$
```

for inline maths.

Use:

```text
$$...$$
```

for display maths on its own line.

Example:

```json
"question": "The sequence satisfies\n$$u_{n+1}=2u_n+3$$\nwith $u_1=1$. Find $u_5$."
```

The JSON itself must remain valid, so escape LaTeX backslashes correctly. For example:

```json
"$\\frac{1}{x}$"
"$\\sqrt{5}$"
```

Do not unnecessarily put ordinary prose inside LaTeX.

### `choices`
Use an array of strings.

There must be at least 4 choices. More than 4 choices is allowed where useful. The choices should be plausible distractors based on realistic mistakes or alternative methods, rather than random numbers. Exactly one choice must be correct. The first choice corresponds to `A`, the second to `B`, the third to `C`, and so on.

### `correct_answer`
Must be a single capital letter matching the correct choice. For example, if the fourth choice is correct:

```json
"correct_answer": "D"
```