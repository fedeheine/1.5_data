# %%
import pandas as pd
import numpy as np
import csv
import datetime

# function to perform hourly analysis
def hourly_data(filtered_data:np.array)->dict:
    global time_d
    global count_in
    global count_fin
    time_d = np.nan
    hour_dict = {}

    for i,j in enumerate(filtered_data):

        #counter to 0 if the timing changes
        if time_d != j[0]:

            #updating the time key
            time_d = j[0]

            # initialising the count during start of the day
            if i==0:
                count_in = j[1]
            
            # initialising the hourly count to 0
            count = 0


        #conditions for counting the modules per hour
        elif i>1:

            # checking the final count in that hour
            count_fin = j[1]
            
            # check if the count has reduced
            if (count_in - count_fin)>=0:
                count+= count_in - count_fin

                # updating the initial count of modules with current
                count_in = count_fin

            # if the final count is increased (re-loaded) and last module is either 1 or 2
            elif (count_in - count_fin)<0 and (count_in==2 or count_in==1):
                count+=count_in
                count_in=count_fin

            # if the final count is increased (re-loaded) and last module is neither 1 nor 2
            elif (count_in - count_fin)<0 and (count_in!=2 or count_in!=1):
                count+=2
                # updating the initial count of modules with current
                count_in=count_fin

            # if it was the last entry on the database, there is a high chnace we placed 2 more modules
            if i+1==len(filtered_data):
                count+=2

        # continuously updating the number
        hour_dict[time_d]=count
    return hour_dict



def dict_to_csv(input_dictionary:dict, output_csv:str):
    with open(output_csv, "w") as f:
            w = csv.writer(f)
            w.writerow(['time','# of panels']) 
            sum = 0 
            for keys,values in input_dictionary.items(): 
                
                    # w.writeheader()
                    w.writerow([keys,values])
                    sum+=values
            w.writerow(['total', sum])




def max_hourly(data:np.array):
        time_slots = []
        max = 0
        start_index, final_index,  = np.nan, np.nan
        for i in range(len(data)):
                # print('row number', i, '\n')
                h_in = data[i,0]
                m_in = data[i,1]
                m_out = (m_in+60)%60
        
                h_out = h_in+1

                start = np.where(np.logical_and(data[:,0]>=h_in, data[:,1]>=m_in))
                # filtered_data_bh = filtered_data[alas]
                #getting the index for the start time
                start = start[0][0]

                # if the hour input is not the last element of the excel
                if h_in < data[-1,0]:
                        final = np.where((np.logical_and(data[:,0]<=h_out, data[:,1]<=m_out)))
                        final = final[0][-1]+1
                        filtered_data_bh = data[start:final]
                else:
                        filtered_data_bh = data[start:]
                # print(filtered_data_bh)
                # alas = np.where(np.logical_and(filtered_data[:,0]<=h_out, filtered_data[:,1]<=m_in))
                # filtered_data_bh = filtered_data[alas]
                rows,col = filtered_data_bh.shape
                filtered_data_empty = np.empty((rows,2))
                filtered_data_empty[:,0] = filtered_data_bh[:,0]
                filtered_data_empty[:,1] = filtered_data_bh[:,2]

                # print(filtered_data_bh)
                # print(h_in, m_in, h_out, m_out)
                # print(final)
                hour_dict = hourly_data(filtered_data_empty)

                

                # print('hour_dict \n', filtered_data_empty)
        
                sum_curr =0
                for values in hour_dict.values():
                        sum_curr+=values
                # print('hour gap', filtered_data_bh[0], ':', filtered_data_bh[-1] )
                # print(sum_curr)
                # print(sum_curr, (h_in,m_in), (h_out, m_out))
                # print(filtered_data_bh)
                if max<sum_curr:
                        max=sum_curr
                        time_slots = [(h_in,m_in), (h_out, m_out)]
                        start_index = start
                        final_index = final
        
        return max, time_slots, start_index, final_index



def max_half_hourly(data:np.array):
        start_index = np.nan
        final_index = np.nan
        time_slots = []
        max = 0
        for i in range(len(data)):
                # print('row number', i, '\n')
                h_in = data[i,0]
                m_in = data[i,1]
                m_out = (m_in+30)%30

                if m_in>=30:
                    h_out = h_in+1
                else:
                    h_out = h_in
                start = np.where(np.logical_and(data[:,0]>=h_in, data[:,1]>=m_in))
                start = start[0][0]
                
                final = np.where((np.logical_and(data[:,0]<=h_out, data[:,1]<=m_out)))
                r_,c_ = np.shape(final)

                print('debug', final)
                if c_:
                        # final = final[0][-1]+1
                        if h_out <= data[-1,0]:
                                final = np.where((np.logical_and(data[:,0]<=h_out, data[:,1]<=m_out)))
                                final = final[0][-1]+1
                                filtered_data_bh = data[start:final]
                        else:
                                filtered_data_bh = data[start:]
                        rows,col = filtered_data_bh.shape
                        filtered_data_empty = np.empty((rows,2))
                        filtered_data_empty[:,0] = filtered_data_bh[:,0]
                        filtered_data_empty[:,1] = filtered_data_bh[:,2]

                        hour_dict = hourly_data(filtered_data_empty)
                
                        sum_curr =0
                        for values in hour_dict.values():
                                sum_curr+=values
                        if max<sum_curr:
                                max=sum_curr
                                time_slots = [(h_in,m_in), (h_out, m_out)]
                                start_index = start
                                final_index = final
                else:
                       pass
        
        return max, time_slots, start_index, final_index



def main():
    # Assuming data is in a CSV file; replace 'data.csv' with your file path
    # Your data file should have columns named 'cycle_sstart_time' and 'panel_count', where 'Time' is in HH:MM:SS format

    # Load data
    data_date = input("Enter the date for which the data is required ('20240409') \n")
    excel_date = input("Enter the date of the excel file (last 6 digits of csv) \n")
    # date = '2024-04-18'
    fields = ['cycle_start_time', 'panel_count']

    data = pd.read_csv('atlasdb.cycle_data_'+excel_date+'.csv', parse_dates=['cycle_start_time'], usecols=fields)

    # Extract date from the columns
    data [ 'date'] = data['cycle_start_time'].dt.date

    # %%
    # Convert the date to datetime64
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    data_f = data.loc[data['date'] == data_date]
    

    # Extract hour from the time
    data_f['hour'] = data_f['cycle_start_time'].dt.hour
    data_f['minute'] = data_f['cycle_start_time'].dt.minute
    
    filtered_data = data_f.filter(['hour', 'minute', 'panel_count'])
    filtered_data = filtered_data.to_numpy()

    # finding best 3 hours
    max, time_slots, start_index, final_index = max_half_hourly(np.copy(filtered_data))


    filtered_data2 = np.delete(filtered_data, np.arange(start_index, final_index+1), 0)


    max2, time_slots2, start_index2, final_index2 = max_half_hourly(np.copy(filtered_data2))

    filtered_data3 = np.delete(filtered_data2, np.arange(start_index2, final_index2+1), 0)

    max3, time_slots3, start_index3, final_index3 = max_half_hourly(filtered_data3)

    print('1st hourly best is', max, '\t between ', time_slots, '\n')
    print('2nd hourly best is', max2, '\t between ', time_slots2, '\n')
    print('3rd hourly best is', max3, '\t between ', time_slots3)

    # call analytic function
    hour_dict = hourly_data(filtered_data[:,[0,2]])

    #call csv writer
    dict_to_csv(hour_dict, 'hourly_data_summary_'+data_date+'.csv')

    print('hourly data: \n', hour_dict)

if __name__ == "__main__":
    main()



