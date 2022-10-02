Подготовка к запуску:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Запуск:
```
source venv/bin/activate
./manage.py runserver
```

Логин\пароль от админки: admin

роуты для получения списка товаров:
`/api/products/`
фильтры и поиск по гет параметрам: 
```
status
article
name
```
Получение конкретного товара:
`/api/products/{id}/`