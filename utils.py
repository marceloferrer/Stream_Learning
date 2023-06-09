from river import linear_model
from river import stream
from rich import print
import pandas as pd
from river import metrics
from river import datasets
import collections 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

# Get the data set from csv path (specifically the instagram dataset)
def getFakeAccountsDataSet(path):
    dataset = stream.iter_csv(
    path,
    target="fake", 
    converters={
        "profile pic": bool,
        "nums/length username": float,
        "fullname words": float,
        "nums/length fullname": float,
        "name==username": bool,
        "description length": float,
        "external URL": bool,
        "private": bool,
        "#posts": float,
        "#followers": float,
        "#follows": float
    }
    )
    return dataset

# Get the data set from csv path (specifically the amazon dataset)
def getAmazonStockDataSet(path):
    # Remove open interest because value is not actually loaded
    removed_attributes=['OpenInt','Date']
    dataset = stream.iter_csv(
    path,
    target="Close", 
    converters={
        "Open": float,
        "High": float,
        "Low": float,
        "Volume": float,
        "Close": float
    },
    drop=removed_attributes
    )

    return dataset

# Auxiliary plot function to analyse the data
def plot_data(stream, dists, drifts=None):
    fig = plt.figure(figsize=(7,3), tight_layout=True)
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
    ax1, ax2 = plt.subplot(gs[0]), plt.subplot(gs[1])
    ax1.grid()
    ax1.plot(stream, label='Stream')
    ax2.grid(axis='y')
    for id, dist in enumerate(dists):
        ax2.hist(dist, label=f'dist_{id}')
    if drifts is not None:
        for drift_detected in drifts:
            ax1.axvline(drift_detected, color='red')
    plt.show()