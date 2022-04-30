from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Car Sharing</title>
        </head>
        <body>
            <h1>Car Sharing</h1>
            <p>Welcome to the Car Sharing API.</p>
        </body>
    </html>
    """