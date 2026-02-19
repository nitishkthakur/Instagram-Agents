"""
Basic tests to validate the workflow structure and configuration.
"""

import os
import sys
import json

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))


def test_config_loading():
    """Test that configuration can be loaded."""
    print("Testing config loading...")
    from src.utils import load_config
    
    config = load_config('config.json')
    
    assert 'researcher' in config, "Config missing researcher section"
    assert 'drafter' in config, "Config missing drafter section"
    assert 'editor_in_chief' in config, "Config missing editor_in_chief section"
    assert 'general' in config, "Config missing general section"
    
    # Check researcher config
    assert 'model' in config['researcher']
    assert 'word_limit' in config['researcher']
    assert 'instructions' in config['researcher']
    
    # Check drafter config
    assert 'model' in config['drafter']
    assert 'max_slides' in config['drafter']
    assert 'instructions' in config['drafter']
    
    # Check editor config
    assert 'model' in config['editor_in_chief']
    assert 'instructions' in config['editor_in_chief']
    
    print("✅ Config loading test passed")


def test_module_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")
    
    from src.researcher_agent import ResearcherAgent
    from src.drafter_agent import DrafterAgent
    from src.editor_agent import EditorInChiefAgent
    from src.workflow import InstagramWorkflow
    from src.utils import (
        setup_logging, load_config, save_final_post, 
        format_post_for_display, log_workflow_state
    )
    
    print("✅ Module imports test passed")


def test_post_formatting():
    """Test post formatting utility."""
    print("Testing post formatting...")
    from src.utils import format_post_for_display
    
    test_post = {
        "topic": "Test Topic",
        "post": {
            "slides": [
                {
                    "page_number": 1,
                    "title": "Test Slide",
                    "content": "Test content",
                    "layout": "Test layout"
                }
            ]
        },
        "slide_count": 1
    }
    
    formatted = format_post_for_display(test_post)
    assert "Test Topic" in formatted
    assert "Test Slide" in formatted
    assert "Test content" in formatted
    
    print("✅ Post formatting test passed")


def test_logging_setup():
    """Test logging configuration."""
    print("Testing logging setup...")
    from src.utils import setup_logging
    import logging
    
    logger = setup_logging('/tmp/test_instagram_agents.log')
    assert logger is not None
    logger.info("Test log message")
    
    # Verify log file was created
    assert os.path.exists('/tmp/test_instagram_agents.log')
    
    print("✅ Logging setup test passed")


def test_config_structure():
    """Test that config has all required fields."""
    print("Testing config structure...")
    
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Test researcher config structure
    researcher = config['researcher']
    assert isinstance(researcher.get('word_limit'), int)
    assert isinstance(researcher.get('temperature'), (int, float))
    assert isinstance(researcher.get('max_output_tokens'), int)
    assert isinstance(researcher.get('model'), str)
    assert isinstance(researcher.get('instructions'), str)
    
    # Test drafter config structure
    drafter = config['drafter']
    assert isinstance(drafter.get('max_slides'), int)
    assert drafter.get('max_slides') <= 10, "Max slides should be <= 10"
    assert isinstance(drafter.get('temperature'), (int, float))
    assert isinstance(drafter.get('max_output_tokens'), int)
    assert isinstance(drafter.get('model'), str)
    assert isinstance(drafter.get('instructions'), str)
    
    # Test editor config structure
    editor = config['editor_in_chief']
    assert isinstance(editor.get('max_iterations'), int)
    assert isinstance(editor.get('temperature'), (int, float))
    assert isinstance(editor.get('max_output_tokens'), int)
    assert isinstance(editor.get('model'), str)
    assert isinstance(editor.get('instructions'), str)
    
    # Test general config
    general = config['general']
    assert isinstance(general.get('log_file'), str)
    assert isinstance(general.get('max_total_iterations'), int)
    
    print("✅ Config structure test passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("Running Instagram Agents Tests")
    print("="*60 + "\n")
    
    tests = [
        test_module_imports,
        test_config_loading,
        test_config_structure,
        test_logging_setup,
        test_post_formatting,
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
        print("✅ All tests passed!")
    else:
        print(f"❌ {len(failed)} test(s) failed:")
        for test_name in failed:
            print(f"  - {test_name}")
    print("="*60 + "\n")
    
    return len(failed) == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
