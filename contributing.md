## How to contribute?
* create new brunch from master with one of prefixes ('fix-', 'feature-', 'model-', 'experiment-')
* add changing to files with tests (pytest)
* check linters/formatters with pre-commit hooks (scroll down for more info)
* ask review for commit to master branch


## Linters and formatters
In project's used pre-commit hooks which checks following linters/formatters:
* flake8 (linter) # poetry run flake8 --exclude=venv .
* black (auto formatter) # poetry run black .
* isort (import sorting) # poetry run isort .
* mypy (type checking) # poetry run mypy --explicit-package-bases --exclude venv .

also in project's used:
* pytest (tests)
* pre-commit

for install pre-commit hooks / install for each commit:
```commandline
pre-commit autoupdate
poetry run pre-commit install
poetry run pre-commit install -t pre-commit
```
for check hooks before commit:
```commandline
poetry run pre-commit run --all-files
```
all restrictions for linters you can find in pyproject.toml file
