# -*- coding: utf-8 -*-

from flask import Flask,render_template,request
import  pandas as pd
import numpy as np 
import datetime as dt
import os
from fbprophet import Prophet
app=Flask(__name__)



@app.route('/',methods=['GET','POST'])
def Index():
    return render_template('index.html')


    
@app.route('/data',methods=['GET','POST'])
def data():
    if request.method=='POST':
        
        file=request.form['upload-file']
        # profile = request.files['upload-file']
        Noofmonths=int(request.form['Noofmonths'])
        # profile.save(profile.filename)  
        data=pd.read_excel(file)
        df2 = pd.DataFrame(data)
        # df2.set_index('Product', inplace=True)
       # data1 = {'Product':['P1', 'P2'],'2017-01-01':['12','92'],'2017-02-01':['13','99'],'2017-03-01':['15','98'],
       #'2017-04-01':['12','95']}
        #df1 = pd.DataFrame(df2)
        gapminder_tidy = df2.melt(id_vars=['Pro'], 
                              var_name='year', 
                              value_name='Amount')
        df = gapminder_tidy.rename(columns={'year': 'ds', 'Amount':'y'})
        grouped = df.groupby('Pro')
        final = pd.DataFrame()
        for g in grouped.groups:
            group = grouped.get_group(g)
            m = Prophet()
            m.fit(group)
            future = m.make_future_dataframe(periods=Noofmonths, freq='M')
            forecast = m.predict(future)    
            forecast = forecast.rename(columns={'yhat': g})
            final = pd.merge(final, forecast.set_index('ds'), how='outer', left_index=True, right_index=True)
            
        final = final[[ g for g in grouped.groups.keys()]]
           
            
        return render_template('data.html',data=final.to_html())
        
if __name__=='__main__':
    app.run(debug=True)