from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from scraper.scraper_v2 import TransformFn


from models import Url


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")



@app.post('/processUrl')
async def processUrl(url: Url):
    try:
        transformer = TransformFn()
        response = transformer.process(url.url)
        return {"status": response}
    except Exception as e:
        # Handle exceptions
        return {"Error": str(e)}

@app.get('/', response_class=HTMLResponse)
async def hello(request: Request):
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    return templates.TemplateResponse("index.html", {"request": request, "message": message, })


if __name__ == '__main__':
    # Get the server port from the environment variable
    server_port = os.environ.get("PORT", "8080")

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=int(server_port))
