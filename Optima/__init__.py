from .Singleton import SingletonMeta
from .Address_book import AddressBook, Record, DuplicatedPhoneError
from .Notes import Note, NotesList
from .Folder_sorter import sort_folders_and_return_result
from .find_command import get_command
from .Commands import CommandManager
from .Bot import BotCLI, BotUIBase

__all__ = ['AddressBook', 'Record', 'DuplicatedPhoneError', 
           'Note', 'NotesList', 'sort_folders_and_return_result',
             'get_command', 'BotCLI', 'BotUIBase', 'SingletonMeta',
             'CommandManager']