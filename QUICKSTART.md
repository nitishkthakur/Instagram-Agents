# Quick Start Guide

## Prerequisites
- Python 3.9+
- API keys (Tavily + at least one LLM provider)

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
# Copy the template
cp .env.example .env

# Edit .env and add your keys
nano .env  # or use your preferred editor
```

Required keys:
- `TAVILY_API_KEY` - Get from https://tavily.com/
- One of:
  - `OPENAI_API_KEY` - Get from https://platform.openai.com/
  - `ANTHROPIC_API_KEY` - Get from https://console.anthropic.com/
  - `GOOGLE_API_KEY` - Get from https://ai.google.dev/
  - `XAI_API_KEY` - Get from https://x.ai/

### 3. Run Your First Post
```bash
python main.py --topic "Random Forests in Machine Learning"
```

## Common Commands

### Create a Post
```bash
# Default topic from config
python main.py

# Custom topic
python main.py --topic "Neural Networks"

# Save to specific file
python main.py --topic "Gradient Boosting" --output my_post.json
```

### View Examples
```bash
python example_usage.py
```

### See Workflow Diagram
```bash
python visualize_workflow.py
```

### Run Tests
```bash
python test_structure.py
python test_style_vault.py  # Test style vault functionality
```

## Configuration

Edit `config.json` to customize:

```json
{
  "researcher": {
    "model": "gpt-4o",           // Change model
    "temperature": 0.7,          // 0-1 (creativity)
    "word_limit": 2500          // Research length
  },
  "drafter": {
    "model": "gpt-4o",
    "temperature": 0.8,
    "max_slides": 10,           // 1-10 slides
    "use_style_vault": true,    // Enable style examples
    "style_vault_file": "style_vault.md"
  },
  "editor_in_chief": {
    "model": "gpt-4o",
    "max_iterations": 5         // Review cycles
  }
}
```

## Style Vault

The **Style Vault** (`style_vault.md`) contains example posts that guide the AI agents:

- 📝 View examples: Open `style_vault.md`
- ➕ Add your own: Follow the format in the file
- 🎨 Each example shows structure, tone, and formatting
- ✅ Agents reference these to maintain consistency

**Quick tip:** Add your best posts to the Style Vault to teach the AI your preferred style!

## Output

### What You Get
1. **JSON file** - Complete post with all slides
2. **Log file** - Detailed workflow trace
3. **Console output** - Formatted post display

### Post Structure
```json
{
  "topic": "Your Topic",
  "post": {
    "slides": [
      {
        "page_number": 1,
        "title": "Title",
        "content": "Content with **bold** terms\n@learningalgorithm",
        "layout": "Layout description"
      }
    ]
  }
}
```

## Troubleshooting

### Missing API Key
```
Error: Missing required API keys: TAVILY_API_KEY
```
**Solution**: Add the key to your `.env` file

### Model Not Found
```
Error initializing model gpt-4o
```
**Solution**: 
- Check model name spelling
- Ensure you have the correct provider API key
- Try a different model (e.g., `gpt-3.5-turbo`)

### JSON Parsing Error
```
Failed to parse JSON response
```
**Solution**: Check logs for the raw response. Try:
- Adjusting temperature (make it lower)
- Using a different model
- Modifying instructions in config

## Tips

### Best Practices
1. **Start simple**: Use default config for first run
2. **Check logs**: Review `instagram_agents.log` for issues
3. **Iterate config**: Adjust instructions based on results
4. **Monitor costs**: API calls cost money, start with cheaper models

### Model Recommendations
- **Best quality**: `gpt-4o`, `claude-3-5-sonnet-20241022`
- **Fast & cheap**: `gpt-3.5-turbo`, `gemini-2.0-flash-exp`
- **Balanced**: `gpt-4o`, `gemini-1.5-pro`

### Common Topics
- Machine Learning: "Random Forests", "Neural Networks", "Gradient Boosting"
- Deep Learning: "Transformers", "LSTM Networks", "CNNs"
- Statistics: "Bayesian Inference", "Hypothesis Testing"
- Tools: "Docker for Data Science", "Git Best Practices"

## Getting Help

1. **Check logs**: `instagram_agents.log` has detailed trace
2. **Run tests**: `python test_structure.py` validates setup
3. **Check examples**: `python example_usage.py` shows all options
4. **View workflow**: `python visualize_workflow.py` explains process
5. **Read docs**: See `README.md` for comprehensive guide

## Advanced Usage

### Custom Configuration File
```bash
# Create custom config
cp config.json my_config.json

# Edit as needed
nano my_config.json

# Use it
python main.py --config my_config.json --topic "Your Topic"
```

### Different Models Per Agent
```json
{
  "researcher": {
    "model": "gpt-4o"           // Precise research
  },
  "drafter": {
    "model": "claude-3-5-sonnet-20241022"  // Creative writing
  },
  "editor_in_chief": {
    "model": "gpt-4o"           // Critical review
  }
}
```

### Adjust Quality vs Speed
```json
{
  "researcher": {
    "word_limit": 1500,         // Faster (less research)
    "temperature": 0.5          // More focused
  },
  "editor_in_chief": {
    "max_iterations": 2         // Fewer review cycles
  },
  "general": {
    "max_total_iterations": 5   // Overall limit
  }
}
```

## Next Steps

1. ✅ Run your first post
2. 📝 Review the output
3. ⚙️ Adjust config for your needs
4. 🚀 Create multiple posts
5. 📊 Track what works best

---

**Need more help?** 
- Full documentation: `README.md`
- Implementation details: `IMPLEMENTATION.md`
- Examples: `example_usage.py`
- Workflow diagram: `visualize_workflow.py`
