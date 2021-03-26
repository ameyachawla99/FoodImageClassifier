from flask import Flask,render_template,request
import cv2
from keras.models import model_from_json
import numpy as np

with open("web (2).json","r") as file:
        loaded_model=file.read()
        model=model_from_json(loaded_model)
        model.load_weights("weights (1).h5")


app=Flask(__name__)

@app.route("/")

def home():
	return render_template("file_upload_form.html")
@app.route('/success', methods = ['POST']) 
def predict():
    if request.method == 'POST': 
                message=request.files["file"]
                message.save(message.filename)
                img=cv2.imread(message.filename)
                data=[]

                img_size = (112, 112)

                imgs = cv2.resize(img, img_size, interpolation=cv2.INTER_AREA)
                data.append(imgs)
        
                # Normalize data
                data = np.array(data)
                data = data / 255.0
                data = data.astype('float32')
    m=model.predict(data)
    m=m/m.sum()
    m=m*100
    print(m)
    print("mother fucking it worked bro")
    max=0
    k=0
    for j in range(5):
        if(m[0][j]>max):
            max=m[0][j]
            k=j
    print(k)
    return render_template('success.html',name=str(k))
if __name__=="__main__":
	app.run(debug=True)
