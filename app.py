from flask import Flask, request, jsonify, render_template
import pandas as pd
from fbprophet import Prophet
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/data',methods=['POST'])        
def data():
    data1 = {'Product':['P1', 'P2'],'2017-01-01':['12','92'],'2017-02-01':['13','99'],'2017-03-01':['15','98'],
       '2017-04-01':['12','95']}
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
        future = m.make_future_dataframe(periods=12, freq='M')
        forecast = m.predict(future)    
        forecast = forecast.rename(columns={'yhat': g})
        final = pd.merge(final, forecast.set_index('ds'), how='outer', left_index=True, right_index=True)
    final = final[[ g for g in grouped.groups.keys()]]
    return render_template('data.html', data=final.to_html())
        
if __name__ == "__main__":
    app.run(debug=True)