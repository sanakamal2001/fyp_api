
from flask import Flask,request,jsonify
from datamodel import DASlabel,extract_frames,video_predictor

import cv2
app=Flask(__name__)

@app.route('/api',methods=['GET'])
def DAS_text():
    print("in DAS function")
    query=str(request.args['text'])
    label=DASlabel(query)
    d={"label":list(label.keys()),"level":list(label.values())}
    print(d)
    response=jsonify(d)
    response.headers.add("Access-Control-Allow-Origin", "*")    
    return response

@app.route('/video',methods=['POST'])
def convertvideo():
  if(request.method=="POST"):
      
    videofile = request.files["video"]
    print("after videofile")    
    filename=videofile.filename
    videofile.save(filename)
    images=extract_frames(filename)
    vp=video_predictor(images)
    prediction=max(set(vp),key=vp.count)
    response=jsonify({'prediction':prediction})
    print(prediction)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__=="__main__":
    app.run()