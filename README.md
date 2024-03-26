# TTEX

## Local development

### Frontend

1. **Create venv**

```
python -m venv .venv
```

2. **Activate .venv**

```
source .venv/Scripts/activate
```

3. **Install requirements**

```
cd ttex/ && pip install -r requirements.txt
```
4. **Export environment variables**
```
export MYENV=value
```

5. **Run development server**

```
python manage.py runserver 0.0.0.0:8000
```


### Backend

**Start celery worker**

```
redis-server

// navigate to ttex/
celery -A ttex worker -l INFO
```
