from io import BytesIO
from turtle import distance
from django.shortcuts import render
from django.http import HttpResponse
from sport.models import BasicData, ComplicatedData
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
import fitparse as fit
import matplotlib.pyplot as plt
import pandas as pd
import sys
import base64
import numpy as np
fitfile = fit.FitFile("Toasty_Trail_Run.fit")

# Loop over the FIT file 'record' messages and build our data structure
activity_data = []

for record in fitfile.get_messages('record'):
    activity_data_entry = {}

    for record_data in record:
        if record_data.name in ["timestamp", "distance", "heart_rate", "cadence", "enhanced_speed", "enhanced_altitude", "position_lat", "position_long"]:
            activity_data_entry[record_data.name] = record_data.value

    if len(activity_data_entry) > 0:
        activity_data.append(activity_data_entry)

# Convert the raw data into a Pandas dataframe
activity = pd.DataFrame(activity_data)

print(activity.head())
print(activity.heart_rate.mean())
plt.switch_backend('Agg') 

# Visualise some of the data
def heartRatechart():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title='Heart Rate Chart', ylabel='Heart Rate', xlabel='Time(Second)')
    ax.plot(activity.heart_rate, color="red")
    ax.axhline(177.25, color='gray', linewidth=2)
    #plt.plot(activity.heart_rate, color="red")
    
    activityN=activity.heart_rate.to_numpy()
    y1_min=np.argmin(activityN)
    y1_max=np.argmax(activityN)
    show_min='Min:'+str(activityN[y1_min])
    show_max='Max:'+str(activityN[y1_max])
    ax.plot(y1_min,activityN[y1_min],'ko') 
    ax.plot(y1_max,activityN[y1_max],'ko') 
    ax.annotate(show_min,xy=(y1_min,activityN[y1_min]),xytext=(y1_min,activityN[y1_min]))
    ax.annotate(show_max,xy=(y1_max,activityN[y1_max]),xytext=(y1_max,activityN[y1_max]))
    ax.annotate('Staying around this line can improve your endurance',xy=(500,160),xytext=(500,160))
    
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd

def distanceChart():
    #plt.plot(activity.distance, color="red")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title='Distance Chart', ylabel='Distance', xlabel='Time(Second)')
    ax.plot(activity.distance, color="red")
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd

def cadenceChart():
    #plt.plot(activity.distance, color="red")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title='Cadence Chart', ylabel='Cadence', xlabel='Time(Second)')
    ax.plot(activity.cadence, color="red")
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd

def speedChart():
    #plt.plot(activity.distance, color="red")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title='Speed Chart', ylabel='Speed', xlabel='Time(Second)')
    ax.plot(activity.enhanced_speed, color="red")
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd

def altitudeChart():
    #plt.plot(activity.distance, color="red")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title='Altitude Chart', ylabel='Altitude', xlabel='Time(Second)')
    ax.plot(activity.enhanced_altitude, color="red")
    
    activityN=activity.enhanced_altitude.to_numpy()
    y1_min=np.argmin(activityN)
    y1_max=np.argmax(activityN)
    show_min='Min:'+ str(activityN[y1_min])
    show_max='Max:'+str(activityN[y1_max])
    ax.plot(y1_min,activityN[y1_min],'ko') 
    ax.plot(y1_max,activityN[y1_max],'ko') 
    ax.annotate(show_min,xy=(y1_min,activityN[y1_min]),xytext=(y1_min,activityN[y1_min]))
    ax.annotate(show_max,xy=(y1_max,activityN[y1_max]),xytext=(y1_max,activityN[y1_max]))
    
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd

def LatitudeChart():
    #plt.plot(activity.distance, color="red")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title='Latitude Chart', ylabel='Latitude', xlabel='Time(Second)')
    ax.plot(activity.position_lat, color="red")
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd

def EnduranceChart():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(xlim=[0, 40],ylim=[20,39], title='Endurance Level Chart', xlabel='VO2max Value')
    ax.set_yticks([20,29,31,33,36,39])
    ax.set_yticklabels(['Very poor','Poor','Average','Good','Great','Execllent'],rotation = 30,fontsize = 'small')
    plt.scatter(37.19, 36, color='red', marker='+')
    show = 'Great' + '(37.19)'
    ax.annotate(show,xy=(37.19,36),xytext=(37.19,36))
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd

#plt.show()

def index(request):
# Query the database for a list of ALL categories currently stored.
# Order the categories by the number of likes in descending order.
# Retrieve the top 5 only -- or all if less than 5.
# Place the list in our context_dict dictionary (with our boldmessage!)
# that will be passed to the template engine.
   # fig, axs = plt.subplots(figsize=(6, 2), dpi=300)
    basicData_list = BasicData.objects.all()
    heartrateChart = heartRatechart()
    distancechart = distanceChart()
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    context_dict['heartRate'] = activity.heart_rate.mean()
    
    context_dict['heartrateChart'] = heartrateChart
    context_dict['distanceChart'] = distancechart
    context_dict['basicdatas'] = basicData_list

# Render the response and send it back!
    return render(request, 'sport/index.html', context=context_dict)

def about(request):
    print(request.method)
    print(request.user)
  #  visitor_cookie_handler(request)
    context_dict = {}
    context_dict['visits'] = request.session['visits']
    response = render(request,'sport/about.html',context = context_dict)

    return response

def view_basicdata(request, basicdata_name_slug):
    # 1. lists the festivals of a particular country
    try:
        basicdata = BasicData.objects.get(slug=basicdata_name_slug)
        complicatedData= ComplicatedData.objects.filter(BasicData=basicdata)
        basicdata_list = BasicData.objects.all()

        context_dict = {}
        context_dict['complicatedDatas'] = complicatedData
        context_dict['basicData'] = basicdata
        context_dict['basicDatas'] = basicdata_list
    except BasicData.DoesNotExist:
        context_dict['complicatedData'] = None
        context_dict['basicData'] = None

    #visitor_cookie_handler(request)

    return render(request, 'sport/basicData.html', context=context_dict)


def view_complicatedData(request,complicatedData_name_slug):
    # 1. lists the festivals of a particular country
    try:
        complicatedData = ComplicatedData.objects.get(slug=complicatedData_name_slug)
        basicdata=BasicData.objects.get(Basicname=complicatedData.BasicData)
        time = activity.timestamp.max()-activity.timestamp.min()
        context_dict = {}
        context_dict['complicatedData'] = complicatedData
        context_dict['basicData'] = basicdata
        context_dict['heartrateChart'] = heartRatechart()
        context_dict['distanceChart'] = distanceChart()
        context_dict['time'] = activity.timestamp.max()-activity.timestamp.min()
        context_dict['distance'] = "%.2f" % (activity.distance.max() / 1000)
        context_dict['heartRateMin'] = activity.heart_rate.min()
        context_dict['heartRateMax'] = activity.heart_rate.max()
        context_dict['heartRateMean'] = "%.2f" % (activity.heart_rate.mean())
        context_dict['cadence'] = "%.2f" % (activity.cadence.mean())
        context_dict['cadenceChart'] = cadenceChart()
        context_dict['speedChart'] = speedChart()
        context_dict['speed'] = "%.2f" % (activity.enhanced_speed.mean())
        context_dict['altitudeChart'] = altitudeChart()
        context_dict['altitude'] = "%.2f" % (activity.enhanced_altitude.mean())
        context_dict['latitudeChart'] = LatitudeChart()
        context_dict['latitude'] = "%.2f" % (activity.position_lat.min())
        context_dict['calories'] = "%.2f" % (activity.distance.max() / time.seconds * 60 / 400 * 30 * (time.seconds / 3600) * 70)
        context_dict['VO2max'] = "%.2f" % ((22.351 * (activity.distance.max() / 1000) / (time.seconds / 60 / 12)) - 11.288)
        context_dict['trainingLoad'] = activity.heart_rate.mean() * time.seconds / 60
        context_dict['LacticAcidValvePace'] = "%.2f" % (time.seconds / 60 / (activity.distance.max() / 1000))
        context_dict['LactateThresholdHeartRate'] = "%.2f" % (activity.heart_rate.mean())
        context_dict['EnduranceChart'] = EnduranceChart()
    except BasicData.DoesNotExist:
        context_dict['complicatedData'] = None
        context_dict['basicData'] =None

    
    return render(request, 'sport/complicatedData.html', context=context_dict)