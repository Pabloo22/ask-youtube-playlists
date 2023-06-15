check_lint:
	poetry run flake8
	poetry run mypy

run_app:
	poetry run streamlit run web_app/Load.py
