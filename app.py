# -*- coding: utf-8 -*-

from flask import Flask,render_template,request
import  pandas as pd
from fbprophet import Prophet
app=Flask(__name__)



@app.route('/',methods=['GET','POST'])
def Index():
    return render_template('index.html')


    
@app.route('/data',methods=['GET','POST'])
def data():
    if request.method=='POST':
        
      return render_template('index.html')
        
if __name__=='__main__':
    app.run(debug=True)