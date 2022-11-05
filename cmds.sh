# install poetry
curl -sSL https://install.python-poetry.org | python3 -

# poetry path setting
export PATH="/Users/ravi/Library/Python/3.10/bin:$PATH"

# poetry to create .venv in the project
poetry config virtualenvs.in-project true

# to check info about virtual env
poetry env info

# activate virtual env
source .venv/bin/activate or source $(poetry env info --path)/bin/activate

# add package using poetry
poetry add fastapi

# run DataDoorway
export ENV_FILE=prod.env
uvicorn main:app --reload --reload-include $ENV_FILE

# run pytest
pytest

# run coverage
coverage run -m pytest
coverage report

# coverage badge
pip3 install readme-coverage-badger
coverage run -m pytest
coverage report
coverage-badge -f -o coverage.svg