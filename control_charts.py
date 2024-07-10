import pandas as pd
from attributes_control_charts import AttributesControlCharts
from variables_control_charts import VariableControlChart



# Check data if attribute data or (variable) numerical data, now we only work with csv files
class ControlCharts:
    def __init__(self,csv_file_path):
        self.file_path=csv_file_path

    def apply_control_char(self):
        data=pd.read_csv(self.file_path)
        dp=data.dropna(axis=1,how='all')
        print(len(dp.columns[1:]))
        if(len(dp.columns[1:])<=2):
            return AttributesControlCharts(dp).get_results()
        else:
            return VariableControlChart(dp).get_results()
    