# Basic file encryption and decryption

Little project to play with file content encryption, made with PyQt5.

## Features

- File content encryption and decryption
- Custom encryption and decryption key
- Drag and drop files

## Run Locally

1. Install both:

   - [Python](https://www.python.org/downloads/) (3.6+)
   - [Poetry](https://github.com/python-poetry/poetry#installation)

1. Clone the project:

   ```bash
   git clone https://github.com/AloisCRR/basic-file-encryption-decryption.git
   ```

1. Go to the project directory:

   ```bash
   cd basic-file-encryption-decryption
   ```

1. Install dependencies:

   ```bash
   poetry install
   ```

1. Run the GUI:

   ```bash
   poetry run python encryption_ui/__init__.py
   ```

## Screenshots

![App Screenshot](https://i.imgur.com/ltBI5AL.png)

## Tech Stack

| Name                                      | Description                                                                                                                   |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [PyQt5](https://pypi.org/project/PyQt5/)  | Set of C++ libraries and development tools that include platform-independent abstractions for Graphical User Interfaces (GUI) |
| [Poetry](https://python-poetry.org/docs/) | Tool for dependency management and packaging in Python                                                                        |

## Roadmap

- [x] Basic encryption and decryption

- [ ] Better UI

- [ ] Improve error handling
