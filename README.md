# website-backend

Backend API for [shu's website](https://github.com/ceshmina/website) on Cloud Functions

## Development

```
cd sample
pipenv run functions-framework --target get_diaries --debug
curl "localhost:8080?month=202305"
```

## Deployment

For now, manual deployment is necessary. First, create `requirements.txt` using the following command:

```
pipenv requirements > requirements.txt
```

Then deploy `requirements.txt` and desired function's `main.py` from the Cloud Functions console.
