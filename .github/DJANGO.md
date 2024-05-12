# DJANGO WEB APP TUTORIAL

https://learn.microsoft.com/en-us/windows/python/

## Development Setup

> Install Linux packages

```bash
sudo apt-get install -y python3 python3-pip python3-venv python-is-python3 python3-tk
```

> Upgrade Pip

```bash
python3 -m pip install --upgrade pip
```

> Create New Project

```bash
mkdir djangoApp
cd djangoApp/
```

> Virtual env create

```bash
python3 -m venv .venv

source .venv/bin/activate

.\.venv\Scripts\activate.ps1
```

> Dependencies.

```bash
py -m pip install django
```

> Python new project starter

```bash
django-admin startproject config .

py manage.py makemigrations

py manage.py migrate
```

> Python new api starter

```bash
py manage.py startapp core

py manage.py createsuperuser
```

> [localhost:8000](http://localhost:8000) > App running.

```bash
chmod +x manage.py

py manage.py runserver 8000
```

> Pip show installed package info

```bash
py -m pip show $package_name
```

> Pip create dependency file

```bash
py -m pip freeze > requirements.txt
```

> Pip install dependencies

```bash
py -m pip install -r requirements.txt
```

> Pip update dependencies

```bash
py -m pip install -U -r requirements.txt
```

> Pip installed list

```bash
py -m pip list
```

> Pip uninstall package

```bash
py -m pip uninstall -y $package_names
```

> Pip uninstall all packages

```bash
py -m pip uninstall -r requirements.txt -y
```

### Pip

[Pipenv Guide](https://realpython.com/what-is-pip/)

### Django setup

[Django Setup](https://code.visualstudio.com/docs/python/tutorial-django)
