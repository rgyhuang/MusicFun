# Music Fun

![Thumbnail](https://i.imgur.com/gTq9Gpy.png)

## What is Music Fun :3?
Music Fun :3 is our submission for [TartanHacks 2023!](https://tartanhacks.com/) Our project features the following functionalities:
* **An aesthetic and interactive graph-based display of music search results, complete with album covers and links to the spotify recommendations!**
* **Song recommendations based on input text emotion!**


## How we made it
This project was built with a html/css javascript frontend and python backend. We used D3.js to make the amazing interactive graph! Music Fun used the [emotify model](https://github.com/orzymandias/emotify-model) to classify the emotion of a particular phrases of text. Afterward encoding the classification, a random seed artist and song is chosen based (this is to put into our Spotify API request). A GET request is sent to the [spofity recommendation API](https://developer.spotify.com/console/get-recommendations). After extracting the responses from the API, we associate each recommendation with a node and connect the nodes together to form a graph representation of the results!

## What we would have done if we had more time
* Randomly distribute node connections
* Further polish our graph aesthetics
* Allow for variable numbers of requests (we currently only fetch 12 requests each time)
* Add varying more seeds for artists and songs to increase randomization

## Short demo of our project in action!
![Demo](https://i.imgur.com/UAipupU.gif)

## Modules for Development
```
pip install tensorflow
pip install flask
pip install flask_co
pip install pandas
pip install numpy
pip install scikit
```

## Have fun~~~ :3333
