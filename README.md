:heavy_exclamation_mark: [Generated from Python Template](https://github.com/KamilMatejuk/BlackSwanPythonTemplate) :heavy_exclamation_mark:

# Temporary Price Emitter
Regular Price Emitter doesn't have endpoints for timerange, so it will temporarly use a hardcoded json

## To start server:
```
echo 'PORT=8000' > .env.local
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --reload
```

## To use SwaggerUI
* update [openapi.yaml](openapi.yaml) based on [documentation](https://swagger.io/specification/)
* open http://127.0.0.1:8000/swagger-ui/
