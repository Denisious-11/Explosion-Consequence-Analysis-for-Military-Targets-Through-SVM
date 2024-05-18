import pandas as pd
import joblib
load_model = joblib.load("Project_Saved_Models/pipeline_svm_model_85acc.sav")

info = []
parameters = ['Target Type',
              'TNT Equivalent(Kg)', 'Range(m)', 'Blast Overpressure']


Target_Type = input(
    "enter Target Type eg:(Light Armour-1,Heavy Armour-2,Troops in Open Field-3,Troops in Bunkers-4,Parked Aircraft-5):::>")
info.append(Target_Type)
TNT_Equivalent = input("enter TNT Equivalent eg:(5,10,15,20):::>")
info.append(TNT_Equivalent)
Range = input("enter range in meter :::>")
info.append(Range)
Blast_Overpressure = input("enter the value of Blast Overpressure:::>")
info.append(Blast_Overpressure)

my_dict = dict(zip(parameters, info))

# convert dict into dataframe
my_data = pd.DataFrame(my_dict, index=[0])

# dataframe is putting into the MODEL to make PREDICTION
my_pred = load_model.predict(my_data)
print(my_pred)

my_pred = my_pred[0]
print(my_pred)


print("\n")
print("RESULT:")
if my_pred == 0:
    print("LOW")
if my_pred == 1:
    print("MODERATE")
if my_pred == 2:
    print("HEAVY")
