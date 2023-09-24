#!/usr/bin/bash
uwsgi --socket 127.0.0.1:3031 --plugin /usr/lib/uwsgi/plugins/python3_plugin.so --wsgi-file wsgi.py --callable app --master --processes 1 --threads 2
