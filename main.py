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
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from recommendHelper import *

app = Flask(__name__)
CORS(app)
@app.route('/run_app', methods=['POST'])
def main():
  prompt = request.args.get('value')
  print(prompt)
  print("clicked")
  # load dataframe 
  df = pd.read_pickle("df.pkl")
  sentiment = df.pop("sentiment")
  content = df

  x_train, y_train, x_test, y_test = train_test_split(content, sentiment, test_size=0.20, shuffle=True, random_state=42)
  print(" Training: size", x_train.shape[0])
  print(" Validation size:",y_train.shape[0])
  training_data, validation_data, training_label, validation_label = np.array(x_train.content), np.array(y_train.content), np.array(x_test), np.array(y_test)

  # set model parameters
  TOP_K = 10000
  MAX_SEQUENCE_LENGTH = 28
  num_classes = 4

  #instatiate saved model
  model = keras.models.load_model('emotifyModif/my_model.h5', compile=False)
  # categories for testing
  labels = ["anger", "fear", "happiness", "sadness"]

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

  # '''
  #   non transfer learning models
  #   labels = ["anger", "fear", "happiness", "sadness"]
  # '''
  # emotion = np.argmax(predict_emo("he's so scary"))
  # print(f"Predicted emotion: {labels[emotion]}")

  # emotion = np.argmax(predict_emo("I am over the moon"))
  # print(f"Predicted emotion: {labels[emotion]}")

  # emotion = np.argmax(predict_emo("dont hurt me"))
  # print(f"Predicted emotion: {labels[emotion]}")

  # emotion = np.argmax(predict_emo("I hate you"))
  # print(f"Predicted emotion: {labels[emotion]}")
  emotion = np.argmax(predict_emo(prompt))

  headers = {
    'Authorization' : 'Bearer {}'.format("BQCOmfaDb2_bSU4oEKCx8ZKfAO2JVVDeFrCaf-FmS9D1esGlOyyJRXsNErDttw9UVkaDySfybJ6cApo7sw_z8hYIagQ06MtsAYIu7q66WyZINjwcV3lDLHV9bAHmAi0UVZTjDe4hGQRXOyqM8BzZREFFu6sU6v8--4jB-1qj-vMn9cAAME6Zv87owKzA6hpvjRn-")
  }

  # adjust parameters
  NUMARTISTS = 10;
  NUMTRACKS = 20;
  MAXARTISTINDEX = NUMARTISTS - 1;
  MAXTRACKINDEX = NUMTRACKS - 1;
  NUMRESULTS = 5;

  seedArtistIndex = round(random.randrange(0, MAXARTISTINDEX));
  seedTrackIndex = round(random.randrange(0, MAXTRACKINDEX));
  recommendationsURL = generateRecommendURL(emotion, seedArtists[emotion][seedArtistIndex],
                                            seedTracks[emotion][seedTrackIndex], NUMRESULTS)
  response = requests.get(recommendationsURL,headers=headers)
  data = json.loads(response.text)
  
  with open("output.json", "w") as outfile:
      json.dump(data, outfile)

  return jsonify({'reply':'success'})

if __name__ == "__main__":
    app.run(debug=True)



