"""
Editor in Chief Agent - ReAct Agent
Reviews posts and provides feedback, can invoke researcher and drafter as subagents.
"""

import json
import logging
from typing import Dict, Any, List, Tuple
from langchain_core.messages import HumanMessage, SystemMessage


class EditorInChiefAgent:
    """ReAct agent that reviews posts and provides feedback."""
    
    def __init__(self, config: Dict[str, Any], llm, researcher_agent, drafter_agent):
        """
        Initialize the Editor in Chief Agent.
        
        Args:
            config: Configuration dictionary for the editor
            llm: Language model instance
            researcher_agent: Instance of ResearcherAgent
            drafter_agent: Instance of DrafterAgent
        """
        self.config = config
        self.llm = llm
        self.researcher_agent = researcher_agent
        self.drafter_agent = drafter_agent
        self.max_iterations = config.get("max_iterations", 5)
        self.instructions = config.get("instructions", "")
        self.logger = logging.getLogger(__name__)
        
    def review_post(self, post_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review a drafted post and decide on actions.
        
        Args:
            post_data: The drafted post to review
            research_data: The original research data
            
        Returns:
            Dictionary containing review decision and feedback
        """
        self.logger.info("Editor reviewing post...")
        
        # Format post for review
        post_text = self.drafter_agent.format_post_for_display(post_data)
        
        system_message = SystemMessage(content=self.instructions)
        
        human_message = HumanMessage(
            content=f"""Review the following Instagram post draft for quality and coherence.

Topic: {post_data.get('topic', 'Unknown')}

Research Summary (first 500 chars):
{research_data.get('research_content', 'N/A')[:500]}...

Post to Review:
{post_text}

Evaluate the post based on:
1. Quality: Is the content valuable for data science professionals with 2-3 years experience?
2. Depth: Does it include intermediate or advanced elements (not just beginner content)?
3. Coherence: Do all slides work together to communicate a unified message?
4. Value: Is there genuine value with no filler content?
5. Structure: Does it start with a clear definition and build logically?

Provide your response in the following JSON format:
{{
  "decision": "approve" or "revise_research" or "revise_draft",
  "feedback": "Detailed feedback explaining your decision",
  "specific_issues": ["List of specific issues if revisions needed"],
  "suggestions": ["Specific suggestions for improvement"]
}}

If you decide "revise_research", include what additional information is needed.
If you decide "revise_draft", include specific content improvements needed.
Only "approve" if the post meets premium quality standards."""
        )
        
        messages = [system_message, human_message]
        response = self.llm.invoke(messages)
        
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        # Parse the JSON response
        try:
            # Extract JSON from markdown code blocks if present
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
            
            review_result = json.loads(json_str)
            
            # Validate decision
            valid_decisions = ["approve", "revise_research", "revise_draft"]
            if review_result.get("decision") not in valid_decisions:
                self.logger.warning(f"Invalid decision: {review_result.get('decision')}, defaulting to revise_draft")
                review_result["decision"] = "revise_draft"
            
            self.logger.info(f"Review decision: {review_result.get('decision')}")
            
            return review_result
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse review response: {str(e)}")
            # Default to requesting revision
            return {
                "decision": "revise_draft",
                "feedback": "Failed to parse review. Please improve the post quality.",
                "specific_issues": ["Review parsing error"],
                "suggestions": ["Ensure content meets quality standards"]
            }
        except Exception as e:
            self.logger.error(f"Unexpected error during review: {str(e)}")
            return {
                "decision": "revise_draft",
                "feedback": f"Error during review: {str(e)}",
                "specific_issues": [str(e)],
                "suggestions": []
            }
    
    def execute_action(self, review_decision: Dict[str, Any], research_data: Dict[str, Any], 
                      post_data: Dict[str, Any], topic: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Execute the action based on review decision.
        
        Args:
            review_decision: The review decision and feedback
            research_data: Current research data
            post_data: Current post data
            topic: The topic being covered
            
        Returns:
            Tuple of (updated_research_data, updated_post_data)
        """
        decision = review_decision.get("decision")
        feedback = review_decision.get("feedback", "")
        suggestions = review_decision.get("suggestions", [])
        
        if decision == "approve":
            self.logger.info("Post approved by editor!")
            return research_data, post_data
        
        elif decision == "revise_research":
            self.logger.info("Editor requesting research revision...")
            # Extract focus areas from feedback
            focus_areas = " ".join(suggestions) if suggestions else feedback
            
            # Request additional research
            updated_research = self.researcher_agent.research(topic, focus_areas=focus_areas)
            
            # Re-draft with updated research
            updated_post = self.drafter_agent.draft_post(updated_research)
            
            return updated_research, updated_post
        
        elif decision == "revise_draft":
            self.logger.info("Editor requesting draft revision...")
            # Create revision feedback
            revision_feedback = f"{feedback}\n\nSpecific suggestions:\n" + "\n".join(f"- {s}" for s in suggestions)
            
            # Re-draft with feedback
            updated_post = self.drafter_agent.draft_post(research_data, revision_feedback=revision_feedback)
            
            return research_data, updated_post
        
        else:
            self.logger.warning(f"Unknown decision: {decision}, no action taken")
            return research_data, post_data
