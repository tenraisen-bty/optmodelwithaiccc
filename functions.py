import pandas as pd
import numpy as np
import statsmodels.api as sm
import itertools
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV
import gc

def _normalize(series):
    """This function takes variables from each column and normalizes between -1 and 1. The correct way to use this code is in one column each row should be in same data type and represents one factor"""
    
    max_val, min_val = series.max(), series.min()
    try:        
        if max_val == min_val:
            return series * 0
        
    except Exception as normfunc:
        print(f"Function usage error of _normalize: {normfunc} ")

    else:
        normalized = (2 * (series - min_val) / (max_val - min_val) - 1).astype('float32')
        return normalized
    
    
def _combinationsaicc(series):
    """This function creates new combinations from variables by multiplication"""

    try:       
        new_series = series.astype('float32').copy()
        for col in series.columns:
            new_series[f"{col}^2"] = (series[col] ** 2).astype('float32')

        for c1,c2 in itertools.combinations(series.columns,2):          
            new_series[f"{c1}*{c2.lstrip('n_')}"] = (series[c1] * series[c2]).astype('float32')
               
        new_series = new_series.mask(new_series.abs() <= 1e-10, 0.0)
        return new_series
                
    except Exception as newcolumn:
        print(f"Error for creating new combination ( Error 0003): {newcolumn}") 

def _findbestmodel(data, target_count):
    data = data.astype('float32')
    predictor_names = data.iloc[:, :-target_count].columns.tolist()
    target_names = data.iloc[:, -target_count:].columns.tolist()
    
    X = data[predictor_names]
    # Kritik: Veriyi ölçeklendirmek ElasticNet için şarttır
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    best_results = {}

    for target in target_names:
        y = data[target]
        
        # l1_ratio=0.7: %70 Lasso, %30 Ridge özelliği taşır. 
        # Bu, birbiriyle ilişkili (n_E ve n_E^2 gibi) değişkenleri korur.
        enet = ElasticNetCV(l1_ratio=0.7, cv=5, random_state=42, max_iter=10000).fit(X_scaled, y)
        
        # Katsayı eşiğini biraz daha hassas yapalım
        selected_indices = [i for i, coef in enumerate(enet.coef_) if abs(coef) > 1e-5]
        selected_cols = [predictor_names[i] for i in selected_indices]
        
        if not selected_cols:
            # Eğer hala boşsa, en yüksek korelasyona sahip 2 değişkeni zorla seç
            corrs = X.corrwith(y).abs().sort_values(ascending=False)
            selected_cols = corrs.head(2).index.tolist()
            

        # SEÇİLENLERLE OLS YAP (Bu kısım katsayıları ilk versiyondaki gibi gerçekçi yapar)
        X_final = sm.add_constant(data[selected_cols])
        final_model = sm.OLS(y, X_final).fit()
        
        n, k = len(data), final_model.df_model + 1
        aicc = final_model.aic + (2*k*(k+1))/(n-k-1) if n-k-1 > 0 else float('inf')
        best_results[target] = {
            "min_aicc": aicc, 
            "best_cols": selected_cols,
            "r2": final_model.rsquared,
            "r2_adj": final_model.rsquared_adj
        }
        gc.collect()
        
       
    return best_results