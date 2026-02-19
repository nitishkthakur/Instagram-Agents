"""
LangGraph Workflow for Instagram Post Creation
Orchestrates the Researcher, Drafter, and Editor agents.
"""

import logging
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages


class WorkflowState(TypedDict):
    """State for the Instagram post creation workflow."""
    topic: str
    research_data: Dict[str, Any]
    post_data: Dict[str, Any]
    review_decision: Dict[str, Any]
    iteration: int
    max_iterations: int
    messages: Annotated[list, add_messages]
    final_post: Dict[str, Any]


class InstagramWorkflow:
    """LangGraph workflow for creating Instagram posts."""
    
    def __init__(self, researcher_agent, drafter_agent, editor_agent, max_iterations: int = 10):
        """
        Initialize the workflow.
        
        Args:
            researcher_agent: Instance of ResearcherAgent
            drafter_agent: Instance of DrafterAgent
            editor_agent: Instance of EditorInChiefAgent
            max_iterations: Maximum number of iteration cycles
        """
        self.researcher = researcher_agent
        self.drafter = drafter_agent
        self.editor = editor_agent
        self.max_iterations = max_iterations
        self.logger = logging.getLogger(__name__)
        
        # Build the workflow graph
        self.workflow = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        # Create the graph
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("research", self.research_node)
        workflow.add_node("draft", self.draft_node)
        workflow.add_node("review", self.review_node)
        workflow.add_node("revise", self.revise_node)
        workflow.add_node("finalize", self.finalize_node)
        
        # Set entry point
        workflow.set_entry_point("research")
        
        # Add edges
        workflow.add_edge("research", "draft")
        workflow.add_edge("draft", "review")
        workflow.add_conditional_edges(
            "review",
            self.review_decision_router,
            {
                "approved": "finalize",
                "revise": "revise",
                "max_iterations": "finalize"
            }
        )
        workflow.add_edge("revise", "review")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    def research_node(self, state: WorkflowState) -> WorkflowState:
        """Node for conducting research."""
        self.logger.info(f"=== RESEARCH NODE (Iteration {state.get('iteration', 0)}) ===")
        
        topic = state["topic"]
        research_data = self.researcher.research(topic)
        
        state["research_data"] = research_data
        state["messages"].append({
            "role": "system",
            "content": f"Research completed for topic: {topic}"
        })
        
        return state
    
    def draft_node(self, state: WorkflowState) -> WorkflowState:
        """Node for drafting the Instagram post."""
        self.logger.info(f"=== DRAFT NODE (Iteration {state.get('iteration', 0)}) ===")
        
        research_data = state["research_data"]
        post_data = self.drafter.draft_post(research_data)
        
        state["post_data"] = post_data
        state["messages"].append({
            "role": "system",
            "content": f"Draft completed with {post_data.get('slide_count', 0)} slides"
        })
        
        return state
    
    def review_node(self, state: WorkflowState) -> WorkflowState:
        """Node for reviewing the post."""
        iteration = state.get("iteration", 0)
        self.logger.info(f"=== REVIEW NODE (Iteration {iteration}) ===")
        
        post_data = state["post_data"]
        research_data = state["research_data"]
        
        review_decision = self.editor.review_post(post_data, research_data)
        
        state["review_decision"] = review_decision
        state["iteration"] = iteration + 1
        state["messages"].append({
            "role": "system",
            "content": f"Review completed. Decision: {review_decision.get('decision')}"
        })
        
        return state
    
    def revise_node(self, state: WorkflowState) -> WorkflowState:
        """Node for revising based on editor feedback."""
        self.logger.info(f"=== REVISE NODE (Iteration {state.get('iteration', 0)}) ===")
        
        review_decision = state["review_decision"]
        research_data = state["research_data"]
        post_data = state["post_data"]
        topic = state["topic"]
        
        # Execute the revision action
        updated_research, updated_post = self.editor.execute_action(
            review_decision, research_data, post_data, topic
        )
        
        state["research_data"] = updated_research
        state["post_data"] = updated_post
        state["messages"].append({
            "role": "system",
            "content": f"Revision completed based on: {review_decision.get('decision')}"
        })
        
        return state
    
    def finalize_node(self, state: WorkflowState) -> WorkflowState:
        """Node for finalizing the post."""
        self.logger.info("=== FINALIZE NODE ===")
        
        state["final_post"] = state["post_data"]
        state["messages"].append({
            "role": "system",
            "content": "Post finalized and ready for publication"
        })
        
        return state
    
    def review_decision_router(self, state: WorkflowState) -> str:
        """Route based on review decision."""
        review_decision = state.get("review_decision", {})
        decision = review_decision.get("decision", "revise_draft")
        iteration = state.get("iteration", 0)
        max_iterations = state.get("max_iterations", self.max_iterations)
        
        # Check if max iterations reached
        if iteration >= max_iterations:
            self.logger.warning(f"Max iterations ({max_iterations}) reached. Finalizing post.")
            return "max_iterations"
        
        # Route based on decision
        if decision == "approve":
            return "approved"
        else:
            return "revise"
    
    def run(self, topic: str) -> Dict[str, Any]:
        """
        Run the workflow for a given topic.
        
        Args:
            topic: The topic to create an Instagram post about
            
        Returns:
            Dictionary containing the final post and workflow metadata
        """
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"Starting Instagram Post Creation Workflow for: {topic}")
        self.logger.info(f"{'='*80}\n")
        
        # Initialize state
        initial_state = {
            "topic": topic,
            "research_data": {},
            "post_data": {},
            "review_decision": {},
            "iteration": 0,
            "max_iterations": self.max_iterations,
            "messages": [],
            "final_post": {}
        }
        
        # Run the workflow
        final_state = self.workflow.invoke(initial_state)
        
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"Workflow completed after {final_state.get('iteration', 0)} iterations")
        self.logger.info(f"{'='*80}\n")
        
        return {
            "final_post": final_state.get("final_post", {}),
            "iterations": final_state.get("iteration", 0),
            "research_data": final_state.get("research_data", {}),
            "messages": final_state.get("messages", [])
        }
