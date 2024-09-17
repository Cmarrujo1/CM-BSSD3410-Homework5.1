from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv('API_KEY')


FILM_LIST_PATH = "https://api.themoviedb.org/3/discover/movie"
CREDITS_LIST_PATH = "https://api.themoviedb.org/3/movie/{}/credits"
RELEASE_DATE = "2018-01-01"


MEGAN_ID = "19537"
MARGOT_ID = "234352"

def get_film_list(actor_id):
    params = {
        "api_key": api_key,
        "with_people": actor_id,
        "primary_release_date.gte": RELEASE_DATE
    }
    response = requests.get(FILM_LIST_PATH, params=params)
    return response.json()

def data_to_set(data):
    film_set = set()
    if 'results' in data:
        for res in data['results']:
            film_set.add(res['title'])
    return film_set

def find_shared_movies(actor1_id, actor2_id):
    actor1_films = get_film_list(actor1_id)
    actor2_films = get_film_list(actor2_id)

    set_actor1 = data_to_set(actor1_films)
    set_actor2 = data_to_set(actor2_films)

    shared_films = set_actor1.intersection(set_actor2)

    if shared_films:
        print("Shared films:")
        for film in shared_films:
            print(f"- {film}")
    else:
        print("No current films in common.")

def search_actor_id(name):
    url = "https://api.themoviedb.org/3/search/person"
    params = {"api_key": api_key, "query": name}
    response = requests.get(url, params=params)
    data = response.json()
    if data['results']:
        return data['results'][0]['id']
    else:
        print(f"No actor found with the name {name}.")
        return None

def main():
    print("Welcome to the Actor Finder!")
    print("\nTo find an actor's ID, you can search on The Movie Database website or use this program.")
    print("Alternatively, you can use actor IDs.")


    choice = input("Do you want to use actor IDs for testing? (yes/no): ").strip().lower()
    if choice == 'yes':
        print(f"\nComparing films of actors with IDs: Megan (ID: {MEGAN_ID}) and Margot (ID: {MARGOT_ID})...")
        find_shared_movies(MEGAN_ID, MARGOT_ID)
    else:
        actor1_name = input("Please enter the name of the first actor: ").strip()
        actor2_name = input("Please enter the name of the second actor: ").strip()

        actor1_id = search_actor_id(actor1_name)
        actor2_id = search_actor_id(actor2_name)

        if actor1_id and actor2_id:
            print(f"Comparing films of {actor1_name} and {actor2_name}...")
            find_shared_movies(actor1_id, actor2_id)
        else:
            print("Cannot find the actor(s).")

if __name__ == "__main__":
    main()
