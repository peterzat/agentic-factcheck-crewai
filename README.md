# Agentic Fact-Check with CrewAI

This project uses a team of AI assistants built with CrewAI to research, summarize, and fact-check news on any given topic. You can simply provide a topic, and the AI team will deliver a concise, verified summary.

## How It Works: A Team of Digital Assistants

Imagine you have a team of three expert assistants working for you. Each has a specific job, and they work together to give you the best possible information. That's how this project works, using AI "agents" to handle each step of the process.

### 1. The News Scout (SearcherAgent)

This is your expert researcher. When you provide a topic, the News Scout immediately gets to work, searching the web to find the most relevant and up-to-date news articles. It's like a librarian who knows exactly where to find the right books for you in seconds.

### 2. The Summarizer (SummarizerAgent)

Once the News Scout has found the articles, the Summarizer takes over. This agent reads through all the information and writes a short, easy-to-understand summary. It captures the main ideas and key points, so you don't have to read through pages of text. Think of it as a student who reads a long chapter and gives you the cliff notes.

### 3. The Fact-Checker (FactCheckerAgent)

After the summary is written, the Fact-Checker steps in. This is your meticulous detective. It carefully reviews the summary, identifies the key factual claims, and then does its own research to verify them. It will tell you if a claim is supported by the facts, contradicted, or if there isn't enough information to be sure.

## The Workflow in Action

The entire process is a simple, automated workflow:

1.  **You provide a topic** (e.g., "latest advancements in solar power").
2.  **The News Scout** finds the top 3 news articles on that topic.
3.  **The Summarizer** reads the articles and creates a summary.
4.  **The Fact-Checker** verifies the claims in the summary.
5.  **You get a final report** with a concise summary and a fact-checking analysis.

## How to Run It

To run this project, first activate the virtual environment:
```bash
source .venv/bin/activate
```

Then, run the script with your topic in quotes:

```bash
python news_checker.py "your topic here"
``` 