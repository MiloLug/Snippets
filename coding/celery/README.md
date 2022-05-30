## Requirements

```bash
pip install celery django-celery-beat

install redis-server
```

## Commands

```bash
celery -A main_app worker -c 1 --beat --scheduler django --loglevel=WARNING
```