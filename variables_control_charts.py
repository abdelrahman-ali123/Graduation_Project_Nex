import numpy as np
from static.scripts.python.constants_table import ConstantTables
from control_charts_tools import get_points_out_of_contols, get_points_with_pattern,get_horizonatl_line,ssd
from storage_control import get_constants_tables

constant_tables_list=get_constants_tables()
const_table=ConstantTables(constant_tables_list[0],constant_tables_list[1])


class VariableControlChart:
    def __init__(self,data):
        self.data=data
        self.data_samples=self.data[data.columns[0]].tolist()
        self.obs=self.data[self.data.columns[1:]].values
        self.n_obs=len(self.data.columns[1:])
    
    def select_chart(self):
        if(len(self.data.columns[1:])>9):
            return 'x_s_chart'
        else:
            return 'x_r_chart'
    
    def R_chart(self):
        R=[]
        for row in self.obs:
            R.append(np.max(row)-np.min(row))
        
        R_bar=np.mean(R)
        ucl=const_table.getD4(self.n_obs)*R_bar
        lcl=const_table.getD3(self.n_obs)*R_bar
        if lcl<0: 
            lcl=0
        
        return [R,R_bar,lcl,ucl]
    
    def S_chart(self):
        s=[]
        for row in self.obs:
            s.append(ssd(row))

        s_bar=np.mean(s)
        ucl=float(const_table.getB4(self.n_obs))*s_bar
        lcl=float(const_table.getB3(self.n_obs))*s_bar

        if lcl<0: 
            lcl=0
        return [s,s_bar,lcl,ucl]

    def apply_R_chart(self):
        [R,R_bar,lcl,ucl]=self.R_chart()

        scv_out_of_limits=get_points_out_of_contols(self.data_samples,R,lcl,ucl)
        scv_with_pattern=get_points_with_pattern(self.data_samples,R,R_bar)

        ucl_line=get_horizonatl_line(self.data_samples,ucl)
        lcl_line=get_horizonatl_line(self.data_samples,lcl)
        r_bar_line=get_horizonatl_line(self.data_samples,R_bar)

        r_graph_coordinates={'x':self.data_samples,'y':R}

        return {'chart_used':'R control chart',
            'scv_out_of_limits':scv_out_of_limits,
            'scv_with_pattern':scv_with_pattern,
            'ucl_line':ucl_line,
            'lcl_line':lcl_line,
            'mean_line':r_bar_line,
            'graph_coordinates':r_graph_coordinates,
            'x_label':self.data.columns[0],
            'y_label':"Observations"}

    def apply_S_chart(self):
        [s,s_bar,lcl,ucl]=self.S_chart()

        ucl_line=get_horizonatl_line(self.data_samples,ucl)
        lcl_line=get_horizonatl_line(self.data_samples,lcl)
        s_bar_line=get_horizonatl_line(self.data_samples,s_bar)

        scv_out_of_limits=get_points_out_of_contols(self.data_samples,s,lcl,ucl)
        scv_with_pattern=get_points_with_pattern(self.data_samples,s,s_bar)

        s_graph_coordinates={'x':self.data_samples,'y':s}

        return {'chart_used':'S control chart',
            'scv_out_of_limits':scv_out_of_limits,
            'scv_with_pattern':scv_with_pattern,
            'ucl_line':ucl_line,
            'lcl_line':lcl_line,
            'mean_line':s_bar_line,
            'graph_coordinates':s_graph_coordinates,
            'x_label':self.data.columns[0],
            'y_label':"Observations"}

    def apply_X_bar_chart(self):
        lcl=0
        X_bar=[]
        X_bar_bar=0
        ucl=0

        if(self.select_chart()=='x_s_chart'):
            [_,S_bar,_,_]=self.S_chart()
            for row in self.obs:
                X_bar.append(np.mean(row))
            X_bar_bar=np.mean(X_bar)
            ucl=X_bar_bar+const_table.getA3(self.n_obs)*S_bar
            lcl=X_bar_bar-const_table.getA3(self.n_obs)*S_bar
        else:
            [_,R_bar,_,_]=self.R_chart()
            for row in self.obs:
                X_bar.append(np.mean(row))

            X_bar_bar=np.mean(X_bar)
            ucl=X_bar_bar+const_table.getA2(self.n_obs)*R_bar
            lcl=X_bar_bar-const_table.getA2(self.n_obs)*R_bar

        if lcl<0: 
            lcl=0

        ucl_line=get_horizonatl_line(self.data_samples,ucl)
        lcl_line=get_horizonatl_line(self.data_samples,lcl)
        X_bar_bar_line=get_horizonatl_line(self.data_samples,X_bar_bar)

        scv_out_of_limits=get_points_out_of_contols(self.data_samples,X_bar,lcl,ucl)
        scv_with_pattern=get_points_with_pattern(self.data_samples,X_bar,X_bar_bar)

        X_bar_graph_coordinates={'x':self.data_samples,'y':X_bar}

        return {'chart_used':'X bar control chart',
            'scv_out_of_limits':scv_out_of_limits,
            'scv_with_pattern':scv_with_pattern,
            'ucl_line':ucl_line,
            'lcl_line':lcl_line,
            'mean_line':X_bar_bar_line,
            'graph_coordinates':X_bar_graph_coordinates,
            'x_label':self.data.columns[0],
            'y_label':"Observations"}
    
    def apply_chart(self):
        if(self.select_chart()=='x_s_chart'):
            return {
                "chart_01":self.apply_S_chart(),
                "chart_02":self.apply_X_bar_chart()
            }
        else:
            return {
                "chart_01":self.apply_R_chart(),
                "chart_02":self.apply_X_bar_chart()
            }

    def is_controlled(self,chart_01,chart_02):
        return len(chart_01["scv_out_of_limits"]['y'])==0 and len(chart_01["scv_with_pattern"]['y'])==0 and len(chart_02["scv_out_of_limits"]['y'])==0 and len(chart_02["scv_with_pattern"]['y'])==0
    
    def can_be_fixed(self,chart_01,chart_02):
        return len(chart_01["scv_out_of_limits"]['y'])==1 and len(chart_02["scv_with_pattern"]['y'])==1
    
    def get_results(self):
        res=self.apply_chart()
        chart_01=res["chart_01"]
        chart_02=res["chart_02"]
        res_text=f"<p>With applying <b>{chart_01['chart_used']}</b> and <b>{chart_02['chart_used']}</b>, we found out that your data is"
        if(self.is_controlled(chart_01,chart_02)):
            res['is_controlled']=True
            res['res_text']=res_text+f" <b>in control</b>, with <i>mean of {round(chart_01['mean_line']['y'][0],3)}, upper control level (UCL) of {round(chart_01['ucl_line']['y'][0],3)}, and low control level (LCL) of {round(chart_01['lcl_line']['y'][0],3)}</i> when using <b>{chart_01['chart_used']}</b>, and <i>mean of {round(chart_02['mean_line']['y'][0],3)}, upper control level (UCL) of {round(chart_02['ucl_line']['y'][0],3)}, and low control level (LCL) of {round(chart_02['lcl_line']['y'][0],3)}</i> when using <b>{chart_02['chart_used']}</b></p>"
            return res
        # else:
        #     res['is_controlled']=True
        #     res['res_text']=res_text+f" out of control, as there is a defeciency in {self.data.columns[0]}s {chart_01["scv_out_of_limits"]['y']}"
        # elif(self.can_be_fixed(chart_01,chart_02)):
        #     res['can_be_fixed']=True
        #     res['is_controlled']=False
        #     return res
        else:
            res['can_be_fixed']=False
            res['is_controlled']=False
            if(len(chart_01['scv_with_pattern']['x'])>0):
                res['res_text']=res_text+f" <b>out of control</b>, as there is a defeciency because of a <i>trend</i> bacuse of {self.data.columns[0]} {res['scv_with_pattern']['x'][0]}"
            else:
                res['res_text']=res_text+f" <b>out of control</b>, as there is a defeciency in {self.data.columns[0]}s"
                for i in range(len(chart_01['scv_out_of_limits']['x'])):
                    res['res_text']+=f" <i>'{chart_01['scv_out_of_limits']['x'][i]}' with values of {round(chart_01['scv_out_of_limits']['y'][i],3)}</i> </p>"
            res['is_controlled']=False
            res['can_be_fixed']=False
            return res
                