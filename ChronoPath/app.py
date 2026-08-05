import os
import uvicorn
from api.main import app

# Hugging Face Spaces expose port 7860 by default for Gradio apps.
# We are simply hijacking this to run our FastAPI backend instead!
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
