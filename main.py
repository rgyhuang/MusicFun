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
  training_data = np.array(x_train.content)

  # set model parameters
  TOP_K = 10000
  MAX_SEQUENCE_LENGTH = 28

  #instatiate saved model
  model = keras.models.load_model('emotifyModif/my_model.h5', compile=False)
  # # categories for testing
  # labels = ["anger", "fear", "happiness", "sadness"]

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
    'Authorization' : 'Bearer {}'.format("BQAe_Yeq3T6NAxK5LNKq-7XPtojz2FcQWHNtTaa4qFjFkDGRDqVxMOjNINdtYRFzpXcPNVmcRrJf68PqfY8yVNfjL9HXaoAtr0wmi14UUVESP77WMJND12sWSHz9Z0SgqDU-TlC8IaPwer0J47e1ZrVlBfMGB9jfQ3Y9256H0LsFKwSMVqjpNSwoOftCgpza3l1w")
  }

  # adjust parameters
  NUMARTISTS = 10;
  NUMTRACKS = 20;
  MAXARTISTINDEX = NUMARTISTS - 1;
  MAXTRACKINDEX = NUMTRACKS - 1;
  NUMRESULTS = 12;

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



