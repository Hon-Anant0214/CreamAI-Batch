
# GATENavigator - Prompt Comparison

## 1. Objective

The objective is to compare two prompt versions and evaluate which one produces better responses for GATENavigator.

We will test both prompts using the 10 questions stored in `Data/user_questions.md`.

## 2. Prompt Versions

### Version 1: Basic Prompt

You are GATENavigator, an AI assistant for GATE students.

Answer the student's question clearly and helpfully.

### Version 2: Improved Prompt

You are GATENavigator, an AI educational assistant for GATE students.

Follow these instructions:

- Provide accurate and student-friendly answers.
- Use available GATE data when answering paper-related questions.
- Never invent official GATE information.
- Clearly mention when information is unavailable.
- Explain technical topics in simple language.
- Return valid JSON containing:
  - answer
  - confidence
  - follow_up

The confidence value must be between 0 and 1.

## 3. Evaluation Criteria

We will evaluate both prompt versions using these criteria:

| Criteria | Description |
|---|---|
| Accuracy | Is the answer correct? |
| Relevance | Does it answer the question? |
| Clarity | Is the response easy to understand? |
| Missing Data Handling | Does it avoid inventing unavailable information? |
| JSON Format | Does it return valid JSON? |

## 4. Test Questions

The following 10 questions will be used for evaluation.

The questions are available in `Data/user_questions.md`.

| Question | Version 1 Result | Version 2 Result |
|---|---|---|
| Q1 | Pending | Pending |
| Q2 | Pending | Pending |
| Q3 | Pending | Pending |
| Q4 | Pending | Pending |
| Q5 | Pending | Pending |
| Q6 | Pending | Pending |
| Q7 | Pending | Pending |
| Q8 | Pending | Pending |
| Q9 | Pending | Pending |
| Q10 | Pending | Pending |

## 5. Evaluation Score

Score each criterion from 1 to 5.

- 1 = Poor
- 2 = Below Average
- 3 = Average
- 4 = Good
- 5 = Excellent

| Evaluation Criteria | Version 1 | Version 2 |
|---|---:|---:|
| Accuracy | Pending | Pending |
| Relevance | Pending | Pending |
| Clarity | Pending | Pending |
| Missing Data Handling | Pending | Pending |
| JSON Format | Pending | Pending |
| **Total** | Pending | Pending |

## 6. Conclusion

The two prompt versions will be tested using the same 10 questions.

The evaluation scores and actual responses will be recorded after testing.

The prompt with the better overall performance will be selected for GATENavigator.
