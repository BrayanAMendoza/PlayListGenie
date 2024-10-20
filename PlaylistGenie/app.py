from flask import Flask, render_template, request 
from auth import access_token
from data_processing import get_playlist_data, get_spotify_library_data
from recommendation_system import content_based_recommendations
from spotipy.exceptions import SpotifyException 


app = Flask(__name__)

@app.route('/') 

#Getting the render_template from the index html form that contains playlist_id and song name 
def index():
    return render_template('index.html')


@app.route('/recommendations', methods = ['POST']) #Need to change to GET here bc we are getting info when we are going to /recommend 

def recommend():

    playlist_id = request.form.get("playlist_id")
    song_name = request.form.get("song_name")
    artist_name = request.form.get("artist_name")

    #validating that the user has entered something into the text boxes
    
    if not playlist_id or not song_name:
        message = "please enter a valid playlist_ID, Song Name, and artist name"
        return render_template("song_rec.html", message= message)

    try:
        userPL_music_df = get_playlist_data(playlist_id, access_token) #gets data based on users entered playlist
        spotify_music_df = get_spotify_library_data(artist_name, access_token)


    except SpotifyException as e:
        message = f"Invalid playlist ID: {e}"    
        return render_template("index.html", message = message)
    
    recommendations = content_based_recommendations(userPL_music_df, song_name, num_recommendations = 5)
    recommendations2 = content_based_recommendations(spotify_music_df, song_name, num_recommendations=5)

    #recommendations = recommendations.to_dict(orient = 'records') #converting from pd df to a dictionary to be able to loop through the segment 

    if not recommendations.empty and not recommendations2.empty:

        recommendations_list = recommendations.to_dict(orient = 'records')
        recommendations2_list = recommendations2.to_dict(orient = 'records')
    
        combined_output = recommendations_list, recommendations2_list

        return render_template('song_rec.html', recommendations = combined_output) #Should return both of the 2 reocmmendation lists
    
        #old return statement below: 
        #return render_template('song_rec.html', recommendations = recommendations_list)
    
    else:
        message = "No recommendations found for the given song"
        return render_template("index.html", message = message)
    #return (render_template('index.html', recommendations = recommendations))

if __name__ == "__main__":
    app.run(debug = True) 


