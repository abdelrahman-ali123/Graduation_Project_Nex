import pandas as pd
import numpy as np
from random import random
from scipy.stats import skew,kurtosis

class OutpatientDepartment:
    def __init__(self,file_path) :
        self.data=pd.read_csv(file_path)
    
    def get_main_analysis(self):
        clinic_types=[*self.data[self.data.columns[0]].values]
        mean_waiting_time=[*self.data[self.data.columns[1]].values]
        mean_service_time=[*self.data[self.data.columns[2]].values]
        mean_number_of_patients=[*self.data[self.data.columns[3]].values]
        
        mean_service_rate_hrs=[] # μ
        mean_arrival_rate_hrs=[] # λ
        utilization_factor=[]  # ρ = λ / μ
        percent_idle_time=[]  # I = 1 - ρ
        mean_interarrival_time=[] # 1 / λ
        Lq=[]  # mean number of customers in the queue = λ^2 / (μ(μ-λ))
        Ls=[]  # mean number of customers in the system = λ / (μ-λ)
        Ts=[]  # mean time per customer in the system = 1 / (μ-λ)
        Pn=[]  # probabiltiy of n units in the entire system = (1-λ/μ) * (λ/μ)^n
        Pk=[]  # probabilty of k or more customers in the entire system p(n>=k) = (λ/μ)^k
        total_time_of_service_min=[]  # mean service time * mean # of patients
        total_time_of_clinic_min=[]  # total_time_of_clinic = total_time_of_service / utilization_factor
        total_time_of_clinic_hrs=[]  # total_time_of_clinic_min / 60
        mean_waiting_time_percentage=[]
        mean_service_time_percentage=[]
        
        for i in range(len(clinic_types)):
            mean_service_rate_hrs.append(60/mean_service_time[i])
            mean_arrival_rate_hrs.append((mean_waiting_time[i]*(mean_service_rate_hrs[i]**2))/(60+mean_waiting_time[i]*mean_service_rate_hrs[i]))
            utilization_factor.append(mean_arrival_rate_hrs[i]/mean_service_rate_hrs[i])
            percent_idle_time.append(1-utilization_factor[i])
            mean_interarrival_time.append(60 / mean_arrival_rate_hrs[i])
            Lq.append(mean_arrival_rate_hrs[i]**2/(mean_service_rate_hrs[i]*(mean_service_rate_hrs[i]-mean_arrival_rate_hrs[i]))) 
            Ls.append(mean_arrival_rate_hrs[i]/(mean_service_rate_hrs[i]-mean_arrival_rate_hrs[i]))
            Ts.append(1/(mean_service_rate_hrs[i]-mean_arrival_rate_hrs[i]))
            Pn.append(1-(1-mean_arrival_rate_hrs[i]/mean_service_rate_hrs[i])*(1+mean_arrival_rate_hrs[i]/mean_service_rate_hrs[i]))
            total_time_of_service_min.append(mean_number_of_patients[i]*mean_service_time[i])
            total_time_of_clinic_min.append(total_time_of_service_min[i]/utilization_factor[i])
            total_time_of_clinic_hrs.append(total_time_of_clinic_min[i]/60)
            mean_service_time_percentage.append(mean_service_time[i]/(mean_service_time[i]+mean_waiting_time[i]))
            mean_waiting_time_percentage.append(mean_waiting_time[i]/(mean_service_time[i]+mean_waiting_time[i]))
            
            
        return {'clinic_types':clinic_types,
                'mean_waiting_times':[round(num, 2) for num in mean_waiting_time],
                'mean_service_time':[round(num, 2) for num in mean_service_time],
                'mean_number_of_patients':[round(num) for num in mean_number_of_patients],
                "mean_service_rate_hrs":mean_service_rate_hrs,
                "mean_arrival_rate_hrs":mean_arrival_rate_hrs,
                "utilization_factor":utilization_factor,
                "percent_idle_time":percent_idle_time,
                "mean_interarrival_time":mean_interarrival_time,
                "Lq":Lq,
                "Ls":Ls,
                "Ts":Ts,
                "Pn":Pn,
                "total_time_of_service_min":[round(num, 2) for num in total_time_of_service_min],
                "total_time_of_clinic_min":[round(num, 2) for num in total_time_of_clinic_min],
                "total_time_of_clinic_hrs":[round(num, 2) for num in total_time_of_clinic_hrs],
                "mean_service_time_percentage":mean_service_time_percentage,
                "mean_waiting_time_percentage":mean_waiting_time_percentage}

    def get_descriptive_analysis(self,main_analysis):
        descriptive_analysis={"descriptive_analysis_pars":["mean","median","max","min","range",'var','std','skew',"kurt"]}
        
        for key,value in main_analysis.items():
            if key !='clinic_types':
                descriptive_analysis[key]=[np.mean(value),np.median(value),max(value),min(value),max(value)-min(value),np.var(value),np.std(value),skew(value),kurtosis(value)]
        
        return descriptive_analysis
        
    def get_max_clinic_in(self,arr,clinic_types):
        max_value=max(arr)
        index_of_max=arr.index(max_value)
        clinic_name=clinic_types[index_of_max]
        return clinic_name
    
    def get_min_clinic_in(self,arr,clinic_types):
        min_value=min(arr)
        index_of_min=arr.index(min_value)
        clinic_name=clinic_types[index_of_min]
        return clinic_name
    
    def get_max_index_clinic_in(self,arr):
        return arr.index(max(arr))
    
    def get_min_index_clinic_in(self,arr):
        return arr.index(min(arr))

    def get_clinics_reports(self,main_analysis):
        clinics_reports={}
        for i in range(len(main_analysis['clinic_types'])): 
            # Key attributes
            clinics_reports[main_analysis['clinic_types'][i]]="<h2>Key attributes</h2><ul>"
            # Patients number
            clinics_reports[main_analysis['clinic_types'][i]]+=f"<li><h3>Patients number</h3><p>Number of patients of "
            clinics_reports[main_analysis['clinic_types'][i]]+= f"<b>{main_analysis['clinic_types'][i].capitalize()} clinic</b> is" 
            clinics_reports[main_analysis['clinic_types'][i]]+=f" <b>{round(main_analysis['mean_number_of_patients'][i])}</b> patients which represents"
            clinics_reports[main_analysis['clinic_types'][i]]+=f" <i>{round((main_analysis['mean_number_of_patients'][i]/sum(main_analysis['mean_number_of_patients']))*100)}%</i> "
            clinics_reports[main_analysis['clinic_types'][i]]+=f"and that is <i>{'above ' if main_analysis['mean_number_of_patients'][i]>np.mean(main_analysis['mean_number_of_patients']) else 'below '}</i>the average of patients of all clinics in the department which is around {round(np.mean(main_analysis['mean_number_of_patients']))} patients. "
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' 'if main_analysis['mean_number_of_patients'][i]!=max(main_analysis['mean_number_of_patients']) else 'and it has the maximum number of patients'}"
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' </p></li>'if main_analysis['mean_number_of_patients'][i]!=min(main_analysis['mean_number_of_patients']) else ', and it has the minmum number of patients.</p></li>'}"
            # Waiting time
            clinics_reports[main_analysis['clinic_types'][i]]+=f"<li><h3>Waiting time</h3><p>The mean waiting time for patients of "
            clinics_reports[main_analysis['clinic_types'][i]]+= f"<b>{main_analysis['clinic_types'][i].capitalize()} clinic</b> is" 
            clinics_reports[main_analysis['clinic_types'][i]]+=f" <b>{round(main_analysis['mean_waiting_times'][i])}</b> minutes which represents {round(main_analysis['mean_waiting_time_percentage'][i],2)}% of the total time at which the patient spend in the clinic and "
            clinics_reports[main_analysis['clinic_types'][i]]+=f"that is <i>{'above ' if main_analysis['mean_waiting_times'][i]>np.mean(main_analysis['mean_waiting_times']) else 'below '}</i>the average of waiting time for patients in all clinics in the department which is around {round(np.mean(main_analysis['mean_waiting_times']))} min."
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' 'if main_analysis['mean_waiting_times'][i]!=max(main_analysis['mean_waiting_times']) else ',and it has <b>the maximum waiting time</b>.'}"
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' </p></li>'if main_analysis['mean_waiting_times'][i]!=min(main_analysis['mean_waiting_times']) else ',a nd it has <b>the minmum waiting time</b>.</p></li>'}"
            # Service time for patient
            clinics_reports[main_analysis['clinic_types'][i]]+=f"<li><h3>Service time for patient</h3><p>Service time for patient of "
            clinics_reports[main_analysis['clinic_types'][i]]+= f"<b>{main_analysis['clinic_types'][i].capitalize()} clinic</b> is" 
            clinics_reports[main_analysis['clinic_types'][i]]+=f" <b>{round(main_analysis['mean_service_time'][i])}</b> minutes which represents {round(main_analysis['mean_service_time_percentage'][i],2)}% of the total time at which the patient spend in the clinic and "
            clinics_reports[main_analysis['clinic_types'][i]]+=f"that is <i>{'above ' if main_analysis['mean_service_time'][i]>np.mean(main_analysis['mean_service_time']) else 'below '}</i>the average of service time for patients in all clinics in the department which is around {round(np.mean(main_analysis['mean_service_time']))} minutes."
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' 'if main_analysis['mean_service_time'][i]!=max(main_analysis['mean_service_time']) else ',and it has <b>the maximum service time</b>.'}"
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' </p></li></ul>'if main_analysis['mean_service_time'][i]!=min(main_analysis['mean_service_time']) else ', and it has <b>the minmum service time</b>.</p></li></ul>'}"
           
            # Observations
            clinics_reports[main_analysis['clinic_types'][i]]+="<h2>Observations</h2><ul>"
            # Number of patients in queue
            clinics_reports[main_analysis['clinic_types'][i]]+=f"<li><h3>Number of patients in queue</h3><p>Number of patients in queue of "
            clinics_reports[main_analysis['clinic_types'][i]]+= f"<b>{main_analysis['clinic_types'][i].capitalize()} clinic</b> is" 
            clinics_reports[main_analysis['clinic_types'][i]]+=f" <b>{round(main_analysis['Lq'][i])}</b> patients which represents <i>{round(main_analysis['Lq'][i]/main_analysis['Ls'][i]*100)}</i> of patinets in the entire system (in queue and reatment room) "
            clinics_reports[main_analysis['clinic_types'][i]]+=f"and that is <i>{'above ' if main_analysis['Lq'][i]>np.mean(main_analysis['Lq']) else 'below '}</i>the average of patient that are waiting for their turn in all clinics in the depratment which is around {round(np.mean(main_analysis['Lq']))} patients."
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' 'if main_analysis['Lq'][i]!=max(main_analysis['Lq']) else ',and it has <b>the maximum number of patients in queue</b>.'}"
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' </p></li>'if main_analysis['Lq'][i]!=min(main_analysis['Lq']) else ', and it has <b>the minmum number of patients in queue</b>.</p></li>'}"
            # Number of patients in system
            clinics_reports[main_analysis['clinic_types'][i]]+=f"<li><h3>Number of patients in system</h3><p>Number of patients in system of "
            clinics_reports[main_analysis['clinic_types'][i]]+= f"<b>{main_analysis['clinic_types'][i].capitalize()} clinic</b> is" 
            clinics_reports[main_analysis['clinic_types'][i]]+=f" <b>{round(main_analysis['Ls'][i])}</b> patients "
            clinics_reports[main_analysis['clinic_types'][i]]+=f"and that is <i>{'above ' if main_analysis['Ls'][i]>np.mean(main_analysis['Ls']) else 'below '}</i>the average of patient that are waiting and taking service in all clinics in the department which is around {round(np.mean(main_analysis['Ls']))} patients."
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' 'if main_analysis['Ls'][i]!=max(main_analysis['Ls']) else ',and it has <b>the maximum number of patients in system</b>.'}"
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' </p></li>'if main_analysis['Ls'][i]!=min(main_analysis['Ls']) else ', and it has <b>the minmum number of patients in system</b>.</p></li>'}"
            # Working time of clinic
            clinics_reports[main_analysis['clinic_types'][i]]+=f"<li><h3>Working time of clinic</h3><p>Total time for "
            clinics_reports[main_analysis['clinic_types'][i]]+= f"<b>{main_analysis['clinic_types'][i].capitalize()} clinic</b> to work is" 
            clinics_reports[main_analysis['clinic_types'][i]]+=f" <b>{round(main_analysis['total_time_of_clinic_hrs'][i])}</b> hours "
            clinics_reports[main_analysis['clinic_types'][i]]+=f"and that is <i>{'above ' if main_analysis['total_time_of_clinic_hrs'][i]>np.mean(main_analysis['total_time_of_clinic_hrs']) else 'below '}</i>the average of time of all clinics to work in the department which is around {round(np.mean(main_analysis['total_time_of_clinic_hrs']))} hours."
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' 'if main_analysis['total_time_of_clinic_hrs'][i]!=max(main_analysis['total_time_of_clinic_hrs']) else ',and it has <b>the maximum working time</b>.'}"
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' </p></li>'if main_analysis['total_time_of_clinic_hrs'][i]!=min(main_analysis['total_time_of_clinic_hrs']) else ', and it has <b>the minmum working time</b>.</p></li>'}"
            
            # Service time of clinic
            clinics_reports[main_analysis['clinic_types'][i]]+=f"<li><h3>Service time of clinic</h3><p>Total time for "
            clinics_reports[main_analysis['clinic_types'][i]]+= f"<b>{main_analysis['clinic_types'][i].capitalize()} clinic</b> to serve patients is" 
            clinics_reports[main_analysis['clinic_types'][i]]+=f" <b>{round(main_analysis['total_time_of_service_min'][i])}</b> minutes which represents {round(main_analysis['total_time_of_service_min'][i]/main_analysis['total_time_of_clinic_min'][i]*100)}% of the total working time of thw clinic, "
            clinics_reports[main_analysis['clinic_types'][i]]+=f"and that is <i>{'above ' if main_analysis['total_time_of_service_min'][i]>np.mean(main_analysis['total_time_of_service_min']) else 'below '}</i>the average of all clinics to serve patients in the department which is around {round(np.mean(main_analysis['total_time_of_service_min']))} minutes."
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' 'if main_analysis['total_time_of_service_min'][i]!=max(main_analysis['total_time_of_clinic_hrs']) else ',and it has <b>the maximum service time</b>.'}"
            clinics_reports[main_analysis['clinic_types'][i]]+=f"{' </p></li></ul>'if main_analysis['total_time_of_clinic_hrs'][i]!=min(main_analysis['total_time_of_clinic_hrs']) else ', and it has <b>the minmum service time</b>.</p></li></ul>'}"
            
        return clinics_reports
    
    def get_summary_report(self,main_analysis):
        summary_report="<h2>Key attributes</h3>"
        summary_report+=f"<ul><li><h3>Patient number</h4> <p>The <i>total paient number</i> in the outpatient department is " 
        summary_report+=f"{round(sum(main_analysis['mean_number_of_patients']))} patients with <i>average</i> of "
        summary_report+=f"{round(np.average(main_analysis['mean_number_of_patients']))} patients, and we found that" 
        summary_report+=f"<b>{self.get_max_clinic_in(main_analysis['mean_number_of_patients'],main_analysis['clinic_types'])}</b> clinic has the <i>maximum number of patients</i> with <b>"
        summary_report+=f"{round(max(main_analysis['mean_number_of_patients']))}</b> patients which represents <b>{round(max(main_analysis['mean_number_of_patients'])*100/sum(main_analysis['mean_number_of_patients']))}%</b> of total patients in OPD, while <b>"
        summary_report+=f"{self.get_min_clinic_in(main_analysis['mean_number_of_patients'],main_analysis['clinic_types'])}</b> has the <i>minimum number of patients</i> with <b>{round(min(main_analysis['mean_number_of_patients']))}</b> patients</p> </li> <li> <h4>Waiting time</h4> <p>The <i>total waiting time</i> in the outpatient department is {round(sum(main_analysis['mean_waiting_times']))} minutes with <i>average</i> of {round(np.average(main_analysis['mean_waiting_times']))} minutes, and we found that <b>{self.get_max_clinic_in(main_analysis['mean_waiting_times'],main_analysis['clinic_types'])}</b> "
        summary_report+=f"clinic has the <i>maximum waiting time</i> in the queue with <b>{round(max(main_analysis['mean_waiting_times']))}</b> minutes with arrival rate of <b>{round(main_analysis['mean_arrival_rate_hrs'][self.get_max_index_clinic_in(main_analysis['mean_waiting_times'])])}</b> patient per hour, while "
        summary_report+=f"<b>{self.get_min_clinic_in(main_analysis['mean_waiting_times'],main_analysis['clinic_types'])}</b> has the <i>minimum waiting time</i> with <b>{round(min(main_analysis['mean_waiting_times']))}</b> minutes with arrival rate of <b>{round(main_analysis['mean_arrival_rate_hrs'][self.get_min_index_clinic_in(main_analysis['mean_waiting_times'])])}</b> patient per hour</p> </li> <li> <h4>Service time for patient</h4> <p>The <i>total service time</i> in the outpatient department is {round(sum(main_analysis['mean_service_time']))} minutes with <i>average</i> of {round(np.average(main_analysis['mean_service_time']))} minutes, and we found that "
        summary_report+=f"<b>{self.get_max_clinic_in(main_analysis['mean_service_time'],main_analysis['clinic_types'])}</b> clinic has the <i>maximum service time</i> with <b>{round(max(main_analysis['mean_service_time']))}</b> minutes with service rate of <b>{round(main_analysis['mean_service_rate_hrs'][self.get_max_index_clinic_in(main_analysis['mean_service_time'])])}</b> patient per hour ,while <b>{self.get_min_clinic_in(main_analysis['mean_service_time'],main_analysis['clinic_types'])}</b> has the <i>minimum service time</i> with "
        summary_report+=f"<b>{min(main_analysis['mean_service_time'])}</b> minutes with service rate of <b>{round(main_analysis['mean_service_rate_hrs'][self.get_min_index_clinic_in(main_analysis['mean_service_time'])])}</b> patient per hour</p> </li> </ul> <h3>Observations</h3> <ul> <li> <h4>Number of patients in queue</h4> "
        summary_report+=f"<p>The <i>average number of patients in queue for all clinics</i> is {round(np.average(main_analysis['Lq']))} patients, we found that <b>{self.get_max_clinic_in(main_analysis['Lq'],main_analysis['clinic_types'])}</b> clinic has the <i>maximum number of patients in queue</i> with <b>{round(max(main_analysis['Lq']))}</b> patients ,while <b>{self.get_min_clinic_in(main_analysis['Lq'],main_analysis['clinic_types'])}</b> has the <i>minimum number of patients in queue</i> with <b>{round(min(main_analysis['Lq']))}</b> patients</p> </li> <li> <h4>Number of patients in system</h4> <p>The <i>average number of patients in system for all clinics</i> is {round(np.average(main_analysis['Ls']))} patients, we found that <b>{self.get_max_clinic_in(main_analysis['Ls'],main_analysis['clinic_types'])}</b> clinic has the "
        summary_report+=f"<i>maximum number of patients in system</i> with <b>{round(round(max(main_analysis['Ls'])))}</b> patients ,while <b>{self.get_min_clinic_in(main_analysis['Ls'],main_analysis['clinic_types'])}</b> has the <i>minimum number of patients in system</i> with <b>{round(min(main_analysis['Ls']))}</b> patients</p> </li> <li> <h4>Working time of clinic</h4> <p>The <i>average of working time of all clinics</i> is {round(np.average(main_analysis['total_time_of_clinic_hrs']))} hours, we found that <b>{self.get_max_clinic_in(main_analysis['total_time_of_clinic_hrs'],main_analysis['clinic_types'])}</b> clinic has the <i>maximum working time</i> as it works for <b>{round(max(main_analysis['total_time_of_clinic_hrs']))}</b> hours ,while <b>{self.get_min_clinic_in(main_analysis['total_time_of_clinic_hrs'],main_analysis['clinic_types'])}</b> has the <i>minimum working time</i> as it works for <b>{round(min(main_analysis['total_time_of_clinic_hrs']))}</b> hours</p> </li> <li> <h4>Service time of clinic</h4> <p>The <i>average of service time of all clinics</i> is {round(np.average(main_analysis['total_time_of_service_min']))} minutes which "
        summary_report+=f"represents {round(np.average(main_analysis['total_time_of_service_min'])*100/sum(main_analysis['total_time_of_clinic_min']))}% of the total working time for all clinics, we found that <b>{self.get_max_clinic_in(main_analysis['total_time_of_service_min'],main_analysis['clinic_types'])}</b> clinic has the <i>maximum service time</i> with <b>{round(max(main_analysis['total_time_of_service_min']))}</b> minutes which represents {round(max(main_analysis['total_time_of_service_min'])*100/main_analysis['total_time_of_clinic_min'][self.get_max_index_clinic_in(main_analysis['total_time_of_service_min'])])}% of working time ,while <b>{self.get_min_clinic_in(main_analysis['total_time_of_service_min'],main_analysis['clinic_types'])}</b> has the <i>minimum service time</i> with <b>{round(min(main_analysis['total_time_of_service_min']))}</b> minutes which represents {round(min(main_analysis['total_time_of_service_min'])*100/main_analysis['total_time_of_clinic_min'][self.get_min_index_clinic_in(main_analysis['total_time_of_service_min'])])}% of working time</p> </li> </ul>"
        
        return summary_report
    
    def generate_random_data(self,mean_patient_num,mean_interarrival_time):
        service_time=[5.5 + random() * (11 - 5.5) for i in range(mean_patient_num)]
        interarrival_time=[*np.random.exponential(1/mean_interarrival_time, mean_patient_num)]
        return service_time,interarrival_time
    
    def simulate_one_clinic(self,mean_patient_num,mean_interarrival_time):
        service_time, interarrival_time=self.generate_random_data(mean_patient_num,mean_interarrival_time)
        
        arrival_time=[]
        completion_time=[0]
        start_time=[]
        wait_time=[]
        system_time=[]
        for i in range(len(interarrival_time)):
            arrival_time.append(round(sum(interarrival_time[0:i+1]),2))
            if arrival_time[i]>completion_time[i]:
                start_time.append(arrival_time[i])
            else:
                start_time.append(completion_time[i])
            wait_time.append(round(start_time[i]-arrival_time[i],2))
            completion_time.append(round(start_time[i]+service_time[i],2))
            system_time.append(round(completion_time[i+1]-arrival_time[i],2))
        
        return {
            'customer':[num for num in range(1, len(interarrival_time)+1)],
            'interarrival_time':interarrival_time,
            'arrival_time':arrival_time,
            'service_start_time':start_time,
            'waiting_time':wait_time,
            'service_time':service_time,
            'completion_time':completion_time[1::],
            'time_in_system':system_time
            }
    
    def simulate_two_clinics(self,mean_patient_num,mean_interarrival_time):
        service_time, interarrival_time=self.generate_random_data(mean_patient_num,mean_interarrival_time)
        arrival_time=[]
        completion_time=[0]
        start_time=[]
        wait_time=[]
        system_time=[]
        server_01=[]
        server_02=[]
        for i in range(len(interarrival_time)):
            arrival_time.append(round(sum(interarrival_time[0:i+1]),2))
            if i+1==1:
                start_time.append(round(arrival_time[i],2))
                completion_time.append(round(service_time[i]+start_time[i],2))
                server_01.append(round(completion_time[i+1],2))
                server_02.append(0)
            else:
                if arrival_time[i]<min(server_02[i-1],server_01[i-1]):
                    start_time.append(min(server_02[i-1],server_01[i-1]))
                else: start_time.append(arrival_time[i])
                
                completion_time.append(service_time[i]+start_time[i])
                
                if server_01[i-1]==min(server_01[i-1],server_02[i-1]):
                    server_01.append(completion_time[i+1])

                else: server_01.append(server_01[i-1])
                
                if server_02[i-1]==min(server_01[i-1],server_02[i-1]):
                    server_02.append(round(completion_time[i+1],2))
                else: server_02.append(round(server_02[i-1],2)) 
            
            wait_time.append(round(start_time[i]-arrival_time[i],2))
            system_time.append(round(wait_time[i]+service_time[i],2))
        
        return {
            'customer':[num for num in range(1, len(interarrival_time)+1)],
            'interarrival_time':interarrival_time,
            'arrival_time':arrival_time,
            'service_start_time':start_time,
            'waiting_time':wait_time,
            'service_time':service_time,
            'completion_time':completion_time[1::],
            'time_in_system':system_time,
            'server_01':server_01,
            'server_02':server_02
            }
    
    
    def simulate_appointments_booking(self,mean_patient_num,appointments_time,mean_interarrival_time):
        # Set appointment times
        customer_appoints = [i * appointments_time for i in range(mean_patient_num)] # appointment for each customer every "appointments_time" min 
             
        server_data=self.simulate_one_clinic(mean_patient_num,mean_interarrival_time)
        booking_wait=[0]

        # Booking every appointments_time min
        for i in range(mean_patient_num-1):
            if customer_appoints[i]<server_data['arrival_time'][i]:
                booking_wait.append(0)
            else: booking_wait.append(server_data['waiting_time'][i])
    
        server_data['appointment_times']=customer_appoints
        server_data['booking_wait']=booking_wait
        server_data['analysis_summary']=f'<p>The implementation of an optimized booking strategy led to a <i>reduction in waiting time</i>, decreasing it by <b>{round((1-np.mean(booking_wait)/np.mean(server_data["waiting_time"]))*100)}%</b></p>'
        server_data["before_after"]=[round(np.mean(server_data["waiting_time"]),2),round(np.mean(booking_wait),2)]
        server_data['times']=appointments_time
        return server_data
        
    def simulate_servers_for_all_clinics(self,main_analysis):
        clinic_server_simulation_data={}
        for i in range(len(main_analysis['clinic_types'])):
            one_clinic=self.simulate_one_clinic(round(main_analysis['mean_number_of_patients'][i]),main_analysis['mean_interarrival_time'][i])
            two_clinics=self.simulate_two_clinics(round(main_analysis['mean_number_of_patients'][i]),main_analysis['mean_interarrival_time'][i])
            analysis_summary=f'<p>The intervention of establishing an additional clinic reduced waiting time, <i>decreasing</i> it by <b>{round((1-np.mean(two_clinics["waiting_time"])/np.mean(one_clinic["waiting_time"]))*100)}%</b></p>'
            clinic_server_simulation_data[main_analysis['clinic_types'][i]]={'one_clinic':one_clinic,'two_clinics':two_clinics,'analysis_summary':analysis_summary,"before_after":[round(np.mean(one_clinic["waiting_time"]),2),round(np.mean(two_clinics["waiting_time"]),2)]}
            
        return clinic_server_simulation_data
        
    def get_result(self):
        main_analysis=self.get_main_analysis()
        return{"main_analysis":main_analysis,
               "descriptive_analysis":self.get_descriptive_analysis(main_analysis),
               "clinics_reports":self.get_clinics_reports(main_analysis),
               "summary_report":self.get_summary_report(main_analysis),
               "simulate_servers":self.simulate_servers_for_all_clinics(main_analysis)
               }

# print(OutpatientDepartment('student_clinic_data.csv').get_result())