import numpy as np


class ProposedMethod:
    def __init__(self,data_input,data_output):
        self.data_ip=data_input
        self.data_op=data_output
        
    def get_entity_io_matrix(self,entity_ip,entity_op):
        io_matrix_for_each_entity=[]

        for op in entity_op:
            op_ip_rel_row=[]
            for ip in entity_ip:
                op_ip_rel_row.append(op/ip)
            io_matrix_for_each_entity.append(op_ip_rel_row)

        return io_matrix_for_each_entity
    
    def get_full_cnversion_matrices_for_all_entities(self,ip_data,op_data):
        full_conversion_matrices_io_data={}
        for entity_name in ip_data.columns[1::]:
            full_conversion_matrices_io_data[f'{entity_name}']=self.get_entity_io_matrix(ip_data[f'{entity_name}'],op_data[f'{entity_name}'])

        return full_conversion_matrices_io_data
    
    def get_maximum_matrix(self,ip_data,op_data):
        converted_data=self.get_full_cnversion_matrices_for_all_entities(ip_data,op_data)
        size_i=len(converted_data[list(converted_data.keys())[0]])
        size_j=len(converted_data[list(converted_data.keys())[0]][0])
        maximum_matrix=[]
        for i in range(size_i):
            maximum_matrix_row=[]
            for j in range(size_j):
                cell_nums=[]
                for entity_name in list(converted_data.keys()):
                    cell_nums.append(converted_data[entity_name][i][j])
                maximum_matrix_row.append(max(cell_nums))
            maximum_matrix.append(maximum_matrix_row)

        return maximum_matrix
    
    def get_normalized_entity_matrices(self,ip_data,op_data):
        normalized_matrix={}
        max_matrix=self.get_maximum_matrix(ip_data,op_data)

        for key,matrix in self.get_full_cnversion_matrices_for_all_entities(ip_data,op_data).items():
            normalized_matrix[key]=[]
            for i in range(len(max_matrix)):
                row=[]
                for j in range(len(max_matrix[0])):
                    row.append(matrix[i][j]/max_matrix[i][j])
                normalized_matrix[key].append(row)
                
        return normalized_matrix
    
    def flatten(self,matrix):
        return [element for row in matrix for element in row]
    
    def get_sorted_entities(self,ip_data,op_data):
        entities_info=[]
        for key, matrix in self.get_normalized_entity_matrices(ip_data,op_data).items():
            entities_info.append({"type":key,'mean':np.mean(self.flatten(matrix)),"std":np.std(self.flatten(matrix))})
        sorted_entity_info=sorted(entities_info,key=lambda x:x["mean"],reverse=True)
        return sorted_entity_info
    
    def get_result(self):
        return self.get_sorted_entities(self.data_ip,self.data_op)
    
