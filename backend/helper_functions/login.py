import snowflake.connector
from snowflake.connector import DictCursor, ProgrammingError

conn = snowflake.connector.connect(
    user='SANJAYKASHYAP',
    password='Bigdata@23',
    account='iogoldm-vcb38713',
    warehouse='COMPUTE_WH',
    database='SEVIR_META',
    schema='PUBLIC'
)

#Hash the Password

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
        
    # finally:
    #     # Close the Snowflake connection
    #     conn.close()


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
            x = cursor.fetchall()
            # print(x)
            users_dict = dict()
            for i in x:
                users_dict[i['USERNAME']] = i
            if len(users_dict) > 0:
                return True
            else:
                raise Exception(False)
    except Exception as e:
        return e


# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }

    # finally:
    #     # Close the Snowflake connection
    #     conn.close()
    

# create_user("Snehil Aryan", "snehilaryan", "gold", "$2b$12$zyCSnwElE02MGbgd8hXdV.j77tIbE/muGYtFl/2B4z.UqRYwU0Vue") #(full_name, username, tier, hashed_password)
# create_user("John Wick", "johnwick@gmail.com", "free", "$2b$12$zyCSnwElE02MGbgd8hXdV.j77tIbE/muGYtFl/2B4z.UqRYwU0Vue") 

# x = get_users()

# print(x)

# for i in x:
#     users_dict[i['USERNAME']] = i
# print(users_dict)

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }

#Run all the functions
if __name__ == "__main__":
    print(check_user_exists("midhun"))
