from sklearn.feature_selection import chi2
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from scipy.stats import chi2_contingency
import shutil
import os
import nltk
nltk.download('punkt')
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity

def calc_chi (O1,O2):

    E = np.mean([O1, O2])
    chi2_value = np.sqrt((pow((O1 - E), 2) + pow((O2 - E), 2)) / E)

    return chi2_value

def calculate_cosine_distance(v1,v2):
    if (len(v1)<len(v2)):
        padded_v1 = np.pad(v1,(0,len(v2)-len(v1)),mode ='constant')
        v1 = padded_v1
    if (len(v1)>len(v2)):
        padded_v2 = np.pad(v2,(0,len(v1)-len(v2)),mode ='constant')
        v2 = padded_v2

    v1 = v1.reshape(1, -1)
    v2 = v2.reshape(1, -1)
    # Calculate cosine similarity between the two vectors
    similarity = cosine_similarity(v1, v2)
    # Return the similarity value
    return similarity[0][0]

def create_initial_segemtns(input):
    df_songs = pd.read_csv(input)
    output_filepath = 'Second article/initial_segments.csv'
    if os.path.exists(output_filepath):
        os.remove(output_filepath)

    # Createing an empty dataset with the required columns //change to "initial segments.csv later"
    df_initial = pd.DataFrame(columns=['Year/Initial Segment', 'Number of Songs', 'Segment'])
    df_initial.to_csv(output_filepath, index=False)
    currSegment = 1
    for i in range(0,df_songs.shape[0]):
        currYear = df_songs.at[i, 'year']
        toRemove = currYear % 10
        currYear = currYear - toRemove
        
        if (df_initial['Year/Initial Segment'] == str(currYear) + "'s").any():
            rowstoedit = df_initial[df_initial['Year/Initial Segment'] == str(currYear) + "'s"].index
    
            for rowtoedit in rowstoedit:
                currNumOfSongs = df_initial.at[rowtoedit, "Number of Songs"]
                df_initial.at[rowtoedit, "Number of Songs"] = currNumOfSongs + 1
                df_initial.to_csv(output_filepath, index=False)

        else:
            new_row = {'Year/Initial Segment': str(currYear) + "'s", 'Number of Songs': 1, 'Segment': np.nan}
            new_row_df = pd.DataFrame([new_row])
            # Append the new row to the DataFrame
            df_initial = pd.concat([df_initial, new_row_df], ignore_index=True)
            df_initial.to_csv(output_filepath, index=False)


    df_sorted = df_initial.sort_values(by='Year/Initial Segment').reset_index(drop=True)

    for i in range(0,df_sorted.shape[0]):
        df_sorted.at[i,"Segment"] =  "S" + str(currSegment)

        currSegment = currSegment + 1

    df_sorted.to_csv(output_filepath, index=False)

#This function runs the chi-squar test presented in the article, and generates a new segmentation for the songs based on its results
def segment_generation_by_chi_test(significance_level=0.05):
    
    #Setting paths for input and output
    input_filepath = 'Second article\initial_segments.csv'
    output_filepath = 'Second article\chi_square_segments.csv'

    if os.path.exists(output_filepath):
        os.remove(output_filepath)

    #Copying the "initial segments" csv and work on its copy
    shutil.copy2(input_filepath, output_filepath)

    df_initial = pd.read_csv(output_filepath)
    #Converting "Segment" column to type 'str'
    df_initial['Segment'] = df_initial['Segment'].astype(str)
    #Setting first Segment as S1
    df_initial.at[0, "Segment"] = "S1"
    df_initial.to_csv(output_filepath, index=False)

    #Setting index for new proposed segments
    j = 2

    #For each neighboring segments, calculating the chi-squar value and deciding on combining them or not
    for i in range(0,df_initial.shape[0] - 1):
        O1 = df_initial.loc[i, 'Number of Songs']
        O2 = df_initial.loc[i + 1, 'Number of Songs']
        chi2_value = calc_chi(O1, O2)

        #Choose weather to combine the segments or not based on the chi-squar value
        if chi2_value < significance_level:
            print("chi test - segments " + df_initial.at[i, "Segment"] + " and " + df_initial.at[i+1, "Segment"] + " chose to combine")
            df_initial.at[i+1, "Segment"] = df_initial.at[i, "Segment"]
        else:
            df_initial.at[i+1, "Segment"] = "S" + str(j)
            j = j + 1
        df_initial.to_csv(output_filepath, index=False)  


#This function gets a block of text representing all the song in specific segment, and returns a feature vector for this segment
def create_feature_vector_for_segment(text):

    # Tokenize the text into words
    words = word_tokenize(text)
    # Generate bigrams
    bigrams = list(ngrams(words, 2))
    # Count bigram frequencies in the text
    bigram_freqs = Counter(bigrams)

    total_bigrams = sum(bigram_freqs.values())

    # Initialize a NumPy array to store the feature vector
    unique_bigrams = list(bigram_freqs.keys())
    feature_vector = np.zeros(len(unique_bigrams))

    # Populate the feature vector with normalized frequencies
    for i, bigram in enumerate(unique_bigrams):
        feature_vector[i] = bigram_freqs[bigram] / total_bigrams

    return feature_vector



# This function runs a document similarity measure based on feature vectors between neighboring segments (based on the chi-squar test), 
# and decides on combining them or not
def segment_generation_by_feature_vectors(similarityThreshold=0.7):
    # Songs csv
    songs_filepath = 'Second article\songs.csv'    
    # Chi-square segments csv
    chi_square_segments = 'Second article\chi_square_segments.csv'
    # Final suggested segments csv
    suggested_segments_filepath = 'Second article\suggested_segments.csv'

    if os.path.exists(suggested_segments_filepath):
        os.remove(suggested_segments_filepath)

    shutil.copy2(chi_square_segments,suggested_segments_filepath)
    
    df_songs = pd.read_csv(songs_filepath)

    df_suggested_segments = pd.read_csv(suggested_segments_filepath)

    #df_final_segments = pd.read_csv(chi_square_segments)
    
    unique_segments = df_suggested_segments['Segment'].unique()
    feature_vector_per_segment = {}

   
    # for each segemnt, calculate the feature vector
    for i in range(0,len(unique_segments)):
        currSegment = unique_segments[i]
        for j in range(0,df_suggested_segments.shape[0]):
            if df_suggested_segments.at[j, 'Segment'] == currSegment:
                currSegmentYear = df_suggested_segments.at[i, 'Year/Initial Segment']
                currSegmentYear = currSegmentYear[:-2]
                currText = ""
                mask = df_songs['year'].astype(str).str.startswith(currSegmentYear[:-1])
                songsOfCurrentSegment = df_songs[mask]
                
                for index, row in songsOfCurrentSegment.iterrows():
                    currText = currText + row['songcontent']

        feature_vector = create_feature_vector_for_segment(currText)
        feature_vector_per_segment[currSegment] = feature_vector

    newSegments = np.full(len(unique_segments) + 1, '', dtype='<U10')
    newSegments[1] = "S1"
   # calculate similarity with cosin methid between each neighboring segments
    for i in range(0,len(unique_segments) - 1):
        currSegment = unique_segments[i]
        nextSegment = unique_segments[i+1]

        v1 = feature_vector_per_segment[currSegment]
        v2 = feature_vector_per_segment[nextSegment]

        similariity = calculate_cosine_distance(v1, v2)

        if similariity > similarityThreshold:
            print("feature vector - segments " + currSegment + " and " + nextSegment + " chose to combine")
            newSegments[int(nextSegment[-1])] = newSegments[int(currSegment[-1])]
        else:
            newSegments[int(nextSegment[-1])] = "S" + str(int(newSegments[int(currSegment[-1])][-1]) + 1)

    for i in range(0,df_suggested_segments.shape[0]):
        currSegmentIndex = int(df_suggested_segments.at[i, 'Segment'][-1])
        df_suggested_segments.at[i, 'Segment'] = newSegments[currSegmentIndex]
        df_suggested_segments.to_csv(suggested_segments_filepath, index=False)  


def print_before_and_after():
    print("Before chi-square test:")
    print(pd.read_csv('Second article\initial_segments.csv'))
    print("After chi-square test:")
    print(pd.read_csv('Second article\chi_square_segments.csv'))
    print("After feature vector:")
    print(pd.read_csv('Second article\suggested_segments.csv'))
    
if __name__ == "__main__":

    chi_significance_level = 0.5
    cosine_similarityThreashold = 0.6

    # Creation of initial segments for the texts - in this example - based on decaeds
    create_initial_segemtns('Second article\songs.csv')
    #First iteration of segment combinaiton using Chi-Square Test
    segment_generation_by_chi_test(chi_significance_level)
    #Second iteration of segment combinaiton using Similarity Measure of feature vectors
    segment_generation_by_feature_vectors(cosine_similarityThreashold)
    print_before_and_after()


