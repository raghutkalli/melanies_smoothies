# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.connector import connect
from snowflake.snowpark import Snowpark

# Replace with your Snowflake connection details
account = "YOMXSHP-JDB77382"
user = "RAGHUKALLI"
password = "Samhita@2011Bgm"
warehouse = "COMPUTE_WH"
database = "SMOOTHIES"
schema = "PUBLIC"

# Create a connection context
ctx = Snowpark.builder.configs(account=account, user=user, password=password, warehouse=warehouse, database=database, schema=schema).create()

# Create a Snowflake session from the context
session = ctx.cursor()

# Write directly to the app
st.title("Customize Your Smoothie!")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
'Choose up to 5 ingredients: '
, my_dataframe
, max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button("Submit Order")

#if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success(f'Your Smoothie is ordered,{name_on_order}!', icon="✅")
