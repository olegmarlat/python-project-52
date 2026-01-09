install:
	uv sync

build:
    ./build.sh

render-start:
    gunicorn task_manager.wsgi

test:
	uv sync
	python manage.py migrate 
    pytest



