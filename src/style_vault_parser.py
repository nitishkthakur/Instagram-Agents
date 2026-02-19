"""
Style Vault Parser
Parses the style_vault.md file to extract example Instagram posts.
"""

import re
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path


class StyleVaultParser:
    """Parser for extracting Instagram post examples from style_vault.md"""
    
    def __init__(self, vault_file: str = "style_vault.md"):
        """
        Initialize the StyleVaultParser.
        
        Args:
            vault_file: Path to the style vault markdown file
        """
        self.vault_file = vault_file
        self.logger = logging.getLogger(__name__)
        
    def load_style_vault(self) -> List[Dict[str, Any]]:
        """
        Load and parse all posts from the style vault.
        
        Returns:
            List of dictionaries containing parsed post data
        """
        try:
            with open(self.vault_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            posts = self._parse_posts(content)
            self.logger.info(f"Loaded {len(posts)} example posts from style vault")
            return posts
            
        except FileNotFoundError:
            self.logger.warning(f"Style vault file not found: {self.vault_file}")
            return []
        except Exception as e:
            self.logger.error(f"Error loading style vault: {str(e)}")
            return []
    
    def _parse_posts(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse posts from markdown content.
        
        Args:
            content: Markdown content containing posts
            
        Returns:
            List of parsed post dictionaries
        """
        posts = []
        
        # Find all <post> tags and their content
        post_pattern = r'<post\s+([^>]+)>(.*?)</post>'
        matches = re.finditer(post_pattern, content, re.DOTALL)
        
        for match in matches:
            attributes_str = match.group(1)
            post_content = match.group(2)
            
            # Parse attributes
            attributes = self._parse_attributes(attributes_str)
            
            # Parse slides
            slides = self._parse_slides(post_content)
            
            # Parse slide count from attributes
            try:
                slide_count = int(attributes.get("slides", len(slides)))
            except (ValueError, TypeError):
                slide_count = len(slides)
            
            post_data = {
                "id": attributes.get("id", "unknown"),
                "topic": attributes.get("topic", "Unknown"),
                "style": attributes.get("style", "educational"),
                "slide_count": slide_count,
                "slides": slides
            }
            
            posts.append(post_data)
        
        return posts
    
    def _parse_attributes(self, attributes_str: str) -> Dict[str, str]:
        """
        Parse attributes from the post tag.
        
        Args:
            attributes_str: String containing attributes (e.g., 'id="example" topic="ML"')
            
        Returns:
            Dictionary of attribute key-value pairs
        """
        attributes = {}
        
        # Match attribute="value" or attribute='value'
        attr_pattern = r'(\w+)=["\'](.*?)["\']'
        matches = re.finditer(attr_pattern, attributes_str)
        
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            attributes[key] = value
        
        return attributes
    
    def _parse_slides(self, content: str) -> List[Dict[str, str]]:
        """
        Parse individual slides from post content.
        
        Args:
            content: Post content containing slide definitions
            
        Returns:
            List of slide dictionaries
        """
        slides = []
        
        # Split by slide headers (### Slide N)
        slide_pattern = r'###\s+Slide\s+(\d+)(.*?)(?=###\s+Slide\s+\d+|$)'
        matches = re.finditer(slide_pattern, content, re.DOTALL)
        
        for match in matches:
            slide_num = int(match.group(1))
            slide_content = match.group(2).strip()
            
            # Extract title, content, and layout
            title = self._extract_field(slide_content, "Title")
            slide_text = self._extract_field(slide_content, "Content")
            layout = self._extract_field(slide_content, "Layout")
            
            slides.append({
                "page_number": slide_num,
                "title": title,
                "content": slide_text,
                "layout": layout
            })
        
        return slides
    
    def _extract_field(self, content: str, field_name: str) -> str:
        """
        Extract a field value from slide content.
        
        Args:
            content: Slide content
            field_name: Name of field to extract (Title, Content, or Layout)
            
        Returns:
            Extracted field value
        """
        pattern = rf'\*\*{field_name}:\*\*\s*(.*?)(?=\*\*(?:Title|Content|Layout):|$)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            value = match.group(1).strip()
            # Clean up extra whitespace and newlines
            value = re.sub(r'\n{3,}', '\n\n', value)
            return value
        
        return ""
    
    def get_post_by_id(self, post_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific post by its ID.
        
        Args:
            post_id: The ID of the post to retrieve
            
        Returns:
            Post dictionary or None if not found
        """
        posts = self.load_style_vault()
        
        for post in posts:
            if post["id"] == post_id:
                return post
        
        self.logger.warning(f"Post with id '{post_id}' not found in style vault")
        return None
    
    def get_posts_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """
        Get all posts related to a specific topic.
        
        Args:
            topic: Topic to search for (case-insensitive partial match)
            
        Returns:
            List of matching posts
        """
        posts = self.load_style_vault()
        topic_lower = topic.lower()
        
        matching_posts = [
            post for post in posts 
            if topic_lower in post["topic"].lower()
        ]
        
        return matching_posts
    
    def get_posts_by_style(self, style: str) -> List[Dict[str, Any]]:
        """
        Get all posts with a specific style.
        
        Args:
            style: Style to filter by
            
        Returns:
            List of matching posts
        """
        posts = self.load_style_vault()
        
        matching_posts = [
            post for post in posts 
            if post["style"] == style
        ]
        
        return matching_posts
    
    def format_post_as_example(self, post: Dict[str, Any]) -> str:
        """
        Format a post as an example for the LLM to reference.
        
        Args:
            post: Post dictionary
            
        Returns:
            Formatted string representation
        """
        output = []
        output.append(f"Example Post: {post['topic']}")
        output.append(f"Style: {post['style']}")
        output.append(f"Number of Slides: {post['slide_count']}")
        output.append("\n---\n")
        
        for slide in post['slides']:
            output.append(f"Slide {slide['page_number']}:")
            output.append(f"  Title: {slide['title']}")
            output.append(f"  Content: {slide['content'][:100]}...")  # Truncate for brevity
            output.append(f"  Layout: {slide['layout']}")
            output.append("")
        
        return "\n".join(output)
    
    def get_style_examples_for_prompt(self, limit: int = 2) -> str:
        """
        Get formatted style examples to include in agent prompts.
        
        Args:
            limit: Maximum number of examples to include
            
        Returns:
            Formatted string with example posts
        """
        posts = self.load_style_vault()
        
        if not posts:
            return "No style examples available."
        
        examples = []
        examples.append("=== STYLE REFERENCE EXAMPLES ===\n")
        
        for post in posts[:limit]:
            examples.append(self.format_post_as_example(post))
            examples.append("\n" + "="*50 + "\n")
        
        return "\n".join(examples)
