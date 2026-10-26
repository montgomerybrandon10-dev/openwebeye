from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="OpenWebEye")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OpenWebEye</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-950 text-white min-h-screen">
        <div class="max-w-4xl mx-auto p-8 text-center">
            <h1 class="text-5xl font-bold mb-4">OpenWebEye</h1>
            <p class="text-slate-400 text-lg mb-6">Facial OSINT Platform</p>
            <p class="text-sm text-slate-500">openwebeye.com is live.</p>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "ok", "site": "https://openwebeye.com"}
