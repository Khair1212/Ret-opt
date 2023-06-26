#import necessary packages
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os
import plotly.graph_objs as go
import datetime as dt 
from sklearn import preprocessing
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler

import seaborn as sns
import numpy as np
import joblib
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


import sys
import os
import django
import pickle

# Add the Django project's root directory to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retopt.settings')
django.setup()

from segmentation.views import insert_processed_data, generate_dataframe

# tran_df = pd.read_csv('/home/nishad/Mine/Development/SPL-3/FinalProject/retopt/segmentation/data/data2.csv')
tran_df = generate_dataframe()

print(tran_df.shape)
from sklearn.base import TransformerMixin


class RFMTransformer(TransformerMixin):
    def __init__(self, Now):
        self.Now = dt.datetime(2014, 2, 20)
        self.RFM = pd.DataFrame()
    
    def transform(self, tran_df):
        tran_df = tran_df.sample(frac=1, random_state=42)
        tran_df['Transaction Date'] = pd.to_datetime(tran_df['Transaction Date'], dayfirst=True)
        
        # Recency
        self.RFM['recency'] = tran_df.groupby('Customer ID').agg({'Transaction Date': lambda x: (self.Now - x.max()).days}) 

        # Frequency
        self.RFM['frequency'] = tran_df.groupby('Customer ID').agg({'Transaction ID': lambda x: len(x)}) 
        
        # Monetary
        self.RFM['monetary'] = tran_df.groupby('Customer ID').agg({'Net_Sales': lambda x: sum(x)})
        
        # Normalization
        self.RFM['normalized_recency'] = pd.qcut(self.RFM['recency'], 5, duplicates='drop', labels=False)
        self.RFM['normalized_recency'] = self.RFM['normalized_recency'] + 1
        self.RFM['normalized_frequency'] = pd.qcut(self.RFM['frequency'], 5, duplicates='drop', labels=False)
        self.RFM['normalized_frequency'] = self.RFM['normalized_frequency'] + 1
        self.RFM['normalized_monetary'] = pd.qcut(self.RFM['monetary'], 5, duplicates='drop', labels=False)
        self.RFM['normalized_monetary'] = self.RFM['normalized_monetary'] + 1
        
        # Handle missing values with median imputation
        self.RFM.fillna(self.RFM.median(), inplace=True)
        
        return self.RFM[['normalized_recency', 'normalized_frequency', 'normalized_monetary']].values 

    def fit(self, tran_df, y=None):
        return self

   
# Load the pipeline from the pickle file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "rfm_pipeline.pkl")

print(model_path)
#tran_df.to_csv('Transaction_dataset.csv', index=False)
with open(model_path, 'rb') as file: 
    pipeline = pickle.load(file) 
print(pipeline) 
#transformed_data = pipeline.transform(tran_df)


# Fit the pipeline
#pipeline.fit(tran_df)

# Get the cluster assignments
cluster_assignments = pipeline.predict(tran_df)
print("Cluster Len:",len(cluster_assignments))

# Reverse map the recency and calculate the RFM score
RFM = pipeline.named_steps['preprocessing'].RFM
RFM['k_means_cluster'] = pipeline.named_steps['kmeans'].labels_ 
RFM['normalized_recency'].replace({1:5,2:4,3:3,4:2,5:1}, inplace=True) 
RFM['Score'] = RFM['normalized_recency'] + RFM['normalized_frequency'] + RFM['normalized_monetary'] 

# Get the mean RFM score by cluster
# RFM['k_means_cluster'] = cluster_assignments
# RFM = RFM.groupby('k_means_cluster')['Score'].mean().reset_index()

# Cluster_name = ['Champions', 'Loyal Customer', 'Potential Loyalist', 'About to Sleep', 'Hibernating', 'Random']
# RFM['Cluster_name'] = Cluster_name

tmp = pd.DataFrame({'k_means_cluster': cluster_assignments, 'Score': RFM['Score']})
tmp = tmp.groupby('k_means_cluster')['Score'].mean().reset_index()

# Name the clusters
Cluster_name = ['Champions', 'Loyal Customer', 'Potential Loyalist', 'About to Sleep', 'Hibernating']
tmp['Cluster_name'] = Cluster_name
RFM = RFM.reset_index()
RFM = RFM.merge(tmp[['k_means_cluster','Cluster_name']], how='left', on = 'k_means_cluster') 

# Add the cluster names to the dataset 
#pipeline.set_params(cluster_names=tmp[['k_means_cluster', 'Cluster_name']])
customer_id = RFM['Customer ID']
RFM['Customer ID'] = customer_id
print(RFM[RFM['Customer ID']==275269])

#Let's see the average of each segment for monetary, frequency and recency. This will help us in naming the clusters

# print("Mean Monetary by segment: ",RFM.groupby("Cluster_name")["monetary"].mean())
# print()
# print("Mean frequency by segment: ",RFM.groupby("Cluster_name")["frequency"].mean())
# print()
# print("Recency by segment: ",RFM.groupby("Cluster_name")["recency"].mean())
print("RFM is ", RFM)

##Visual

PLOT = go.Figure()

for C in list(RFM.k_means_cluster.unique()):
    
    PLOT.add_trace(go.Scatter3d(x = RFM[RFM.k_means_cluster == C]['recency'],
                                y = RFM[RFM.k_means_cluster == C]['frequency'],
                                z = RFM[RFM.k_means_cluster == C]['monetary'],
                                mode = 'markers', marker_size = 8, marker_line_width = 1,
                                name =  str(C))) 

PLOT.update_layout(width = 1000, height = 800, autosize = True, showlegend = True,
                   scene = dict(xaxis=dict(title = 'Recency', titlefont_color = 'black'),
                                yaxis=dict(title = 'Frequency', titlefont_color = 'black'),
                                zaxis=dict(title = 'Monetary Value', titlefont_color = 'black')),
                   font = dict(family = "Gilroy", color  = 'black', size = 12))



selected_columns = RFM[['Customer ID', 'Cluster_name']]
#selected_columns = selected_columns.sort_values('Customer ID', ascending=False)

insert_processed_data(selected_columns, PLOT)
