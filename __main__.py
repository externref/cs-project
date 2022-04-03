from source.user import User
from source.database import setup
from source.menu import start_menu

username: str = input("Enter your name here: ")
database = setup()
user = User(username)
start_menu(user, database)
