import pandas as pd

app_launched = pd.read_csv('Data/AppLaunched.csv')
app_uninstalled = pd.read_csv('Data/AppUninstalled.csv')
registration = pd.read_csv('Data/Registration.csv')
utm_visited = pd.read_csv('Data/UTMVisited.csv')
video_details = pd.read_csv('Data/VideoDetails.csv')
video_started = pd.read_csv('Data/VideoStarted.csv')

print('App Launched Features:\n{}'.format(app_launched.columns))
print('App Uninstalled Features:\n{}'.format(app_uninstalled.columns))
print('Registration Features:\n{}'.format(registration.columns))
print('UTM Visited Features:\n{}'.format(utm_visited.columns))
print('Video Details Features:\n{}'.format(video_details.columns))
print('Video Started Features:\n{}'.format(video_started.columns))

def user_data(user_id):
    temp_app_launched = app_launched[app_launched['UserId']==user_id][['UserId','Date','Minute_Of_Day','Second']]
    temp_app_uninstalled= app_uninstalled[app_uninstalled['UserId']==user_id][['UserId','Date','Minute_Of_Day','Second']]
    temp_registration = registration[registration['UserId']==user_id][['UserId','Date','Minute_Of_Day','Second']]
    temp_utm_visited =utm_visited[utm_visited['UserId']==user_id][['UserId','Date','Minute_Of_Day','Second']]
    temp_video_details = video_details[video_details['UserId']==user_id][['UserId','Date','Minute_Of_Day','Second']]
    temp_video_started = video_started[video_started['UserId']==user_id][['UserId','Date','Minute_Of_Day','Second']]
    
    temp_app_launched['Event'] = 'App Launched'
    temp_app_uninstalled['Event'] = 'App Uninstalled'
    temp_registration['Event'] = 'App Registration'
    temp_utm_visited['Event'] = 'App UTM Visited'
    temp_video_details['Event'] = 'App Video Details'
    temp_video_started['Event'] = 'App Video Started'
    
    data = pd.concat([temp_app_launched,temp_app_uninstalled,temp_registration,temp_utm_visited,temp_video_details,temp_video_started],axis=0)
    data['sort_parameter'] = data['Date']*1000000 + data['Minute_Of_Day']*100 + data['Second']
    return data

