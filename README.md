create environment

```bash
conda create -n name python=3.7 -y
```

activate environment
```bash
conda activate name
```

create a requirements file and install the req
```bash
pip install requirements.txt
```

```bash
git init
```

```bash
dvc init
```

dvc add will track the data file 
```bash
dvc add data_given/winequality.csv
```

Pushing it to github
```bash
git add . && git commit -m 'first commit'

git remote add origin url

git branch -M main

git push origin main

git push origin main -f
```

comment to commit dvc stages, it will commit a new stages & leave already commited stages

```bash
dvc repro
```

dvc comments to view parmas and scores, also show diff 

```bash
dvc metrics show

dvc metrics diff
```

create tox file and tests folder
```bash
touch tox.ini
touch pyproject.toml
touch setup.py

mkdir tests
touch tests/conftest.py tests/test_config.py tests/__init__.py tests/schema_in.json
```

tox command -
```bash
tox
```

for rebulding tox -
```bash
tox -r
```

pytest command
```bash
pytest -v
```

setup commands - for local package install
```bash
pip install -e .
```

build your own package commands-
```bash
python setup.py sdist bdist_wheel
```

to create a new folders
```bash
mkdir -p .github/workflows/
```