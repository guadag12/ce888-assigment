# -*- coding: utf-8 -*-
"""assigment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KGZJ--BjtCXd9bUHoIFYDkRuS7ez2YFX

## Classifying stress in Nurses 👩‍⚕️

It seeks to predict nurses' stress (Dependent Variable) during a pandemic based on metrics monitored with E4 watchbrust, such as heart rate and skin temperature (Independent Variable). For this process, there are two datasets. The first contains our dependent variables, and the second is an excel file that contains the classification made by the nurses on whether or not there was stress at a particular time.

Stress is measured from an ordinal scale where 0 indicates 'no stress', 1 is 'there are signs of stress', 2 is 'high stress'. Likewise, and in this case, the responses to the level of stress that contain 'na' have been eliminated since they were not situations recognized as stressful by the nurses.

So, this part is divided into five parts:

1. [Packages & data](#section1)
2. [Import datasets](#section2)

    2.a. [Data I: Nurses data](#section2a)
    
    2.b. [Data II: Survey Results](#section2b)
    
    2.c. [Join of the datasets](#section2c)
    
    2.d. [Transformation of the data](#section2c)
    

3. [Exploration & Visualization](#section3)
4. [Modelling](#section3)
5. [Some conclusions & limitations of the data](#section5)
6. [References](#section6)

## 1. Packages & Data 📦 <a class="anchor" id="section1"></a>
"""

#import packages
import pandas as pd
import numpy as np
from itertools import chain
import warnings
import datetime
import glob
import zipfile 
import re
from math import pi
import os
from os import walk
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats

#numeric object without scientific notation format:
pd.options.display.float_format = '{:.2f}'.format

#display all columns
pd.set_option('display.max_columns', None)

#filter warnings
warnings.filterwarnings("ignore", category=FutureWarning)

#add path and save the files in 'filenames'
mypath = "G:/Mi unidad/CE888-7-SP - Data Science and Decision Making/Assigment/Data/Stress_dataset"
filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file

#establish path with data
os.walk(mypath)

"""## 2. Import datasets 💻<a class="anchor" id="section2"></a>

###  2.a. Data I: Nurses data <a class="anchor" id="section2a"></a>
"""

#get a list with every file in the folder
x2=[x[2] for x in os.walk(mypath)]

x2

#get every nurse name and folder
mypath = "G:/Mi unidad/CE888-7-SP - Data Science and Decision Making/Assigment/Data/Stress_dataset"
filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
x2=[x[2] for x in os.walk(mypath)]
k = []
for i in list(chain(*x2)):
    j=''.join(i)
    j='G:/Mi unidad/CE888-7-SP - Data Science and Decision Making/Assigment/Data/Stress_dataset/'+''.join(i)[:2]+"/"+j
    k.append(j)

my_dict=set([i[89:91] for i in k ])

#show the ID and the folder
my_dict

#In the data the first row gave the Hz frequency of the dataset. In this case, I create a function that
#convert this hz frequency into seconds.
#For example, if the first row has a 32, that means that the frequency of the variable is 32 hz per second. That is, 
#in one second there are 32 measurements of that variable.
#Therefore, what this function does is: every 32 rows add a second to the previous datetime of the previous row

def from_hz_to_datetime(data, frequency):
    data["datetime"] = np.nan
    j = 0
    for i in data.iloc[::frequency, :].index:
        data.loc[i, ["datetime"]] = datetime.datetime.utcfromtimestamp(float(data.columns[0])) + datetime.timedelta(0,j)
        j=j+1
    data = data.fillna(method='ffill')
    return data

#This loop has many steps. The first is an iteration between the different files that a nurse's case has inside. 
#Once it concatenates the different files inside it, it generates a sample (because the original dataset is very large).

#The sample is prepared to have at least one record per minute. That is, there will always be at least one record every minute. 
#Likewise, this for loop generates the dataset for each nurse and saves the file to be able to be consumed later.

## The data related with beat-to-beat interval will not be used in this

for nurse in my_dict:
    print("##################################################################")
    print(nurse)
    print("##################################################################")

    data_user = pd.DataFrame(columns = ['accelerometer_1', 'accelerometer_2', 'accelerometer_3',
       'blood_volume_pulse', 'electrodermal_activity', 'heart_rate',
       'skin_temperature', 'datetime', 'Nurse_ID'])
    
    k1 = [i for i in k if i[89:91] == nurse]
    
    for zip_file in k1:
        zf = zipfile.ZipFile(zip_file)
        dfs = [pd.read_csv(zf.open(f), sep = ",", header = 0) for f in zf.namelist() if f in ("EDA.csv", "TEMP.csv", 
                                                                                          "BVP.csv", "ACC.csv", "HR.csv")]
        dfs1 = pd.DataFrame(dfs[0])
        freq = dfs1.iloc[0,0]
        dfs1.drop(index=dfs1.index[0], axis=0, inplace=True)
        dfs1 = from_hz_to_datetime(dfs1, int(freq))

        dfs2 = pd.DataFrame(dfs[1])
        freq = dfs2.iloc[0,0]
        dfs2.drop(index=dfs2.index[0], axis=0, inplace=True)
        dfs2 = from_hz_to_datetime(dfs2, int(freq))

        dfs3 = pd.DataFrame(dfs[2])
        freq = dfs3.iloc[0,0]
        dfs3.drop(index=dfs3.index[0], axis=0, inplace=True)
        dfs3 = from_hz_to_datetime(dfs3, int(freq))

        dfs4 = pd.DataFrame(dfs[3])
        freq = dfs4.iloc[0,0]
        dfs4.drop(index=dfs4.index[0], axis=0, inplace=True)
        dfs4 = from_hz_to_datetime(dfs4, int(freq))

        dfs5 = pd.DataFrame(dfs[4])
        freq = dfs5.iloc[0,0]
        dfs5.drop(index=dfs5.index[0], axis=0, inplace=True)
        dfs5 = from_hz_to_datetime(dfs5, int(freq))


        dfs1.rename(columns = {dfs1.columns[0]: "accelerometer_1" , 
                               dfs1.columns[1]: "accelerometer_2" ,
                               dfs1.columns[2]: "accelerometer_3"}, inplace = True)
        sample1 = dfs1.groupby('datetime').sample(1, random_state=1)

        dfs2.rename(columns = {dfs2.columns[0]: "blood_volume_pulse"}, inplace = True)
        sample2 = dfs2.groupby('datetime').sample(1, random_state=1)


        dfs3.rename(columns = {dfs3.columns[0]: "electrodermal_activity"}, inplace = True) 
        sample3 = dfs3.groupby('datetime').sample(1, random_state=1)

        dfs4.rename(columns = {dfs4.columns[0]: "heart_rate"}, inplace=True)
        sample4 = dfs4.groupby('datetime').sample(1, random_state=1)

        dfs5.rename(columns = {dfs5.columns[0]: "skin_temperature"  }, inplace = True)   
        sample5 = dfs5.groupby('datetime').sample(1, random_state=1)

        data_i = sample1.merge(sample2, how = 'left', on = "datetime")
        data_i = data_i.drop_duplicates()

        data_i = data_i.merge(sample3, how = 'left', on = "datetime")
        data_i = data_i.drop_duplicates()

        data_i = data_i.merge(sample4, how = 'left', on = "datetime")
        data_i = data_i.drop_duplicates()

        data_i = data_i.merge(sample5, how = 'left', on = "datetime")
        data_i = data_i.drop_duplicates()

        data_i['Nurse_ID'] =  zip_file[89:91]

        data_user = pd.concat([data_user, data_i])
    data_user['datetime'] = pd.to_datetime(data_user['datetime'], format='%Y-%m-%d %H:%M:%S')
    data_user['datetime']=data_user.datetime.apply(lambda x: pd.datetime(x.year, x.month, x.day, x.hour, (x.minute//10)*10+5, 0))
    data_user['datetime_1'] = data_user['datetime']
    data_user['datetime_1'] = pd.to_datetime(data_user['datetime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    # Extract the dates from the 'datetime' column
    data_user['date'] = data_user['datetime_1'].dt.date
    path = f"C:/Users/User/Documents/Python Scripts/file_{nurse}.csv" # modify the output file path
    data_user.to_csv(path_or_buf=path)

#import all the datasets write it in the for loop done above
mypath = "C:/Users/User/Documents/Python Scripts/processed_data/"
filenames = next(walk(mypath), (None, None, []))[2]  
os.walk(mypath)
x2=[x[2] for x in os.walk(mypath)]

k = []
for i in list(chain(*x2)):
    j=''.join(i)
    j='C:/Users/User/Documents/Python Scripts/processed_data/'+j
    k.append(j)

k

data_user = pd.DataFrame(columns=['Unnamed: 0', 'accelerometer_1', 'accelerometer_2', 'accelerometer_3',
       'blood_volume_pulse', 'electrodermal_activity', 'heart_rate',
       'skin_temperature', 'datetime', 'Nurse_ID', 'datetime_1', 'date'])

for i in k:
    data_i = pd.read_csv(i)
    data_user = pd.concat([data_i, data_user])
    data_user = data_user.drop("Unnamed: 0", axis = 1)

data_user

"""###  2.b. Data II: Survey Results <a class="anchor" id="section2b"></a>"""

#For the survey dataset we are going to work only with the variables of "Nurse_ID", "Start time", "End time", "Date", 
#"Stress level". In this case, there are two variables that will help us join both datasets, 'Nurse_id' and "start time". 
#However, many of the stress observations do not match the vital signs of the previous dataset and this creates problems.

survey = pd.read_csv('C:/Users/User/Documents/Python Scripts/SurveyResults.csv',# index_col=None,
                      converters={'ID':str, 'Start time':str,'End time':str, 'duration':str,'date':str}) 
survey.rename(columns={'ID': 'Nurse_ID', 'Start time': 'start_time', 'End time':'end_time'}, inplace=True)
survey['datetime'] = survey['date'].astype(str) + ' ' + survey['start_time'].astype(str)
survey['datetime'] = [datetime.datetime.strptime(i,"%d/%m/%Y %H:%M" ).strftime('%Y-%m-%d %H:%M') for i in survey['datetime']]
survey['datetime'] = pd.to_datetime(survey['datetime'], format='%Y-%m-%d %H:%M:%S')
survey['datetime']=survey.datetime.apply(lambda x: pd.datetime(x.year, x.month, x.day, x.hour, (x.minute//10)*10+5, 0))
survey = survey.loc[:,#(survey['Nurse_ID'] == data_user["Nurse_ID"].values[0]),
    ["Nurse_ID", "start_time", "end_time", "duration", "date", "datetime", "Stress level"]]

survey.rename(columns = {"Stress level":"stress_level"}, inplace = True)

#Cases where the stress level is 'na' will be eliminated. Given the fact that the 'na' represent cases where the vital 
#signs seem to recognize signs of stress, they are nevertheless false positive cases.
survey_na = survey.loc[survey.stress_level == 'na',:] 

survey = survey.loc[survey.stress_level != 'na',:] 
survey.loc[survey.stress_level == '0',  "stress_level"] = 0
survey.loc[survey.stress_level == '1',  "stress_level"] = 1
survey.loc[survey.stress_level == '2',  "stress_level"] = 2
survey.drop(["start_time", "end_time", "date"], axis = 1, inplace = True)

survey.sort_values("datetime", ascending = True)

survey.loc[survey["Nurse_ID"] == 'DF', ]

mypath = "C:/Users/User/Downloads/doi_10.5061_dryad.5hqbzkh6f__v6/Stress_dataset"
filenames = next(walk(mypath), (None, None, []))[2]  
os.walk(mypath)
x2=[x[2] for x in os.walk(mypath)]

k = []
for i in list(chain(*x2)):
    j=''.join(i)
    j='C:/Users/User/Downloads/doi_10.5061_dryad.5hqbzkh6f__v6/Stress_dataset/'+''.join(i)[:2]+"/"+j
    k.append(j)
my_dict=set([i[71:73] for i in k ])

data_path= pd.DataFrame(columns = ["path", "Nurse_ID"])
data_path['path'] =pd.Series(k)
data_path["Nurse_ID"]= [i[71:73] for i in data_path.path ]
data_path = data_path.groupby("Nurse_ID", as_index = False).size()

data_path

data_path.loc[data_path.Nurse_ID=="15" , "size"]

j = 0 
k= 0

## Extract the dates from the 'datetime' column

#A sample is taken per user grouping by hour and minute to facilitate data manipulation. Grouping we make sure that our
#sample has at least one record for every hour and minute of our nurses.

sample = data_user.drop_duplicates(['date', 'Nurse_ID']).sample(n=len(survey.loc[:,["datetime", "Nurse_ID"]]))

#One very important thing to pay attention to is that since the dates and times do not join correctly, the time values 
#of the survey are replaced by the vital signs data.

#In this case, for each case of stress, a random date of the vital signs is taken, so that they are later compatible 
#to match. It is important to clarify that the random dates of vital signs are not 100% random because dates that
#are moderately distant from each other are chosen, so the stress events are not all together at the same time.
for x in data_path.Nurse_ID:
    j = 0 
    k= 0
    for i in survey.loc[:,"datetime"].index:
        survey.loc[i, "datetime"] = sample.iloc[k]["datetime"]
        j = j+int(data_path.loc[data_path.Nurse_ID==x , "size"]/len(survey.loc[:,"datetime"]))
        k = k+1

survey.loc[survey["Nurse_ID"] == 'DF', ]

#Before joining the datasets, one of the variables to consider is the duration of the stress event. For this, a 
#function is generated that calculates the duration of the event in minutes.

def convert_to_minutes(time_str):
    hour, minute = time_str.split(':')
    return int(hour) * 60 + int(minute)

# apply the function to the 'time' column using apply()
survey['total_minutes'] = survey['duration'].apply(convert_to_minutes)

survey

#Before joining the datasets, it is important to make sure that the matching is going to be done correctly. 
#For this, additional rows will be created adding a minute
#difference in each one. There will be as many new rows as the duration of each stress event.

new_rows = []

# Loop through the rows in the dataset
for i in range(len(survey)):
    # Get the total minutes for the current row
    total_minutes = survey.iloc[i]['total_minutes']
    
    # Add the number of rows specified by the total minutes
    for j in range(total_minutes):
        # Create a new row with the same hour value
        new_row = {'total_minutes': 1,
                   'total_minutes_original': survey.iloc[i]['total_minutes'],
                   'datetime': survey.iloc[i]['datetime'],
                   'Nurse_ID': survey.iloc[i]['Nurse_ID'],
                   'stress_level': survey.iloc[i]['stress_level'],
                  }
        
        # Add the new row to the list
        new_rows.append(new_row)
        
survey = survey.append(pd.DataFrame(new_rows), ignore_index=True)
survey = survey.loc[survey["total_minutes"] == 1, :]
survey.drop("duration", axis = 1, inplace = True)

survey['Stress level'].replace('na', np.nan, inplace=True)
survey.dropna(inplace=True)

survey['Start datetime'] =  pd.to_datetime(survey['date'].map(str) + ' ' + survey['Start time'].map(str))
survey['End datetime'] =  pd.to_datetime(survey['date'].map(str) + ' ' + survey['End time'].map(str))
survey.drop(['Start time', 'End time', 'date'], axis=1, inplace=True)

survey = survey[survey['End datetime'] <= daylight].copy()
survey['Start datetime'] = survey['Start datetime'].apply(lambda x: x + timedelta(hours=5))
survey['End datetime'] = survey['End datetime'].apply(lambda x: x + timedelta(hours=5))

survey.reset_index(drop=True, inplace=True)

"""###  2.c. Join of the datasets <a class="anchor" id="section2c"></a>"""

print('Labelling ...')
ids = df['id'].unique()

for id in ids:
    new_df = pd.DataFrame(columns=['X', 'Y', 'Z', 'EDA', 'HR', 'TEMP', 'id', 'datetime', 'label'])

    sdf = data_user[data_user['id'] == id].copy()
    survey_sdf = survey[survey['ID'] == id].copy()

    for _, survey_row in survey_sdf.iterrows():
        ssdf = sdf[(sdf['datetime'] >= survey_row['Start datetime']) & (sdf['datetime'] <= survey_row['End datetime'])].copy()

        if not ssdf.empty:
            ssdf['label'] = np.repeat(survey_row['Stress level'], len(ssdf.index))
            new_df = pd.concat([new_df, ssdf], ignore_index=True)
        else:
            print(f"{survey_row['ID']} is missing label {survey_row['Stress level']} at {survey_row['Start datetime']} to {survey_row['End datetime']}")
        
    results = pd.concat([new_df, results], ignore_index=True)

pool = multiprocessing.Pool(len(ids))
results = pool.map(parallel, ids)
pool.close()
pool.join()

print('Saving ...')
results.to_csv('C:/Users/gg22406.CAMPUS/OneDrive - University of Essex/New folder/combined/merged_data_labeled.csv', index=False)
print('Done')

data = pd.read_csv("C:/Users/gg22406/OneDrive - University of Essex/New folder/combined/merged_data_labeled.csv",
                  dtype={'id': 'str'})

data["datetime"]=pd.to_datetime(data["datetime"])

# -------------------------------------------------------------#
#EDA (mean, min, max, std, kurtosis, skew, number of peaks, Amphitude, duration)
#HR (mean, min, max, std, RMS)
#TEMP (mean, min, max, std, RMS)
# -------------------------------------------------------------#
data_mean = data.groupby([pd.Grouper(key="datetime", freq = "5S"), "id", "label"]).agg({
#    'X':['mean', 'min', 'max'],
#    'Y':['mean', 'min', 'max'],
#    'Z':['mean', 'min', 'max'],
    'EDA':['mean', 'min', 'max', np.std],
    'HR':['mean', 'min', 'max', np.std],
    'TEMP':['mean', 'min', 'max', np.std],
    
})#.reset_index()

data.loc[(data["datetime"] >= "2020-04-14 22:31:00") &
     (data["datetime"] <= "2020-04-14 22:31:05") &
         (data["id"] == "5C")
        ]

#data_mean1 =data_mean.iloc[1:200, :]
#data_mean1['index1'] = data_mean1.index
data_mean["id"]= data_mean.index.get_level_values(1)
data_mean["datetime"]= data_mean.index.get_level_values(0)
data_mean["index1"]= data_mean.index
data_empty = pd.DataFrame(columns =['X', 'Y', 'Z', 'EDA', 'HR', 
                                    'TEMP', 'id', 'datetime', 'label', 
                                    'num_Peaks', 'amphitude', 'duration'])

for j in data.id.unique():
    print("user_id: ", j)
    dat_filter = data.loc[(data["id"] == j)]
    data_mean1 = data_mean.loc[(data_mean["id"] == j)]
    for i in range(0, len(data_mean1['index1'])):
        print("user_id: ",j, " ;; range: ", i)
        dat_prev = dat_filter.loc[(dat_filter["datetime"] >= data_mean1['index1'][i][0]) &
                    (dat_filter["datetime"] <  (data_mean1['index1'][i][0] + datetime.timedelta(seconds=5))) 
          ]

        peaks,properties = find_peaks(dat_prev["EDA"], width=5)
        dat_prev["num_Peaks"] = len(peaks)

        prominences = np.array(properties['prominences'])
        widths = np.array(properties['widths'])
        dat_prev["amphitude"] = np.sum(prominences)
        dat_prev["duration"] = np.sum(widths)
        dat_prev = dat_prev.groupby([pd.Grouper(key="datetime", freq = "5S"), "id", "label"],
                                   as_index = False).head(1)
        data_empty = pd.concat([data_empty, dat_prev])

data_empty.to_csv("C:/Users/gg22406/OneDrive - University of Essex/New folder/combined/dat_prev_before_merge.csv")

data_empty = pd.read_csv("C:/Users/gg22406/OneDrive - University of Essex/New folder/combined/dat_prev_before_merge.csv")

data_empty[["datetime", "id", "num_Peaks", "amphitude", "duration"]]

data_mean[['HR_rms', 'TEMP_rms']] =data.groupby([pd.Grouper(key="datetime", freq = "5S"), "id", "label"]).agg(
    {"HR": lambda x:  np.sqrt(np.mean(np.square(np.ediff1d(x)))),
     "TEMP": lambda x:  np.sqrt(np.mean(np.square(np.ediff1d(x))))
    })

data_mean.columns = data_mean.columns.droplevel(level=1)
data_mean =data_mean.reset_index()

data_mean.rename(columns={ data_mean.columns[3]: "EDA_mean",
                         data_mean.columns[4]: "EDA_min",
                         data_mean.columns[5]: "EDA_max",
                         data_mean.columns[6]: "EDA_std",
                          
                        data_mean.columns[7]: "HR_mean",
                         data_mean.columns[8]: "HR_min",
                         data_mean.columns[9]: "HR_max",
                         data_mean.columns[10]: "HR_std",
                          
                         data_mean.columns[11]: "TEMP_mean",
                         data_mean.columns[12]: "TEMP_min",
                         data_mean.columns[13]: "TEMP_max",
                         data_mean.columns[14]: "TEMP_std",
                          
                          data_mean.columns[15]: "HR_rms",
                         data_mean.columns[16]: "TEMP_rms"
                         }, inplace = True)

"""## Join data_mean and the data empty"""

data_empty["datetime"]=pd.to_datetime(data_empty["datetime"])
data_mean["datetime"]=pd.to_datetime(data_mean["datetime"])

data_mean=data_mean.merge(data_empty[["datetime", "id", "label","num_Peaks", "amphitude", "duration"]], 
                on=['id', 'datetime'],
               how = "left")

"""## 2. Kurtosis"""

data_index_kurtosis_mean = data.groupby([pd.Grouper(key="datetime", freq = "5S"), "id", "label"]).agg({"EDA": lambda x: x.kurtosis(skipna=True)})
data_index_kurtosis_mean.rename(columns={'EDA':'EDA_kurtosis'},inplace=True)

data_index_kurtosis_mean=data_index_kurtosis_mean.dropna(how='all')

"""## 3. Skew"""

data_skew_mean = data.groupby([pd.Grouper(key="datetime", freq = "5S"), "id", "label"]).agg(
    { "EDA": lambda x: x.skew(skipna=True)})
data_skew_mean.rename(columns={'EDA':'EDA_skew'},inplace=True)

data_skew_mean=data_skew_mean.dropna(how='all')

data_sk_kurt=data_skew_mean.merge(data_index_kurtosis_mean, on=['id', 'datetime'], how = "left")
data_sk_kurt=data_sk_kurt.reset_index()
data_sk_kurt.head(2)

"""## 4. Join everything together"""

data_final=data_mean.merge(data_sk_kurt,  on=['id', 'datetime'], how = "left")

data_final=data_final.drop('label_y',axis =1)

cols = ['datetime', 'id', 'label', 
        'EDA_mean', 'EDA_min', 'EDA_max', 'EDA_std',
       'HR_mean', 'HR_min', 'HR_max', 'HR_std', 
        'TEMP_mean', 'TEMP_min', 'TEMP_max', 'TEMP_std',  'HR_rms',
       'TEMP_rms', 'num_Peaks', 'amphitude', 'duration', 'EDA_skew',
       'EDA_kurtosis']

data_final.columns = cols

data_final=data_final.drop(['id2', 'datetime', 'groupiddatetime'],axis =1)

# count the number of NaN values in each column
nan_counts = data_final.isna().sum()

# print the results
print(nan_counts)

data_final.to_csv("C:/Users/gg22406/OneDrive - University of Essex/New folder/combined/data_final_to_model_LSTM.csv")

df_features=data_final

df_lag_features = pd.concat([
    df_features['HR_mean'].shift(10),  df_features['HR_mean'].shift(9),    df_features['HR_mean'].shift(8),
    df_features['HR_mean'].shift(7),   df_features['HR_mean'].shift(6),    df_features['HR_mean'].shift(5),
    df_features['HR_mean'].shift(4),   df_features['HR_mean'].shift(3),    df_features['HR_mean'].shift(2),
    df_features['HR_mean'].shift(1),   df_features['TEMP_mean'].shift(10), df_features['TEMP_mean'].shift(9),
    df_features['TEMP_mean'].shift(8), df_features['TEMP_mean'].shift(7),  df_features['TEMP_mean'].shift(6),
    df_features['TEMP_mean'].shift(5), df_features['TEMP_mean'].shift(4),  df_features['TEMP_mean'].shift(3),
    df_features['TEMP_mean'].shift(2), df_features['TEMP_mean'].shift(1),  df_features['EDA_mean'].shift(10),
    df_features['EDA_mean'].shift(9),  df_features['EDA_mean'].shift(8),   df_features['EDA_mean'].shift(7),
    df_features['EDA_mean'].shift(6),  df_features['EDA_mean'].shift(5),   df_features['EDA_mean'].shift(4),
    df_features['EDA_mean'].shift(3),  df_features['EDA_mean'].shift(2),   df_features['EDA_mean'].shift(1)], axis=1)

cols = list(map(str, range(30, 0, -1)))
df_lag_features.columns = cols
df_lag_featuresna = df_lag_features.dropna()
df_lag_featuresna.shape

#df_temp = df_lag_features.iloc[30:, ]
df_total = pd.concat([df_lag_features, data_final], axis=1)

df_total = df_total.dropna(how='all')

df_total =df_total[30:]

df_total.to_csv("C:/Users/gg22406/OneDrive - University of Essex/New folder/combined/data_model.csv")

"""## 6. References 📚 <a class="anchor" id="section6"></a>

Hosseini, Seyedmajid et al. (2021), A multi-modal sensor dataset for continuous stress detection of nurses in a hospital, Dryad, Dataset, https://doi.org/10.5061/dryad.5hqbzkh6f

Siirtola, & Röning, J. (2020). Comparison of Regression and Classification Models for User-Independent and Personal Stress Detection. Sensors (Basel, Switzerland), 20(16), 4402–. https://doi.org/10.3390/s20164402
"""