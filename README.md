# <img src="ddlogo.png" width="70px" height="90px"> DataDoorway (DD)
DataDoorway simplifies your data transfer between data multiverse.
```
curl --location --request POST 'http://localhost:8999/v1/kafka \
--header 'Content-Type: application/json' \
--data-raw '{
      "event": {
        "order_id" : 1234
        "item" : "door"
        "price" : 150
        "currency" : "dollar"
      },
      "env": "test"
}'
```
