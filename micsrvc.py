import zmq
import csv
import time
import requests
from bs4 import BeautifulSoup


#API key wasnt working, so i parse from wikipedia
def wikipedia(movie_name, year):
    #"""Fetch the IMDb link from Wikipedia for a specific movie and year."""
    search_url = f"https://en.wikipedia.org/wiki/{movie_name.replace(' ', '_')}"

    response = requests.get(search_url)
    if response.status_code != 200:
        return {"error": "page not found for the given movie name and year."}

    soup = BeautifulSoup(response.text, "html.parser")
    imdb_link = None

   
    for link in soup.find_all("a", href=True):
        if "imdb.com/title" in link["href"]:
            imdb_link = link["href"]
            break

    return {"imdb_link": imdb_link} if imdb_link else {"error": "No IMDb link found for the given movie name and year."}

def load_movies(filepath):
    #"""Loads movie data from a CSV file."""
    movies = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            movies.append(row)
    return movies

def main():
    csv_filepath = "movies.csv"
    movies = load_movies(csv_filepath)

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")


    while True:
        request = socket.recv_json()

        
        if request.get("shutdown"):
            socket.send_json({"status": "Shutting down"})
            break  

        movie_name = request.get("movie_name", "").strip()
        year = request.get("year")

        if year:
            year = year.strip()
        else:
            year = None

        if not movie_name:
            socket.send_json({"error": "cannot be processed without a name"})
            continue

        if not year:
            socket.send_json({"error": "cannot be processed without a year"})
            continue

        movie_found = False
        for movie in movies:
            if movie["movie_name"].lower() == movie_name.lower() and movie["year"].strip() == year:
                movie_found = True
                break

        if not movie_found:
            socket.send_json({"error": "No matching movie found with the given name and year"})
            continue

        response = wikipedia(movie_name, year)
        time.sleep(1)  
        socket.send_json(response)

    socket.close()
    context.term()
    print("Bye!")


main()
