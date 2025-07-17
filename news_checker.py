import os
import sys
import logging
from typing import Any, Dict, List
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from ddgs import DDGS
from dotenv import load_dotenv
from crewai.tools import tool

load_dotenv()
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DebugCallbackHandler(BaseCallbackHandler):
    """Custom callback handler to show detailed debugging output."""
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> Any:
        """Called when LLM starts running."""
        purple = "\033[95m"
        bold_purple = "\033[1;95m"
        reset = "\033[0m"
        
        print(f"\n{purple}{'='*60}")
        print(f"🚀 CALLING OPENAI API")
        print(f"{'='*60}{reset}\n")
        
        for i, prompt in enumerate(prompts, 1):
            print(f"{bold_purple}PROMPT {i}:")
            print(f"{prompt}")
            print(f"{reset}")
        
        print(f"{purple}{'='*60}")
        print(f"END OF OPENAI PROMPTS")
        print(f"{'='*60}{reset}\n")

    def on_llm_end(self, response, **kwargs: Any) -> Any:
        """Called when LLM ends running."""
        green = "\033[92m"
        reset = "\033[0m"
        
        print(f"\n{green}✅ OPENAI API RESPONSE RECEIVED{reset}")
        if hasattr(response, 'generations') and response.generations:
            for i, generation in enumerate(response.generations[0], 1):
                print(f"{green}RESPONSE {i}: {generation.text[:200]}...{reset}\n")

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        """Called when tool starts running."""
        blue = "\033[94m"
        reset = "\033[0m"
        
        tool_name = serialized.get("name", "Unknown Tool")
        print(f"\n{blue}🔧 TOOL EXECUTION: {tool_name}")
        print(f"Input: {input_str}{reset}\n")

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """Called when tool ends running."""
        cyan = "\033[96m"
        reset = "\033[0m"
        
        print(f"\n{cyan}🔧 TOOL COMPLETED")
        print(f"Output: {output[:300]}...{reset}\n")

    def on_agent_action(self, action, **kwargs: Any) -> Any:
        """Called when agent takes an action."""
        yellow = "\033[93m"
        reset = "\033[0m"
        
        print(f"\n{yellow}🤖 AGENT ACTION")
        print(f"Tool: {action.tool}")
        print(f"Input: {action.tool_input}")
        print(f"Log: {action.log}{reset}\n")

    def on_agent_finish(self, finish, **kwargs: Any) -> Any:
        """Called when agent finishes."""
        green = "\033[92m"
        reset = "\033[0m"
        
        print(f"\n{green}🎯 AGENT FINISHED")
        print(f"Output: {finish.return_values}{reset}\n")

@tool("DuckDuckGo Search")
def search_tool(query: str):
    """A tool to search DuckDuckGo for recent results.
    It returns a list of dictionaries, each containing the 'title', 'snippet', and 'url' of a search result.
    """
    print(f"\n🔎 Searching DuckDuckGo for: '{query}'\n")
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
        if not results:
            print("\n⚠️ No results found on DuckDuckGo.\n")
            return "No results found."

        print(f"\n✅ Found {len(results)} results on DuckDuckGo:\n")
        for i, r in enumerate(results, 1):
            print(f"  Result {i}:")
            print(f"    Title: {r.get('title')}")
            print(f"    URL: {r.get('href')}")
            print("-" * 25)

        return [{"title": r.get("title", ""), "snippet": r.get("body", ""), "url": r.get("href", "")} for r in results]


def main():
    if "OPENAI_API_KEY" not in os.environ:
        print("Please set the OPENAI_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <topic>", file=sys.stderr)
        sys.exit(1)
    
    topic = " ".join(sys.argv[1:])

    # Create callback handler for debugging
    debug_handler = DebugCallbackHandler()

    # Initialize LLM with callback
    llm = ChatOpenAI(
        model="gpt-4", 
        temperature=0.3,
        callbacks=[debug_handler]
    )

    print(f"\n🚀 STARTING AGENTIC WORKFLOW FOR TOPIC: '{topic}'\n")

    # Define Agents
    print("🤖 Creating SearcherAgent...")
    searcher = Agent(
        role='News Searcher',
        goal=f'Find the top 3 most relevant news articles on "{topic}" from DuckDuckGo.',
        backstory='An expert in using DuckDuckGo to find the most relevant and up-to-date news articles.',
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )

    print("🤖 Creating SummarizerAgent...")
    summarizer = Agent(
        role='News Summarizer',
        goal='Summarize the provided news articles, capturing the main ideas.',
        backstory='A skilled writer who can distill complex news into clear, concise summaries.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    print("🤖 Creating FactCheckerAgent...")
    fact_checker = Agent(
        role='Fact Checker',
        goal='Identify 2-3 factual claims from the summary and verify them using DuckDuckGo searches.',
        backstory='A meticulous fact-checker who verifies information by cross-referencing multiple sources.',
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=llm
    )

    # Define Tasks
    print("\n📋 Creating Tasks...")
    search_task = Task(
        description=f'Search for the top 3 most relevant news articles about "{topic}". Return the titles, snippets, and URLs.',
        agent=searcher,
        expected_output="A list of 3 news articles with their titles, snippets, and URLs."
    )

    summary_task = Task(
        description='Summarize the main ideas from the search results. Focus on the key points and developments.',
        agent=summarizer,
        expected_output="A concise summary of the main ideas from the news articles."
    )

    fact_check_task = Task(
        description='Identify 2-3 specific factual claims from the summary. For each claim, search for verification and mark it as "Supported", "Contradicted", or "Unconfirmed".',
        agent=fact_checker,
        expected_output="A fact-checking report with 2-3 claims, each marked as Supported, Contradicted, or Unconfirmed with brief explanations."
    )

    # Create and run the crew
    print("\n👥 Creating Crew...")
    news_crew = Crew(
        agents=[searcher, summarizer, fact_checker],
        tasks=[search_task, summary_task, fact_check_task],
        process=Process.sequential,
        verbose=True
    )

    print("\n\n" + "="*80)
    print("🚀 KICKING OFF THE CREW WORKFLOW")
    print("="*80 + "\n")
    
    result = news_crew.kickoff()
    
    print("\n" + "="*80)
    print("✅ CREW EXECUTION FINISHED")
    print("="*80 + "\n")

    print("\n\n########################")
    print("## Final Result")
    print("########################")
    print(result)

if __name__ == "__main__":
    main() 