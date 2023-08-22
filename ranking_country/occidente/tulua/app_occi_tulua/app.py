#libraries
from datetime import datetime, timedelta
import timeit
import warnings
warnings.filterwarnings('ignore')
import sys
from dateutil.relativedelta import relativedelta
import os
current_dir = os.getcwd()
path_file = r"Documents\Proyectos-Cemex\sld_v2\ranking_country"
current_dir = os.path.join(current_dir,path_file)
# Define the relative path to the data directory
data_dir = os.path.join(current_dir, r'occidente\tulua')
print(data_dir)
#our own py scripts
#insert path to get help files 
sys.path.insert(0, data_dir)
from help_files_occi_tulua.sql_occi_tulua.connect_sql_server import *
from help_files_occi_tulua.clean_data_occi_tulua.clean_data import clean_data
from help_files_occi_tulua.send_to_excel_occi_tulua.send_to_excel import send_to_excel
from help_files_occi_tulua.functions_occi_tulua.functions import *


#run program
try:
    def main_tulua(plant):
         

      
        #get current date        
        today_date_dt = datetime.now()              
    
        #RUN ALL FUNCTIONS

        #get client list from last 3 months
        get_clients_df = get_clients(plant,today_date_dt,relativedelta,query_sql_df)
     

        #run for volumen attribute
        volumen_attribute_df = volumen_attribute(plant,query_sql_df)

        #run for profits
        profits_attribute_df = profits_attribute(query_sql_df,get_clients_df)
   
        #run for payment discipline
        payment_discipline_attribute_df = payment_discipline_attribute(query_sql_df)
        
        #run for bran visibility
        brandvis_growthpot_attribute_df = brandvis_growthpot_attribute(query_sql_df)

        #run for tool adoption
        tools_adoption_attribute_df = tools_adoption_attribute(query_sql_df,get_clients_df)
            
        #run for average site time
        time_in_site_attribute_df = time_in_site_attribute(plant,today_date_dt,relativedelta,query_sql_df)

        plant = 'CO-PLANTA TULUA PARAJE LA RIVERA'
        cluster = 'CLUSTER OCCIDENTE'
        #clean data to get final DF
        x = clean_data(get_clients_df,volumen_attribute_df,
                       time_in_site_attribute_df,profits_attribute_df,
                       payment_discipline_attribute_df,tools_adoption_attribute_df,brandvis_growthpot_attribute_df,cluster,plant)
        
        #delete data and send to sql
        database_name = "SCAC_AT51_SLDClientes_teorico"
        sql_statement = "delete from "+database_name+" where planta = ?"
        query_sql_crud(sql_statement,(plant))
        send_df_to_sql(x,database_name)
    main_tulua("F075")

except Exception as e:
    print(str(e))
    sys.exit()

