# Instagram-Agents

An intelligent agentic workflow for creating high-quality Instagram carousel posts using LangGraph. This system employs three specialized AI agents that work together to research, draft, and refine educational content for data science professionals.

## Features

- 🔍 **Researcher Agent**: Uses Tavily Search API to gather comprehensive information on any topic
- ✍️ **Drafter Agent**: Creates engaging Instagram carousel posts (up to 10 slides) with proper layout
- 👔 **Editor in Chief Agent**: ReAct agent that reviews and provides feedback, can invoke subagents for revisions
- ⚙️ **Fully Configurable**: All agent instructions, models, and parameters configurable via `config.json`
- 📊 **Comprehensive Logging**: All intermediate outputs logged for transparency
- 🤖 **Multi-Model Support**: Compatible with OpenAI, Anthropic, Google Gemini, and xAI Grok models

## Architecture

The workflow uses LangGraph to orchestrate three agents in an iterative feedback loop:

```
┌─────────────┐     ┌─────────┐     ┌────────┐
│ Researcher  │────▶│ Drafter │────▶│ Editor │
│   Agent     │     │  Agent  │     │  Agent │
└─────────────┘     └─────────┘     └────┬───┘
      ▲                  ▲                │
      │                  │                │
      └──────────────────┴────────────────┘
           (Revision Loop)
```

The Editor can request:
- **Research revisions**: When more/better information is needed
- **Draft revisions**: When content needs improvement
- **Approval**: When quality standards are met

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nitishkthakur/Instagram-Agents.git
cd Instagram-Agents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required API keys:
- `TAVILY_API_KEY`: For web search (required)
- At least one LLM provider key:
  - `OPENAI_API_KEY`: For OpenAI models (GPT-4, etc.)
  - `ANTHROPIC_API_KEY`: For Anthropic models (Claude)
  - `GOOGLE_API_KEY`: For Google Gemini models
  - `XAI_API_KEY`: For xAI Grok models

## Configuration

Edit `config.json` to customize the workflow:

### Agent Configuration

Each agent has the following configurable parameters:

```json
{
  "researcher": {
    "model": "gpt-4o",              // LLM model to use
    "max_output_tokens": 4000,      // Maximum output tokens
    "temperature": 0.7,             // Creativity level (0-1)
    "word_limit": 2500,            // Target word count for research
    "instructions": "..."           // System prompt for the agent
  },
  "drafter": {
    "model": "gpt-4o",
    "max_output_tokens": 3000,
    "temperature": 0.8,
    "max_slides": 10,              // Maximum slides per post
    "instructions": "..."
  },
  "editor_in_chief": {
    "model": "gpt-4o",
    "max_output_tokens": 4000,
    "temperature": 0.7,
    "max_iterations": 5,           // Max iterations per review cycle
    "instructions": "..."
  },
  "general": {
    "default_topic": "Random Forests in Machine Learning",
    "log_file": "instagram_agents.log",
    "max_total_iterations": 10     // Max total workflow iterations
  }
}
```

### Supported Models

You can use any model supported by LangChain's `init_chat_model`:

- **OpenAI**: `gpt-4o`, `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`
- **Anthropic**: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`, `claude-3-sonnet-20240229`
- **Google**: `gemini-2.0-flash-exp`, `gemini-1.5-pro`, `gemini-1.5-flash`
- **xAI**: `grok-beta`

## Usage

### Basic Usage

Run with default topic from config:
```bash
python main.py
```

### Specify a Topic

```bash
python main.py --topic "Gradient Boosting Machines"
```

### Custom Configuration

```bash
python main.py --config my_config.json --topic "Neural Networks"
```

### Specify Output File

```bash
python main.py --topic "Deep Learning" --output my_post.json
```

## Output

The workflow generates:

1. **JSON file**: Complete post structure with all slides
2. **Log file**: Detailed logs of all intermediate steps
3. **Console output**: Formatted display of the final post

### Example Output Structure

```json
{
  "topic": "Random Forests",
  "post": {
    "slides": [
      {
        "page_number": 1,
        "title": "Random Forests",
        "content": "A **Random Forest** is an ensemble learning method...",
        "layout": "Title at top, definition in center, handle at bottom"
      }
    ]
  },
  "slide_count": 9
}
```

## Post Quality Guidelines

The workflow is designed to create posts for data science professionals with 2-3 years of experience:

- ✅ Start with clear definitions (key terms in **bold**)
- ✅ Include intermediate to advanced concepts
- ✅ Provide practical examples and formulas
- ✅ Focus on genuine value, no filler
- ✅ Ensure coherent narrative across all slides
- ✅ Maximum 10 slides per post
- ✅ Include @learningalgorithm handle

## Logging

All workflow steps are logged to `instagram_agents.log` (configurable):

- Research phase: Word count, focus areas
- Draft phase: Number of slides created
- Review phase: Editor decisions and feedback
- Revision phase: Actions taken
- Final phase: Completion status

## Development

### Project Structure

```
Instagram-Agents/
├── main.py                 # Entry point
├── config.json            # Configuration
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
├── src/
│   ├── __init__.py
│   ├── researcher_agent.py   # Research agent
│   ├── drafter_agent.py      # Draft agent
│   ├── editor_agent.py       # Editor agent
│   ├── workflow.py           # LangGraph workflow
│   └── utils.py              # Utilities
└── README.md
```

### Adding Custom Agents

You can extend the workflow by:

1. Creating new agent classes in `src/`
2. Adding agent configurations to `config.json`
3. Integrating them into the workflow in `src/workflow.py`

## Troubleshooting

### API Key Issues

If you get API key errors:
- Ensure your `.env` file is in the project root
- Check that API keys are correctly formatted
- Verify the keys are valid and have sufficient credits

### Model Not Found

If a model is not recognized:
- Check the model name spelling
- Ensure you have the correct provider API key set
- Try using a different model from the supported list

### JSON Parsing Errors

If the drafter produces invalid JSON:
- The workflow will attempt to extract JSON from markdown blocks
- Check the logs for the raw LLM response
- Adjust the drafter temperature or instructions if needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the logs in `instagram_agents.log` for detailed error information

## Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [LangChain](https://github.com/langchain-ai/langchain)
- Search powered by [Tavily](https://tavily.com/)
