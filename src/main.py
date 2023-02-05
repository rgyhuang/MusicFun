# # adapted from emotify model
# # Helper libraries
import pandas as pd
import numpy as np
import random
from keras_preprocessing.sequence import pad_sequences
from keras.preprocessing import text
from tensorflow import keras
from sklearn.model_selection import train_test_split
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from recommendHelper import *

# set model parameters
TOP_K = 10000
MAX_SEQUENCE_LENGTH = 28

# adjust parameters
NUMARTISTS = 10;
NUMTRACKS = 20;
MAXARTISTINDEX = NUMARTISTS - 1;
MAXTRACKINDEX = NUMTRACKS - 1;
NUMRESULTS = 12;

app = Flask(__name__)
CORS(app)

#instatiate saved model
model = keras.models.load_model('../emotifyModel/my_model.h5', compile=False)

# load dataframe 
df = pd.read_pickle("df.pkl")
sentiment = df.pop("sentiment")
content = df

x_train, y_train, x_test, y_test = train_test_split(content, sentiment, test_size=0.20, shuffle=True, random_state=42)
print(" Training: size", x_train.shape[0])
print(" Validation size:",y_train.shape[0])
training_data = np.array(x_train.content)


# encode input string and pass into model
def tokenize_and_pad(input):
    tokenizer = text.Tokenizer(num_words=TOP_K)
    tokenizer.fit_on_texts(training_data)
    tokenized = tokenizer.texts_to_sequences(input)
    padded = pad_sequences(tokenized, maxlen=MAX_SEQUENCE_LENGTH)
    return padded

def predict_emo(input):
    encoded = tokenize_and_pad([input])
    return model.predict(encoded)

@app.route('/run_app', methods=['POST'])
def main():
  prompt = request.args.get('value')
  print(prompt+ " was send to server")

  emotion = np.argmax(predict_emo(prompt))
  # generate random artist and track seeds
  seedArtistIndex = round(random.randrange(0, MAXARTISTINDEX));
  seedTrackIndex = round(random.randrange(0, MAXTRACKINDEX));
  
  headers = {
    'Authorization' : 'Bearer {}'.format(os.getenv('SPOTIFY_TOKEN'))
  }
  # get recommendation url and send request
  recommendationsURL = generateRecommendURL(emotion, seedArtists[emotion][seedArtistIndex],
                                            seedTracks[emotion][seedTrackIndex], NUMRESULTS)
  response = requests.get(recommendationsURL,headers=headers)
  data = json.loads(response.text)
  
  # write request to output.json
  with open("output.json", "w") as outfile:
      json.dump(data, outfile)

  return jsonify({'reply':'success'})

if __name__ == "__main__":
    app.run(debug=True)



