# <img src="ddlogo.png" width="70px" height="90px"> DataDoorway (DD)
DataDoorway simplifies your data transfer in the data multiverse. For example sending data from a microservice to 
######  For example sending data from a microservice to Kafka
```
curl --location --request POST 'http://localhost:8999/v1/kafka \
--header 'Content-Type: application/json' \
--data-raw '[{
      "event": {
        "order_id" : 1234
        "item" : "door"
        "price" : 150
        "currency" : "dollar"
      }],
}'
```
###### For example sending data from a microservice to AWS S3
```
curl --location --request POST 'http://localhost:8999/v1/s3 \
--header 'Content-Type: application/json' \
--data-raw '[{
      "event": {
        "order_id" : 1234
        "item" : "door"
        "price" : 150
        "currency" : "dollar"
      }],
}'
```
###### For example sending data from a microservice to multiple sources
```
curl --location --request POST 'http://localhost:8999/v1/send \
--header 'Content-Type: application/json' \
--header 'X-Source-List: kafka,s3,bigquery' \
--data-raw '[{
      "event": {
        "order_id" : 1234
        "item" : "door"
        "price" : 150
        "currency" : "dollar"
      }],
}'
```

### Key Features

- Inbuilt Auth using EasyAuth
- Send data to multiple sources simultaneously 
- Validations like
  
  - CORS
  - Schema checks 
  - Regex based data validations
  - Payload checks (size, content-type, ...)
- Regex based routing on headers / data fields 
- Supports custom connectors 