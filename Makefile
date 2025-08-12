install: 
	pip install -r requirements.txt
dev:
	uvicorn app.main:create_app --reload --port 8000
