# GATENavigator – Prompt Comparison

## 1. Objective

The objective is to compare two prompt versions and evaluate which one produces better responses for GATENavigator.

Both prompts were tested using the 10 questions stored in `Data/user_questions.md`.

A total of 20 API requests were made: 10 using Version 1 and 10 using Version 2.

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

Both prompt versions were evaluated using the following criteria:

| Criteria | Description |
|---|---|
| Accuracy | Is the answer correct? |
| Relevance | Does it answer the question? |
| Clarity | Is the response easy to understand? |
| Missing Data Handling | Does it avoid inventing unavailable information? |
| JSON Format | Does it follow the required JSON response structure? |

## 4. Automated Evaluation Results

Both versions were tested using the same 10 questions.

| Question | Version 1 | Version 2 |
|---|---|---|
| Q1 – Available GATE papers | Success | Success |
| Q2 – CS paper code | Success | Failed (HTTP 500) |
| Q3 – Marks allocation | Success | Success |
| Q4 – CS paper details | Success | Success |
| Q5 – DA syllabus URL | Success | Success |
| Q6 – Official cutoff score | Success | Success |
| Q7 – AE paper details | Success | Success |
| Q8 – Total stored papers | Success | Success |
| Q9 – EC paper code | Success | Success |
| Q10 – AE syllabus URL | Success | Success |

### Evaluation Summary

| Metric | Version 1 | Version 2 |
|---|---:|---:|
| Total requests | 10 | 10 |
| Successful requests | 10 | 9 |
| Failed requests | 0 | 1 |
| Success rate | 100% | 90% |

### Important Observations

**Version 1:**

- Returned useful and detailed answers.
- Often included additional information such as syllabus URLs.
- All returned confidence values were 0.5.
- The API fallback handling assigns this default confidence when the model response cannot be parsed as JSON.

**Version 2:**

- Generally returned concise and structured answers.
- Followed the JSON response requirement.
- Correctly identified unavailable cutoff information in Q6.
- Q2 encountered an HTTP 500 server error and needs further investigation.

**Question-specific observations:**

- Q1: Both versions listed the available papers. Version 1 also included syllabus URLs.
- Q2: Version 1 correctly returned CS and its syllabus URL. Version 2 failed.
- Q3: Both versions returned the 15 + 85 marks allocation.
- Q4: Both versions returned CS paper details and acknowledged that syllabus sections were not available.
- Q5: Both versions returned the DA syllabus URL.
- Q6: Both versions correctly stated that the official cutoff score was unavailable in the supplied data.
- Q7: Both versions identified AE as Aerospace Engineering.
- Q8: Both versions returned 28 stored papers.
- Q9: Both versions identified EC as the paper code.
- Q10: Both versions returned the Aerospace Engineering syllabus URL.

## 5. Evaluation Score

Each criterion is scored from 1 to 5.

- 1 = Poor
- 2 = Below Average
- 3 = Average
- 4 = Good
- 5 = Excellent

The following are provisional qualitative scores based on the observed responses and prompt requirements.

| Evaluation Criteria | Version 1 | Version 2 |
|---|---:|---:|
| Accuracy | 5 | 4 |
| Relevance | 5 | 4 |
| Clarity | 4 | 5 |
| Missing Data Handling | 5 | 5 |
| JSON Format Compliance | 2 | 5 |
| **Total** | **21/25** | **23/25** |

Note: These scores are qualitative project evaluation scores, not statistically measured accuracy. Version 2's Q2 failure is included in its assessment. Version 1's API-generated fallback JSON should not be confused with native JSON compliance by the model.

## 6. Conclusion

Both prompt versions produced useful responses for GATENavigator.

Version 1 provided more detailed answers and additional syllabus links. However, it does not explicitly require the model to return structured JSON.

Version 2 provides a clearer structure, follows the JSON response requirement, and handles unavailable information appropriately.

Although Version 2 encountered one API error during automated evaluation, it achieved the higher provisional evaluation score.

**Final Selection: Version 2 – Improved Prompt**

Version 2 will be used as the primary system prompt for GATENavigator. The Q2 API error remains a known issue and should be investigated separately.

## 7. Additional Manual Prompt Comparison

Question: What is the paper code and syllabus URL for Computer Science?

Task: syllabus

**Version 1: Basic Prompt**

- Paper code: CS
- Paper name: Computer Science & Information Technology
- Syllabus URL: Correctly provided
- Confidence: 0.99
- JSON response: Valid

**Version 2: Improved Prompt**

- Paper code: CS
- Paper name: Computer Science & Information Technology
- Syllabus URL: Not included in the answer
- Confidence: 1.0
- JSON response: Valid

**Observation:**

Both versions correctly identified the Computer Science paper code.

Version 1 included the syllabus URL, while Version 2 provided a shorter response.

Version 1 was more informative for this particular question.

This manual test demonstrates that answer detail can vary even when both prompts return correct information.