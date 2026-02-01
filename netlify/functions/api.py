import sys
import os

# Add current directory to path (api folder is copied here during build)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the FastAPI app
from api.index import app
from mangum import Mangum

# Create the handler
handler = Mangum(app, lifespan="off")

