import streamlit as st
import requests
from streamlit.hashing import _CodeHasher
import SessionState

# "st.session_state object:" , st.session_state
host_url = "http://127.0.0.1:8501"
host_url_api = "http://localhost:8000"

def add_to_session_state(new, value):
        st.session_state[new] = value
# Define the Streamlit app
def is_authorized(username, password):
    url_token = f"{host_url_api}/token"
    data = {'username': username, 'password': password}
    response_token = requests.post(url_token, data=data)
    print(response_token.json())
    if response_token.status_code == 200:
        add_to_session_state("access_token", response_token.json()["access_token"])
        return True
    else:
        return False
    
def app():
    api_host = 'http://127.0.0.1:8000'

    # Add a background color or image
    st.set_page_config(page_title="GoesNex", page_icon=":rocket:", layout="wide", initial_sidebar_state="expanded")
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f5f5f5;
            background-image: url('https://example.com/background.jpg');
            background-size: cover;
            font-family: Arial, sans-serif;
            font-size: 16px;
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add a logo or branding element
    st.image("https://example.com/logo.png", width=200)

    # Add a title and header
    st.title('GoesNex')
    st.header("Data as a Service")

    # Get the current login state from the session
    session_state = SessionState.get(logged_in=False)

    # Center the login form
    col1, _, col2 = st.columns([1, 2, 1])
    with col1:
        st.write("")
    with col2:
        st.subheader("Login")
        username = st.text_input("Username", key="username_input", placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="password_input", placeholder="Enter your password")
        if st.button("Sign In"):
            if is_authorized(username, password):
                session_state.logged_in = True
                st.success("Logged in as {}".format(username))
            else:
                st.error("Invalid username or password")

    # Center the registration form
    col1, _, col2 = st.columns([1, 2, 1])
    with col1:
        st.write("")
    with col2:
        st.subheader("Register")
        new_username = st.text_input("Username", key="new_username_input", placeholder="Choose a username")
        new_name = st.text_input("Full Name", key="new_name_input", placeholder="Enter your full name")
        new_password = st.text_input("Password", type="password", key="new_password_input", placeholder="Choose a password")
        service_plan = st.selectbox("Choose a service plan", ["Free", "Gold", "Platinum"], index=0, help="Select the service plan that best suits your needs")
        if st.button("Create Account"):
            payload = {
                "USERNAME": new_username,
                "FULL_NAME": new_name,
                "TIER": service_plan,
                "HASHED_PASSWORD": new_password,
                "DISABLED": False
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            response = requests.post(f"{api_host}/create_user/", json=payload, headers=headers)
            response = response.json()
            if response['status'] == True:
                st.success("Account created. You can now sign in.")
            else:
                st.error("This username is already taken")

    # Show the logout button in the sidebar if a user is logged in
    # Show the logout button in the sidebar if a user is logged in
    if session_state.logged_in:
        st.sidebar.subheader("User Options")
        st.sidebar.write("")
        if st.sidebar.button("Logout"):
            session_state.logged_in = False
            st.success("Logged out successfully.")

            # Clear the input fields
            st.session_state.pop("username_input", None)
            st.session_state.pop("password_input", None)
            st.session_state.pop("new_username_input", None)
            st.session_state.pop("new_name_input", None)
            st.session_state.pop("new_password_input", None)

    # Hide the logout button if no user is logged in
    else:
        st.sidebar.write("Please sign in to access user options.")

    # Add a footer with links or other information
    st.markdown(
        """
        <hr>
        &copy; 2023 GoesNex. All rights reserved.
        """
        , unsafe_allow_html=True
    )
