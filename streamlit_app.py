# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose your fruit!
  """
)

name_on_order = st.text_input("Name on smoothie")
st.write("The name on your smoothie will be",name_on_order )

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df = my_dataframe.to_pandas()
st.datframe(pd_df)
st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients', my_dataframe)
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ''
    for fruit_selected in ingredients_list:
        ingredients_string+=fruit_selected+' '
        st.subheader(fruit_selected + ' Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_selected)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered,{name_on_order}!', icon="✅")



        
