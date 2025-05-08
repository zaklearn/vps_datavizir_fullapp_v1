"""
Module interpretation.py - Hybrid interpretation system.

This module provides a hybrid interpretation system that combines rule-based
analysis with AI-generated insights using the Anthropic Claude API or a local fallback.
"""

import os
import random
import streamlit as st
from modules import language
from config import STANDARDS, EGRA_INDICATORS, EGMA_INDICATORS, INTERPRETATION_TEMPLATES

# Try to initialize local model for fallback generation
generator = None
try:
    from transformers import pipeline
    model_name = "gpt2"  # Simple English model as fallback
    try:
        # Try GPU first
        generator = pipeline("text-generation", model=model_name, device=0)
        print(f"Loaded model {model_name} on GPU")
    except Exception as gpu_error:
        try:
            # Try CPU if GPU fails
            print(f"GPU loading failed: {gpu_error}, falling back to CPU")
            generator = pipeline("text-generation", model=model_name, device=-1)
            print(f"Loaded model {model_name} on CPU")
        except Exception as cpu_error:
            print(f"Model loading failed completely: {cpu_error}")
            generator = None  # Fallback if not available
except ImportError:
    print("Transformers library not available. Install with: pip install transformers torch")
    generator = None

def generate_rule_based_interpretation(scores_egra, scores_egma):
    """
    Generate a basic text message based on student scores.
    
    Args:
        scores_egra: DataFrame of EGRA scores
        scores_egma: DataFrame of EGMA scores
        
    Returns:
        str: Rule-based interpretation message
    """
    interpretations = []
    templates = INTERPRETATION_TEMPLATES["rule_based"]

    def interpret_section(scores, domain):
        section = f"### {domain} Interpretation\n"
        for _, row in scores.iterrows():
            status = row["Status"]
            indicator = row["Indicator"]
            score = row["Student Score"]
            
            if status == "Mastery":
                section += f"- {templates['mastery'].format(indicator=indicator, score=score)}\n"
            elif status == "Developing":
                section += f"- {templates['developing'].format(indicator=indicator, score=score)}\n"
            elif status == "Emerging":
                section += f"- {templates['emerging'].format(indicator=indicator, score=score)}\n"
                
        return section

    if scores_egra is not None and not scores_egra.empty:
        interpretations.append(interpret_section(scores_egra, "EGRA"))
    if scores_egma is not None and not scores_egma.empty:
        interpretations.append(interpret_section(scores_egma, "EGMA"))

    return "\n".join(interpretations)

def create_llm_prompt(rule_message, scores_egra=None, scores_egma=None):
    """
    Generate a prompt from scores and the rule-based message.
    
    Args:
        rule_message: Rule-based interpretation message
        scores_egra: DataFrame of EGRA scores (optional)
        scores_egma: DataFrame of EGMA scores (optional)
        
    Returns:
        str: Formatted prompt for LLM
    """
    def scores_to_text(scores):
        if scores is None or scores.empty:
            return ""
        lines = []
        for _, row in scores.iterrows():
            lines.append(f"{row['Indicator']}: {row['Student Score']} (Status: {row['Status']})")
        return "\n".join(lines)
    
    prompt = f"""
Here are the student's results:

EGRA:
{scores_to_text(scores_egra) if scores_egra is not None else "No EGRA data available"}

EGMA:
{scores_to_text(scores_egma) if scores_egma is not None else "No EGMA data available"}

Systematic analysis:
{rule_message}

Based on this information, write a concise overall interpretation and provide recommendations in English, using clear language for teachers.
    """
    
    return prompt.strip()

def create_group_prompt(summary_text):
    """
    Format a prompt for group interpretation via LLM
    
    Args:
        summary_text: Summary of group performance
        
    Returns:
        str: Formatted prompt for group interpretation
    """
    return f"""
Here is a summary of a group of students' performance:
{summary_text}

Please write a concise interpretation and suggest appropriate recommendations for this group.
    """.strip()

def generate_llm_message(prompt):
    """
    Generate an enriched interpretation using Anthropic API with fallback.
    
    Args:
        prompt: Prompt text to send to LLM
        
    Returns:
        str: Generated interpretation or fallback message
    """
    # Use anthropic module for API integration
    from modules import anthropic
    return anthropic.generate_llm_message(prompt)

def generate_fallback_message(prompt):
    """
    Generate a fallback message when LLM is not available.
    
    Args:
        prompt: Original prompt text
        
    Returns:
        str: Fallback message
    """
    # Use anthropic module for fallback generation
    from modules import anthropic
    return anthropic.generate_fallback_message(prompt)

def display_interpretation(scores_egra, scores_egma):
    """
    Display interpretation in Streamlit and return messages for export.
    
    Args:
        scores_egra: DataFrame of EGRA scores
        scores_egma: DataFrame of EGMA scores
        
    Returns:
        tuple: (rule_message, llm_message)
    """
    if scores_egra is not None and not scores_egra.empty and scores_egma is not None and not scores_egma.empty:
        try:
            rule_message = generate_rule_based_interpretation(scores_egra, scores_egma)
            prompt = create_llm_prompt(rule_message, scores_egra, scores_egma)
            llm_message = generate_llm_message(prompt)

            st.markdown(f"### 🧠 {language.t('interpretation')}")
            st.markdown(f"**{language.t('systematic_analysis')} :**")
            st.info(rule_message)
            st.markdown(f"**{language.t('enriched_synthesis')} :**")
            st.success(llm_message)

            return rule_message, llm_message
        except Exception as e:
            st.error(f"Error generating interpretation: {str(e)}")
            return None, None
    return None, None

def generate_group_summary(means_df, level='class'):
    """
    Generate a text summary from class or school averages.
    
    Args:
        means_df: DataFrame with means by group
        level: Level of analysis ('class' or 'school')
        
    Returns:
        str: Summary text
    """
    labels = {}
    for key in STANDARDS.keys():
        labels[key] = language.get_label(key)
    
    summary = f"Comparison by {level}:\n"
    for indicator in means_df.columns:
        # Skip non-indicator columns if any
        if indicator not in STANDARDS:
            continue
            
        mean_val = means_df[indicator].mean()
        if mean_val < 0.75 * STANDARDS[indicator]["Mastery"]:
            summary += f"- Overall low performance in **{labels[indicator]}** (average: {mean_val:.1f}).\n"
        elif mean_val < STANDARDS[indicator]["Mastery"]:
            summary += f"- Average level achieved for **{labels[indicator]}** (average: {mean_val:.1f}).\n"
        else:
            summary += f"- Good level in **{labels[indicator]}** (average: {mean_val:.1f}).\n"
    
    return summary