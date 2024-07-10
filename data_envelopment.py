import numpy as np
from scipy.optimize import linprog

class DataEnvelopment:
    def __init__(self,data_input,data_output):
        self.data_ip=data_input
        self.data_op=data_output
        
    def get_op_ineq_matrix_and_right_hand(self,data_op,entity_name):
        A=[] # Coefficients for inequalities (Ax <= b)
        b=data_op[entity_name].tolist() # Right-hand side of inequalities
        for row in -data_op[data_op.columns[1:]].values:
            temp_list=[0]+row.tolist()
            A.append(temp_list)
        return A,b
    
    def get_ip_ineq_matrix_and_right_hand(self,data_ip,entity_name):
        A=[] # Coefficients for inequalities (Ax <= b)
        b=[] # Right-hand side of inequalities
        entity_name_index=self.data_op.columns[1::].tolist().index(entity_name)
        for row in data_ip[self.data_op.columns[1:]].values:
            temp_list=[-row[entity_name_index]]+row.tolist()
            A.append(temp_list)
            b.append(0)
        return A,b
    
    def get_ineq_matrix_and_right_hand(self,data_ip,data_op,entity_name):
        a_op,b_op=self.get_op_ineq_matrix_and_right_hand(data_op,entity_name)
        a_ip,b_ip=self.get_ip_ineq_matrix_and_right_hand(data_ip,entity_name)
        
        A=np.array(a_op+a_ip)
        b = [-x for x in np.array(b_op+b_ip)]
        return A,np.array(b)
    
    def get_bounds(self,variables_number:int):
        # Bounds for the variables (E >= 0, wg >= 0, wu >= 0, wc >= 0, ws >=0)
        return [(0, None) for _ in range(variables_number+1)]
    
    def get_equality_const(self,variables_number:int):
        # Equality constraints (A_eq x = b_eq)
        # 0E + wg + wu + wc + ws = 1
        A_eq =[np.array([0]+[1 for _ in range(variables_number)])]
        b_eq = np.array([1])

        return A_eq, b_eq
    
    def get_obj_fun(self,variables_number:int):
        # Objective function (we just need a feasible solution, so we can minimize 0)
        return np.array([1 for _ in range(variables_number+1)])

    def apply_data_envelop(self,data_ip,data_op):
        vars_num=len(data_ip.columns[1::])
        objective_function=self.get_obj_fun(vars_num)
        bnds=self.get_bounds(vars_num)
        A_eq,b_eq=self.get_equality_const(vars_num)

        data_summary={}

        for entity_name in data_ip.columns[1::]:
            A,b=self.get_ineq_matrix_and_right_hand(data_ip,data_op,entity_name)
            res = linprog(objective_function, A_ub=A, b_ub=b, A_eq=A_eq, b_eq=b_eq, bounds=bnds, method='highs')
            # data_summary.append({'type':entity_name,'result':[abs(round(x, 3)) for x in res.x]})
            data_summary[entity_name]=[round(x, 3) for x in res.x]

        return data_summary
    
    def get_result(self):
        # for data in self.apply_data_envelop(self.data_ip,self.data_op):
        #     if data['result'][0]<1: print(f"Hospital {data['type']} is relatively inefficient compared to the other hospitals in the group, as E = {data['result'][0]}")
        return self.apply_data_envelop(self.data_ip,self.data_op)
            

