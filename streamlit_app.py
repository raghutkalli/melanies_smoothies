# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("Customize Your Smoothie!")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)

# Initialize session
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Convert to a list for multiselect
fruit_options = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,  # Ensure this line is correct
    max_selections=5  # Make sure 'max_selections' is correct, but the parameter is 'max_items'
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                        VALUES (%s, %s)"""

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt, (ingredients_string, name_on_order)).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
