import sys
import os

# Add current directory to path so we can import the copied 'api' package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the FastAPI app and its handler
from api.index import handler

# Export the handler for Netlify
__all__ = ['handler']
