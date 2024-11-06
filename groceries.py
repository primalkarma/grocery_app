from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client, Client
import streamlit as st

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@st.cache_data(ttl=3600)
def fetch_and_save_views(_supabase):
    """
    Fetches data from category_subcategory_view and item_subcategory_view from Supabase and saves it to cat_subcat and subcat_item lists respectively.

    Args:
      supabase (Client): The Supabase client object.
    """
    
    try:
        # Fetch data from category_subcategory_view
        cat_subcat_data = supabase.table("category_subcategory_view").select("*").execute()
        cat_subcat = cat_subcat_data.data

        # Fetch data from item_subcategory_view
        subcat_item_data = supabase.table("item_subcategory_view").select("*").execute()
        subcat_item = subcat_item_data.data

        return cat_subcat, subcat_item
    except Exception as e:
        print(f"Error accessing Supabase: {e}")
        return None, None

def main():
    """
    Fetches data from Supabase views and displays it in a Streamlit app.
    """
    st.title("G R O C E R Y - A P P")

    cat_subcat_data, subcat_item_data = fetch_and_save_views(supabase)

    if cat_subcat_data and subcat_item_data:

        # Group subcategories by category
        category_subcategories = {}
        for row in cat_subcat_data:
            category_name = row['category_name']
            subcategory_name = row['subcategory_name']
            if category_name not in category_subcategories:
                category_subcategories[category_name] = []
            category_subcategories[category_name].append(subcategory_name)

        # Get list of categories
        categories = list(category_subcategories.keys())

        # Sidebar menu
        choice = st.sidebar.selectbox("Menu", categories)

        if choice:
            st.subheader(choice)
            st.write("")
            subcategories = category_subcategories[choice]
            cols = st.columns(len(subcategories))
            for i, subcategory in enumerate(subcategories):
                with cols[i]:
                    if i % 2 == 0:
                        st.markdown(f'<div style="background-color: lightgray; padding: 10px; border-radius: 5px;">{subcategory}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="background-color: darkgrey; padding: 10px; border-radius: 5px;">{subcategory}</div>', unsafe_allow_html=True)
                    st.write("")
                    items = [item['item_name'] for item in subcat_item_data 
                             if item['subcategory_name'] == subcategory]
                    for item in items:
                        st.markdown(f"- {item}")
        st.title("")
        st.title("")
        st.write(category_subcategories)
if __name__ == "__main__":
    main()