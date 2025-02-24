# IMDb Lookup Microservice

## Overview
This microservice allows users to retrieve **IMDb links for movies** based on a provided **movie name and year**.  
It uses **ZeroMQ (ZMQ) for communication** and **scrapes Wikipedia** for accurate IMDb URLs (instead of using an API).  

## Communication contract
Please feel free to dm me on Discord or email me at ganesnar@oregonstate.edu

---

## Request Data (Send a Request)

To programmatically **request** data from the microservice, use a **ZeroMQ REQ (request) socket** and send a JSON object **containing the movie name and year**.

### **Example**
```python
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

request_data = {
    "movie_name": "Minions",
    "year": "2015"
}

socket.send_json(request_data)  # Send request to the microservice
response = socket.recv_json()   # Receive the response
print(response)
```

---

## Receive Data

The microservice responds with a JSON object, containing either an IMDb link or an error message.

### **Successful IMDb Link Response**
```json
{
    "imdb_link": "https://www.imdb.com/title/12312312312313/"
}
```

### **Error Response (Movie Not Found)**
```json
{
    "error": "IMDb link not found for the specified movie."
}
```

---


---

## Dependencies
Ensure you have the following installed before running:

```bash
pip install pyzmq requests beautifulsoup4
```

---
