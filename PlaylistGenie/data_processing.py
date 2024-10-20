import spotipy
import pandas as pd

# Function to fetch track data once
def fetch_track_data(track_id, sp):

    try:    
        track_info = sp.track(track_id) if track_id != 'Not available' else None
        
        if track_info is None:
            return None
        
        track_name = track_info['name']
        artists = ', '.join([artist['name'] for artist in track_info['artists']])
        album_name = track_info['album']['name']
        album_id = track_info['album']['id']
        popularity = track_info['popularity']
        release_date = track_info['album']['release_date']

        audio_features = sp.audio_features(track_id)
        if audio_features and isinstance(audio_features, list) and audio_features[0] is not None:
            audio_features = audio_features[0]
        else:
            audio_features = None

        track_data = {
            'Track Name': track_name,
            'Artists': artists,
            'Album Name': album_name,
            'Album ID': album_id,
            'Track ID': track_id,
            'Popularity': popularity,
            'Release Date': release_date,
            'Danceability': audio_features['danceability'] if audio_features else None,
            'Energy': audio_features['energy'] if audio_features else None,
            'Key': audio_features['key'] if audio_features else None,
            'Loudness': audio_features['loudness'] if audio_features else None,
            'Mode': audio_features['mode'] if audio_features else None,
            'Speechiness': audio_features['speechiness'] if audio_features else None,
            'Acousticness': audio_features['acousticness'] if audio_features else None,
            'Instrumentalness': audio_features['instrumentalness'] if audio_features else None,
            'Liveness': audio_features['liveness'] if audio_features else None,
            'Valence': audio_features['valence'] if audio_features else None,
            'Tempo': audio_features['tempo'] if audio_features else None,
        }

        return track_data
    
    except Exception as e:
        print(f"Error fetching data for track {track_id}: {e}")
        return None

def get_playlist_data(playlist_id, access_token):
    sp = spotipy.Spotify(auth=access_token)
    music_data = []

    playlist_tracks = sp.playlist_tracks(playlist_id, fields='items(track(id))')
    
    # Extract relevant information and store it in a list of dictionaries
    for track_info in playlist_tracks['items']:
        track_id = track_info['track']['id']
        track_data = fetch_track_data(track_id, sp)

        if track_data:
            music_data.append(track_data)

    # Create a pandas DataFrame from the list of dicts
    df = pd.DataFrame(music_data)
    return df

# Function --> Queries based on specific aritsts from spotify 
def get_spotify_library_data(artist_name, access_token, genre=None, limit=50):
    sp = spotipy.Spotify(auth=access_token)
    spotify_music_data = []
    seen_tracks = set()  # used to keep track of tracks already seen
    
    if genre:
        results = sp.search(q=f'genre:{genre}', type='track', limit=limit)
    else:
        results = sp.search(q=f"artist:{artist_name}", type='track', limit=limit)  # query searches based on the artist name
    
    #Getting track details 
    for track_info in results['tracks']['items']:
        track_id = track_info['id']
        track_name = track_info['name']
        artists = ', '.join([artist['name'] for artist in track_info['artists']])
        artists_list = [artist['name'] for artist in track_info['artists']] #list of artists for that specific track 

        track_signature = (track_name, artists)
        main_artist = artists_list[0] #filtering based on the first artist that shows up 
        
        if main_artist.lower() != artist_name.lower():
            continue #we skip tracks by other artists whose name isn't the same as the main_arist

        if track_signature in seen_tracks:
            continue  # skips duplicate tracks -- so we don't return any duplicates

        seen_tracks.add(track_signature)

        # Fetch track data
        track_data = fetch_track_data(track_id, sp)

        if track_data:
            spotify_music_data.append(track_data)

    return pd.DataFrame(spotify_music_data)
