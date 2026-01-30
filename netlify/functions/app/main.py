import sys
import os
from mangum import Mangum

# Add the current directory to sys.path to allow importing the 'api' package
# In the Netlify Lambda environment, this folder will contain the 'api' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from api.index import app

# Netlify expects a variable named 'handler'
handler = Mangum(app)
