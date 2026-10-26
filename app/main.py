from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
import sys
sys.path.insert(0, ".")

app = FastAPI(title="OpenWebEye")

try:
    from lib.facecheck import facecheck
    from lib.osint import osint
    from lib.pimeyes import pimeyes
except Exception:
    facecheck = osint = pimeyes = None

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
        <nav class="border-b border-slate-800 px-6 py-4 flex gap-6">
            <a href="/" class="font-bold text-lg">OpenWebEye</a>
            <a href="/multi" class="text-slate-400 hover:text-white">Multi Search</a>
        </nav>
        <div class="max-w-4xl mx-auto p-8 text-center">
            <h1 class="text-5xl font-bold mb-4">OpenWebEye</h1>
            <p class="text-slate-400 text-lg mb-8">Facial OSINT Platform</p>
            <a href="/multi" class="inline-block bg-indigo-600 hover:bg-indigo-500 px-6 py-3 rounded-lg font-medium">Search Faces</a>
        </div>
    </body>
    </html>
    """

@app.get("/multi", response_class=HTMLResponse)
async def multi_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Multi Search - OpenWebEye</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-950 text-white min-h-screen">
        <nav class="border-b border-slate-800 px-6 py-4 flex gap-6">
            <a href="/" class="font-bold text-lg">OpenWebEye</a>
            <a href="/multi" class="text-white">Multi Search</a>
        </nav>
        <div class="max-w-2xl mx-auto p-8">
            <h1 class="text-3xl font-bold mb-2">Multi-Source Search</h1>
            <p class="text-slate-400 mb-6">Search FaceCheck.id, OSINT engines, and more.</p>
            <form id="searchForm" class="space-y-4">
                <input type="file" name="file" accept="image/*" required class="block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:bg-indigo-600 file:text-white">
                <div class="flex gap-4 text-sm">
                    <label><input type="checkbox" name="use_facecheck" checked class="mr-1"> FaceCheck</label>
                    <label><input type="checkbox" name="use_osint" checked class="mr-1"> OSINT</label>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 py-3 rounded-lg font-medium">Search</button>
            </form>
            <div id="results" class="mt-8 space-y-4"></div>
        </div>
        <script>
        document.getElementById('searchForm').onsubmit = async (e) => {
            e.preventDefault();
            const form = e.target;
            const data = new FormData(form);
            const resultsEl = document.getElementById('results');
            resultsEl.innerHTML = '<p class="text-slate-400">Searching...</p>';
            try {
                const res = await fetch('/api/search/multi', { method: 'POST', body: data });
                const json = await res.json();
                let html = '';
                for (const [src, result] of Object.entries(json.sources || {})) {
                    html += `<div class="p-4 bg-slate-900 rounded"><h3 class="font-medium capitalize mb-2">${src}</h3>`;
                    if (result.error) {
                        html += `<p class="text-red-400 text-sm">${result.error}</p>`;
                    }
                    if (result.results && result.results.length) {
                        html += '<ul class="space-y-2 text-sm">';
                        for (const item of result.results) {
                            if (item.url) {
                                html += `<li><a href="${item.url}" target="_blank" class="text-indigo-400 hover:underline">${item.note || item.url}</a></li>`;
                            } else if (item.note) {
                                html += `<li class="text-slate-400">${item.note}</li>`;
                            }
                        }
                        html += '</ul>';
                    } else if (!result.error) {
                        html += '<p class="text-slate-500 text-sm">No results</p>';
                    }
                    html += '</div>';
                }
                resultsEl.innerHTML = html || '<p class="text-slate-500">No results</p>';
            } catch (err) {
                resultsEl.innerHTML = `<p class="text-red-400">${err}</p>`;
            }
        };
        </script>
    </body>
    </html>
    """

@app.post("/api/search/multi")
async def api_search_multi(
    file: UploadFile = File(...),
    use_facecheck: bool = Form(True),
    use_osint: bool = Form(True),
):
    image_bytes = await file.read()
    sources = {}
    if use_facecheck and facecheck:
        sources["facecheck"] = facecheck.search(image_bytes)
    if use_osint and osint:
        sources["osint"] = osint.search(image_bytes)
    return JSONResponse({"sources": sources})

@app.get("/health")
async def health():
    return {"status": "ok"}
