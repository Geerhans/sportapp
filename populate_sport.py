import os

from django import views 
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'sportapp.settings')
import django
django.setup() 
from sport.models import BasicData, ComplicatedData
def populate():
# First, we will create lists of dictionaries containing the pages
# we want to add into each category.
# Then we will create a dictionary of dictionaries for our categories. # This might seem a little bit confusing, but it allows us to iterate # through each data structure, and add the data to our models.
    timestamp_data = [
        {'Complicatedname': 'Timestamp'}
         ]
    distance_data = [
        {'Complicatedname': 'Distance'},
         ]
    heartrate_data = [
        {'Complicatedname': 'HeartRate'}, 
         ]
    cadence_data =  [
        {'Complicatedname': 'Cadence'},
         ]
    enhancedspeed_data = [
        {'Complicatedname': 'EnhancedSpeed'},
    ]
    enhancedaltitude_data = [
        {'Complicatedname': 'EnhancedAltitude'},
    ]
    positionlat_data = [
        {'Complicatedname': 'PositionLong'}
    ]
    
    
    data = {'Timestamp': {'complicatedDatas': timestamp_data},
            'Distance': {'complicatedDatas': distance_data},
            'HeartRate': {'complicatedDatas': heartrate_data},
            'Cadence': {'complicatedDatas': cadence_data},
            'Speed': {'complicatedDatas': enhancedspeed_data},
            'Altitude': {'complicatedDatas':enhancedaltitude_data},
            'Latitude': {'complicatedDatas': positionlat_data},
            }
    # If you want to add more categories or pages,
    # add them to the dictionaries above.
# The code below goes through the cats dictionary, then adds each category, # and then adds all the associated pages for that category.
    for sport, sport_data in data.items():
        c = add_basic(sport)
        for p in sport_data['complicatedDatas']:
            add_complicated(c,p['Complicatedname'])
    # Print out the categories we have added.
    for c in BasicData.objects.all():
        for p in ComplicatedData.objects.filter(BasicData=c):
            print("-{0}-{1}".format(str(c),str(p)))
def add_complicated(BasicData,Complicatedname):
    p = ComplicatedData.objects.get_or_create(Complicatedname=Complicatedname, BasicData=BasicData)[0] 
    p.save()
    return p
def add_basic(Basicname):
    c = BasicData.objects.get_or_create(Basicname=Basicname)[0] 
    c.save()
    return c
#Startexecutionhere!
if __name__== '__main__':
    print('Starting Sportapp population script...') 
    populate()