import os
from werkzeug.serving import run_simple

from web import app
app.debug = True

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    run_simple('0.0.0.0', port, app, use_reloader=True)
