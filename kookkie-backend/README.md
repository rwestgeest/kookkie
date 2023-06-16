## Kookkie Back-end

## Libraries

Get Python lib versions:
```
pip freeze -r requirements.txt
```

Check & upgrade Python library versions:
```
pip list --outdated
vim requirements.txt
pip install --upgrade -r requirements.txt
```

## DB migrations

After changing the database mapping, generate a new migration via:
```
./migrate.py <migration message>
```

## Debt

- Remove CORS fix for local development
- Introduce Proxy
