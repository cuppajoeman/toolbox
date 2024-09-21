#!/bin/bash
cd fast-html
python main.py --config-file ../fast-html.ini
cd ../fsweb
python main.py --base-dir ../fast-html/generated_html/ --gen-dir fsweb_generated --theme dark --wrapper --search --breadcrumb
