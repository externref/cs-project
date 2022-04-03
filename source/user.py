import json

import colorama

_ok = colorama.Fore.GREEN
_error = colorama.Fore.RED
_fix = colorama.Fore.RESET
_input = colorama.Fore.CYAN


class User:
    name: str
    is_admin: bool = True
    correct = 0
    wrong = 0

    def __init__(self, name: str) -> None:
        self.name = name

    def login(self) -> None:
        print(_input)
        passwd: str = input("Enter Admin Password: ")
        print(_fix)
        with open("configs.json", "r") as file:
            data = json.load(file)
        if passwd == data["password"].lower():
            self.is_admin = True
            print(_ok, f"Logged in as admin with user: {self.name}.", _fix)
            return True
        else:
            print(_error, "Wrong Password.", _fix)

    def logout(self) -> None:
        if not self.is_admin:
            return print(_error, "You didn't login.", _fix)
        self.is_admin = False
        print(_ok, f"Logged out from {self.name}'s admin account.", _fix)
