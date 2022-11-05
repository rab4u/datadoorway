[Work in progress] - Not yet ready for use

![Code Coverage](coverage.svg)

# <img src="ddlogo.png" width="70px" height="90px"> DataDoorway (DD)
DataDoorway simplifies your data transfer in the data multiverse.
######  For example sending data from a microservice to Kafka
```
curl -X 'POST' \
  'http://localhost:8000/publish?publishers=kafka&publishers=s3&backup_publisher=bigquery&schema_id=sales.order.vq' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2NjYyMjQwMDAsInNjb3BlIjoiZGQ6YWRtaW4gcHVibGlzaDp3cml0ZSBtZXRyaWNzOnJlYWQifQ.q-Fncgu9LhHN49mUZ-c4DkaVtz0TyEIAedxyJKHZcVE' \
  -d '[{
      "event": {
        "order_id" : 1234
        "item" : "door"
        "price" : 150
        "currency" : "dollar"
      }],
}'
```

### Key Features

- Authorization using JWT Token
- Send data to multiple sources simultaneously 
- Validations like
  - CORS
  - Schema checks 
  - Regex based data validations
  - Payload checks (size, content-type, ...)
- Regex based routing on headers / data fields 
- Supports custom connectors 
