

````
docker build -t iris-api .
````

````
docker run -d -p 5000:5000 --name iris-api iris-api
````

```
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"features\": [5.1, 3.5, 1.4, 0.2]}"
```

