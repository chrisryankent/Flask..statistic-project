import base64
from io import BytesIO
from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

numbers = []
count = 0
total_sum = 0
data = 0
mean = 0
variance = 0
plot_url = 0
buf = 0
mode = 0
median = 0 
percentile=0
percentage=0
x=[]
y=[]


@app.route('/', methods=['GET', 'POST'])
def index():
    global count, total_sum, data, mean, variance, plot_url, buf,mode,median
    if request.method == 'POST':
        if request.form["action"]=="add":
            num = int(request.form['number'])
        
            numbers.append(num)
            count += 1
            total_sum += num
            data = np.array(numbers)
            mean = np.mean(data)
            variance = np.var(data)
            mode = stats.mode(data)
            median = np.median(data)
        
            
            plt.figure()
            plt.plot(numbers)
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        elif request.form["action"]=="clear_list":
            numbers.clear()
            mean = 0
            variance = 0
            mode = 0
            median = 0
            plot_url=0
        
    return render_template('index.html', numbers=numbers, count=count, sum=total_sum, mean=mean, variance=variance, plot_url=plot_url,mode=mode,median=median,percentile=percentile)

@app.route("/more",methods=['GET', 'POST'])
def more():
    global percentile,percentage
    if request.method == 'POST':
        percentage = int(request.form['percent'])
        percentile = np.percentile(data,percentage)
    return render_template('more.html',percentile=percentile,percentage=percentage)
@app.route("/plots",methods=['GET', 'POST'])
def plots():
    if request.method=="POST":
        numX = int(request.form['x'])
        numY = int(request.form['y'])
        x.append(numX)
        y.append(numY)



    return render_template('xyplots.html',x=x,y=y)
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
