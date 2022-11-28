import glob, os, time
from os.path import isfile
import pandas as pd
from matplotlib import pyplot as plt
#from scipy.signal import argrelextrema
import numpy as np
import re
import pprint

# function to convert to subscript
def get_sub(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
    res = x.maketrans(''.join(normal), ''.join(sub_s))
    return x.translate(res)

def graph_char(): 
#Graph characterisation - formats plot
    plt.grid(True)
    title = str(file)
    plt.xlabel("Tip Bias / V", fontsize = 10)
    plt.ylabel("I{}/I{} / Hz/nA ".format(get_sub('E'),get_sub('a')), fontsize = 10)
    #plt.xticks(np.arange(min(df['Kinetic Energy (eV)']), max(df['Kinetic Energy (eV)'])+10, 10.0), fontsize=8)
    plt.yticks(fontsize=8)
    plt.title(title, fontsize = 18)
    plt.legend(fontsize = 10)
    

#Select the desired files 
path = "*00[1-9].dat"
path2 = "*01[0-2].dat"
items = glob.glob(path)
items2 = glob.glob(path2)
project_files = (items + items2) #Added to a list containing all required files for analysis


#If Backward scan performed. Need to sort out Index so all data reads the same in script
    
#os.path.split
#pathname = "C:/Users/oskar/Desktop/My_Scripts/2022-10-12/BBX_HOPG_001.dat"

#(dirname, filename) = os.path.split(pathname)
#(shortname, extension) = os.path.splitext(filename)

# =============================================================================
# metadata = os.stat('BBX_spectrum.py')
# print(time.localtime(metadata.st_mtime))
# =============================================================================

#sub_path = '*\\*.dat'

#Load each file at a time
my_list=[]
#title_list = []

#Define variables
TC = "Tip Current (A)"
TCN = "Tip Current (nA)"
BB = "BB Back Bias (V)"
KE = "Kinetic Energy (eV)"
Hz = "BBX (Hz)"
Nm = "Normalised data"



for file in project_files:
    
    #print("Loading file\n"+ file)  #loading message to show data has been taken in and processed successfully
    #Dataframe for graphical use
    line_counter = 0
    r = re.compile("DATA")
    with open(file , "r") as f_in:
        for l in f_in:
            line_counter += 1
            if r.search(l):
                break
              
        
    #print("Count =", line_counter)   
    df = pd.read_csv(file, delimiter='\t',skiprows = line_counter, usecols=(TC, BB, Hz))
    df[TC] = df[TC] * 10**(9)
    df = df.rename(columns={TC: TCN, BB: KE})
    df[Nm] = (df[Hz] / df[TCN])      #Formating  with subscripts and then divide BBX counts by current to get normalised data
    
    #if statement to check the order of the indices 
    #continue if order runs from low to high
    #else if runs from high to low, flip indices round and continue with statement.

    min_index = df[KE].idxmin()
    
    #Create a list of Dataframe from multiple CSV files  
    if min_index == 0:
        my_list.append(df)
        min_index = df[KE].idxmin()
        print("Index=", min_index)
    else:
        df = df.loc[::-1].reset_index(drop=True)
        my_list.append(df)
        min_index = df[KE].idxmin()
        print("New Index = ", min_index)
        
    
    df.plot.line(x = KE, y = Nm)
    graph_char()

length = len(my_list)
average = pd.concat(my_list, axis=1, join="inner")   #Dataframe of all Normalised value
average = average.T.drop_duplicates().T          #Use DataFrame.drop_duplicates() to Remove Duplicate Columns
average.drop(([Hz, TCN]), inplace=True, axis=1)

#my_list[0].plot.line(x=KE, y=Nm)


def Group():
    fig, ax = plt.subplots()
    for i in range(length):
        my_list[i].plot.line(ax=ax, x = KE, y = Nm, label = project_files[i])
        graph_char()
        plt.title("Graphs plotted together")
        #fig.set_size_inches(14,8)

def Average():
    average["Average"] = average[Nm].mean(axis=1)
    average.plot.line(x=KE, y="Average")
    graph_char()
    title_avg =  "Graph averaged from {} data files".format(length)
    plt.title(title_avg)

#Plot Average data together


    
                    


#Next plot multiple graphs on same axis to see if features consistent throughout

