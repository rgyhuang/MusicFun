# Music Fun :3

![Image Demo]([https://i.imgur.com/3O99hp0.jpg](https://i.imgur.com/gTq9Gpy.png))

## What is title?
Our project features the following functionalities:
* **An aesthetic graph-based display of results, complete with album covers and links to the spotify recommendations!**
* **Song recommendations based on input text emotion!**


## How we made it
This project was built with a html/css javascript frontend and python backend. We used D3.js to make the amazing interactive graph! Music Fun used the [emotify model](https://github.com/orzymandias/emotify-model) to classify the emotion of a particular phrases of text. Afterward encoding the classification, a random seed artist and song is chosen based (this is to put into our Spotify API request). A GET request is sent to the [spofity recommendation API](https://developer.spotify.com/console/get-recommendations). After extracting the responses from the API, we associate each recommendation with a node and connect the nodes together to form a graph representation of the results!

## What we would have done if we had more time
* Randomly distribute node connections
* Further polish our graph aesthetics
* Allow for variable numbers of requests (we currently only fetch 12 requests each time)
* Add varying more seeds for artists and songs to increase randomization

## Modules for Development
```
pip install tensorflow
pip install flask
pip install pandas
pip install numpy
pip install scikit
```

## Have fun~~~ :3333
