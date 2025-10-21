"""
Simplified LangChain Tools Collection
Only tools that are actually used in agents.py, in the correct order.
"""
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import json
import re
import tempfile
from pathlib import Path

from langchain_core.tools import tool

# DuckDuckGo search integration
from ddgs import DDGS

@tool
def web_search(query: str, num_results: int = 5) -> str:
    """Search the web using DuckDuckGo.
    
    Args:
        query: Search query string
        num_results: Number of results to return (default: 5)
    
    Returns:
        Formatted search results with titles, descriptions, and URLs
    """
    
    try:
        results = list(DDGS().text(query=query,
                                   max_results=num_results,
                                   region="us-en",
                                   timelimit="d",
                                   backend="google, bing, brave, yahoo, wikipedia, duckduckgo"))
        
        if not results:
            return f"No results found for '{query}'"
        
        formatted_results = [f"Search Results for '{query}':\n"]
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            body = result.get('body', 'No description available')
            href = result.get('href', '')
            formatted_results.append(f"{i}. **{title}**\n   {body}\n   {href}")
        
        return "\n\n".join(formatted_results)
    
    except Exception as e:
        return f"Search error: {str(e)}"



@tool
def calculate(expression: str) -> str:
    """Calculate mathematical expressions.

    Supports basic math: +, -, *, /, ** (power), sqrt(), abs()

    Args:
        expression: Math expression like "2+2" or "sqrt(16)"

    Returns:
        Result as a string
    """
    try:
        import math

        # Allow only safe math operations
        safe_functions = {
            'sqrt': math.sqrt,
            'abs': abs,
            'round': round,
            'pow': pow
        }

        # Calculate the result safely
        result = eval(expression, {"__builtins__": {}}, safe_functions)

        return f"{expression} = {result}"

    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except Exception as e:
        return f"Error: {str(e)}"

