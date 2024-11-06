from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client, Client
import streamlit as st

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@st.cache_data(ttl=3600)
def fetch_grocery_data(_supabase):
    """
    Fetches data from category_subcategory_view and item_subcategory_view from Supabase and saves it to cat_subcat and subcat_item lists respectively.

    Args:
      supabase (Client): The Supabase client object.
    """
    try:
        # Fetch data from category_subcategory_view
        data = supabase.table("complete_view").select("*").execute()
        

        return data.data
        
    except Exception as e:
        print(f"Error accessing Supabase: {e}")
        return None, None

def main():
    """
    Fetches data from Supabase views and displays it in a Streamlit app.
    """
    st.title("G R O C E R Y - A P P")

    # Initialize cart in session state if it doesn't exist
    if 'cart' not in st.session_state:
        st.session_state.cart = {}



    grocery_data = fetch_grocery_data(supabase)

    if grocery_data:
        category_data = {}
        for row in grocery_data:
            category_name = row['category_name']
            subcategory_name = row['subcategory_name']
            item_name = row['item_name']
            if category_name not in category_data:
                category_data[category_name] = {}
            if subcategory_name not in category_data[category_name]:
                category_data[category_name][subcategory_name] = []
            category_data[category_name][subcategory_name].append(item_name)

        # Get list of categories
        categories = list(category_data.keys())

        # Sidebar menu
        choice = st.sidebar.selectbox("Menu", categories)

        if choice:
            with st.form(key=f"grocery_form_{choice}"):
                st.subheader(choice)  # Display the selected category
                st.write("")  # Add some spacing
                subcategories = category_data[choice]
                cols = st.columns(len(subcategories))  # Create columns for subcategories

                for i, subcategory in enumerate(subcategories):
                    with cols[i]:
                        if i % 2 == 0:
                            st.markdown(
                                f'<div style="background-color: lightgray; padding: 10px; border-radius: 5px;">{subcategory}</div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f'<div style="background-color: darkgrey; padding: 10px; border-radius: 5px;">{subcategory}</div>',
                                unsafe_allow_html=True,
                            )
                        st.write("")  # Add spacing between subcategories
                        items = subcategories[subcategory]
                        for item in items:
                            # Use st.checkbox for each item and store state in the cart
                            checked = st.checkbox(item, key=f"{choice}-{subcategory}-{item}")
                            if checked:
                                if choice not in st.session_state.cart:
                                    st.session_state.cart[choice] = {}
                                if subcategory not in st.session_state.cart[choice]:
                                    st.session_state.cart[choice][subcategory] = []
                                st.session_state.cart[choice][subcategory].append(item)
                            else:  # Remove from cart if unchecked
                                if choice in st.session_state.cart and \
                                subcategory in st.session_state.cart[choice] and \
                                item in st.session_state.cart[choice][subcategory]:
                                    st.session_state.cart[choice][subcategory].remove(item)
                submitted = st.form_submit_button("Add to Cart")
    # Display the cart
    st.subheader("Cart")
    
    if st.session_state.cart:
        for category, subcategories in st.session_state.cart.items():
            st.write(f"**{category}**")  # Display the category
            for subcategory, items in subcategories.items():
                st.write(f"***{subcategory}***")  # Display the subcategory
                for item in items:
                    st.write(f"    - {item}")  # Display the item
    else:
        st.write("Your cart is empty.")

       
if __name__ == "__main__":
    main()