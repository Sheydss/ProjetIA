import pandas as pd
import os

# other configurations 
path = 'C:/IA'
path_csv = path + '/data/csv'
path_zip = path + '/data/zip'

# load data
def loadData() :
    general = pd.read_csv(path_csv + '/general_data.csv')
    employeeSurvey = pd.read_csv(path_csv + '/employee_survey_data.csv')
    managerSurvey = pd.read_csv(path_csv + '/manager_survey_data.csv')
    inTime = pd.read_csv(path_csv + '/in_time.csv')
    outTime = pd.read_csv(path_csv + '/out_time.csv')
    return general, employeeSurvey, managerSurvey, inTime, outTime

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
    general, employeeSurvey, managerSurvey, inTime, outTime = loadData()
    merge1 = general.merge(employeeSurvey, on=['EmployeeID'], how='outer')
    merge2 = merge1.merge(managerSurvey, on=['EmployeeID'], how='outer')
    
    return merge2

