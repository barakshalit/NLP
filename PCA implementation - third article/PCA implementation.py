import pandas as pd
import json
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def addtomatrix(directory_path, label):
    # Initialize lists to store the data
    lyrics_list = []
    noun_counts = []
    avg_sentence_lengths = []

    # Iterate through each JSON file in the directory
    for filename in os.listdir(directory_path):
        
        filepath = os.path.join(directory_path, filename)
            
        # Load JSON data
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract and calculate the required information
        lyrics_list.append(data['text'])
            
        nouns = sum(1 for token in data['tokens'] if token['morph']['pos'] == 'VERB')
        noun_counts.append(nouns)
            
        sentences = data['text'].split('\n')  # Split by newline characters
        sentences = [s.strip() for s in sentences if s]
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        avg_sentence_lengths.append(avg_length)

    # Create a DataFrame for the current directory
    df_temp = pd.DataFrame({
        'lyrics': lyrics_list,
        'noun_count': noun_counts,
        'avg_sentence_length': avg_sentence_lengths
    })
    
    # Add a label column
    df_temp['label'] = label
    
    return df_temp

# Path to the directories containing the JSON files
directory_path_old = 'BERT analysis\outputs\Dor Ha-Medina BERT output'
directory_path_new = 'BERT analysis\outputs\Present BERT output'

# Create DataFrames for old and new songs
df_old = addtomatrix(directory_path_old, 'old')
df_new = addtomatrix(directory_path_new, 'new')

# Combine the DataFrames
df = pd.concat([df_old, df_new], ignore_index=True)

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[['noun_count', 'avg_sentence_length']])

# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Plot
plt.figure(figsize=(10, 8))
for label in df['label'].unique():
    plt.scatter(X_pca[df['label'] == label, 0], X_pca[df['label'] == label, 1], label=label, alpha=0.7)

plt.title('PCA Visualization of Songs with Noun Counts and Avg Sentence Length')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.show()
