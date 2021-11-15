import os
import pandas as pd
import json
import matplotlib.pyplot as plt
#If you'd like to see this pipeline in action, feel free to delete folders 1,2 & 3 in results. Then, run main.py. 

def XYZimporter(filepath): 
    stem = os.path.splitext(os.path.basename(filepath))[0] 
    try:
        os.mkdir(r"python/data_engineer_1/results/" + f'{stem}')
    except FileExistsError: 
        print(f"Folder : "r"python/data_engineer_1/results/" + f'{stem}'+ ', already exists')

    if stem == '1':
        data = pd.read_csv(filepath,index_col=False,skiprows=5)

        json1 = pd.read_csv(filepath,index_col=False,header=None,sep=':').head(3)
        mydict = dict(zip(json1[0],json1[1]))
        with open(r"python/data_engineer_1/results/1/1.txt",'w') as f:
            json.dump(dict(zip(json1[0],json1[1])),f,indent=2)

    if stem == '2':
        # I am using the fillna method to replace NaN values. NaN values take the value of the entry above it. If there is no entry above, it copies the entry below.
        data = pd.read_csv(filepath, sep='\t', engine='python',skiprows=1,index_col=False,skipinitialspace=True).fillna(method='pad').fillna(method='bfill')

    if stem == '3':
        data = pd.read_csv(filepath,skiprows=41,sep=';',index_col=False)

        json3 = pd.read_csv('python/data_engineer_1/test_files/3/3.xyz',sep=":;",engine='python',header=None).head(33)
        json3vals=[]
        for i in json3[0]:
            json3vals.append(i)
        json32 = pd.read_csv('python/data_engineer_1/test_files/3/3.xyz',sep=":;",engine='python',index_col=False,header=None).head(33)
        xyz2dict = dict(zip(json32[0],json3vals))
        with open(r"python/data_engineer_1/results/3/3.txt",'w') as f:
            json.dump(xyz2dict,f,indent=2)

    elif stem not in ['1','2','3']:
        print('Sorry, I have not created a pipeline extensive enough to parse this data format yet.' )

    data.to_csv(f'{r"python/data_engineer_1/results/" + stem + os.sep + stem}.csv',index=False) #I am not including an index column. Seems unnecessary. 

def MDBimporter(filepath):
    #TODO 
    pass

def main():
    for subdirectory,directory,files in os.walk(os.getcwd()):
        for filename in files:
            filepath = subdirectory + os.sep + filename
            if filepath.endswith(".xyz"):
                XYZimporter(filepath)
            elif filepath.endswith(".mdb"):
                MDBimporter(filepath)

def plotting():

    data1 = pd.read_csv('python/data_engineer_1/results/1/1.csv')
    plt.plot(pd.to_numeric(data1['Time [s]'])-min(data1['Time [s]']),data1['Voltage [V]'])
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.savefig('python/data_engineer_1/results/1/One.png')

    plt.clf()

    data2 = pd.read_csv('python/data_engineer_1/results/2/2.csv')
    plt.plot(data2['Test (Sec)'],data2['Volts'])
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.savefig('python/data_engineer_1/results/2/Two.png')

    plt.clf()

    data3 = pd.read_csv('python/data_engineer_1/results/3/3.csv',)
    i = data3[(data3.Circuit_action == 'Message')].index
    data3 = data3.drop(i)
    data3 = data3.iloc[1:]
    plt.plot(data3['Time'],data3['Voltage'])
    plt.xlabel("Time")
    plt.ylabel("Voltage")
    plt.savefig('python/data_engineer_1/results/3/Three.png')

if __name__ == "__main__":
    main()
    plotting()
