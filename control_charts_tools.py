import numpy as np
def get_points_out_of_contols(x,y,lcl,ucl):
        '''
            input x_value, y_value, low_contol_level, and upper_control_level
            output special_control_variation => out_of_control_points
        '''
        scv={'x':[],'y':[]}
        for k in range(len(y)):
            if y[k]>ucl or y[k]<lcl:
                scv['x'].append(x[k])
                scv['y'].append(y[k])
        return scv

def check_less_than_value(arr,value):
    '''
        input array_of_values, and compared_value
        output is_less_than or not in form of boolean value
    '''
    for i in arr:
        if(i>=value):return False
    return True

def check_greater_than_value(arr,value):
    '''
        input array_of_values, and compared_value
        output is_greater_than or not in form of boolean value
    '''
    for i in arr:
        if(i<=value):return False
    return True

def get_points_with_pattern(x,y,mean):
    '''
        input x_value, y_value, and mean_of_y_values
        output special_control_variation => points_with_pattern
    '''
    scv={'x':[],'y':[]}
    for k in range(len(y)):
        if(k+7<len(y)): 
            if check_less_than_value(y[k:k+8],mean):
                scv['x']+=x[k:k+8]
                scv['y']+=y[k:k+8]
            if check_greater_than_value(y[k:k+8],mean):
                scv['x']+=x[k:k+8]
                scv['y']+=y[k:k+8]
    return scv

def get_horizonatl_line(x,value):
    horizontal_line={'x':x,'y':[]}
    for i in x:
        horizontal_line['y']+=[value]
    return horizontal_line

def ssd(arr):
    '''
    ssd => Sample Standard Deviation
    s=sqrt(sum(xi-x_bar)^2/N-1)
    '''
    x_bar=np.mean(arr)
    sum=0
    for xi in arr:
        sum+=(xi-x_bar)**2
    s=np.sqrt(sum/(len(arr)-1))
    return s

