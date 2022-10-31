from flask import Flask, render_template,request
from Data_Base.data_processing import predict,get_graph_data



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/results', methods = ["POST", "GET"])
def showresults():
    if request.method == 'POST':
        results = []
        backgroundcolors = []
        results.append(float(request.form['3']))
        results.append(float(request.form['4']))
        results.append(float(request.form['5']))
        results.append(float(request.form['6']))
        results.append(float(request.form['7']))
        results.append(float(request.form['8']))
        results.append(float(request.form['9']))
        DATA = get_graph_data(results[1:])

    #coordinates for each graph
        age_x = []
        age_y = []
        age_color = []

        PE_x = []
        PE_y = []
        PE_color=[]

        FS_x = []
        FS_y = []
        FS_color=[]

        EPSS_x = []
        EPSS_y = []
        EPSS_color=[]

        LVDD_x = []
        LVDD_y = []
        LVDD_color = []

        WMI_x = []
        WMI_y = []
        WMI_color = []

        coord = [[age_x,age_y,age_color],[PE_x,PE_y,PE_color],[FS_x,FS_y,FS_color],[EPSS_x,EPSS_y,EPSS_color],[LVDD_x,LVDD_y,LVDD_color],[WMI_x,WMI_y,WMI_color]]
        for j in range(len(DATA)):
            for i in DATA[j]:
                coord[j][0].append(i[1])
                coord[j][1].append((i[0]*100)/126)
                if i[1] == results[j+1]:
                    coord[j][2].append("rgb(255,140,0, 0.8)")
                else:
                    coord[j][2].append("rgb(0,128,128, 0.8)")

        pericardial_effusion = DATA[1]
        fractional_shortening = DATA[2]
        epss = DATA[3]
        lvdd = DATA[4]
        wall_motion_index = DATA[5]
        result = predict(results)
        return render_template('results.html', results = result[0],description = result[1],
        age_x = age_x, age_y = age_y, age_color = age_color,
        PE_x = PE_x, PE_y = PE_y, PE_color = PE_color,
        FS_x = FS_x, FS_y = FS_y, FS_color = FS_color,
        EPSS_x = EPSS_x, EPSS_y = EPSS_y, EPSS_color = EPSS_color,
        LVDD_x = LVDD_x, LVDD_y = LVDD_y, LVDD_color = LVDD_color,
        WMI_x = WMI_x, WMI_y = WMI_y , WMI_color = WMI_color
        )


if __name__ == '__main__':
    app.run(debug = True)