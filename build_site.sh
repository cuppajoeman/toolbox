#!/bin/bash
set -euo pipefail

PYTHON=${PYTHON:-/usr/bin/python}

cd fast-html
"$PYTHON" main.py --config-file ../fast-html.ini
cd ../fsweb
"$PYTHON" main.py --source-dir ../fast-html/generated_html/ --output-dir fsweb_generated --theme dark --wrapper --search --breadcrumb
