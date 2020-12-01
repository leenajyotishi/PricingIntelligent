from flask import Flask, request, jsonify, render_template,redirect,url_for
import pandas as pd
from fbprophet import Prophet
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('Main.html')
    
@app.route('/data',methods=['POST'])        
def data():
   
    Noofmonths=int(request.form['Noofmonths'])
    Productnm=request.form['Product']
    PriceQ1=int(request.form['Quarter1'])
    PriceQ2=int(request.form['Quarter2'])
    PriceQ3=int(request.form['Quarter3'])
    PriceQ4=int(request.form['Quarter4'])
    data1 = {'Product':[Productnm],'2020-01-01':[PriceQ1],'2020-03-01':[PriceQ2],'2020-06-01':[PriceQ3],
       '2020-09-01':[PriceQ4]}
    df1 = pd.DataFrame(data1)
    gapminder_tidy = df1.melt(id_vars=["Product"], 
                              var_name="year", 
                              value_name="Amount")
    df = gapminder_tidy.rename(columns={'year': 'ds', 'Amount':'y'})
    grouped = df.groupby('Product')
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
    dff = pd.DataFrame(final)
    dff = dff.rename(columns={'ds': 'd'})
    return render_template('data.html', data=dff.to_html(classes='form-group'))


if __name__ == "__main__":
     app.run(debug=True)