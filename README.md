# Agentic Fact-Check with CrewAI

This project uses a team of AI assistants built with CrewAI to research, summarize, and fact-check news on any given topic. You can simply provide a topic, and the AI team will deliver a concise, verified summary.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/peterzat/agentic-factcheck-crewai.git
cd agentic-factcheck-crewai
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the example environment file and add your OpenAI API key:
```bash
cp env.example .env
```

Then edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_openai_api_key_here
```

You can get an OpenAI API key from: https://platform.openai.com/api-keys

## How It Works: A Team of Digital Assistants

Imagine you have a team of three expert assistants working for you. Each has a specific job, and they work together to give you the best possible information. That's how this project works, using AI "agents" to handle each step of the process.

### 1. The News Scout (SearcherAgent)

This is your expert researcher. When you provide a topic, the News Scout immediately gets to work, searching the web to find the most relevant and up-to-date news articles. It's like a librarian who knows exactly where to find the right books for you in seconds.

### 2. The Summarizer (SummarizerAgent)

Once the News Scout has found the articles, the Summarizer takes over. This agent reads through all the information and creates a clear, concise summary of the main points. Think of it as having a skilled editor who can take complex news stories and turn them into an easy-to-understand overview.

### 3. The Fact-Checker (FactCheckerAgent)

The most important member of the team! The Fact-Checker takes the summary and identifies specific claims that need verification. It then conducts additional searches to check whether each claim is supported by evidence, contradicted, or simply unconfirmed. This agent acts like an investigative journalist, making sure the information is reliable.

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

Or use the convenient bash script:

```bash
./fact-check.sh "your topic here"
```

## Example Usage

```bash
./fact-check.sh "latest developments in renewable energy"
```

This will return a comprehensive report with:
- Top 3 relevant news articles
- A clear summary of the main developments
- Fact-checking analysis of key claims

## What Makes This Special?

**Transparency**: You can see exactly what each agent is doing and how they reach their conclusions.

**Verification**: Unlike simple news aggregators, this system actively fact-checks the information it provides.

**Comprehensive**: You get both the big picture (summary) and the details (original articles and fact-checks).

**Easy to Use**: Just provide a topic, and the AI team does the rest. 