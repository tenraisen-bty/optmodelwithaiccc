import pandas as pd
import sys
import numpy as np
import statsmodels.api as sm
import itertools
import functions as fn

def main():
    
    # TODO: Check for command-line usage
    try:

        if len(sys.argv) != 4:
          sys.exit("Usage: python main.py data.xlsx inumber fnumber")

    except FileNotFoundError:
        print(f"Error 0001: Couldn't found '{sys.argv[1]}")
    
    except Exception as error0002:
        print(f"command-line Error (Error 0002): {error0002} ")

    
    try:
        # TODO: Read data file into a variable
        rawdatafiles = pd.read_excel(sys.argv[1])
        a = int(sys.argv[2])
        b = int(sys.argv[3] ) + 1
        datafile = rawdatafiles.iloc[:, a:b]
    

    #TODO: Write the datas into a array for variables
        variabledata = datafile.iloc[:,:]
        normalizeddata = variabledata.copy().add_prefix('n_')
        for column in normalizeddata:
            normalizeddata[column] = fn._normalize(normalizeddata[column])
        
    
    #TODO: Write the datas into a array for results
        resultdata = rawdatafiles.iloc[:, b:]
        n = len(resultdata.iloc[:])   


    #TODO: Create New Columns that are combination of initial coulmns
        normalizeddata = fn._combinations(normalizeddata)
        cols = normalizeddata.columns.tolist()
        num_preds = len(cols)
        comps = [list(format(i, f'0{num_preds}b')) for i in range(2**num_preds)]
        comps = np.array(comps).astype(int)


    #TODO: Calculate All The Models Possibilities
        results = []        
        for i in range(len(comps)):
            current_mask = comps[i]
            selected_cols = [cols[j] for j in range(len(cols)) if current_mask[j] == 1]
            if not selected_cols:
                continue
        df_x = normalizeddata.reset_index(drop=True)
        df_y = resultdata.reset_index(drop=True)
        alldatas = pd.concat([df_x, df_y], axis=1)
        results = fn._findbestmodel(alldatas,len(df_y.columns))
        coefficient_list= []
        for target, info in results.items():
            y = alldatas[target]
            x= sm.add_constant(alldatas[info["best_cols"]])
            model = sm.OLS(y,x).fit()
            coeffs = model.params.copy()
            coeffs.name = target
            coefficient_list.append(coeffs)
        
        coefficient_table = pd.concat(coefficient_list, axis=1).fillna("-")
        print(coefficient_table)


    except Exception as generr:
        print(f"General Error: {generr}")  


if __name__ == "__main__":
    main()
