echo '=== Updating piplock ==='
pipenv update

echo '=== Running Pytest ==='
pipenv run pytest test

echo '=== Running autopep8 fixes === '
pipenv run autopep8 . -r --in-place

echo '=== Running flake8 ==='
pipenv run flake8 .