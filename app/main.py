from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
import sys, os, base64
sys.path.insert(0, ".")

app = FastAPI(title="OpenWebEye")

try:
    from lib.facecheck import facecheck
    from lib.osint import osint
except Exception:
    facecheck = osint = None

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenWebEye</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-white min-h-screen">
<nav class="border-b border-slate-800 px-6 py-4 flex gap-6 items-center">
<a href="/" class="font-bold text-xl">OpenWebEye</a>
<a href="/" class="text-slate-400 hover:text-white text-sm">Search</a>
</nav>
<div class="max-w-xl mx-auto p-6">
<h1 class="text-3xl font-bold mb-1">Face Search</h1>
<p class="text-slate-400 text-sm mb-6">Upload a face. Get links to search engines + optional FaceCheck results.</p>

<form id="f" class="space-y-4">
<input type="file" name="file" accept="image/*" required class="block w-full text-sm text-slate-400 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-indigo-600 file:text-white file:font-medium">
<label class="flex items-center gap-2 text-sm"><input type="checkbox" name="use_facecheck" class="accent-indigo-500"> Use FaceCheck API (requires token)</label>
<button class="w-full bg-indigo-600 hover:bg-indigo-500 py-3 rounded-lg font-medium">Search</button>
</form>

<div id="out" class="mt-8 space-y-3"></div>
</div>
<script>
document.getElementById('f').onsubmit = async (e) => {
  e.preventDefault();
  const out = document.getElementById('out');
  out.innerHTML = '<p class="text-slate-400">Searching...</p>';
  const data = new FormData(e.target);
  try {
    const r = await fetch('/api/search', {method:'POST', body:data});
    const j = await r.json();
    let h = '';
    // FaceCheck
    if (j.facecheck) {
      h += '<div class="p-4 bg-slate-900 rounded-lg"><h3 class="font-medium mb-2">FaceCheck</h3>';
      if (j.facecheck.error) h += `<p class="text-amber-400 text-sm">${j.facecheck.error}</p>`;
      else if (j.facecheck.results && j.facecheck.results.length) {
        h += '<ul class="space-y-1 text-sm">';
        j.facecheck.results.forEach(it => {
          h += `<li><a href="${it.url}" target="_blank" class="text-indigo-400 hover:underline">${it.url}</a> <span class="text-slate-500">(${Math.round((it.score||0)*100)}%)</span></li>`;
        });
        h += '</ul>';
      } else h += '<p class="text-slate-500 text-sm">No matches</p>';
      h += '</div>';
    }
    // OSINT links
    if (j.osint && j.osint.results) {
      h += '<div class="p-4 bg-slate-900 rounded-lg"><h3 class="font-medium mb-2">Search Engines</h3><ul class="space-y-2 text-sm">';
      j.osint.results.forEach(it => {
        h += `<li><a href="${it.url}" target="_blank" class="text-indigo-400 hover:underline font-medium">${it.source}</a><span class="text-slate-500 block text-xs">${it.note||''}</span></li>`;
      });
      h += '</ul></div>';
    }
    out.innerHTML = h || '<p class="text-slate-500">No results</p>';
  } catch(err) {
    out.innerHTML = `<p class="text-red-400">${err}</p>`;
  }
};
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return PAGE

@app.post("/api/search")
async def search(
    file: UploadFile = File(...),
    use_facecheck: bool = Form(False),
):
    image_bytes = await file.read()
    result = {"osint": None, "facecheck": None}
    if osint:
        result["osint"] = osint.search(image_bytes)
    if use_facecheck and facecheck:
        result["facecheck"] = facecheck.search(image_bytes)
    return JSONResponse(result)

@app.get("/health")
async def health():
    return {"status": "ok", "facecheck": bool(os.getenv("FACECHECK_API_TOKEN"))}
