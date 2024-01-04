#!/Users/jimanderssen/anaconda3/bin/python
import sys
import os
#print(sys.executable)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
# plots a line given an intercept and a slope
from statsmodels.graphics.regressionplots import abline_plot

def load_file():
    df = pd.read_csv('one year test.csv', sep=';', encoding='latin-1', on_bad_lines='skip')

    ## Choosing columns from whole df
    data = "'Tid;P4_L10_C&% Temp [C];P4_L10_C&% Hum [%RH];P4_L10_C&% Pres [mBar];P4_L9_C&% Temp [C];P4_L9_C&% Hum [%RH];P4_L9_C&% Pres [mBar];P4_L6_C&% Temp [C];P4_L6_C&% Hum [%RH];P4_L6_C&% Pres [mBar];P4_L4_C&% Temp [C];P4_L4_C&% Hum [%RH];P4_L4_C&% Pres [mBar];P3_L13_C&% Temp [C];P3_L13_C&% Hum [%RH];P3_L13_C&% Pres [mBar];P3_L14_C&% Temp [C];P3_L14_C&% Hum [%RH];P3_L14_C&% Pres [mBar];P4_L8_C&% Temp [C];P4_L8_C&% Hum [%RH];P4_L8_C&% Pres [mBar];P4_L5_C&% Temp [C];P4_L5_C&% Hum [%RH];P4_L5_C&% Pres [mBar];P4_L12_Vai.C& Temp1 [C];P4_L12_Vai.C& Temp2 [C];P4_L12_Vai.C& Hum [%RH];P4_L12_Vai.C& Dew [C];P4_L12_Vai.C& Abs Hum [g/m3];P4_L12_Vai.C& Vapor P [hPa];P4_L1_Vai.C&% Temp1 [C];P4_L1_Vai.C&% Temp2 [C];P4_L1_Vai.C&% Hum [%RH];P4_L1_Vai.C&% Dew [C];P4_L1_Vai.C&% Abs Hum [g/m3];P4_L1_Vai.C&% Vapor P [hPa];P3_L13_Vai.C& Temp1 [C];P3_L13_Vai.C& Temp2 [C];P3_L13_Vai.C& Hum [%RH];P3_L13_Vai.C& Dew [C];P3_L13_Vai.C& Abs Hum [g/m3];P3_L13_Vai.C& Vapor P [hPa];P4_U.LnsiC& Temp [C];P4_U.LnsiC& Hum [%RH];P4_U.LnsiC& Pres [mBar];O3_U.It_C&% Temp [C];O3_U.It_C&% Hum [%RH];O3_U.It_C&% Pres [mBar];P4_L10_Vai.C& Temp1 [C];P4_L10_Vai.C& Temp2 [C];P4_L10_Vai.C& Hum [%RH];P4_L10_Vai.C& Dew [C];P4_L10_Vai.C& Abs Hum [g/m3];P4_L10_Vai.C& Vapor P [hPa];P3_L13_S/YP.Pa Pres [Pa];P4_L7_S/YP.Pa Pres [Pa];P4_Sis/Ulk.Pa Pres [Pa];P4_L2_S/YP.Pa Pres [Pa];P4_S.Ln_C&% Temp [C];P4_S.Ln_C&% Hum [%RH];P4_S.Ln_C&% Pres [mBar];P4_S.It_C&% Temp [C];P4_S.It_C&% Hum [%RH];P4_S.It_C&% Pres [mBar]" 
    data = data.replace(';', "','" )
    data += "'"
    data_list = [col.strip("'") for col in data.split(',')]
   
    df = df[data_list]
    # Making shorter names
    short_col = "'Tid;P4_L10_T;P4_L10_H;P4_L10_P;P4_L9_T;P4_L9_H;P4_L9_P;P4_L6_T;P4_L6_H;P4_L6_P;P4_L4_T;P4_L4_H;P4_L4_P;P3_S13_T;P3_S13_H;P3_S13_P;P3_L14_T;P3_L14_H;P3_L14_P;P4_L8_T;P4_L8_H;P4_L8_P;P4_L5_T;P4_L5_H;P4_L5_P;P4_L12_T1;P4_L12_T2;P4_L12_H;P4_L12_D;P4_L12_AH;P4_L12_VP;P4_L1_T1;P4_L1_T2;P4_L1_H;P4_L1_D;P4_L1_AH;P4_L1_VP;P3_L13_T1;P3_L13_T2;P3_L13_H;P3_L13_D;P3_L13_AH;P3_L13_VP;P4_UL_T;P4_UL_H;P4_UL_P;O3_UI_T;O3_UI_H;O3_UI_P;P4_M10_T1;P4_M10_T2;P4_M10_H;P4_M10_D;P4_M10_AH;P4_M10_VP;P3_L13_S_L;P4_L7_S_L;P4_S_U;P4_L2_S_L;P4_SL_T;P4_SL_H;P4_SL_P;P4_SI_T;P4_SI_H;P4_SI_P"
    short_col = short_col.replace(';', "','" )
    short_col += "'"
    short_list = [col.strip("'") for col in short_col.split(',')]

    # Changing names from long to short in dataFrame
    col_dict = {data_list[i]: short_list[i] for i in range(len(data_list))}
    df.rename(columns=col_dict, inplace=True)
    
    ###

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', 20)
    #pd.set_option('display.max_columns', None)
    
    ###

    # Changing to numeric => float
    df = df.apply(lambda col: col.str.replace(',', '.', regex=False) if col.dtype == 'object' else col)
    first_column = df.iloc[:, 0]
    numeric_cols = df.iloc[:,1:].apply(pd.to_numeric, errors='coerce')
    df = pd.concat([first_column, numeric_cols], axis=1)
    
    #change to float32
    numeric_cols = df.select_dtypes(include=['float64']).columns
    df[numeric_cols] = df[numeric_cols].astype('float32')
    return df


def RH(df, sensor):
    RH_mask = abs(100 - df[sensor] <= 0.50)
    col_to_mask = df.filter(like=f"{sensor[0:6]}").columns
    col_to_mask = list(col_to_mask)
    working_df = df[['Tid'] + col_to_mask + ['P4_UL_T','P4_UL_H','P4_UL_P']]
    #working_df = df.loc[RH_mask, col_to_mask]

    
    if working_df.shape[1] == 7:
        working_df = calculate_dew(working_df, sensor)
        # Dew mask trial
        dew_mask = (abs(working_df[f"{sensor[:-1]+'T'}"] - working_df[f"{sensor[:-1]+'D'}"]) <= 0.5)
        working_df = working_df[RH_mask | dew_mask]
    else:
        #working_df = df.loc[RH_mask, col_to_mask]
        dew_mask = (abs(working_df[f"{sensor[:-1]+'T1'}"] - working_df[f"{sensor[:-1]+'D'}"]) <= 0.5)
        working_df = working_df[RH_mask | dew_mask]
    print(apply_RH_mask(working_df))
    #return df.loc[RH_mask, col_to_mask]
    
def calculate_dew(df, sensor):
    #Calculate dew point for climate 
    # T(dt) = (243.04*(ln(RH/100))+(17.625*Ta)/(243.04+Ta))/(17.625-ln(RH/100))
    RH = sensor
    
    Ta = f"{sensor[:-1]+'T'}"    
    ##
    N = (np.log(df[RH]/100)+((17.27*df[Ta])/(237.3+df[Ta])))/17.27
    Dt = (237.3*N)/(1-N)
    ##
    df.insert(df.columns.get_loc(f"{RH}"), f"{sensor[:-1] + 'D'}", Dt)
    return df

def apply_RH_mask(df):
    print('Mean: ')
    print(df.mean())
    print('Std_dev: ')
    print(df.std())
    print(f"Number of days: {len(df)}")
    #return 
    return df

def group_data(df):
    # Altering the format of the time column
    df['Tid'] = pd.to_datetime(df['Tid'], format='%d.%m.%Y %H:%M:%S')
    #df.set_index('Tid', inplace=True)
    return df
    
def condense(df, sensor):
    pass

def multi_regression(df, sensor):
    # Making a multi regressional model
    
    #  Adjusting for T1 edge case (Vaisala sensors)
    if len(sensor) == 7 and sensor[4] != '1':
        df = calculate_dew(df, sensor)
    col_to_mask = df.filter(like=f"{sensor[0:6]}").columns
    col_to_mask = list(col_to_mask)
    working_df = df[col_to_mask + ['P4_UL_T','P4_UL_H','P4_UL_P','O3_UI_T', 'O3_UI_H', 'O3_UI_P','P3_L13_S_L','P4_L7_S_L', 'P4_S_U', 'P4_L2_S_L','P4_SL_T','P4_SL_H','P4_SL_P','P4_SI_T','P4_SI_H','P4_SI_P']]
    working_df.index = pd.to_datetime(df['Date'])
    #working_df = df[col_to_mask + ['P4_UL_T','P4_UL_H','P4_UL_P','O3_UI_T', 'O3_UI_H', 'O3_UI_P']]
    
    choice = input('Select choice (multi or not)')
    if choice == 'm':
        working_df = mean_delta_T_Dew(working_df, sensor)
        working_df = working_df.loc['2022-10-1':'2023-03-30']   
        working_df.dropna(inplace=True)
        print(len(working_df))
        print(working_df.shape)
        print(working_df.head())
        #fit = smf.ols(f'{sensor} ~ {sensor[:-1]+"T1"} + P4_UL_T + P4_UL_H + P4_UL_P + P4_L7_S_L + P4_L2_S_L + P4_S_U + P4_SL_T + P4_SL_H + P4_SL_P + P4_SI_T + P4_SI_H + P4_SI_P', data = working_df).fit()
        fit = smf.ols(f'{sensor} ~ P4_L2_S_L', data = working_df).fit()
        #fit = smf.ols(f'{sensor} ~ {sensor[:-1]+"T"}', data = working_df).fit()
        #fit = smf.ols(f'TDew ~ {sensor[:-1]+"T1"}', data = working_df).fit()
        #fit = smf.ols(f'TDew ~ {sensor}', data = working_df).fit()
        #fit = smf.ols(f'{sensor[:-1]+"T"} ~ P4_UL_T + P4_UL_H + P4_UL_P + P4_L7_S_L + P4_L2_S_L + P4_S_U + P4_SL_H + P4_SL_P + P4_SI_T + P4_SI_H + P4_SI_P', data = working_df).fit()
        #fit = smf.ols(f'{sensor[:-1]+"T1"} ~ P4_UL_T + P4_UL_H + P4_UL_P + P4_L7_S_L + P4_L2_S_L + P4_S_U + P4_SL_H + P4_SL_P + P4_SI_T + P4_SI_H + P4_SI_P', data = working_df).fit()
        print(fit.summary())
    

def mean_delta_T_Dew(df, sensor):
    df.index = pd.to_datetime(df.index)
    pd.set_option('mode.chained_assignment', None)
    df_copy = df.copy()
    if len(sensor) == 7 and sensor[4] != '1':
        df_copy['TDew'] = df_copy[f"{sensor[:-1]+'T'}"] - df[f"{sensor[:-1]+'D'}"]
    else:
        df_copy['TDew'] = df_copy[f"{sensor[:-1]+'T1'}"] - df[f"{sensor[:-1]+'D'}"]
    return df_copy

def mean_conditions(df, sensor, count_times):
        #print(len(df))
        #print(df.shape)
        #print(df)

        # Flexibility to analyse mean data file
        print('Are you using mean or full data?')
        if len(df) > 365:
            if count_times == 0:
                df = daily_mean(df)
                count_times += 1
        
        #RH_mask = abs(100 - df[sensor] <= 5.0)
        col_to_mask = df.filter(like=f"{sensor[0:6]}").columns
        col_to_mask = list(col_to_mask)
        working_df = df[col_to_mask + ['P4_UL_T','P4_UL_H','P4_UL_P','O3_UI_T', 'O3_UI_H', 'O3_UI_P','P3_L13_S_L','P4_L7_S_L', 'P4_S_U', 'P4_L2_S_L']]


        choice = input('Select choice (mask or not)')
        if choice == 'mask':
            # Edge case (Vaisala sensors)
            if len(sensor) == 7 and sensor[4] != '1':
                if count_times == 0:
                    working_df = calculate_dew(working_df, sensor)
                # Dew mask trial
                dew_mask = (abs(working_df[f"{sensor[:-1]+'T'}"] - working_df[f"{sensor[:-1]+'D'}"]) <= 1.5)
                working_df = working_df[dew_mask]

                working_df = working_df.loc['2022-11-01':'2023-03-01']

                masked_df = index_for_T_Dew_mask(working_df, sensor)
                print()
                print('Values for masked df:')
                print(apply_RH_mask(masked_df))
                return masked_df
            else:
                dew_mask = (abs(working_df[f"{sensor[:-1]+'T1'}"] - working_df[f"{sensor[:-1]+'D'}"]) <= 1.5)
                #working_df = working_df[RH_mask | dew_mask]
                working_df = working_df[dew_mask]

                working_df = working_df.loc['2022-11-01':'2023-03-01']

                masked_df = index_for_T_Dew_mask(working_df, sensor)
                print()
                print('Values for masked df:')
                print(apply_RH_mask(masked_df))
                return working_df
        
        else:
            # If not Vaisala
            if len(sensor) == 7 and sensor[4] != '1':
                df = calculate_dew(df, sensor)
            df.index = pd.to_datetime(df.index)

            df_slice = df.loc['2022-11-01':'2023-03-01']   
            #print(len(df_slice))
            #print(df_slice.shape)
            #print(df_slice)
            df_slice = mean_delta_T_Dew(df_slice, sensor)
            #print(apply_RH_mask(df_slice))
            include = input('Include specific days (y/n): ')
            if include == 'y':
                # Recursive functionality
                masked_df = mean_conditions(df, sensor, count_times)
                print()
                #print('Values for df slice:')
                #print(df_slice.loc[:,'P4_L4_D'])
                #print(apply_RH_mask(df_slice))
                plot_multiple(df_slice, masked_df, sensor)
            elif include == 'n':
                plot_data(df_slice)
            else:
                return  
        return count_times

def daily_mean(df):
    ##  Make daily mean version of file
    #   Convert tid column to datetime format
    df['Tid'] = pd.to_datetime(df['Tid'], format='%d.%m.%Y %H:%M:%S')

    ##  Extract only the date part from the tid column
    df['Date'] = df['Tid'].dt.date
    daily_mean = df.groupby('Date').mean()
    daily_mean.to_csv('mean_data_all.csv', sep=';', encoding='latin-1')
    #df['Tid'] = df['Tid'].dt.date
    #daily_mean = df.groupby('Tid').mean()
    
    #daily_mean = df.groupby('Date')
    df = daily_mean
    #df.set_index('Tid', inplace=True)

    return df
    
def index_for_T_Dew_mask(working_df, sensor):
    working_df.index = pd.to_datetime(working_df.index)
    if len(sensor) == 7 and sensor[4] != '1':
        working_df['TDew'] = working_df[f"{sensor[:-1]+'T'}"] - working_df[f"{sensor[:-1]+'D'}"]
    else:
        working_df['TDew'] = working_df[f"{sensor[:-1]+'T1'}"] - working_df[f"{sensor[:-1]+'D'}"]
    return working_df
#working_df.insert(working_df.columns.get_loc(f"{RH}"), "Delta T", )


def plot_multiple(df_slice, masked_df, sensor):
    df_slice.dropna(inplace=True)
    #print(masked_df)
    #masked_df.dropna(inplace=True)

    #fig, axes = plt.subplots(nrows=1,ncols=1)
    plt.figure()
    plt.plot(df_slice['TDew'])
    #x_min, x_max = plt.gca().get_xlim()
    #print('xmin, xmax', x_min, x_max)
    filtered_masked = masked_df[(masked_df.index >= df_slice.index[0]) & (masked_df.index <= df_slice.index[-1])]
    print(filtered_masked.shape)
    print(filtered_masked)
    plt.scatter(filtered_masked.index, filtered_masked['TDew'], color='red', s=15)
    #plt.scatter(masked_df.index, masked_df['TDew'], color='red', s=15)

    plt.ylabel('D T-Dew')
    plt.grid(True)    
    plt.text(0.95,0.98, f"Total days: {masked_df['TDew'].count()}", ha='right', va='top', transform=plt.gca().transAxes)

    #Calculate variance in x-axis (days)
    diff_masked = pd.Series(masked_df.index).diff().dt.days.dropna()
    mean_distance = diff_masked.mean()
    #var_masked = diff_masked.var()
    #std_masked = diff_masked.std()
    #pe_std = std_masked/np.sqrt(len(masked_df))
    plt.text(0.95,0.93, f"Mean distance (days): {mean_distance:.2f}", ha='right', va='top', transform=plt.gca().transAxes)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    if len(sensor) == 7:
        plt.title(f"{sensor[0:5]}")
    elif len(sensor) > 7:
        plt.title(f"{sensor[0:6]}")

    plt.show(block=False)
    return df_slice

def plot_data(df):
    df.dropna(inplace=True)
    fig, axes = plt.subplots(nrows=1,ncols=2)
    #axes[0].scatter(df['Delta UT'], df['Delta T-Dew'])
    axes[0].plot(df['Delta T-Dew'])
    #axes[0].set_xlabel('D UT')
    axes[0].set_ylabel('D T-Dew')
    axes[0].grid(True)
    

    axes[1].scatter(df['Delta UT'], df['Delta LT'])
    axes[1].set_xlabel('D UT')
    axes[1].set_ylabel('D LT')
    slope, intercept = np.polyfit(df['Delta UT'], df['Delta LT'], 1)
    
    axes[1].plot(df['Delta UT'], slope * df['Delta UT'] + intercept, color='red', label = f"y = {slope:.2f}x + {intercept:.2f}")
    axes[1].legend()
    axes[1].grid(True)
    plt.show(block=False)
    return df

def main():
    df = load_file()

    # Make different choices of data and masks
    while True:
        print('Are you using mean or full data?')
        print('P4: L1 (Vai), L4, L5, L6, L8, L9, L10, L12 (Vai) \n'
              'P3: L13 (Vai), L14')    
        sensor = input('Type which sensor (Type 0 to quit): ')
        count_times = 0
        if sensor == '0':
            break
        selection = input('Choose condition (rh, multi = m, blank (=winter)): ')
        if selection == 'rh':
            RH(df, sensor)
        if selection == 'condense':
            df = group_data(df)
            condense(df, sensor)
        if selection == 'm':
            multi_regression(df, sensor)
        #if selection == 'winter':
        #    df_slice = df.loc['2022-10-1':'2023-03-30']
        #    mean_conditions(df_slice, sensor, count_times)
        else:
            mean_conditions(df, sensor, count_times)
            #continue

if __name__ == "__main__":
    main()