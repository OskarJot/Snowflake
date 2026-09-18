# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

import requests  

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Safe session binding for Streamlit Cloud & SiS
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except Exception:
    conn = st.connection("snowflake")
    session = conn.session()

# Fetch fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Convert Snowpark DataFrame column to a standard Python list
fruit_options_list = [row['FRUIT_NAME'] for row in my_dataframe.collect()]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:", 
    fruit_options_list,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button('Submit: Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


