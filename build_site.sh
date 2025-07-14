#!/bin/bash
cd fast-html
python main.py --config-file ../fast-html.ini
cd ../fsweb
python main.py --source-dir ../fast-html/generated_html/ --output-dir fsweb_generated --theme dark --wrapper --search --breadcrumb
