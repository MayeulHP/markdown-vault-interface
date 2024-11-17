# markdown-vault-interface
A simple web interface for Obsidian Vaults. Uses markdown-vault-api as a backend.

Here's a summary of the available endpoints in `markdown-vault-api`, used by this tool:

- **View a Note:** `/note/<path:note_path>` (GET)
- **Edit a Note:** `/note/<path:note_path>` (PUT)
- **Append to a Note:** `/note/<path:note_path>` (PATCH)
- **Search within a Note:** `/note/<path:note_path>/search` (GET)
- **Search across the Entire Vault:** `/search` (GET)
- **View Folder Contents:** `/folder/<path:folder_path>` (GET)
- **View Specific Lines of a Note:** `/note/<path:note_path>/lines/<int:start_line>-<int:end_line>` (GET)
- **Edit Specific Lines of a Note:** `/note/<path:note_path>/lines/<int:start_line>-<int:end_line>` (PATCH)

