import pandas as pd
from data_envelopment import DataEnvelopment
from proposed_method_entities_comparison import ProposedMethod

class EntitiesComparison:
    def __init__(self,csv_input_file_path, csv_output_file_path):
        self.data_input=pd.read_csv(csv_input_file_path)
        self.data_output=pd.read_csv(csv_output_file_path)
        
    def apply_assessment(self):
        proposed_method_res=ProposedMethod(self.data_input,self.data_output).get_result()
        data_envelopment_res=DataEnvelopment(self.data_input,self.data_output).get_result()
        return self.combine_results(proposed_method_res,data_envelopment_res)
    
    def combine_results(self,proposed_method_res,data_envelopment_res):
        combined_results=[]
        for res in proposed_method_res:
            e=data_envelopment_res[res["type"]][0]
            stat='in'
            if e<1:
                stat='out'
                
            combined_results.append({"type":res["type"],"mean":round(res['mean'],3),"std":round(res['std'],3),"E":e,"stat":stat})
        
        return combined_results
    
    def get_data_details(self):
        ip_data={"attributes":[*self.data_input[self.data_input.columns[0]].values]}
        op_data={"attributes":[*self.data_output[self.data_output.columns[0]].values]}
        
        for hos_type in self.data_input.columns[1::]:
            ip_data[f"{hos_type}"]=[*self.data_input[hos_type].values]
            
        for hos_type in self.data_output.columns[1::]:
            op_data[f"{hos_type}"]=[*self.data_output[hos_type].values]
              
        return [ip_data,op_data] 
    
    def get_result(self):
        combined_methods_res=self.apply_assessment()
        # Filtering out the dictionaries with 'stat' of 'out'
        out_dicts = [d for d in combined_methods_res if d['stat'] == 'out']
        
        analysis_summary="<p>After making the assessment, the order of hospitals according to their effiecency assessemnt is <b>"
        analysis_summary += ', '.join([f'{i["type"]}' for i in combined_methods_res[:-1]]) + f',</b> and <b>{combined_methods_res[-1]["type"]}</b> with mean values of <i>'+', '.join([f'{i["mean"]}' for i in combined_methods_res[:-1]])+ f',</i> and <i>{combined_methods_res[-1]["mean"]}</i>.</p>'+f"<p>Then, with applying <b>DEA (Data Envelopmnet Analyis)</b>, it has been found out that, the {len(out_dicts)} {'hospitals' if len(out_dicts)>1 else 'hospital'} <b>"
        analysis_summary+=', '.join([f'{i["type"]}' for i in out_dicts[:-1]]) + f'</b>, and <b>{out_dicts[-1]["type"]}</b>'+f" {'are' if len(out_dicts)>1 else 'is'}"+" <i>relatively inefficient</i> compared to the other hospitals in the group.</p>"
        
        return {"combined_methods":combined_methods_res,'analysis_summary':analysis_summary,"ineff_ent":out_dicts,"det_data":self.get_data_details()}
    
  