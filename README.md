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
4. **Create user**
```
python manage.py createsuperuser
```

5. **Export environment variables**
```
export MYENV=value
```

6. **Run development server**
```
python manage.py runserver 0.0.0.0:8000
```

7. **Login**
Go to localhost:8000/admin and type in your login info


### Backend

**Start celery worker**

```
redis-server

// navigate to ttex/
celery -A ttex worker -l INFO
```
