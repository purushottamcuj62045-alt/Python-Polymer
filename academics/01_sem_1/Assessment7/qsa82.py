'''A movie rating system is a way of evaluating and scoring films based on 
various criteria, often to help audiences determine the quality or suitability 
of a movie. There are several types of movie rating systems in use today, 
ranging from simple star-based systems to more complex scoring methods.
 As a python developer You need to build a simple system that stores movie 
 ratings (Star Rating System (1–5 stars)). Each movie's title will be the 
 key, and its rating will be the value (Star Rating System (1–5 stars)).
   Following are the requirements of the system given below:

Requirements:

•	Store Movie Ratings: Create a dictionary where the key is the movie title, and the
value is the movie's rating (Star Rating System (1–5 stars)).
o	Example: {'Inception': 9, 'Avatar': 8, 'Titanic': 7}
•	Add a New Movie: Write a function to add a new movie with its title and rating.
•	Update Movie Rating: Implement a function that allows the user to update the rating of a movie.
•	Delete a Movie: Write a function to delete a movie from the system.
•	Find the Highest Rated Movie: Write a function to find the highest-rated movie.
 
•	Average Rating: Implement a function to calculate the average rating of all movies.

'''
movies = {
    'Inception': 9,
    'Avatar': 8,
    'Titanic': 7,
    'The Dark Knight': 10,
    'Interstellar': 9,
    'The Godfather': 10,
    'Pulp Fiction': 8,
    'The Shawshank Redemption': 10,
    'Forrest Gump': 9,
    'The Matrix': 9,
    'Gladiator': 8,
    'The Lord of the Rings: The Return of the King': 10,
    'Schindler\'s List': 10,
    'Fight Club': 8,
    'The Silence of the Lambs': 9,
    'Jurassic Park': 7,
    'The Avengers': 8,
    'Spider-Man: No Way Home': 9,
    'Black Panther': 8, 
    'Wonder woman': 7
}
def add_movie(title, rating):
    """Add a new movie with its title and rating."""
    movies[title] = rating
    print(f"Movie '{title}' added with rating {rating}.")
def update_movie_rating(title, new_rating):
    """Update the rating of an existing movie."""
    if title in movies:
        movies[title] = new_rating
        print(f"Movie '{title}' updated to new rating {new_rating}.")
    else:
        print(f"Movie '{title}' not found.")
def delete_movie(title):
    """Delete a movie from the system."""
    if title in movies:
        del movies[title]
        print(f"Movie '{title}' deleted.")
    else:
        print(f"Movie '{title}' not found.")
def find_highest_rated_movie():
    """Find the highest-rated movie."""
    if movies:
        highest_rated_movie = max(movies, key=movies.get)
        print(f"Highest rated movie: '{highest_rated_movie}' with rating {movies[highest_rated_movie]}.")
    else:
        print("No movies available.")
def calculate_average_rating():
    """Calculate the average rating of all movies."""
    if movies:
        average_rating = sum(movies.values()) / len(movies)
        print(f"Average rating of all movies: {average_rating:.2f}")
    else:
        print("No movies available.")
# Example usage
add_movie('Coco', 8)
update_movie_rating('Avatar', 9)
delete_movie('Titanic')
find_highest_rated_movie()
calculate_average_rating()
#<-- IGNORE --->
