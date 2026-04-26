import pandas as pd
import sys
import numpy as np
import statsmodels.api as sm
import itertools
import functions as fn
import tracemalloc
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
import gc
__version__ = "1.1.0"  # Lasso/ElasticNet Optimize Edilmiş Sürüm
__author__ = "tenraisen-bty"

def main():
    tracemalloc.start()
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
        datafile = rawdatafiles.iloc[:, a:b].astype('float32')
    

    #TODO: Write the datas into a array for variables
        normalizeddata = datafile.iloc[:,:].copy().add_prefix('n_')
        del datafile
        for column in normalizeddata:
            normalizeddata[column] = fn._normalize(normalizeddata[column])
        
    
    #TODO: Write the datas into a array for results
        resultdata = rawdatafiles.iloc[:, b:].astype('float32')
        del rawdatafiles


    #TODO: Create New Columns that are combination of initial coulmns
        normalizeddata = fn._combinationsaicc(normalizeddata)


    #TODO: Calculate All The Models Possibilities
        # --- 1. VERİ HAZIRLIĞI (Döngüye Girmeden Önce) ---
        df_x = normalizeddata.reset_index(drop=True)
        df_y = resultdata.reset_index(drop=True)
        target_count = len(df_y.columns)

        # Orijinal büyük parçaları hemen silelim ki RAM'de yer açılsın
        del normalizeddata
        del resultdata

        # Veriyi birleştir ve float32 yaparak RAM'i %50 koru
        alldatas = pd.concat([df_x, df_y], axis=1).astype('float32')
        
        # Gereksiz ara kopyaları sil
        del df_x
        del df_y
        gc.collect()

        # --- 2. MODEL SEÇİMİ (Artık Döngüye Gerek Yok!) ---
        # fn._findbestmodel kendi içinde her hedef için en iyi değişkenleri bulacak
        results = fn._findbestmodel(alldatas, target_count)

        # --- 3. KATSAYI TABLOSUNU OLUŞTURMA ---
        coefficient_list = []
        for target, info in results.items():
            if not info["best_cols"]: # Eğer hiç değişken seçilemediyse atla
                continue
                
            y = alldatas[target]
            # Sadece seçilen kolonlarla model kur
            x = sm.add_constant(alldatas[info["best_cols"]])
            
            model = sm.OLS(y, x).fit()
            coeffs = model.params.copy()
            coeffs.name = target
            coefficient_list.append(coeffs)
        
        # --- 4. SONUÇLARI YAZDIR VE TEMİZLE ---
        if coefficient_list:
            final_table = pd.concat(coefficient_list, axis=1).fillna("-")
            r2_row = pd.Series({t: f"{info['r2']:.4f}" for t, info in results.items()}, name="R-Squared")
            r2_adj_row = pd.Series({t: f"{info['r2_adj']:.4f}" for t, info in results.items()}, name="Adj. R-Squared")
            aicc_row = pd.Series({t: f"{info['min_aicc']:.2f}" for t, info in results.items()}, name="AICc")

            # Tabloya ekle
            final_table = pd.concat([final_table, pd.DataFrame([r2_row, r2_adj_row, aicc_row])])
            print(f"Analysis Report - Version: {__version__}\nby: {__author__}")
            print("\n--- Model Coefficients ---")
            print(final_table)
        else:
            print("Uyarı: Hiçbir hedef değişken için anlamlı bir model kurulamadı.")

        del alldatas
        gc.collect()

        # --- 5. HAFIZA RAPORU ---
        current, peak = tracemalloc.get_traced_memory()
        print(f"\nMemory Report:")
        print(f"Current Memory Usage: {current / 10**6:.2f} MB")
        print(f"Peak Memory Usage: {peak / 10**6:.2f} MB")  
        
        tracemalloc.stop()
    except Exception as generr:

        print(f"General Error: {generr}")  
        
if __name__ == "__main__":
    main()
