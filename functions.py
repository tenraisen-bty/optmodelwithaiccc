import pandas as pd
import numpy as np
import statsmodels.api as sm
import itertools

def _normalize(series):
    """This function takes variables from each column and normalizes between -1 and 1. The correct way to use this code is in one column each row should be in same data type and represents one factor"""
    
    max_val = series.max()
    min_val= series.min()
    try:        
        if max_val == min_val:
            return series -series + 0
        
    except Exception as normfunc:
        print(f"Function usage error of _normalize: {normfunc} ")

    else:
        normalized = 2 * (series - min_val) / (max_val - min_val) - 1
        return normalized
    
    
def _combinations(series):
    """This function creates new combinations from variables by multiplication"""


    try:
        list_column = list(series.columns)
        new_series = series.copy()
        for col in list_column:
            new_series[f"{col}^2"] = series[col] ** 2

        for i in range(len(list_column)):
            for j in range(i + 1, len(list_column)):
                c1 = list_column[i]
                c2 = list_column[j]            
                new_name = f"{c1}*{c2.replace('n_', '')}"
                new_series[new_name] = series[c1] * series[c2]
        
        new_series = new_series.apply(lambda x: x.where(x.abs() > 1e-10, 0.0))
        return new_series
                
    except Exception as newcolumn:
        print(f"Error for creating new combination ( Error 0003): {newcolumn}") 


def _findbestmodel(data,target_count):

    """Calculates all variations AICCc and finds best combinations for results"""
    n = len(data)
    X_all = data.iloc[:,:-target_count]
    Y_all = data.iloc[:,-target_count:]

    predictor_names = X_all.columns.tolist()
    target_names = Y_all.columns.tolist()
    num_preds = len(predictor_names)
    mask_matrix = np.array(list(itertools.product([0, 1], repeat=num_preds)))
    
    # 3. Sonuçları tutmak için bir sözlük
    # Her hedef değişken için en iyi AICc ve en iyi sütunları saklayacağız
    best_results = {target: {"min_aicc": float('inf'), "best_cols": []} for target in target_names}

    print(f"Started to Analyze: {num_preds} variable, {len(mask_matrix)} combination, {target_count} target.")

    # 4. Genel Döngü
    for i in range(len(mask_matrix)):
        mask = mask_matrix[i]
        selected_cols = [predictor_names[j] for j in range(num_preds) if mask[j] == 1]
        
        # Seçilen sütunlarla X verisini hazırla
        if len(selected_cols) == 0:
            X_current = pd.DataFrame(np.ones((n, 1)), columns=['intercept'])
        else:
            X_current = sm.add_constant(X_all[selected_cols])

        # Her bir hedef değişken için modeli test et
        for target in target_names:
            y = Y_all[target]
            
            try:
                model = sm.OLS(y, X_current).fit()
                k = model.df_model + 1 # Parametre sayısı
                
                # AICc Hesaplama
                if n - k - 1 <= 0:
                    aicc = float('inf')
                else:
                    aicc = model.aic + (2 * k * (k + 1)) / (n - k - 1)
                
                # Eğer bu model daha iyiyse kaydet
                if aicc < best_results[target]["min_aicc"]:
                    best_results[target]["min_aicc"] = aicc
                    best_results[target]["best_cols"] = selected_cols
                    
            except Exception as e:
            # Hangi sütun kombinasyonunda ne hatası aldığını görelim
                print(f"ERROR while finding best combination: {selected_cols}, Error in _findbestmodel: {e}")
                continue

    return best_results