.PHONY: frontend-install frontend-build run build example install

frontend-install:
	cd packages/frontend && npm install

frontend-build:
	cd packages/frontend && npm run build

run:
	python main.py

build:
	call .\venv\Scripts\activate.bat && pyinstaller HertaLauncher.spec

install:
	pip install -r requirements.txt

example:
	cd .\packages\example && python example.py