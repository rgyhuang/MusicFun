import * as tf from './node_modules/@tensorflow/tfjs';
const model = await tf.loadLayersModel('emotifyModif/model.json')
function getEmotion() {
    const input = prompt("What are you feeling today?")
    const prediction = model.predict(input)
    console.log(prediction)
}

getEmotion()