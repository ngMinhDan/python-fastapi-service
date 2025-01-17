install: 
	pip install -r requirements.txt

run: ## Run the FastAPI app.
	uvicorn app:app --reload --port 8000

clean: ## Clean up the project.
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete

