import streamlit as st
import sqlite3
import requests

# Create a database connection

"st.session_state object:" , st.session_state
host_url = "http://127.0.0.1:8501"
host_url_api = "http://3.22.188.56:8000"
def add_to_session_state(new, value):
        st.session_state[new] = value
        
        
# Define a function to check if the user is authorized
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
    


# Define the Streamlit app
def app():
    # Add a cover image
    st.title('GoesNex')
    st.header("Data as a Service")
    #st.image("images/cover.png", width=500)

    # Add a login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        
        st.write(is_authorized(username, password))
        
        if is_authorized(username, password):
            st.success("Logged in as {}".format(username))
            
            # Open the link in a new tab
            #st.markdown(f'<meta http-equiv="refresh" content="0; url={host_url}"/HOME.py>', unsafe_allow_html=True)
        else:
            st.error("Invalid username or password")

    # Add a register form
#     register_option = st.selectbox("Don't have an account?", ["Select an option", "Register here"])
#     if register_option == "Register here":
#         new_username = st.text_input("New username")
#         new_password = st.text_input("New password", type="password")
#         confirm_password = st.text_input("Confirm password", type="password")
#         if st.button("Register"):
#             if new_username and new_password and confirm_password:
#                 if new_password == confirm_password:
#                     # Check if the username is already taken
#                     c.execute("SELECT * FROM users WHERE username=?", (new_username,))
#                     if c.fetchone():
#                         st.error("Username already taken")
#                     else:
#                         # Add the new user to the database
#                         c.execute("INSERT INTO users VALUES (?, ?)", (new_username, new_password))
#                         conn.commit()
#                         st.success("User created")
#                 else:
#                     st.error("Passwords don't match")
#             else:
#                 st.error("Please fill in all fields")

# # Call the Streamlit app
app()
