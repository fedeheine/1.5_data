import streamlit as st
import pandas as pd
from io import StringIO
from utils import hourly_data, dict_to_csv, max_hourly, max_half_hourly
import numpy as np

def convert_df_to_csv(df):
    # Convert DataFrame to CSV
    output = StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

version = st.text_input('enter the version (1 or 2)')

if len(version)>0:
    version= int(float(version))

st.title('Maximo ' + str(version) + ' Performance Data Analysis')

if version==1:
    st.image("robot.JPG")

elif version==2:
    st.image("robot_new.jpg")

else:
    pass

if (version):

    # File uploader allows user to add a file
    uploaded_file = st.file_uploader("Upload the database CSV file", type=['csv'])
    data_date=None
    if uploaded_file is not None:
        
        # Load data
        data_date = st.text_input('enter the date for analysis in the format (yyyymmdd)')
        print(data_date)
        
        fields = ['cycle_start_time', 'panel_count']

        data = pd.read_csv(uploaded_file, parse_dates=['cycle_start_time'], usecols=fields)

        if  (data_date):    

        
            # Extract date from the columns
            data [ 'date'] = data['cycle_start_time'].dt.date

            # %%
            # Convert the date to datetime64
            data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

            try:
                data_f = data.loc[data['date'] == data_date]
            
            
            

                # Extract hour from the time
                data_f['hour'] = data_f['cycle_start_time'].dt.hour
                data_f['minute'] = data_f['cycle_start_time'].dt.minute
                filtered_data = data_f.filter(['hour', 'minute', 'panel_count'])
                filtered_data = filtered_data.to_numpy()

                if version==2:
                    filtered_data = filtered_data[::-1]
                    st.write('version selected is', version)


                else:
                    st.write('version selected is', version)
                # print(filtered_data[::-1])

                # call analytic function
                hour_dict = hourly_data(filtered_data[:,[0,2]])

                #call csv writer
                dict_to_csv(hour_dict, 'hourly_data_summary_'+data_date+'.csv')

                # finding best 3 hours

                # Show processed data in the app
                
                # Read the CSV file into a pandas DataFrame
                df = pd.read_csv('hourly_data_summary_'+data_date+'.csv')

                st.write("Processed Data", df) 

                if len(filtered_data)>1:
                    max, time_slots, start_index, final_index = max_hourly(np.copy(filtered_data))
                    print('max is', max)
                    st.write('1st hourly best is', max, '\t between ', time_slots[0],' to ', time_slots[1])

                    max_h, time_slots_h, start_index_h, final_index_h = max_half_hourly(np.copy(filtered_data))
                    st.write('1st half hourly best is', max_h, '\t between ', time_slots_h[0],' to ', time_slots_h[1])

                    filtered_data2 = np.delete(filtered_data, np.arange(start_index, final_index), 0)
                    filtered_data2h = np.delete(filtered_data, np.arange(start_index_h, final_index_h), 0)

                else:
                    max, time_slots, start_index, final_index = 0,0,0,0
                    max_h, time_slots_h, start_index_h, final_index_h = 0,0,0,0
                

                if len(filtered_data2h)>1:
                    max2, time_slots2, start_index2, final_index2 = max_hourly(np.copy(filtered_data2))
                    st.write('2nd hourly best is', max2, '\t between ', time_slots2[0],' to ', time_slots2[1])
            

                    max2_h, time_slots2_h, start_index2_h, final_index2_h = max_half_hourly(np.copy(filtered_data2h))
            
                    st.write('2nd half hourly best is', max2_h, '\t between ', time_slots2_h[0],' to ', time_slots2_h[1])

                    filtered_data3 = np.delete(filtered_data2, np.arange(start_index2, final_index2), 0)
                    filtered_data3h = np.delete(filtered_data2h, np.arange(start_index2_h, final_index2_h), 0)

                else:
                    max2, time_slots2, start_index2, final_index2 = 0,0,0,0
                    max2_h, time_slots2_h, start_index2_h, final_index2_h = 0,0,0,0

                if len(filtered_data3h)>1:

                    max3, time_slots3, start_index3, final_index3 = max_hourly(filtered_data3)
                    st.write('3rd hourly best is', max3, '\t between ', time_slots3[0],' to ', time_slots3[1])

                    max3_h, time_slots3_h, start_index3_h, final_index3_h = max_half_hourly(filtered_data3h)
                    st.write('3rd half hourly best is', max3_h, '\t between ', time_slots3_h[0],' to ', time_slots3_h[1])

                else:
                    max3, time_slots3, start_index3, final_index3 = 0,0,0,0
        
            except:
                print("Data not available , please try again! ")
                st.write(" You need to work to get the data, try again!")






