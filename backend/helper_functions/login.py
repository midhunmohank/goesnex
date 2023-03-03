import snowflake.connector
from snowflake.connector import DictCursor, ProgrammingError



# Connect to Snowflake using environment variables
conn = snowflake.connector.connect(
    user='SANJAYKASHYAP',
    password='Bigdata@23',
    account='iogoldm-vcb38713',
    warehouse='COMPUTE_WH',
    database='SEVIR_META',
    schema='PUBLIC'
)

#Function to Create User
def create_user(full_name, username, tier, hashed_password):
    # Set up connection to Snowflake
    try:
        # Create a cursor object using the DictCursor to work with dictionaries
        with conn.cursor(DictCursor) as cursor:
            # Execute the INSERT statement to add the new user to the table
            cursor.execute(
                "INSERT INTO users (full_name, username, tier, hashed_password, created_at) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP())",
                (full_name, username, tier, hashed_password)
            )
            
            # Commit the transaction
            conn.commit()
            
            # Return the ID of the new user
            return 1
            
    except ProgrammingError as e:
        print(f"Error: {e.msg}")
        


def get_users():
    
    try:
        # Create a cursor object using the DictCursor to work with dictionaries
        with conn.cursor(DictCursor) as cursor:
    
            cursor.execute(f"select  username, full_name, username, tier, hashed_password, disabled from users")
            x = cursor.fetchall()
            # print(x)
            users_dict = dict()
            for i in x:
                users_dict[i['USERNAME']] = i

            return users_dict
            
    except ProgrammingError as e:
        print(f"Error: {e.msg}")
        

#Check if user exists
def check_user_exists(username):
    try:
        # Create a cursor object using the DictCursor to work with dictionaries
        with conn.cursor(DictCursor) as cursor:
            cursor.execute(f"select  username, full_name, username, tier, hashed_password, disabled from users where username = '{username}'")
            users_dict = cursor.fetchall()[0]
            # users_dict = dict()
            # print(users_dict)
            if users_dict['USERNAME'] == username:
                return True
            else:
                raise Exception(False)
    except Exception as e:
        return e


#Run all the functions
if __name__ == "__main__":

    # print(check_user_exists("midhun"))
    print(get_users())
