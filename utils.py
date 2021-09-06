import json;import datetime;from datetime import timedelta;import os, zipfile;
# import pandas as pd
# from sqlalchemy import func
# from flask_bcrypt import Bcrypt
import requests
import time
import pytz
# import zoneinfo
from pytz import timezone
import datetime;from datetime import timedelta

def add_activity_util(title,note, user_id, var_timezone_utc_delta_in_mins):
    url="http://api.life-buddy.org/add_activity"
    
    payload={}
    payload['datetime_of_activity']='2021-08-18T15:31:00'
    payload["note"]= note
    payload["source_filename"]= "phone application"
    # payload["time_stamp_utc"]= time.now()
    payload["user_id"]= user_id
    payload["var_activity"]= title
    payload["var_timezone_utc_delta_in_mins"]= var_timezone_utc_delta_in_mins
    payload["var_type"]= "Activity"
    
    # return ('success! ', url,' ', title,' ', note)
    return ('success! ', payload)

def current_time_util(user_timezone):
    date_time_obj=datetime.datetime.now()
    date_time_obj_tz_aware=timezone(user_timezone).localize(date_time_obj)
    hour_temp=date_time_obj_tz_aware.strftime("%H")
    hour=hour_temp if hour_temp[0]!='0' else hour_temp[1]
    
    am_pm='AM' if int(hour)<12 else 'PM'
    
    hour=hour if int(hour)<13 else str(int(hour)-12)
    minute=date_time_obj_tz_aware.strftime("%M")
    # time_thing=date_time_obj_tz_aware.strftime("%H:%M%p")
    time_thing=f'{hour}:{minute} {am_pm}'
    
    
    month=date_time_obj_tz_aware.strftime("%m")
    # month=month if month[0]!='0' else month[1]
    day=date_time_obj_tz_aware.strftime("%d")
    # day=day if day[0]!='0' else day[1]
    year=date_time_obj_tz_aware.strftime("%Y")
    
    
    
    
    
    date_time_now=(year,month,day,time_thing)
    
    
    # print('local time:::',date_time_obj_tz_aware)
    # print('time:::',date_time_obj)
    print('year:::',year)
    return(date_time_now)
    