"""
Tests for Style Vault functionality
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from src.style_vault_parser import StyleVaultParser


def test_style_vault_loading():
    """Test that style vault can be loaded and parsed."""
    print("Testing style vault loading...")
    
    parser = StyleVaultParser("style_vault.md")
    posts = parser.load_style_vault()
    
    assert len(posts) > 0, "Style vault should contain at least one post"
    print(f"✅ Loaded {len(posts)} posts from style vault")
    
    # Check first post structure
    first_post = posts[0]
    assert "id" in first_post, "Post should have an id"
    assert "topic" in first_post, "Post should have a topic"
    assert "style" in first_post, "Post should have a style"
    assert "slides" in first_post, "Post should have slides"
    assert "slide_count" in first_post, "Post should have slide_count"
    
    print(f"✅ Post structure validated")
    print(f"   First post: {first_post['topic']} ({first_post['slide_count']} slides)")


def test_slide_structure():
    """Test that slides are properly parsed."""
    print("\nTesting slide structure...")
    
    parser = StyleVaultParser("style_vault.md")
    posts = parser.load_style_vault()
    
    if posts:
        first_post = posts[0]
        slides = first_post["slides"]
        
        assert len(slides) > 0, "Post should have at least one slide"
        
        first_slide = slides[0]
        assert "page_number" in first_slide, "Slide should have page_number"
        assert "title" in first_slide, "Slide should have title"
        assert "content" in first_slide, "Slide should have content"
        assert "layout" in first_slide, "Slide should have layout"
        
        print(f"✅ Slide structure validated")
        print(f"   First slide title: {first_slide['title']}")


def test_get_post_by_id():
    """Test retrieving a post by ID."""
    print("\nTesting get post by ID...")
    
    parser = StyleVaultParser("style_vault.md")
    
    # Try to get the Random Forests example
    post = parser.get_post_by_id("random-forests-example")
    
    if post:
        assert post["id"] == "random-forests-example"
        assert "Random" in post["topic"]
        print(f"✅ Retrieved post by ID: {post['topic']}")
    else:
        print("⚠️  Post not found (check if style_vault.md exists and has the example)")


def test_get_posts_by_topic():
    """Test retrieving posts by topic."""
    print("\nTesting get posts by topic...")
    
    parser = StyleVaultParser("style_vault.md")
    posts = parser.get_posts_by_topic("Random")
    
    assert isinstance(posts, list), "Should return a list"
    print(f"✅ Found {len(posts)} posts matching 'Random'")


def test_get_posts_by_style():
    """Test retrieving posts by style."""
    print("\nTesting get posts by style...")
    
    parser = StyleVaultParser("style_vault.md")
    posts = parser.get_posts_by_style("educational-technical")
    
    assert isinstance(posts, list), "Should return a list"
    print(f"✅ Found {len(posts)} posts with style 'educational-technical'")


def test_format_post_as_example():
    """Test formatting a post as an example."""
    print("\nTesting format post as example...")
    
    parser = StyleVaultParser("style_vault.md")
    posts = parser.load_style_vault()
    
    if posts:
        formatted = parser.format_post_as_example(posts[0])
        
        assert len(formatted) > 0, "Formatted output should not be empty"
        assert "Example Post:" in formatted, "Should include 'Example Post:' header"
        assert "Style:" in formatted, "Should include style information"
        
        print(f"✅ Successfully formatted post as example")
        print(f"   Output length: {len(formatted)} characters")


def test_get_style_examples_for_prompt():
    """Test getting style examples for LLM prompt."""
    print("\nTesting get style examples for prompt...")
    
    parser = StyleVaultParser("style_vault.md")
    examples = parser.get_style_examples_for_prompt(limit=2)
    
    assert len(examples) > 0, "Should return example text"
    assert "STYLE REFERENCE" in examples, "Should include header"
    
    print(f"✅ Generated style examples for prompt")
    print(f"   Output length: {len(examples)} characters")


def run_all_tests():
    """Run all style vault tests."""
    print("\n" + "="*60)
    print("Running Style Vault Tests")
    print("="*60 + "\n")
    
    tests = [
        test_style_vault_loading,
        test_slide_structure,
        test_get_post_by_id,
        test_get_posts_by_topic,
        test_get_posts_by_style,
        test_format_post_as_example,
        test_get_style_examples_for_prompt,
    ]
    
    failed = []
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ {test.__name__} failed: {str(e)}")
            failed.append(test.__name__)
    
    print("\n" + "="*60)
    if not failed:
        print("✅ All style vault tests passed!")
    else:
        print(f"❌ {len(failed)} test(s) failed:")
        for test_name in failed:
            print(f"  - {test_name}")
    print("="*60 + "\n")
    
    return len(failed) == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
