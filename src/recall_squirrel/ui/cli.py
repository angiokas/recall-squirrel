import cmd
from .console import *
from recall_squirrel.db.db_operations import create_flashcard, get_all_flashcards

class AppShell(cmd.Cmd):
    intro = print_command("Welcome to my app! Here are some commands:\n- hello (prints hello)", "success")
    prompt = "🐿️> "

    def do_hello(self, arg):
        print_command("Hello!!", "success")

    def do_new_flashcard(self,arg):
        f_question = input("Enter the flashcard question: ")
        f_answer = input("Enter the flashcard answer: ")
        studyset_name = input("Enter the study set name (or press Enter to skip): ")
        create_flashcard(f_question, f_answer, studyset_name if studyset_name else None)

    def do_list_flashcards(self, arg):
        get_all_flashcards()

    def do_exit(self, arg):
        print_command("Goodbye! Exiting the app.", "error")
        return True
    