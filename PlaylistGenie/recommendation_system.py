import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler


def content_based_recommendations(music_df, input_song_name, num_recommendations):
    if input_song_name not in music_df['Track Name'].values:
        print(f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
        return


    scaler = MinMaxScaler()
    music_features = music_df[['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo"]].values #need to check what .values does 
    music_features_scaled = scaler.fit_transform(music_features)

    # Get the index of the input song in the music DataFrame
    input_song_index = music_df[music_df['Track Name'] == input_song_name].index[0]

    #ADD something like the below -- to add more weight to some features in song -- personalize the recommendation system even more 
    #weighted_features = music_features_scaled * np.array([0.2, 0.2, 0.05, 0.1, 0.05, 0.05, 0.1, 0.05, 0.05, 0.1, 0.15])  # Example weights
    #imilarity_scores = cosine_similarity([weighted_features[input_song_index]], weighted_features)

    #Use consine similarity to calc similarity scores based on music_Features then find songs with most similarity scores
    similarity_scores = cosine_similarity([music_features_scaled[input_song_index]], music_features_scaled)
    similar_song_indices = similarity_scores.argsort()[0][::-1][1:num_recommendations + 1] 

    content_based_recommendations = music_df.iloc[similar_song_indices][['Track Name', 'Artists', 'Album Name', 'Release Date', 'Popularity']]
    return content_based_recommendations




