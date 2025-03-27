NEXT_QUESTION_PROMPT="You're a helpful assistant! Your task is to suggest the next question that user might ask. 
Here is the conversation history
---------------------
{conversation}
---------------------
Given the conversation history, please give me 3 questions that user might ask next!
Your answer should be wrapped in three sticks which follows the following format:
```
<question 1>
<question 2>
<question 3>
```"

# The system prompt for the AI model.
SYSTEM_PROMPT="You are a helpful assistant who helps users with their questions.
You have access to a knowledge base including the facts that you should start with to find the answer for the user question. Use the query engine tool to retrieve the facts from the knowledge base."

