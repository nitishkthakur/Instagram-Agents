"""
Style Vault Demo
Demonstrates how to use the Style Vault feature
"""

from src.style_vault_parser import StyleVaultParser


def main():
    print("="*80)
    print("STYLE VAULT DEMO")
    print("="*80)
    print()
    
    # Initialize parser
    parser = StyleVaultParser("style_vault.md")
    
    # 1. Load all posts
    print("1. Loading all posts from style vault...")
    posts = parser.load_style_vault()
    print(f"   Found {len(posts)} example posts\n")
    
    for post in posts:
        print(f"   - {post['topic']} ({post['slide_count']} slides, style: {post['style']})")
    print()
    
    # 2. Get a specific post by ID
    print("2. Getting specific post by ID...")
    post = parser.get_post_by_id("random-forests-example")
    if post:
        print(f"   Retrieved: {post['topic']}")
        print(f"   First slide title: {post['slides'][0]['title']}")
        print()
    
    # 3. Search by topic
    print("3. Searching posts by topic...")
    matching = parser.get_posts_by_topic("Neural")
    print(f"   Found {len(matching)} posts matching 'Neural'")
    for p in matching:
        print(f"   - {p['topic']}")
    print()
    
    # 4. Filter by style
    print("4. Filtering posts by style...")
    styled = parser.get_posts_by_style("educational-technical")
    print(f"   Found {len(styled)} posts with 'educational-technical' style")
    for p in styled:
        print(f"   - {p['topic']}")
    print()
    
    # 5. Format for LLM prompt
    print("5. Formatting examples for LLM prompt...")
    examples = parser.get_style_examples_for_prompt(limit=1)
    print(f"   Generated {len(examples)} characters of example text")
    print()
    print("   Preview (first 500 chars):")
    print("   " + "-"*76)
    print("   " + examples[:500].replace("\n", "\n   "))
    print("   " + "-"*76)
    print()
    
    # 6. Show how it's used in config
    print("6. Configuration in config.json:")
    print("""
   {
     "drafter": {
       "use_style_vault": true,
       "style_vault_file": "style_vault.md",
       ...
     }
   }
   """)
    
    print("="*80)
    print("DEMO COMPLETE")
    print("="*80)
    print()
    print("To use the Style Vault:")
    print("  1. Enable in config.json: 'use_style_vault': true")
    print("  2. Add your own examples to style_vault.md")
    print("  3. The Drafter agent will reference them automatically")
    print()


if __name__ == "__main__":
    main()
