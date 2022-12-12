from fastapi import FastAPI
from pydantic import BaseModel
from deta import Deta
import os
from os.path import join, dirname
from dotenv import load_dotenv
from typing import Optional



# accesing the project key
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
PROJECT_KEY = os.environ.get("PROJECT_KEY")

# app isntance creation
app = FastAPI()


# detabase set up
deta = Deta(PROJECT_KEY)
user_account_db = deta.Base("User_account") # creating an database for user accounts




# base data model for hte User data
class User(BaseModel):
    first_name : str
    last_name : str
    age : int
    skicoin : float

class UpdateUser(BaseModel):
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    age : Optional[int] = None
    

#utility functions
def check_user_name_data(name):
    try :
        user_account_db.fetch({"user_name" : name})._items[0]
        return True
    except : return False













# setting up all the routes


# Get routes
@app.get("/")
def index_page():
    data = user_account_db.fetch()
    return {
        "status" : "welcome to the skicoin-base" ,
        "data" :data
    }


@app.get("/search-by-name/")
def search_by_name(first_val : str , last_val : str):
    '''
    first name and last name is required to ge the data
    '''
    data = user_account_db.fetch(
        {
            "first_name" : first_val.upper() ,
            "last_name" : last_val.upper()
        }
    )
    return data

@app.get("/search-by-age/")
def serach_by_age(age:int):
    '''
    fetch all the data regarding the age specified by the query 
    and also returns the data only greater than or equals to the age specified
    '''
    data = user_account_db.fetch(
        {
            "age?gte": age
        }
    )
    return data

@app.get("/search-by-skicoin/")
def search_by_skicoin(skicoin_val:float):
    '''
    quearry all the user who have more skicoin than skicoin_val
    '''
    data = user_account_db.fetch(
        {
            "skicoin?gt": skicoin_val
        }
    )
    return data

@app.get("/search-by-id/{user_id}")
def search_by_id(user_id : int):
    '''
        So here the fetch command requesting to retrive the diserd data but sometime when the user
        give the wrong data it will throw and status of data can not be founded
    '''
    try :
        data = user_account_db.fetch(
            {
                "id": user_id
            }
        )._items[0]
        return data
    except:
        return {
            "status" : "data can not be founded or confidential"
        }
    
@app.get("/search-by-username/{user_name}")
def search_by_username(user_name : str ):
    '''
    searching using the username provided for the user
    '''
    try :
        data = user_account_db.fetch({"user_name" : user_name})._items[0]
        return data
    except : return {
        "status" : "wrong username or confidential data"
    }



# Post routes
@app.post("/add-user")
def add_user(user_name : str ,user : User):

    '''
    It checks if the user name given to the end point already exists in the database, 
    if it exists then it will discard the request and return in username already exists 
    and if the user name dose not exists it will add the data and return the data as a json
    ''' 
    user_name_exists = check_user_name_data(user_name)
    
    if  user_name_exists:
        return {
            "status" : "action can not be completed",
            "Reason" : "Username already exists"
        }

    if not user_name_exists :
        user_account_db.put(
            {
                "user_name" : user_name,
                "id" : len(user_account_db.fetch()._items),
                "first_name" : user.first_name.upper(),
                "last_name" : user.last_name.upper(),
                "age" : user.age,
                "skicoin": user.skicoin
            }
        )
        return user





# updating existing user
@app.put("/update-user/{user_id}")
def update_user(user_id : int , user : UpdateUser):
    '''
    updates the user data using user_id
    '''
    try:
        update = {}
        user_key = user_account_db.fetch({"id" : user_id})._items[0]["key"]
        if user.first_name != None:
            update["first_name"] = user.first_name
        if user.last_name != None:
            update["last_name"] = user.last_name
        if user.age != None:
            update["age"] = user.age

        try: 
            res = user_account_db.update(updates=update , key=user_key)
            return {"status" : "user details updated"}
        except:
            return{"status" : "unscussesfull"}
    except:
        return {"Status" : "There is no User"}






# delete routes
@app.delete("/delete-user")
def delete_user(user_id : int):
    '''
    Delete any user by there specified id
    '''
    try:
        user_key = user_account_db.fetch({"id" : user_id})._items[0]["key"]
        response = user_account_db.delete(user_key)
        return {
            "response" : response,
            "status" : "user deleted"
        }
    except:
        return {
            "response" : "User can not be identified",
            "status" : "Error"
        }


