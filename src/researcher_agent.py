"""
Researcher Agent for Instagram Post Creation
Uses Tavily API to search and gather information on a given topic.
"""

import json
import logging
from typing import Dict, Any
from tavily import TavilyClient
from langchain_core.messages import HumanMessage, SystemMessage


class ResearcherAgent:
    """Agent responsible for researching topics using Tavily search API."""
    
    def __init__(self, config: Dict[str, Any], llm, tavily_api_key: str):
        """
        Initialize the Researcher Agent.
        
        Args:
            config: Configuration dictionary for the researcher
            llm: Language model instance
            tavily_api_key: API key for Tavily search
        """
        self.config = config
        self.llm = llm
        self.tavily_client = TavilyClient(api_key=tavily_api_key)
        self.word_limit = config.get("word_limit", 2500)
        self.instructions = config.get("instructions", "")
        self.logger = logging.getLogger(__name__)
        
    def search_topic(self, topic: str, focus_areas: str = None) -> str:
        """
        Search for information on a topic using Tavily.
        
        Args:
            topic: The main topic to research
            focus_areas: Optional specific areas to focus on
            
        Returns:
            Search results as a formatted string
        """
        try:
            query = topic
            if focus_areas:
                query = f"{topic} {focus_areas}"
            
            self.logger.info(f"Searching for: {query}")
            
            # Perform comprehensive search
            search_results = self.tavily_client.search(
                query=query,
                search_depth="advanced",
                max_results=10
            )
            
            # Format search results
            formatted_results = []
            for result in search_results.get('results', []):
                formatted_results.append(f"Title: {result.get('title', 'N/A')}\n"
                                       f"Content: {result.get('content', 'N/A')}\n"
                                       f"URL: {result.get('url', 'N/A')}\n")
            
            return "\n---\n".join(formatted_results)
        
        except Exception as e:
            self.logger.error(f"Error during Tavily search: {str(e)}")
            return f"Search error: {str(e)}"
    
    def research(self, topic: str, focus_areas: str = None) -> Dict[str, Any]:
        """
        Conduct research on a topic and synthesize information.
        
        Args:
            topic: The topic to research
            focus_areas: Optional specific areas to focus on
            
        Returns:
            Dictionary containing research results
        """
        self.logger.info(f"Starting research on: {topic}")
        
        # Search for information
        search_results = self.search_topic(topic, focus_areas)
        
        # Create prompt for LLM to synthesize research
        system_message = SystemMessage(content=self.instructions)
        
        focus_instruction = ""
        if focus_areas:
            focus_instruction = f"\n\nPlease pay special attention to: {focus_areas}"
        
        human_message = HumanMessage(
            content=f"""Based on the following search results, create comprehensive research content about "{topic}".
            
Your research should be approximately {self.word_limit} words and cover:
1. Core concepts and definitions
2. Technical details and mechanisms
3. Practical applications and use cases
4. Best practices and common pitfalls
5. Advanced considerations for intermediate users
{focus_instruction}

Search Results:
{search_results}

Provide well-structured, informative content that will serve as the foundation for an Instagram educational post."""
        )
        
        # Get LLM response
        messages = [system_message, human_message]
        response = self.llm.invoke(messages)
        
        research_content = response.content if hasattr(response, 'content') else str(response)
        
        self.logger.info(f"Research completed. Length: {len(research_content.split())} words")
        
        return {
            "topic": topic,
            "research_content": research_content,
            "focus_areas": focus_areas,
            "word_count": len(research_content.split())
        }
