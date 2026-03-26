import openeo
from openeo.processes import ProcessBuilder
import rasterio
import matplotlib.pyplot as plt
import os
from shapely.geometry import shape,mapping
from shapely.ops import unary_union
import json
import pandas as pd
import matplotlib.dates as mdates

def load_geojson(file):
    geometries = [shape(feature["geometry"]) for feature in file["features"]]
    merged_geom = unary_union(geometries)
    return mapping(merged_geom)


def create_scan(con, name, timespan, bands, area):
    print(f'Scanning location {name} over timespan {timespan} with bands {bands}')
    cube = con.load_collection(
    "SENTINEL2_L2A",
    spatial_extent = area,
    temporal_extent = timespan,
    bands = bands
    )

    # SCL band, scene classification layer
    scl = cube.band("SCL")       # make sure the cube name matches yours
    
    # build a mask that is True everywhere the pixel is *not* water
    non_water = (scl != 6)   # DataCube of booleans
    
    # apply the mask once and drop SCL
    water_only = (
        cube
            .mask(non_water)             # True ➜ set to nodata
            .filter_bands(["B04", "B05"])  # keep just the spectral bands you need
    )

    B5 = water_only.band("B05")
    B4 = water_only.band("B04")
    
    ndci = (B5-B4)/(B5+B4)     

    ndci_agg_spat = ndci.aggregate_spatial(geometries = area, reducer = "mean")
    ndci_agg_spat_std = ndci.aggregate_spatial(geometries = area, reducer = "sd")
    
    res_agg_spat = ndci_agg_spat.save_result(format='csv')
    res_agg_spat_std = ndci_agg_spat_std.save_result(format='csv')
    
    job_agg_spat = res_agg_spat.create_job(title=f"2025 {name}_m")
    job_agg_spat_std = res_agg_spat_std.create_job(title=f"2025 {name}_sd")
    
    job_agg_spat.start_and_wait()
    job_agg_spat_std.start_and_wait()

    path = f"data/2025 {name}"
    job_agg_spat.get_results().download_files(f"data/{name}_m")
    job_agg_spat_std.get_results().download_files(f'data/{name}_sd')
    print('Scan completed, find results in: ', f'data/{name}_m')
    




def create_latest_df(name):
    daily_mean = pd.read_csv(f"data/{name}_m/timeseries.csv")
    daily_std = pd.read_csv(f"data/{name}_sd/timeseries.csv")

    daily_mean = daily_mean.sort_values(by='date')
    daily_std = daily_std.sort_values(by='date')
    
    daily_mean = daily_mean.dropna()
    daily_std = daily_std.dropna()
    
    daily_mean['date'] = pd.to_datetime(daily_mean['date']).dt.date
    daily_std['date'] = pd.to_datetime(daily_std['date']).dt.date
    #daily_mean["month_day"] = pd.to_datetime(daily_mean["date"]).dt.strftime("%m-%d")
    #daily_std["month_day"] = pd.to_datetime(daily_std["date"]).dt.strftime("%m-%d")
    
    daily_mean.rename(columns={'band_unnamed':'mean'},inplace=True)
    daily_std.rename(columns={'band_unnamed':'std'},inplace=True)

    return pd.merge(daily_mean[['date','mean']],daily_std[['date','std']],on='date',how='inner')
    #to_return['date'] = pd.to_datetime(daily_std['date']).dt.date
    #return to_return

def concatenate_to_series(latest, name):
    df = pd.read_csv(f"../rolling_timeseries/{name}.csv",sep=',')
    concatenated = pd.concat([df,latest]).reset_index().drop(columns='index')
    concatenated.to_csv(f"../rolling_timeseries/{name}.csv",index=False,sep=',')
    return concatenated

def create_plot(df, name):
    # Plot
    df['date'] = pd.to_datetime(df['date'])
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.plot(df['date'], df['mean'],label='mean')
    ax.scatter(df['date'], df['mean'])
    ax.plot(df['date'], df['std'],label='std')
    ax.scatter(df['date'], df['std'])
    # Format x-axis to show only month and day
    
    
    # Optional: rotate x-tick labels for readability
    plt.xticks(rotation=45)
    locator = mdates.DayLocator(interval=5)
    formatter = mdates.DateFormatter('%m-%d')
    
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    
    plt.legend()
    plt.xlabel('Date (MM-DD)')
    plt.ylabel('Chlorophyll (NDCI) index')
    plt.title(f'{name} Chlorophyll index')
    plt.tight_layout()
    plt.grid()
    plt.savefig(f'../plots/{name} CI.png')
    return



def from_single_csv_to_plot(name):
    df = create_latest_df(name)
    df.to_csv(f"../rolling_timeseries/{name}.csv",index=False,sep=',')
    create_plot(df,name)