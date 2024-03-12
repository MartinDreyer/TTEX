# TTEX

## Local development

**Start python server**

```
python3 manage.py runserver 0.0.0.0:8000
```

**Start celery worker**

```
redis-server

// navigate to ttex/
celery -A ttex worker -l INFO
```
