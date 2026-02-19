"""
Utility functions for the Instagram Agents workflow.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any


def setup_logging(log_file: str = "instagram_agents.log", log_level: int = logging.INFO):
    """
    Set up logging configuration.
    
    Args:
        log_file: Path to the log file
        log_level: Logging level
    """
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger


def log_workflow_state(state: Dict[str, Any], phase: str, log_file: str):
    """
    Log the current workflow state to a file.
    
    Args:
        state: Current workflow state
        phase: Current phase of the workflow
        log_file: Path to the log file
    """
    logger = logging.getLogger(__name__)
    
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "iteration": state.get("iteration", 0),
            "topic": state.get("topic", "N/A")
        }
        
        if phase == "research":
            log_entry["research_word_count"] = state.get("research_data", {}).get("word_count", 0)
        elif phase == "draft":
            log_entry["slide_count"] = state.get("post_data", {}).get("slide_count", 0)
        elif phase == "review":
            log_entry["decision"] = state.get("review_decision", {}).get("decision", "N/A")
            log_entry["feedback"] = state.get("review_decision", {}).get("feedback", "N/A")
        
        logger.info(f"{phase.upper()}: {json.dumps(log_entry, indent=2)}")
        
    except Exception as e:
        logger.error(f"Error logging workflow state: {str(e)}")


def save_final_post(post_data: Dict[str, Any], output_file: str = None):
    """
    Save the final post to a JSON file.
    
    Args:
        post_data: The final post data
        output_file: Optional output file path
    """
    logger = logging.getLogger(__name__)
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic = post_data.get("topic", "unknown").replace(" ", "_").lower()
        output_file = f"instagram_post_{topic}_{timestamp}.json"
    
    try:
        with open(output_file, 'w') as f:
            json.dump(post_data, f, indent=2)
        
        logger.info(f"Final post saved to: {output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"Error saving final post: {str(e)}")
        return None


def format_post_for_display(post_data: Dict[str, Any]) -> str:
    """
    Format post data for console display.
    
    Args:
        post_data: Post data to format
        
    Returns:
        Formatted string
    """
    if not post_data or "post" not in post_data:
        return "No post data available"
    
    lines = []
    lines.append("\n" + "="*80)
    lines.append(f"INSTAGRAM POST: {post_data.get('topic', 'Unknown')}")
    lines.append(f"Total Slides: {post_data.get('slide_count', 0)}")
    lines.append("="*80 + "\n")
    
    for slide in post_data["post"].get("slides", []):
        lines.append(f"\n{'─'*80}")
        lines.append(f"📄 SLIDE {slide.get('page_number', '?')}")
        lines.append(f"{'─'*80}")
        lines.append(f"\n🏷️  TITLE: {slide.get('title', 'N/A')}\n")
        lines.append(f"📝 CONTENT:\n{slide.get('content', 'N/A')}\n")
        lines.append(f"🎨 LAYOUT: {slide.get('layout', 'N/A')}")
        lines.append(f"{'─'*80}")
    
    return "\n".join(lines)


def load_config(config_file: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from JSON file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file: {str(e)}")
