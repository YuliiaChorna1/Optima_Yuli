# Optima
Developed by ICT (In Code we Trust) team.


## Description 
Optima is a command-line assistant that allows you to store,
                      edit, search, and manage notes and contacts.
                      It features a convenient interface and easy integration with your system.
                      Developed by Yulia Chorna, Valentyn Tonkonig, Anastasia Makarova,
                      Ryslan Shypka, Vita Filimonikhina, Roman Synyshyn.



## Installation

To install the package locally, navigate to the root directory (where setup.py is located) and execute the command:
pip install .
After installing the package, you can run your program from anywhere in the system using the command optima.
```bash
pip install .
```

## Usage

```bash
# After installing the package locally
# start program
optima
```

```bash
# To view the list of commands, use the command:
>>> help
```

```bash
# To exit the program, use either of the following commands:
>>> good bye
>>> close
>>> exit
>>> stop
```

## Supported bot commands

|  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp; Command  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp;  &nbsp; | Description |
|---------|-------------|
| **Address book commands** |
| **add contact** [name] [phone-1] [phone-2] ... [phone-n] | Adds new contact record with name and phone number/numbers |
| **delete contact** [name] | Deletes contact by name |
| **delete contact** [name] [phone-1] [phone-2] ... [phone-n] | Deletes phone numbers for contact |
| **edit contact** [name] [old phone] [new phone] | Changes phone number for contact |
| **phone** [name] | Shows phone numbers for contact |
| **address** [name] | Shows contact's address |
| **address** [name] ["address"] | Adds address for contact. Wrap address with double quotes |
| **birthday** [name] | Shows number of days till the contact's next birthday |
| **birthday** [name] [date] | Adds birthday for contact. Format for date: DD-MM-YYYY |
| **email** [name] | Shows contact's email |
| **email** [name] [email] | Adds email for contact. Format for email: example@email.com |
| **search contacts** [query] | Searches for contacts by partial match of name or phone  |
| **show contacts** | Prints all contacts info with pagination |
| **show birthdays** [days] | Prints contacts having birthday within following number of days |
| **Notes commands** |
| **add note** ["title"] ["text"] | Adds a new note with a title and text. Wrap title and text with double quotes |
| **delete note** ["title"] | Deletes the note with the specified title. Wrap title and text with double quotes |
| **delete note** [number] | Deletes the note with the specified number. Hint: use 'show notes' to see numbers |
| **edit note** ["old title"] ["new title"] ["new text"] | Edits a note by its old title, changing it to a new title and text. Wrap titles and text with double quotes |
| **edit note** [number] ["new title"] ["new text"] | Edits a note by its number, changing it to a new title and text. Hint: use 'show notes' to see numbers |
| **search note** ["query"] | Searches for notes by a query in the text or title. Wrap query with double quotes |
| **search note tag** [tag] | Searches for notes by a tag |
| **show notes** | Prints all saved notes in a table format |
| **sort tag** | Sorts notes by the number of tags from the most to the least |
| **Exit commands** |
| **sort files** [path] | Sorts files in the target folder by type, unpacks archives, deletes empty folders. Saves result of sorting to the report file |
| **good bye, close, exit, stop** | Stops work and exits bot


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
