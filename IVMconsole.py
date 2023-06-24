#!/usr/bin/python3
"""Defines the InventoryMaster console."""
import cmd
import re
from hashlib import md5
from shlex import split
from models import storage
from models.users_record_update import User
from models.base_model import Base, BaseModel

def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class IMSCommand(cmd.Cmd):
    """Defines the InventoryMaster command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(IMS)> "
    __classes = {
        "Inventory",
        "Users",
        "Sales"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Usage: create <class> <key 1>=<value 1> <key 2>=<value 2> ...
        Create a new class instance with given keys/values and print its id.
        """
        try:
            if not line:
                raise SyntaxError()

            # Split the line by spaces
            tokens = line.split()

            if len(tokens) < 2:
                raise SyntaxError()

            class_name = tokens[0]
            attr_value_pairs = tokens[1:]

            kwargs = {}
            for pair in attr_value_pairs:
                match = re.match(r"(\w+)=(.*)", pair)
                if match:
                    attr = match.group(1)
                    value = match.group(2)
                    if attr == "password":
                        value = md5(value.encode("utf-8")).hexdigest()
                    elif value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]  # Remove surrounding quotes
                    kwargs[attr] = value

            # Create the object and save it
            obj = eval(class_name)(**kwargs)
            storage.new(obj)
            storage.save()
            print(obj.id)
            print(kwargs)

        except SyntaxError:
            print("** Invalid syntax. Please provide class name and attribute-value pairs **")
        except NameError:
            print("** Class doesn't exist **")

if __name__ == "__main__":
     IMSCommand().cmdloop()
