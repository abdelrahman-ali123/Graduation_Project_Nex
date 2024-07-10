import numpy as np
from control_charts_tools import get_points_out_of_contols, get_points_with_pattern,get_horizonatl_line

class AttributesControlCharts:
    def __init__(self,data):
        self.data=data

    def prepare_data(self):
        if(self.select_chart()=='c_chart'):
            i=self.data[f'{self.data.columns[0]}'].tolist()
            c=self.data[f'{self.data.columns[1]}'].tolist()
            return {'i':i,'c':c}
        else:
            i=self.data[f'{self.data.columns[0]}'].tolist()
            n=self.data[f'{self.data.columns[1]}'].tolist()
            X=self.data[f'{self.data.columns[2]}'].tolist()
            return {'i':i,'n':n,'X':X}

    def apply_p_chart(self,i,n,X):
        '''
        all output are object of attributes x and y as coordinates of points
        scv_out_of_limits=scv={'x':[],'y':[]}, 
        scv_with_pattern=scv={'x':[],'y':[]},
        ucl_line=scv={'x':[],'y':[]},
        lcl_line=scv={'x':[],'y':[]},
        mean_line=scv={'x':[],'y':[]},
        '''
        p=[]
        for k in range(len(i)):
            p.append(X[k]/n[k])
        p_mean=np.mean(p)
        ucl=p_mean+3*np.sqrt(p_mean*(1-p_mean)/np.mean(n))
        lcl=p_mean-3*np.sqrt(p_mean*(1-p_mean)/np.mean(n))
        if lcl<0: 
            lcl=0

        scv_out_of_limits=get_points_out_of_contols(i,p,lcl,ucl)
        scv_with_pattern=get_points_with_pattern(i,p,p_mean)

        ucl_line=get_horizonatl_line(i,ucl)
        lcl_line=get_horizonatl_line(i,lcl)
        p_mean_line=get_horizonatl_line(i,p_mean)

        p_graph_coordinates={'x':i,'y':p}

        return {'chart_used':'p control chart',
                'scv_out_of_limits':scv_out_of_limits,
                'scv_with_pattern':scv_with_pattern,
                'ucl_line':ucl_line,
                'lcl_line':lcl_line,
                'mean_line':p_mean_line,
                'graph_coordinates':p_graph_coordinates,
                'x_label':self.data.columns[0],
                'y_label':'Proportion'}

    def apply_c_chart(self,i,c):
        c_mean=np.mean(c)
        ucl=c_mean+3*np.sqrt(c_mean)
        lcl=c_mean-3*np.sqrt(c_mean)
        if lcl<0: 
            lcl=0

        scv_out_of_limits=get_points_out_of_contols(i,c,lcl,ucl)
        scv_with_pattern=get_points_with_pattern(i,c,c_mean)

        ucl_line=get_horizonatl_line(i,ucl)
        lcl_line=get_horizonatl_line(i,lcl)
        c_mean_line=get_horizonatl_line(i,c_mean)

        c_graph_coordinates={'x':i,'y':c}

        return {'chart_used':'c control chart',
                'scv_out_of_limits':scv_out_of_limits,
                'scv_with_pattern':scv_with_pattern,
                'ucl_line':ucl_line,
                'lcl_line':lcl_line,
                'mean_line':c_mean_line,
                'graph_coordinates':c_graph_coordinates,
                'x_label':self.data.columns[0],
                'y_label':self.data.columns[1]}

    def select_chart(self):
        if(len(self.data.columns[1:])==1):
            return 'c_chart'
        return 'p_chart'
    
    def apply_chart(self):
        if(self.select_chart()=='c_chart'):
            c_chart_comp=self.prepare_data()
            return self.apply_c_chart(c_chart_comp['i'],c_chart_comp['c'])
        p_chart_comp=self.prepare_data()
        return self.apply_p_chart(p_chart_comp['i'],p_chart_comp['n'],p_chart_comp['X'])
    
    def is_controlled(self,scv_out_of_limits,scv_with_pattern):
        return len(scv_out_of_limits['y'])==0 and len(scv_with_pattern['y'])==0
    
    def can_be_fixed(self,scv_out_of_limits):
        return len(scv_out_of_limits['y'])==1
    
    def fix_data(self,scv_out_of_limits):
        data=self.prepare_data()
        index_of_value=data['i'].index(scv_out_of_limits['x'][0])
        if(len(data)==2):
            i=data['i'][0:index_of_value]+data['i'][index_of_value+1::]
            c=data['c'][0:index_of_value]+data['i'][index_of_value+1::]
            return  self.apply_c_chart(i,c)
        else:
            i=data['i'][0:index_of_value]+data['i'][index_of_value+1::]
            n=data['n'][0:index_of_value]+data['n'][index_of_value+1::]
            X=data['X'][0:index_of_value]+data['X'][index_of_value+1::]
            return self.apply_p_chart(i,n,X)
    
    def get_results(self):
        res=self.apply_chart()
        res_text=f"<p>With applying <b>{res['chart_used']}</b>, we found out that your data is"
        if(self.is_controlled(res['scv_out_of_limits'],res['scv_with_pattern'])):
            res['is_controlled']=True
            res['res_text']=res_text+f" <b>controlled</b>, with <i>mean of {round(res['mean_line']['y'][0],3)}, upper control level (UCL) of {round(res['ucl_line']['y'][0],3)}, and low control level (LCL) of {round(res['lcl_line']['y'][0],3)}</i></p>"
            return res
        elif(self.can_be_fixed(res['scv_out_of_limits'])):
            res['new_res']=self.fix_data(res['scv_out_of_limits'])
            res['res_text']=res_text+f" <b>out of control</b>, but <i>it can be fixed</i>, as the deficencey at point {self.data.columns[0]} {res['scv_out_of_limits']['x'][0]} with value of {round(res['scv_out_of_limits']['y'][0],3)} can be extracetd.</p><p class='hint'>You can press fix button</p>"
            if(self.is_controlled(res['new_res']['scv_out_of_limits'],res['new_res']['scv_with_pattern'])):
                res['new_res_text']=f"<p>After fixing the data, we found that your data become <b>in control</b> with <i>mean of {round(res['new_res']['mean_line']['y'][0],3)}, upper control level (UCL) of {round(res['new_res']['ucl_line']['y'][0],3)}, and low control level (LCL) of {round(res['new_res']['lcl_line']['y'][0],3)}</i></p>"
            else:
                res['new_res_text']=f"<p>After trying to fix your data, unfortunately we couldn't, and still have deficiency in point {round(res['new_res']['scv_with_pattern']['x'][0],3)} with value of {round(res['new_res']['scv_with_pattern']['x'][1],3)}</p>"
            res['can_be_fixed']=True
            res['is_controlled']=False
            return res
        else:
            if(len(res['scv_with_pattern']['x'])>0):
                res['res_text']=res_text+f" <b>out of control</b>, as there is a defeciency because of a <i>trend</i> in {self.data.columns[0]} {res['scv_with_pattern']['x'][0]}</p>"
            else:
                res['res_text']=res_text+f" <b>out of control, as there is a defeciency in {self.data.columns[0]}s"
                for i in range(len(res['scv_out_of_limits']['x'])):
                    res['res_text']+=f"{res['scv_out_of_limits']['x'][i]} with values of {res['scv_out_of_limits']['y'][i]}</p>"
            res['res_text']+=f"<p><b>Thus, it can't be fixed</b></p>"
            res['is_controlled']=False
            res['can_be_fixed']=False
            return res

