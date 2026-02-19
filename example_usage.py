"""
Example usage of the Instagram Agents workflow.

This script demonstrates how to use the Instagram Agents system.
For actual usage, you need to set up API keys in the .env file.
"""

import os
import sys
from pathlib import Path

# Example 1: Basic usage
print("="*80)
print("EXAMPLE 1: Basic Usage")
print("="*80)
print("""
To run the workflow with the default topic from config.json:

    python main.py

This will:
1. Load configuration from config.json
2. Use the default topic specified in config
3. Run the complete workflow (Research -> Draft -> Review -> Revise if needed)
4. Save the final post to a JSON file
5. Log all steps to instagram_agents.log
""")

# Example 2: Custom topic
print("\n" + "="*80)
print("EXAMPLE 2: Custom Topic")
print("="*80)
print("""
To create a post about a specific topic:

    python main.py --topic "Gradient Boosting Machines"

You can use any data science or machine learning topic:
- "Neural Networks and Backpropagation"
- "Support Vector Machines"
- "K-Means Clustering"
- "Principal Component Analysis"
- "LSTM Networks for Time Series"
""")

# Example 3: Custom configuration
print("\n" + "="*80)
print("EXAMPLE 3: Custom Configuration")
print("="*80)
print("""
To use a custom configuration file:

    python main.py --config my_config.json --topic "Deep Learning"

This is useful when you want to:
- Use different LLM models
- Adjust temperature/creativity
- Change word limits or slide counts
- Modify agent instructions
""")

# Example 4: Specify output file
print("\n" + "="*80)
print("EXAMPLE 4: Specify Output File")
print("="*80)
print("""
To save the output to a specific file:

    python main.py --topic "Transformers" --output my_post.json

The output JSON file will contain:
- Complete post structure
- All slides with titles, content, and layout information
- Metadata (topic, slide count, etc.)
""")

# Example 5: Configuration customization
print("\n" + "="*80)
print("EXAMPLE 5: Configuration Customization")
print("="*80)
print("""
Edit config.json to customize the workflow:

{
  "researcher": {
    "model": "gpt-4o",           // Change to "claude-3-5-sonnet-20241022", "gemini-2.0-flash-exp", etc.
    "temperature": 0.7,          // 0.0 = deterministic, 1.0 = creative
    "word_limit": 2500,         // Target word count for research
    "instructions": "..."        // Custom instructions for researcher
  },
  "drafter": {
    "model": "gpt-4o",
    "temperature": 0.8,         // Higher = more creative posts
    "max_slides": 10,           // Maximum slides (1-10)
    "instructions": "..."       // Custom instructions for drafter
  },
  "editor_in_chief": {
    "model": "gpt-4o",
    "max_iterations": 5,        // Max revisions per cycle
    "instructions": "..."       // Custom instructions for editor
  },
  "general": {
    "default_topic": "Random Forests",
    "log_file": "instagram_agents.log",
    "max_total_iterations": 10  // Total workflow iterations
  }
}
""")

# Example 6: Environment setup
print("\n" + "="*80)
print("EXAMPLE 6: Environment Setup")
print("="*80)
print("""
Required steps before running:

1. Copy .env.example to .env:
   cp .env.example .env

2. Add your API keys to .env:
   
   # Required
   TAVILY_API_KEY=your_tavily_key_here
   
   # At least one LLM provider (depends on model in config.json)
   OPENAI_API_KEY=your_openai_key_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   GOOGLE_API_KEY=your_google_key_here
   XAI_API_KEY=your_xai_key_here

3. Install dependencies:
   pip install -r requirements.txt

4. Run the workflow:
   python main.py --topic "Your Topic"
""")

# Example 7: Output structure
print("\n" + "="*80)
print("EXAMPLE 7: Output Structure")
print("="*80)
print("""
The workflow produces several outputs:

1. JSON file (e.g., instagram_post_random_forests_20240219_123456.json):
   {
     "topic": "Random Forests",
     "post": {
       "slides": [
         {
           "page_number": 1,
           "title": "Random Forests",
           "content": "A **Random Forest** is an ensemble...",
           "layout": "Title at top, definition centered..."
         },
         ...
       ]
     },
     "slide_count": 9
   }

2. Log file (instagram_agents.log):
   - Detailed logs of all workflow steps
   - Research results
   - Draft attempts
   - Editor feedback
   - Revision actions

3. Console output:
   - Formatted display of the final post
   - All slides with titles, content, and layout
   - Workflow statistics (iterations, etc.)
""")

# Example 8: Workflow overview
print("\n" + "="*80)
print("EXAMPLE 8: Workflow Overview")
print("="*80)
print("""
The workflow follows these steps:

1. RESEARCH: Researcher agent searches for information using Tavily
   - Performs advanced web search
   - Synthesizes ~2500 words of content
   - Focuses on intermediate to advanced concepts

2. DRAFT: Drafter agent creates Instagram post
   - Creates up to 10 slides
   - Starts with clear definition (bold key terms)
   - Includes practical examples and formulas
   - Ensures value for 2-3 year experienced data scientists

3. REVIEW: Editor in Chief evaluates the post
   - Checks quality and coherence
   - Ensures intermediate/advanced content
   - Verifies no filler content
   - Makes decision: approve, revise_research, or revise_draft

4. REVISE: If needed, executes the revision
   - revise_research: Researcher gets specific focus areas
   - revise_draft: Drafter gets detailed feedback

5. LOOP: Steps 3-4 repeat until approved or max iterations reached

6. FINALIZE: Post is saved and workflow completes
""")

# Check if API keys are set
print("\n" + "="*80)
print("ENVIRONMENT CHECK")
print("="*80)

# Load .env if exists
from dotenv import load_dotenv
load_dotenv()

api_keys = {
    "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
    "XAI_API_KEY": os.getenv("XAI_API_KEY"),
}

print("\nAPI Key Status:")
for key, value in api_keys.items():
    status = "✅ Set" if value else "❌ Not set"
    print(f"  {key}: {status}")

tavily_set = bool(api_keys["TAVILY_API_KEY"])
llm_set = any([api_keys["OPENAI_API_KEY"], api_keys["ANTHROPIC_API_KEY"], 
               api_keys["GOOGLE_API_KEY"], api_keys["XAI_API_KEY"]])

print("\nReadiness:")
if tavily_set and llm_set:
    print("  ✅ System is ready to run!")
    print("  Run: python main.py --topic 'Your Topic'")
elif not tavily_set:
    print("  ❌ Tavily API key is required")
    print("  Please set TAVILY_API_KEY in .env file")
elif not llm_set:
    print("  ❌ At least one LLM API key is required")
    print("  Please set one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, or XAI_API_KEY")
else:
    print("  ❌ Missing required API keys")
    print("  Please check .env file")

print("\n" + "="*80)
