import streamlit as st
import requests

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
    # print(response_token.json())
    if response_token.status_code == 200:
        add_to_session_state("access_token", response_token.json()["access_token"])
        return True
    else:
        return False
    

# Define the Streamlit app
def app():
    api_host = 'http://127.0.0.1:8000'
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
    register_option = st.selectbox("Don't have an account?", ["Select an option", "Register here"])
    if register_option == "Register here":

        new_username = st.text_input("New username", key="new_username_input")
        new_name = st.text_input("Full Name", key="new_name_input")
        new_password = st.text_input("New password", type="password", key="new_password_input")
        service_plan = st.selectbox("Choose a service plan", ["Free", "Gold", "Platinum"])
        if st.button("Register"):
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
            # responses = requests.post(, user={"USERNAME": new_username, "FULL_NAME":new_name,"tier": service_plan,"password": new_password,"DISABLED": False})
            response = response.json()
            if response['status'] == True:
                st.success("User created")
            else:
                st.error("This username is already taken")

    # Add a change password form
    change_password_option = st.selectbox("Change password?", ["Select an option", "Change password"])
    if change_password_option == "Change password":
        ch_old_password = st.text_input("Old password", type="password", key="old_pw_change_password")
        ch_new_password = st.text_input("New password", type="password", key="new_pw_change_password")
    if st.button("Change password"):
        payload = {
                    "USERNAME": username,
                    "HASHED_PASSWORD": ch_new_password,
                    "OLD_HASHED_PASSWORD": ch_old_password
                }
        
        headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
        
        response_ch = requests.post(f"{api_host}/update_user/", json=payload, headers=headers)
        response_ch = response_ch.json()
        print(response_ch)
        # if response['status'] == True:
        #     st.success(response['response'])
        # else:
        #     st.error("Invalid username or password")
        # if st.button("Change password"):
        #     if is_authorized(username, old_password):
        #         c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
        #         conn.commit()
        #         st.success("Password changed successfully")
        #     else:
        #         st.error("Invalid username or password")

    # Close the database connection


if __name__ == '__main__':
    app()