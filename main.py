"""
Main entry point for the Instagram Agents workflow.
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from langchain_core.language_models import init_chat_model

from src.utils import setup_logging, load_config, save_final_post, format_post_for_display
from src.researcher_agent import ResearcherAgent
from src.drafter_agent import DrafterAgent
from src.editor_agent import EditorInChiefAgent
from src.workflow import InstagramWorkflow


def initialize_llm(model_name: str, **kwargs):
    """
    Initialize a language model using init_chat_model.
    
    Args:
        model_name: Name of the model (e.g., 'gpt-4o', 'claude-3-5-sonnet-20241022', 'gemini-2.0-flash-exp')
        **kwargs: Additional parameters like temperature, max_tokens, etc.
        
    Returns:
        Initialized language model
    """
    try:
        # Extract parameters
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_output_tokens', kwargs.get('max_tokens', 4000))
        
        # Initialize the model
        llm = init_chat_model(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            model_kwargs=kwargs
        )
        
        return llm
        
    except Exception as e:
        print(f"Error initializing model {model_name}: {str(e)}")
        raise


def main():
    """Main function to run the Instagram Agents workflow."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Instagram Post Creation Workflow")
    parser.add_argument(
        "--topic",
        type=str,
        help="Topic for the Instagram post"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to configuration file (default: config.json)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path for the final post (optional)"
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Check for required API keys
    required_keys = ["TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"Error: Missing required API keys: {', '.join(missing_keys)}")
        print("Please set these in your .env file or environment variables.")
        sys.exit(1)
    
    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        sys.exit(1)
    
    # Setup logging
    log_file = config.get("general", {}).get("log_file", "instagram_agents.log")
    logger = setup_logging(log_file)
    
    logger.info("="*80)
    logger.info("Instagram Agents Workflow Starting")
    logger.info("="*80)
    
    # Get topic
    topic = args.topic or config.get("general", {}).get("default_topic")
    if not topic:
        logger.error("No topic provided. Use --topic or set default_topic in config.json")
        sys.exit(1)
    
    logger.info(f"Topic: {topic}")
    
    try:
        # Initialize language models for each agent
        logger.info("Initializing language models...")
        
        researcher_config = config.get("researcher", {})
        researcher_llm = initialize_llm(
            researcher_config.get("model", "gpt-4o"),
            temperature=researcher_config.get("temperature", 0.7),
            max_output_tokens=researcher_config.get("max_output_tokens", 4000)
        )
        
        drafter_config = config.get("drafter", {})
        drafter_llm = initialize_llm(
            drafter_config.get("model", "gpt-4o"),
            temperature=drafter_config.get("temperature", 0.8),
            max_output_tokens=drafter_config.get("max_output_tokens", 3000)
        )
        
        editor_config = config.get("editor_in_chief", {})
        editor_llm = initialize_llm(
            editor_config.get("model", "gpt-4o"),
            temperature=editor_config.get("temperature", 0.7),
            max_output_tokens=editor_config.get("max_output_tokens", 4000)
        )
        
        logger.info("Language models initialized successfully")
        
        # Initialize agents
        logger.info("Initializing agents...")
        
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        researcher = ResearcherAgent(researcher_config, researcher_llm, tavily_api_key)
        drafter = DrafterAgent(drafter_config, drafter_llm)
        editor = EditorInChiefAgent(editor_config, editor_llm, researcher, drafter)
        
        logger.info("Agents initialized successfully")
        
        # Initialize and run workflow
        logger.info("Initializing workflow...")
        
        max_iterations = config.get("general", {}).get("max_total_iterations", 10)
        workflow = InstagramWorkflow(researcher, drafter, editor, max_iterations)
        
        logger.info("Starting workflow execution...")
        result = workflow.run(topic)
        
        # Display final post
        final_post = result.get("final_post", {})
        print("\n" + format_post_for_display(final_post))
        
        # Save final post
        output_file = args.output
        saved_file = save_final_post(final_post, output_file)
        
        logger.info(f"Workflow completed successfully in {result.get('iterations', 0)} iterations")
        logger.info(f"Final post saved to: {saved_file}")
        
        print(f"\n✅ Workflow completed successfully!")
        print(f"📄 Final post saved to: {saved_file}")
        print(f"📊 Total iterations: {result.get('iterations', 0)}")
        print(f"📝 Log file: {log_file}")
        
    except Exception as e:
        logger.error(f"Error during workflow execution: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
