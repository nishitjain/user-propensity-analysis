import pandas as pd
from sklearn.cluster import KMeans

rfm_raw_data = pd.read_pickle('Data/clevertap.pkl')
registration = pd.read_csv('Data/Registration.csv')
registration_sample = registration.sample(n=100)
filter_data = rfm_raw_data['UserId'].isin(registration_sample['UserId'].values.tolist())
data_sample = rfm_raw_data[filter_data]

# Initializing required filters
app_launch_filter = data_sample['Event']=='AppLaunched'
video_detail_filter = data_sample['Event']=='VideoDetails'
video_started_filter = data_sample['Event']=='VideoStarted'

# initializing RFM Dataframe
rfm_sample = pd.DataFrame()
rfm_sample['UserId'] = registration_sample['UserId'].values
rfm_sample['Recency'] = 0
rfm_sample['Frequency'] = 0
rfm_sample['Engagement'] = 0
data_sample.drop(['Date','Minute_Of_Day','Second'],axis=1,inplace=True)

# Recency
max_date = data_sample.timestamp.max()
for user in rfm_sample['UserId'].values.tolist():
    data = data_sample[app_launch_filter | video_detail_filter | video_started_filter]
    data = data[data['UserId']==user]
    recent_date = data.timestamp.max()
    recency = (max_date - recent_date)
    rfm_sample.loc[rfm_sample.UserId == user,'Recency']=(recency.days + ((recency.seconds/3600)/24))
    
# Freqency
for user in rfm_sample['UserId'].values.tolist():
    data = data_sample[app_launch_filter]
    data = data[data['UserId']==user]
    frequency = len(data)
    rfm_sample.loc[rfm_sample.UserId == user,'Frequency']=frequency
    
# Engagement
for user in rfm_sample['UserId'].values.tolist():
    data1 = data_sample[video_detail_filter]
    data2 = data_sample[video_started_filter]
    data1 = data1[data1['UserId']==user]
    data2 = data2[data2['UserId']==user]
    engagement = (0.3*len(data1)) + (0.7*len(data2))
    rfm_sample.loc[rfm_sample.UserId == user,'Engagement']=engagement

# Kmeans Clustering
model = KMeans(n_clusters=4)
model.fit(rfm_sample.iloc[:,1:])
rfm_sample['Cluster'] = model.labels_