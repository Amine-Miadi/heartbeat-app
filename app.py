from lib2to3.pgen2.token import GREATER
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
        results.append(float(request.form['3']))
        results.append(float(request.form['4']))
        results.append(float(request.form['5']))
        results.append(float(request.form['6']))
        results.append(float(request.form['7']))
        results.append(float(request.form['8']))
        results.append(float(request.form['9']))
        DATA = get_graph_data()

    #coordinates for each graph
        age_x = []
        age_y = []

        PE_x = []
        PE_y = []

        FS_x = []
        FS_y = []

        EPSS_x = []
        EPSS_y = []

        LVDD_x = []
        LVDD_y = []

        WMI_x = []
        WMI_y = []

        coord = [[age_x,age_y],[PE_x,PE_y],[FS_x,FS_y],[EPSS_x,EPSS_y],[LVDD_x,LVDD_y],[WMI_x,WMI_y]]
        for j in range(len(DATA)):
            for i in DATA[j]:
                coord[j][0].append(i[1])
                coord[j][1].append((i[0]*100)/126)

        pericardial_effusion = DATA[1]
        fractional_shortening = DATA[2]
        epss = DATA[3]
        lvdd = DATA[4]
        wall_motion_index = DATA[5]
        result = predict(results)
        return render_template('results.html', results = result[0],description = result[1], usr=results,
        age_x = age_x, age_y = age_y,
        PE_x = PE_x, PE_y = PE_y,
        FS_x = FS_x, FS_y = FS_y,
        EPSS_x = EPSS_x, EPSS_y = EPSS_y,
        LVDD_x = LVDD_x, LVDD_y = LVDD_y,
        WMI_x = WMI_x, WMI_y = WMI_y,
        )


if __name__ == '__main__':
    app.run(debug = True)