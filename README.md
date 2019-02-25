# LIGHTWEIGHT FLASK BOILERPLATE

## INSTALLING

Copy env.example to .env
```
cp env.example .env
```
setting your environment

```
pip install -r requirements.txt
```

## DATABASE
Installing InfluxDB Reference [action](https://docs.influxdata.com/influxdb/v1.7/introduction/installation/)

## DEVELOPMENT

```
python manager.py server
```

## PRODUCTION
using gunicorn run
```
sh run.sh
```