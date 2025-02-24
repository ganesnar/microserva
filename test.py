import zmq
import csv

def request_imdb_link(movie_name, year):
    """Sends a request to the IMDb lookup microservice and receives the IMDb link."""
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    
    request_data = {"movie_name": movie_name, "year": year}
    socket.send_json(request_data)
    response = socket.recv_json()
    return response

def main():
    csv_filename = "movies.csv"

    with open(csv_filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            movie_name = row["movie_name"].strip()
            year = row["year"].strip() if row["year"].strip() else None
            
            response = request_imdb_link(movie_name, year)
            print(f"Movie: {movie_name}, Year: {year}, Response: {response}")

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send_json({"shutdown": True})  # Send shutdown request
    socket.recv_json()

main()




