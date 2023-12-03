import shlex
from abc import ABC, abstractmethod
from Optima import *



class CommandManager:
    def __init__(self, bot_instance, address_book, notes) -> None:
        self.bot_instance = bot_instance
        self.address_book = address_book
        self.notes = notes
        self.commands_dict = {}
        self.__initialize_commands()

    def __initialize_commands(self):
        all_commands = self.__get_commands(Command)
        self.commands_dict = {cc._command_name:cc for cc in all_commands}

    def __get_commands(self, command_class: type) -> list:
        all_commands = []
        for command in command_class.__subclasses__():
            if command._command_name:
                all_commands.append(command)
            all_commands.extend(self.__get_commands(command))
        return all_commands
    
    def execute_command(self, user_input: str):
        try:
            command_class, args = self.__find_command_class(user_input)
            command = self.__create(command_class, *args)
            command.execute()
        except IndexError:
            params = [f"[{arg}]" for arg in command_class._expected_args]                                                                       
            self.bot_instance.output(f"Please enter command in the format:    command {' '.join(params)}   or use help.")
        except KeyError:
            self.bot_instance.output(f"The record for contact {args[0]} not found. Try another contact or use help.")
        except ValueError as error:
            if error.args:
                self.bot_instance.output(error.args[0])           
        except DuplicatedPhoneError as phone_error:
            self.bot_instance.output(f"Phone number {phone_error.args[1]} already exists for contact {phone_error.args[0]}.")
        except AttributeError:
            self.bot_instance.output(f"Contact {args[0]} doesn't have birthday yet.")

    def __find_command_class(self, user_input) -> tuple:
        for command_name, command_class in self.commands_dict.items():
            if user_input.lower().startswith(command_name):
                args = shlex.split(user_input[len(command_name):], posix=False)
                args = [arg.removeprefix('"').removesuffix('"') for arg in args]
                return command_class, args            
            
    def __create(self, command_class: type, *args): # -> Command:        
        if issubclass(command_class, AddressBookCommands):
            ...
        else:
            command = command_class(None, self.bot_instance, *args)
        return command
        

    # copy = function() {executeCommand(
    #         new CopyCommand(this, activeEditor)) }
    #     copyButton.setCommand(copy)
    #     shortcuts.onKeyPress("Ctrl+C", copy)

class Command(ABC):
    _command_name = ""
    _expected_args = []

    @abstractmethod
    def __init__(self, receiver, bot_instance) -> None:
        self._receiver = receiver
        self.bot_instance = bot_instance

    
    def execute(self) -> None:
        self.bot_instance.output(self._do_execute())

    @abstractmethod
    def _do_execute(self) -> str:
        pass

class AddressBookCommands(Command):
    ...

class NotesCommands(Command):
    ...


class GreetingCommand(Command):
    _command_name = "hello"

    def __init__(self, receiver, bot_instance, *args) -> None:
        super().__init__(receiver, bot_instance, *args)
        

    def _do_execute(self) -> str:
        greeting = "How can I help you?"
        return greeting


class SorterCommand(Command):
    ...

class HelpCommand(Command):
    ...

class ExitCommand(Command):
    ...


class AddContactCommand(AddressBookCommands):
    def execute(self, *args):
        user_name = args[0]
        user_phones = args[1:]
        record = self.records.find(user_name, True)
        if not record:
            record = Record(user_name)
            for user_phone in user_phones:
                record.add_phone(user_phone)
            self.records.add_record(record)
            if user_phones:
                return f"New record added for {user_name} with phone number{'s' if len(user_phones) > 1 else ''}: {'; '.join(user_phones)}."
            return f"New record added for {user_name}."
        else:
            response = []
            for user_phone in user_phones:
                record.add_phone(user_phone)
                response.append(f"New phone number {user_phone} for contact {user_name} added.")
            return "\n".join(response)

class DeleteContactCommand(AddressBookCommands):
    ...

class EditContactCommand(AddressBookCommands): 
    ...

class PhoneCommand(AddressBookCommands):
    ...

class AddressCommand(AddressBookCommands):
    ...

class BirthdayCommand(AddressBookCommands):
    ...

class EmailCommand(AddressBookCommands):
    ...

class SearchContactsCommand(AddressBookCommands):
    ...

class ShowContactsCommand(AddressBookCommands):
    ...

class ShowBirthdaysCommand(AddressBookCommands):
    ...

class AddNoteCommand(NotesCommands):
    ...

class DeleteNoteCommand(NotesCommands):
    ...

class EditNoteCommand(NotesCommands):
    ...

class SearchNoteCommand(NotesCommands):
    ...

class ShowNotesCommand(NotesCommands):
    ...

class SortNotesByTagCommand(NotesCommands):
    ...

