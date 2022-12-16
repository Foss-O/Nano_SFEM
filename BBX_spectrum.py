import glob, os, time
from os.path import isfile
import pandas as pd
from matplotlib import pyplot as plt
#from scipy.signal import argrelextrema
import numpy as np
import re
import pprint


#Define variables
TC = "Tip Current (A)"
TCN = "Tip Current (nA)"
BB = "BB Back Bias (V)"
KE = "Kinetic Energy (eV)"
Hz = "BBX (Hz)"
Nm = "Normalised data"
Av = "Average"

# function to convert to subscript
def get_sub(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
    res = x.maketrans(''.join(normal), ''.join(sub_s))
    return x.translate(res)

    plt.legend(fontsize = 10)

#Select the desired files 
path = "C:/Users/oskar/Desktop/My_Scripts/Si(111)/2022_08_23/"
file_name = "BBX_Spectroscopy_00[1-3].dat"
#path2 = "*04[0-4].dat"
items = glob.glob(path + file_name)
#items2 = glob.glob(path2)
project_files = items #+ items2 #Added to a list containing all required files for analysis

#User defined path - Using menus, select Material and then date. 
    
print(path, "\n\n")
my_list=[]


def graph_char(): 
#Graph characterisation - formats plot
    plt.grid(True)
    title = str(file)
    plt.xlabel("Kinetic Energy / eV", fontsize = 10)
    plt.ylabel("I{}/I{} / Hz/nA ".format(get_sub('E'),get_sub('a')), fontsize = 10)
    plt.yticks(fontsize=8)
    plt.title(title, fontsize = 8)


for file in project_files:
    
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
        #print("Index=", min_index)
    else:
        df = df.loc[::-1].reset_index(drop=True)
        my_list.append(df)
        min_index = df[KE].idxmin()
        #print("New Index = ", min_index)
        
# =============================================================================
#     single_graphs=input("Press y to show plots of all the data:")
#     if single_graphs == "y":
# =============================================================================
    df.plot.line(x = KE, y = Nm)
    graph_char()
    plt.show()
        
length = len(my_list)

average = pd.concat(my_list, axis=1, join="inner")   #Dataframe of all Normalised value
average = average.T.drop_duplicates().T          #Use DataFrame.drop_duplicates() to Remove Duplicate Columns
average.drop(([Hz, TCN]), inplace=True, axis=1)
average[Av] = average[Nm].mean(axis=1)
    #Loss graph of average
loss_df = average[[KE, Av]].copy()
Index_elastic = loss_df[Av].idxmax()
Elastic_energy = loss_df.loc[Index_elastic, KE]
loss_df[KE] = (loss_df[KE] - Elastic_energy)*-1

#my_list[0].plot.line(x=KE, y=Nm)


def group():
    fig, ax = plt.subplots()
    for i in range(length):
        my_list[i].plot.line(ax=ax, x = KE, y = Nm, label = project_files[i])
        graph_char()
        plt.title("Graphs plotted together")
        fig.set_size_inches(14,8)
    plt.show()  
    
def Average():
    average.plot.line(x=KE, y=Av)
    graph_char()
    title_avg =  "Graph averaged from {} data files".format(length)
    plt.title(title_avg)
    plt.show()
  

def loss():
    loss_df.plot.line(x = KE, y =Av, color = 'g')
    graph_char()
    plt.title("Loss features as a function of Kinetic energy")

    print("Here is the full graph, do you want to set the x limits of the graph?")
    plt.show()
    while True:
        Prompt = input("Answer y or n\n")
        if Prompt in ['y', 'yes']:
            x_lower = int(input("Enter the lower limit:"))
            x_higher = int(input("Enter the higher limit:"))
            
            loss_df.plot.line(x = KE, y =Av, color = 'g')
            plt.xlim(x_lower, x_higher)
            graph_char()
            plt.title("Loss features as a function of Kinetic energy")
            plt.show()
            break
        elif Prompt in ['n', 'no']:
            print("You are happy with the graph, thank you")
            break

def main():
    print("Files loaded and graphs ready to be plotted \n There are three options:")
    print(" 1 to plot all the data on one group\n 2 to plot average of the data\n 3 to plot average as a loss function")
    User_graph = int(input("Enter number between 1-3:"))
    if User_graph == 1:
        group()
    elif User_graph == 2:
        Average()
    elif User_graph == 3:
        loss()
    else:
        print("You entered a wrong number")
    restart=input("Do you want to generate more plots\t\t\t Press y to continue?")
    if restart == "y":
        print("\n\n\n")
        main()
    else:
        print("\nGoodbye")
    
main()


#Plot loss features and then get Guassian peaks for the data










    
                    


#Next plot multiple graphs on same axis to see if features consistent throughout

