from flask import Flask,render_template,request
import pickle
import json
import numpy as np
import CONFIG


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

with open(CONFIG.MODEL_PATH, 'rb') as file:
    model = pickle.load(file)

with open(CONFIG.ASSET_PATH,'r') as file:
    asset = json.load(file)
col = asset['columns']

@app.route('/getdata', methods=["POST"])
def data():
    with open(CONFIG.COL_NAMES_PATH,"r") as file:
        column_names = json.load(file)
    with open(CONFIG.ENCODED_DATA_PATH,"r") as file:
        encoded_data = json.load(file)

    input_data = request.form
    print(input_data)

    data = np.zeros(len(column_names['Column Names']))
    age = input_data['age']
    job = input_data['htmljob'] 
    marital = input_data['htmlmarital'] 
    education = input_data['htmleducation'] 
    default = input_data['htmldefault'] 
    housing = input_data['htmlhousing'] 
    loan = input_data['htmlloan'] 
    contact = input_data['htmlcontact'] 
    month = input_data['htmlmonth'] 
    day_of_week = input_data['htmlday_of_week'] 
    duration = input_data['htmlduration'] 
    campaign = input_data['htmlcampaign'] 
    pdays = input_data['htmlpdays'] 
    previous = input_data['htmlprevious'] 
    poutcome = input_data['htmlpoutcome'] 
    emp_var_rate = input_data['htmlemp_var_rate'] 
    cons_price_idx = input_data['htmlcons_price_idx'] 
    cons_conf_idx = input_data['htmlcons_conf_idx'] 
    euribor3m = input_data['htmleuribor3m'] 
    nr_employed = input_data['htmlnr_employed']

    
    ##passing value from front to code
    data[0]= int(age)

    #giving values to OHE -->
    ##prefix is job_ 
    search_str = "job_"+job   ##index name formatting
    column_array = np.array(column_names['Column Names']) ##convert to arrays
    index = np.where(column_array == search_str)  ##getting index pos
    data[index]=1                          #setting value for job


    search_str = "marital_"+marital   ##index name formatting
    column_array = np.array(column_names['Column Names']) ##convert to arrays
    index = np.where(column_array == search_str)  ##getting index pos
    data[index]=1    


    data[3]= int(education)
    print(education)
    print(type(education))
    data[4]= int(default)
    data[5]= int(housing)
    data[6]= int(loan)


    search_str = "contact_"+contact   ##index name formatting
    column_array = np.array(column_names['Column Names']) ##convert to arrays
    index = np.where(column_array == search_str)  ##getting index pos
    data[index]=1    


    search_str = "month_"+month   ##index name formatting
    column_array = np.array(column_names['Column Names']) ##convert to arrays
    index = np.where(column_array == search_str)  ##getting index pos
    data[index]=1    


    search_str = "day_of_week_"+day_of_week   ##index name formatting
    column_array = np.array(column_names['Column Names']) ##convert to arrays
    index = np.where(column_array == search_str)  ##getting index pos
    data[index]=1 

    data[10] = duration
    data[11] = campaign
    data[12] = pdays
    data[13] = previous

    data[14] = int(poutcome)
    data[15] = emp_var_rate
    data[16] = cons_price_idx
    data[17] = cons_conf_idx
    data[18] = euribor3m
    data[19] = nr_employed

    # result = model.predict([data])
    # print(result)
    print(data)

    result = model.predict([data])
    print(result)
    
    if result == 0:  #1
        customer = "Client subscribed a term deposit?: No"
    else:
        customer = "Client subscribed a term deposit?: Yes"
    return render_template('index.html',PREDICT_VALUE=customer)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=False)