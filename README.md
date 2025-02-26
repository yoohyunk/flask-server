# Flask Server

## Installation
- **SKIP** if you already have `poetry` - Set up `pipx` and `poetry`
    - `brew install pipx && pipx ensurepath && pipx install poetry`
- `poetry install`

## Development

We use `poe` as a task runner and `poetry` as a dependency manager.

- start dev server: `poe dev`
- run pytest: `poe test`

# Database Models Summary

| Table Name                                       | Fields and Data Types                                                                                                                                                  | Relationships                                                                                                            | Description                                                    |
|--------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| **lists (ListModel)**                            | - **id**: `String(64)`, primary key<br>- **name**: `str`                                                                                                               | - **todos**: One-to-many relationship with `TodoModel` (cascade all, delete-orphan)<br>- **owners**: Relationship with `UserListAssociationModel` | Represents a list with multiple todos and associated owners.   |
| **todos (TodoModel)**                            | - **id**: `String(64)`, primary key (SHA-256 hash)<br>- **name**: `str`<br>- **description**: `str`<br>- **is_done**: `bool`<br>- **list_id**: `str`, foreign key (`lists.id`) | - **todo_list**: Back reference to `ListModel` (back_populates: todos)                                                    | Represents an individual todo item belonging to a list.         |
| **user_list_associtaion (UserListAssociationModel)** | - **user_id**: `String(64)`, primary key<br>- **list_id**: `String(64)`, primary key, foreign key (`lists.id`)<br>- **permission**: `Enum('collaborator', 'admin')`         | - **list**: Relationship with `ListModel` (back_populates: owners)                                                        | Manages many-to-many relationships between users and lists, including permission settings. |
| **users (UserModel)**                            | - **email**: primary key (`str`)<br>- **password_hash**: `str`                                                                                                         | (No explicit relationship defined)                                                                                       | Stores user information, including email and password hash.     |
