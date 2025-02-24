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
    "error": "page not found for the given movie name and year."
}
```

---
## UML
<img width="662" alt="Screenshot 2025-02-24 at 12 00 09 PM" src="https://github.com/user-attachments/assets/7b3d6227-0461-4c3b-8072-8f122fffa01e" />



---

## Dependencies
Because I don't use an API call, you need to make sure you have pyzmq to use beautifulsoup4:

```bash
pip install pyzmq requests beautifulsoup4
```

---
