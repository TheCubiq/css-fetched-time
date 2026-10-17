from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from flask import Flask, Response, request


app = Flask(__name__)


@app.get("/")
def serve_time_svg():
    timezone = request.headers.get("x-vercel-ip-timezone")
    try:
        now = datetime.now(ZoneInfo(timezone)) if timezone else datetime.now()
    except (ZoneInfoNotFoundError, ValueError):
        now = datetime.now()

    total_seconds = now.hour * 3600 + now.minute * 60 + now.second

    svg_data = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_seconds}" height="50">'
        f'<rect width="100%" height="100%" fill="#CAFEBABE"/>'
        f'</svg>'
    )

    res = Response(svg_data, mimetype="image/svg+xml")
    res.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return res
