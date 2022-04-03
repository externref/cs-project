from __future__ import annotations

from simple_term_menu import TerminalMenu

from colorama import Fore, Style

from .database import Database
from .user import User

_correct = Fore.GREEN
_wrong = Fore.RED
_fix = Fore.RESET, Style.RESET_ALL
_input = Fore.CYAN


def start_menu(user: User, connection: Database) -> None:
    option = TerminalMenu(
        ["About", "Start Quiz.", "Login as Admin.", "Add questions.", "END."]
    ).show()
    if option == 0:
        ...
    if option == 1:
        ask_questions(user, connection)
        start_menu(user, connection)
    if option == 2:
        user.login()
        start_menu(user, connection)
    if option == 3:
        add_question(user, connection)
        start_menu(user, connection)
    if option == 4:
        exit()


def ask_questions(
    user: User,
    connection: Database,
) -> None:
    questions: list(tuple) = connection.get_questions()
    for question in questions:
        print(Fore.LIGHTYELLOW_EX, Style.BRIGHT, "Question: ", question[0])
        for option in enumerate(question[1:-1], start=1):
            print(
                Fore.LIGHTGREEN_EX,
                Style.NORMAL,
                "Option {}: {}".format(option[0], option[1]),
            )
        print(_input)
        answer = int(input("Enter your answer: "))
        if answer == question[-1]:
            print(_correct, "Correct!", *_fix)
            user.correct += 1
        else:
            print(_wrong, "Wrong!")
            print("The correct answer is: ", question[-1], *_fix)
            user.wrong += 1
    print("You have {} correct and {} wrong answer(s)".format(user.correct, user.wrong))
    user.wrong = 0
    user.correct = 0
    start_menu(user, connection)


def add_question(user: User, connection: Database) -> None:
    if user.is_admin:
        connection.add_question(
            input("Enter the question: "),
            input("Enter option 1: "),
            input("Enter option 2: "),
            input("Enter option 3: "),
            input("Enter option 4: "),
            int(input("Enter the correct option: ")),
        )
