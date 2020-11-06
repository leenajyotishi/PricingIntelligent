from flask import Flask, request, jsonify, render_template,redirect,url_for
import pandas as pd
from fbprophet import Prophet
import os,json,boto3
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('Demo.html')
    
@app.route('/data',methods=['POST'])        
def data():
    profile = request.files['upload-file']
    Noofmonths=int(request.form['Noofmonths'])
    profile.save(profile.filename) 
    data=pd.read_excel(profile.filename)
    data1 = {'Product':['P1', 'P2'],'2017-01-01':['12','92'],'2017-02-01':['13','99'],'2017-03-01':['15','98'],
       '2017-04-01':['12','95']}
    df1 = pd.DataFrame(data)
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
    return render_template('data.html', data=final.to_html())
 
@app.route('/sign_s3/')
def sign_s3():
  S3_BUCKET = os.environ.get('S3_BUCKET')

  file_name = request.args.get('file_name')
  file_type = request.args.get('file_type')

  s3 = boto3.client('s3')

  presigned_post = s3.generate_presigned_post(
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
  )

  return json.dumps({
    'data': presigned_post,
    'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
  })       
if __name__ == "__main__":
    app.run(host = '0.0.0.0',port=8080)