"""
Module anthropic.py - Integration with Anthropic Claude API.

This module provides functions to interact with the Anthropic Claude API
for generating AI-assisted interpretations of student performance data.
"""

import os
import random
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Import INTERPRETATION_TEMPLATES to avoid circular imports
from config import INTERPRETATION_TEMPLATES

# Try to import Anthropic library
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Anthropic API not available. Install with: pip install anthropic")

def generate_llm_message(prompt):
    """
    Generate an enriched interpretation using Anthropic API with fallback.
    
    Args:
        prompt: Prompt text to send to LLM
        
    Returns:
        str: Generated interpretation or fallback message
    """
    # Check API key before attempting API call
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        # Skip API call entirely if key is missing or default
        # Log a friendlier message, just once per session
        if not hasattr(generate_llm_message, "api_warning_shown"):
            generate_llm_message.api_warning_shown = True
            print("Note: No valid Anthropic API key found. Using fallback message generation.")
        
        # Go directly to fallback
        return generate_fallback_message(prompt)
    
    # Try Anthropic API since we have a key
    if ANTHROPIC_AVAILABLE:
        try:
            # Initialize client with API key
            client = Anthropic(api_key=api_key)
            
            # Make API call with modern parameters
            response = client.messages.create(
                model="claude-3-haiku-20240307",  # Using a stable model version
                max_tokens=500,
                temperature=0.7,
                system="You are an educational specialist interpreting assessment data and providing useful insights and recommendations for teachers.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract and return text content
            return response.content[0].text
            
        except Exception as e:
            # Only log the error once per session to reduce console spam
            if not hasattr(generate_llm_message, "error_shown"):
                generate_llm_message.error_shown = True
                print(f"Note: Anthropic API call failed. Using fallback message generation. Error details: {str(e)}")
            
            # Continue to fallback when API fails
    else:
        # Only log this once
        if not hasattr(generate_llm_message, "import_warning_shown"):
            generate_llm_message.import_warning_shown = True
            print("Note: Anthropic library not available. Using fallback message generation.")
    
    # If Anthropic unavailable or failed, use fallback
    return generate_fallback_message(prompt)

def generate_fallback_message(prompt):
    """
    Generate a fallback message when LLM is not available.
    This creates a more useful response than an error message.
    
    Args:
        prompt: Original prompt text
        
    Returns:
        str: Fallback message
    """
    # Extract key information from the prompt
    lines = prompt.split('\n')
    
    # Generate generic recommendations
    fallback_recommendations = INTERPRETATION_TEMPLATES["fallback"]
    
    # Create a structured response
    response = "Based on the analysis of results, the following observations can be made:\n\n"
    
    # Add a comment about EGRA if it exists in the prompt
    if "EGRA:" in prompt:
        response += "In reading (EGRA), the student shows varying results depending on skills. "
        response += "It's important to strengthen emerging skills while consolidating achievements.\n\n"
    
    # Add a comment about EGMA if it exists in the prompt
    if "EGMA:" in prompt:
        response += "In mathematics (EGMA), some skills need reinforcement. "
        response += "Regular practice of basic concepts is recommended.\n\n"
    
    # Add recommendations
    response += "Educational recommendations:\n"
    
    # Select a few random recommendations
    selected_recommendations = random.sample(fallback_recommendations, min(3, len(fallback_recommendations)))
    
    # Add the recommendations to the response
    for rec in selected_recommendations:
        response += f"- {rec}\n"
    
    response += "\nRegular monitoring will help adapt activities to the student's progress."
    
    return response