import pandas as pd
import numpy as np


class ConstantTables:
    def __init__(self,const_table_01,const_table_02):
        self.const_table_01=const_table_01
        self.const_table_02=const_table_02

    def getD3(self,n):
        if n>=2:
            return self.const_table_01['D3'].tolist()[n-2]
        else: return 
    def getD4(self,n):
        if n>=2:
            return self.const_table_01['D4'].tolist()[n-2]
        else: return 
        
    def getA2(self,n):
        if n>=2:
            return self.const_table_01['A2'].tolist()[n-2]
        elif n>25: return 3/np.sqrt(n)
        else: return 

    def getA3(self,n):
        if n>=2:
            return self.const_table_02['A3'].tolist()[n-2]
        else: return 

    def getB3(self,n):
        if n>=2:
            return self.const_table_02['B3'].tolist()[n-2]
        elif n>25: return 1-3/np.sqrt(2*n)
        else: return 

    def getB4(self,n):
        if n>=2:
            return self.const_table_02['B4'].tolist()[n-2]
        elif n>25: return 1+3/np.sqrt(2*n)
        else: return 

    def getE2(self,n):
        if n>=2 and n<=10:
            return self.const_table_02['E2'].tolist()[n-2]
        else: return