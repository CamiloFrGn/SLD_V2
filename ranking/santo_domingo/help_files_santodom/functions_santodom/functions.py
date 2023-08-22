import sys
import pandas as pd


def get_clients(cluster,today_date_dt,relativedelta,query_sql_df):
    try:

        sql_call_client_list = "{CALL sld_v2_client_list (?,?,?)}"
        startdate = today_date_dt - relativedelta(months=+3)
        startdate = startdate.replace(day=1)
        startdate = startdate.strftime("%Y-%m-%d")
        today_date_string = today_date_dt.strftime("%Y-%m-%d")
        client_list = query_sql_df(sql_call_client_list,(cluster,startdate,today_date_string))
        return client_list
    except Exception as e:
        print(str(e))
        sys.exit() 

def volumen_attribute(cluster,today_date_dt,relativedelta,query_sql_df):
    try:

        weight = 0.35
  
        sql_call_client_list = "{CALL sld_v2_volume_attribute (?,?,?)}"
        startdate = today_date_dt - relativedelta(months=+6)
        startdate = startdate.replace(day=1)
        startdate = startdate.strftime("%Y-%m-%d")
        today_date_string = today_date_dt.strftime("%Y-%m-%d")
        df_volumen_attribute = query_sql_df(sql_call_client_list,(cluster,startdate,today_date_string))
        df_volumen_attribute['volume'] = df_volumen_attribute['volume'].astype(float)
        df_volumen_attribute['volume'] = df_volumen_attribute['volume'].fillna(0)

        max_value = pd.DataFrame()
        max_value['volume'] = df_volumen_attribute['volume']
        max_value = max_value.loc[max_value['volume'].idxmax()]
        max_value = max_value/10
     
        range1 = max_value[0]
        range2 = max_value[0]*2
        range3 = max_value[0]*3
        range4 = max_value[0]*4
        range5 = max_value[0]*5
        range6 = max_value[0]*6
        range7 = max_value[0]*7
        range8 = max_value[0]*8
        range9 = max_value[0]*9

        def conditions(df_volumen_attribute):
            if (df_volumen_attribute['volume'] <= range1 ):
                x = (0.1*weight)*100
            if (df_volumen_attribute['volume'] > range1 ) and (df_volumen_attribute['volume'] <= range2 ):
                x = (0.2*weight)*100
            if (df_volumen_attribute['volume'] > range2 ) and (df_volumen_attribute['volume'] <= range3 ):
                x = (0.3*weight)*100
            if (df_volumen_attribute['volume'] > range3 ) and (df_volumen_attribute['volume'] <= range4 ):
                x = (0.4*weight)*100
            if (df_volumen_attribute['volume'] > range4 ) and (df_volumen_attribute['volume'] <= range5 ):
                x = (0.5*weight)*100
            if (df_volumen_attribute['volume'] > range5 ) and (df_volumen_attribute['volume'] <= range6 ):
                x = (0.6*weight)*100
            if (df_volumen_attribute['volume'] > range6 ) and (df_volumen_attribute['volume'] <= range7 ):
                x = (0.7*weight)*100
            if (df_volumen_attribute['volume'] > range7 ) and (df_volumen_attribute['volume'] <= range8 ):
                x = (0.8*weight)*100
            if (df_volumen_attribute['volume'] > range8 ) and (df_volumen_attribute['volume'] <= range9 ):
                x = (0.9*weight)*100
            if (df_volumen_attribute['volume'] > range9 ):
                x = (weight)*100
       

            return x
        
        df_volumen_attribute['volume_final'] = df_volumen_attribute.apply(conditions, axis=1)

        
        return df_volumen_attribute
    except Exception as e:
        print(str(e))
        sys.exit() 

def profits_attribute(query_sql_df,get_clients_df):
    try:

        weight = 0.25
        sql_call_client_list = "select * from sld_profits"
        profits_list = query_sql_df(sql_call_client_list,())
        profits_list = pd.merge(get_clients_df['Cliente'],profits_list,on="Cliente",how="left")
        profits_list['mc'] = profits_list['mc'].fillna(0)
        profits_list['update_date'] = profits_list['update_date'].fillna(profits_list['update_date'][0])
        profits_list['mc'] = profits_list['mc'].astype(float)
        profits_list = profits_list.sort_values(by=["mc"], ascending=[False])
        max_value = pd.DataFrame()
        max_value['mc'] = profits_list['mc']
        max_value = max_value.loc[max_value['mc'].idxmax()]
        def conditions(profits_list):
            if (profits_list['mc'] <= 0):
                x = (0*weight)*100
            if (profits_list['mc'] > 0):
                x = (profits_list['mc']/max_value)*weight*100
            return x
        
        profits_list['profits_final'] = profits_list.apply(conditions, axis=1)


        return profits_list
    except Exception as e:
        print(str(e))
        sys.exit() 

def payment_discipline_attribute(query_sql_df):
    try:
   
        weight = 0.2
        sql_call_client_list = "select * from sld_payment_discipline"
        payment_discipline_list = query_sql_df(sql_call_client_list,())
        payment_discipline_list['value_discipline'] = payment_discipline_list['value_discipline'].fillna(5)
        payment_discipline_list['value_discipline'] = payment_discipline_list['value_discipline'].astype(float)
        payment_discipline_list['payment_discipline_final'] = payment_discipline_list['value_discipline']*weight*(100/5)

        return payment_discipline_list
    except Exception as e:
        print(str(e))
        sys.exit() 

def fidelity_attribute(query_sql_df,get_clients_df):
    try:
        
        weight = 0.1
        sql_call_client_list = "select * from sld_fidelity"
        fidelity_list = query_sql_df(sql_call_client_list,())
        fidelity_list = pd.merge(get_clients_df['Cliente'],fidelity_list,on="Cliente",how="left")
        fidelity_list['fidelity_value'] = fidelity_list['fidelity_value'].fillna("NO")
        fidelity_list['update_date_fidelity'] = fidelity_list['update_date_fidelity'].fillna(fidelity_list['update_date_fidelity'][0])
        
        
        def conditions(fidelity_list):
            if (fidelity_list['fidelity_value'] == "SI"):
                x = (weight)*100
            else:
                x = 0
            return x
        
        fidelity_list['fidelity_final'] = fidelity_list.apply(conditions, axis=1)


        return fidelity_list
    except Exception as e:
        print(str(e))
        sys.exit() 

def cancelations_attribute(cluster,query_sql_df,get_clients_df):
    try:
        
        weight = 0.1
        sql_call_client_list = "{CALL sld_cancelations (?)}"
        profits_list = query_sql_df(sql_call_client_list,(cluster))
        profits_list = pd.merge(get_clients_df['Cliente'],profits_list,on="Cliente",how="left")
        profits_list['vol_cancelado'] = profits_list['vol_cancelado'].fillna(0)
        profits_list['vol_cancelado'] = profits_list['vol_cancelado'].astype(float)
        profits_list = profits_list.sort_values(by=["vol_cancelado"], ascending=[False])
        max_value = pd.DataFrame()
        max_value['vol_cancelado'] = profits_list['vol_cancelado']
        max_value = max_value.loc[max_value['vol_cancelado'].idxmax()]
        def conditions(profits_list):
            if (profits_list['vol_cancelado'] <= 0):
                x = weight*100
            if (profits_list['vol_cancelado'] > 0):
                x = (1-(profits_list['vol_cancelado']/max_value))*weight*100
            return x
        
        profits_list['cancelations_final'] = profits_list.apply(conditions, axis=1)


        return profits_list
    except Exception as e:
        print(str(e))
        sys.exit() 
