import os
import shlex
from pathlib import Path
from abc import ABC, abstractmethod
from Optima import *

class BotUIBase(ABC):

    root_path: Path = None
    records: AddressBook = None
    notes_list: NotesList = None
    help_txt: str = ""

    @abstractmethod
    def _output(self, data) -> None:
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def _initialize(self):
        pass

    def input_error(*expected_args):
        def input_error_wrapper(func):
            def inner(self, *args):
                try:
                    return func(self, *args)
                except IndexError:
                    params = [f"[{arg}]" for arg in expected_args]                                                                       
                    return f"Please enter command in the format:    command {' '.join(params)}   or use help."
                except KeyError:
                    return f"The record for contact {args[0]} not found. Try another contact or use help."
                except ValueError as error:
                    if error.args:
                        return error.args[0]
                    return f"Phone format '{args[1]}' is incorrect. Use digits only for phone number."
                except DuplicatedPhoneError as phone_error:
                    return f"Phone number {phone_error.args[1]} already exists for contact {phone_error.args[0]}."
                except AttributeError:
                    return f"Contact {args[0]} doesn't have birthday yet."
            return inner
        return input_error_wrapper

    def capitalize_user_name(func):
        def inner(self, *args):
            new_args = list(args)
            if new_args:
                new_args[0] = new_args[0].title()
            return func(self, *new_args)
        return inner
    
    def output_result(func): # TEMPORARY before refactoring
        def inner(self, *args):
            result = func(self, *args)
            if not result:
                return result
            self._output(result)
        return inner

    @output_result
    def unknown_handler(self, *args):    
        list_of_commands = [v for _, v in self.COMMANDS.items()] + list(self.EXIT_COMMANDS)
        suggested_command = get_command(list(args), list_of_commands)
        if suggested_command:
            func, new_args = self.parser(suggested_command)
            return func (self, *new_args)
        return f"Unknown command. Use 'help' command"    

    @output_result
    def help_handler(self, *args):
        if not self.help_txt:
            file_path = Path(__file__).parent.joinpath("help.txt")
            with open(str(file_path)) as file:            
                self.help_txt = "".join(file.readlines())
        return self.help_txt
     

    @output_result
    @input_error([])
    def greeting_handler(self, *args):
        greeting = "How can I help you?"
        return greeting

    @output_result
    @capitalize_user_name
    @input_error("name", "phone")
    def add_contact_handler(self, *args):
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

    @output_result
    @capitalize_user_name    
    @input_error("name")
    def delete_contact_handler(self, *args):
        user_name = args[0]
        user_phones = args[1:]
        if len(user_phones) >= 1:
            record = self.records.find(user_name)
            if record:
                response = []
                for user_phone in user_phones:
                    record.remove_phone(user_phone)
                    response.append(f"Phone number {user_phone} for contact {user_name} removed.")
                return "\n".join(response)
        else:
            if self.records.delete(user_name):
                return f"Record for contact {user_name} deleted."
            return f"Record for contact {user_name} not found."

    @output_result
    @capitalize_user_name
    @input_error("name", "old_phone", "new_phone")
    def edit_contact_handler(self, *args):
        user_name = args[0]
        old_phone = args[1]
        new_phone = args[2]
        record = self.records.find(user_name)
        if record:
            record.edit_phone(old_phone, new_phone)
            return f"Phone number for {user_name} changed from {old_phone} to {new_phone}."

    @output_result
    @capitalize_user_name
    @input_error("name")
    def phone_handler(self, *args):
        user_name = args[0]
        record = self.records.find(user_name)
        if record:
            return "; ".join(p.value for p in record.phones)

    @output_result
    @capitalize_user_name    
    @input_error("name", "address")        
    def address_handler(self, *args):
        user_name = args[0]
        user_address = args[1] if len(args) > 1 else None
        record = self.records.find(user_name)
        if record:
            if user_address:
                record.add_address(user_address)
                return f"Address '{user_address}' for contact {user_name} added."
            else:
                return f"Address for contact {user_name}: {record.address}."

    @output_result            
    @capitalize_user_name    
    @input_error("name", "DD-MM-YYYY")
    def birthday_handler(self, *args):
        user_name = args[0]
        user_birthday = args[1] if len(args) > 1 else None
        record = self.records.find(user_name)
        if record:
            if user_birthday:
                record.add_birthday(user_birthday)
                return f"Birthday {user_birthday} for contact {user_name} added."
            else:
                return f"{record.days_to_birthday()} days to the next {user_name}'s birthday ({record.birthday})."

    @output_result            
    @capitalize_user_name    
    @input_error("name", "email")        
    def email_handler(self, *args):
        user_name = args[0]
        user_email = args[1] if len(args) > 1 else None
        record = self.records.find(user_name)
        if record:
            if user_email:
                record.add_email(user_email)
                return f"Email '{user_email}' for contact {user_name} added."
            else:
                return f"Email for contact {user_name}: {record.email}."

    @output_result            
    @input_error("query")
    def search_contacts_handler(self, *args):
        query: str = args[0]
        contacts = self.records.search_contacts(query)
        if contacts:
            return "\n".join(str(contact) for contact in contacts)
        return f"No contacts found for '{query}'."

    @output_result
    @input_error([])
    def show_contacts_handler(self, *args):
        print("{:<10} {:<40} {:<35} {:<15} {:<60}".format("name", "phones", "email", "birthday", "address"))
        return self.records.iterator()

    @output_result
    @input_error("days")
    def show_birthdays_handler(self, *args):
        days = int(args[0])
        contacts = self.records.contacts_upcoming_birthdays(days)
        if contacts:
            return "\n".join(str(contact) for contact in contacts)
        return f"No contacts have birthday within following {days} days."

    @output_result
    @input_error("title", "text")    
    def add_note_handler(self, *args):
        note_title = args[0] if len(args) > 1 else "Untitled"
        note_text = args[1] if len(args) > 1 else args[0]
        note = Note(note_title, note_text)
        self.notes_list.append(note)
        return f"New note with title '{note_title}' and text '{note_text}' added."

    @output_result
    @input_error("title or number")
    def delete_note_handler(self, *args):
        param = " ".join(args)
        if self.notes_list.remove(param):
            return "Note deleted successfully."
        else:
            return "Note with this title not found."

    @output_result
    @input_error("old title or number", "new title", "new text")
    def edit_note_handler(self, *args):
        param, new_title, new_text = args[0], args[1], args[2]
        if self.notes_list.edit(param, new_title, new_text):
            return f"Note '{param}' edited successfully."
        else:
            return f"No notes found by the specified param '{param}'."

    @output_result        
    @input_error("query")
    def search_notes_handler(self, *args):
        query = args[0]
        matches = self.notes_list.search(query)
        if matches:
            return "\n".join(map(lambda note: str(note), matches))
        else:
            return f"No notes found for query '{query}'."

    @output_result
    @input_error("tag")
    def search_notes_by_tag_handler(self, *args):
        tag = args[0]
        matches = self.notes_list.search_by_tag(tag)
        if matches:
            return "\n".join(map(lambda note: str(note), matches))
        else:
            return f"No notes found with tag '{tag}'."

    @output_result
    def show_notes_handler(self, *args):
        return "\n".join(self.notes_list.output_notes())

    @output_result
    def sort_notes_by_tag_count_handler(self):
        sorted_notes = self.notes_list.sort_by_tag_count()
        if sorted_notes:
            return "\n".join(map(lambda note: str(note), sorted_notes))
        else:
            return "No notes to sort."

    @output_result
    @input_error("path")
    def sort_files_handler(self, *args):
        folder_path = args[0]
        result = sort_folders_and_return_result(folder_path, self.root_path)
        return result

    COMMANDS = {
                help_handler: "help",
                greeting_handler: "hello",                        
                add_contact_handler: "add contact",
                delete_contact_handler: "delete contact",
                edit_contact_handler: "edit contact",
                phone_handler: "phone",
                address_handler: "address",            
                birthday_handler: "birthday",
                email_handler: "email",            
                search_contacts_handler: "search contacts",
                show_contacts_handler: "show contacts",            
                show_birthdays_handler: "show birthdays",            
                add_note_handler: "add note",
                delete_note_handler: "delete note",
                edit_note_handler: "edit note",
                search_notes_by_tag_handler: "search note tag",
                search_notes_handler: "search note",
                show_notes_handler: "show notes",            
                sort_notes_by_tag_count_handler: "sort tag",
                sort_files_handler: "sort files"
                }
    EXIT_COMMANDS = {"good bye", "close", "exit", "stop"}

    def parser(self, text: str):
        for func, kw in self.COMMANDS.items():
            if text.lower().startswith(kw):
                args = shlex.split(text[len(kw):], posix=False)
                args = [arg.removeprefix('"').removesuffix('"') for arg in args]
                return func, args
        return BotUIBase.unknown_handler, shlex.split(text, posix=False)


class BotCLI(BotUIBase):
    
    def __init__(self) -> None:
        self._initialize()

    def _initialize(self):
        self.root_path = Path(os.path.expanduser("~")).joinpath("OPTIMA")
        if not self.root_path.exists():
            self.root_path.mkdir()

    def start(self):
        self.notes_list = NotesList(self.root_path)        
        with AddressBook(str(self.root_path.joinpath("address_book.bin"))) as book:
            os.system('cls' if os.name == 'nt' else 'clear')    
            print("\33[92m" + f"Wake up {os.getlogin().title()}...")
            print("The OPTIMA has you...")
            print("Follow the 'help' command.")

            self.records = book
            while True:
                user_input = input(">>> ")

                if user_input in self.EXIT_COMMANDS:
                    print("Good bye!")
                    break
                
                func, data = self.parser(user_input)
                        
                func(self, *data)

            print ("\033[0m")

    def _output(self, data) -> None:       
        if isinstance(data, str):
            print(data)
        else:
            for i in data:                
                print("\n".join(i))
                input("Press enter to show more records")
    

class BotWebUI(BotUIBase):
    ...

class BotGUI(BotUIBase):
    ...