"""
Drafter Agent for Instagram Post Creation
Creates Instagram carousel posts with proper layout and formatting.
"""

import json
import logging
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, SystemMessage


class DrafterAgent:
    """Agent responsible for drafting Instagram carousel posts."""
    
    def __init__(self, config: Dict[str, Any], llm):
        """
        Initialize the Drafter Agent.
        
        Args:
            config: Configuration dictionary for the drafter
            llm: Language model instance
        """
        self.config = config
        self.llm = llm
        self.max_slides = config.get("max_slides", 10)
        self.instructions = config.get("instructions", "")
        self.logger = logging.getLogger(__name__)
        
    def draft_post(self, research_data: Dict[str, Any], revision_feedback: str = None) -> Dict[str, Any]:
        """
        Draft an Instagram carousel post based on research data.
        
        Args:
            research_data: Research content to base the post on
            revision_feedback: Optional feedback for revisions
            
        Returns:
            Dictionary containing the drafted post with slides
        """
        self.logger.info(f"Drafting Instagram post for topic: {research_data.get('topic', 'Unknown')}")
        
        system_message = SystemMessage(content=self.instructions)
        
        revision_note = ""
        if revision_feedback:
            revision_note = f"\n\n**IMPORTANT REVISION FEEDBACK:**\n{revision_feedback}\n\nPlease address this feedback in your revised draft."
        
        human_message = HumanMessage(
            content=f"""Create an engaging Instagram carousel post (maximum {self.max_slides} slides) based on the following research.

Topic: {research_data.get('topic', 'N/A')}

Research Content:
{research_data.get('research_content', 'N/A')}
{revision_note}

Requirements:
1. Maximum {self.max_slides} slides
2. Start with a clear definition with key terms in **bold**
3. Provide genuine value to data science professionals with 2-3 years of experience
4. Include intermediate to advanced concepts (not just beginner content)
5. Use practical examples and simple formulas where appropriate
6. Be concise and avoid filler content
7. Each slide must have a clear purpose
8. Include @learningalgorithm on each slide
9. End with an engaging call-to-action

Format your response as a valid JSON object with this structure:
{{
  "slides": [
    {{
      "page_number": 1,
      "title": "Title of the slide",
      "content": "Main content of the slide",
      "layout": "Description of visual layout"
    }}
  ]
}}

Ensure the JSON is valid and complete."""
        )
        
        messages = [system_message, human_message]
        response = self.llm.invoke(messages)
        
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        # Parse the JSON response
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in response_content:
                json_start = response_content.find("```json") + 7
                json_end = response_content.find("```", json_start)
                json_str = response_content[json_start:json_end].strip()
            elif "```" in response_content:
                json_start = response_content.find("```") + 3
                json_end = response_content.find("```", json_start)
                json_str = response_content[json_start:json_end].strip()
            else:
                json_str = response_content.strip()
            
            post_data = json.loads(json_str)
            
            # Validate the structure
            if "slides" not in post_data:
                raise ValueError("Response does not contain 'slides' key")
            
            if len(post_data["slides"]) > self.max_slides:
                self.logger.warning(f"Post has {len(post_data['slides'])} slides, truncating to {self.max_slides}")
                post_data["slides"] = post_data["slides"][:self.max_slides]
            
            self.logger.info(f"Successfully drafted post with {len(post_data['slides'])} slides")
            
            return {
                "topic": research_data.get('topic'),
                "post": post_data,
                "slide_count": len(post_data["slides"])
            }
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {str(e)}")
            self.logger.error(f"Response content: {response_content}")
            
            # Return a fallback structure
            return {
                "topic": research_data.get('topic'),
                "post": {
                    "slides": [
                        {
                            "page_number": 1,
                            "title": "Error",
                            "content": f"Failed to generate post. Error: {str(e)}",
                            "layout": "Error message"
                        }
                    ]
                },
                "slide_count": 1,
                "error": str(e)
            }
        except Exception as e:
            self.logger.error(f"Unexpected error during drafting: {str(e)}")
            return {
                "topic": research_data.get('topic'),
                "post": {
                    "slides": [
                        {
                            "page_number": 1,
                            "title": "Error",
                            "content": f"Unexpected error: {str(e)}",
                            "layout": "Error message"
                        }
                    ]
                },
                "slide_count": 1,
                "error": str(e)
            }
    
    def format_post_for_display(self, post_data: Dict[str, Any]) -> str:
        """
        Format the post data for human-readable display.
        
        Args:
            post_data: Dictionary containing the post data
            
        Returns:
            Formatted string representation of the post
        """
        if "post" not in post_data:
            return "No post data available"
        
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"INSTAGRAM POST: {post_data.get('topic', 'Unknown Topic')}")
        output.append(f"Total Slides: {post_data.get('slide_count', 0)}")
        output.append(f"{'='*60}\n")
        
        for slide in post_data["post"].get("slides", []):
            output.append(f"\n--- SLIDE {slide.get('page_number', '?')} ---")
            output.append(f"Title: {slide.get('title', 'N/A')}")
            output.append(f"\nContent:\n{slide.get('content', 'N/A')}")
            output.append(f"\nLayout: {slide.get('layout', 'N/A')}")
            output.append(f"{'-'*60}")
        
        return "\n".join(output)
