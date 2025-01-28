import pandas as pd
import os
import numpy as np

# other configurations 
path = 'C:/dev/IA'
path_csv = path + '/data'
path_zip = path + '/data'

# load data
def loadData() :
    general = pd.read_csv(path_csv + '/general_data.csv')
    employeeSurvey = pd.read_csv(path_csv + '/employee_survey_data.csv')
    managerSurvey = pd.read_csv(path_csv + '/manager_survey_data.csv')
    return general, employeeSurvey, managerSurvey

def loadGeneral():
    general = pd.read_csv(path_csv + '/general_data.csv')
    return general

def loadEmployeeSurvey():
    employeeSurvey = pd.read_csv(path_csv + '/employee_survey_data.csv')
    return employeeSurvey

def loadManagerSurvey():
    managerSurvey = pd.read_csv(path_csv + '/manager_survey_data.csv')
    return managerSurvey

def loadInTime():
    inTime = pd.read_csv(path_csv + '/in_time.csv')
    return inTime

def loadOutTime():
    outTime = pd.read_csv(path_csv + '/out_time.csv')
    return outTime

def exportDataCSV(data):
    # Déterminer le chemin de la racine du projet
    root_path = os.path.abspath("..")  # Racine actuelle du projet
    
    # Chemin complet du fichier
    file_path = os.path.join(root_path, "dataClean.csv")
    
    # Vérifier le type des données et les convertir en DataFrame si nécessaire
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, (list, dict)):
        df = pd.DataFrame(data)
    else:
        raise ValueError("Les données doivent être un DataFrame, une liste ou un dictionnaire.")
    
    # Enregistrer les données dans un fichier CSV
    df.to_csv(file_path, index=False)
    print(f"Fichier CSV enregistré : {file_path}")

def loadAndMergeData():
    general, employeeSurvey, managerSurvey = loadData()
    merge1 = general.merge(employeeSurvey, on=['EmployeeID'], how='outer')
    merge2 = merge1.merge(managerSurvey, on=['EmployeeID'], how='outer')
    
    return merge2

def calculWorkTime():
    inTime = loadInTime()
    outTime = loadOutTime()
    # Charger les données
    inTime.rename(columns={'Unnamed: 0':'EmployeeID'},inplace=True)
    outTime.rename(columns={'Unnamed: 0':'EmployeeID'},inplace=True)
    inTime.replace("NA",np.nan,inplace=True)

    for col in inTime.columns.array[1::]:
        inTime[col] = pd.to_datetime(inTime[col],format='%Y-%m-%d %H:%M:%S')
    for col in outTime.columns.array[1::]:
        outTime[col] = pd.to_datetime(outTime[col],format='%Y-%m-%d %H:%M:%S')
        inTime.dtypes
    # refractor the time_diff inTime and outTime into a single dataframe with the following columns : employeeID, date, time_diff, entry_time, exit_time, exit_time - entry_time
    # Melt the inTime and outTime dataframes to long format
    inTime_melted = inTime.melt(id_vars=['EmployeeID'], var_name='Date', value_name='Entry_Time')
    outTime_melted = outTime.melt(id_vars=['EmployeeID'], var_name='Date', value_name='Exit_Time')

    # Merge the melted dataframes on EmployeeID and Date
    merged_times = pd.merge(inTime_melted, outTime_melted, on=['EmployeeID', 'Date'])
    merged_times.dropna(inplace=True)

    # Calculate the time difference
    merged_times['Worktime'] = merged_times['Exit_Time'] - merged_times['Entry_Time']

    # Reorder columns
    times_df = merged_times[['EmployeeID', 'Entry_Time', 'Exit_Time', 'Worktime']]
    # Calculate the mean worktime and number of days worked per employee
    worktime_df = times_df.groupby('EmployeeID').agg(MeanWorktime=('Worktime', 'mean'),DaysWorked=('Worktime', 'count')).reset_index()

    return worktime_df
