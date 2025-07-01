[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/huntsyea-mcp-tasks-organizer-badge.png)](https://mseep.ai/app/huntsyea-mcp-tasks-organizer)

# MCP Tasks Organizer

An MCP server that converts Cursor agent plans into structured markdown task lists and organizes them in your repository. This server helps you track AI-generated plans and recommendations as actionable specifications.

## Features

- Automatically extracts tasks from Cursor agent plans
- Creates a `.tasks` folder in your repository for organized task management
- Uses descriptive filenames (e.g., "refactor-authentication.md") for easy identification
- Automatically marks completed task lists with a ✅ prefix
- Formats plans with proper Markdown structure
- Organizes content into Overview, Implementation Details, and Next Steps
- Integrates with Claude for Desktop and other MCP clients

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or another Python package manager

### Quick Install

For Unix-based systems (macOS, Linux):

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-tasks-organizer.git
cd mcp-tasks-organizer

# Run the installation script
./install.sh
```

For Windows:

```batch
# Clone the repository
git clone https://github.com/yourusername/mcp-tasks-organizer.git
cd mcp-tasks-organizer

# Run the installation script
install.bat
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-tasks-organizer.git
cd mcp-tasks-organizer

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Usage with Claude for Desktop

1. Install Claude for Desktop from [claude.ai/download](https://claude.ai/download)

2. Configure Claude for Desktop to use this MCP server:

   Open `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows) and add:

   ```json
   {
     "mcpServers": {
       "tasks-organizer": {
         "command": "python",
         "args": ["-m", "tasks_organizer"]
       }
     }
   }
   ```

3. Restart Claude for Desktop

4. Use the server by asking Claude about your cursor plans, for example:
   - "Convert this cursor plan into a task list called 'Refactor Authentication' with description 'auth-refactor': [paste plan]"
   - "Create a markdown task list from this cursor agent output with title 'Database Migration' and description 'db-migration': [paste output]"
   - "Mark task 2 in the auth-refactor task list as complete"
   - "List all task files in my repository"

## Available Tools

The server provides these tools:

### 1. create_task_list

Create a new task list and save it to the .tasks folder.

Parameters:
- `title`: Title for the task list
- `description`: Short 2-3 word description for the filename (e.g., "refactor-authentication") 
- `repo_path`: Path to the repository root (defaults to current directory)
- `include_metadata`: Whether to include creation date/time

### 2. convert_plan_to_tasks

Convert a Cursor agent's plan text into a formatted Markdown task list and save it.

Parameters:
- `plan_text`: The plan text from the Cursor agent
- `title`: Title for the task list
- `description`: Short 2-3 word description for the filename (e.g., "refactor-authentication")
- `repo_path`: Path to the repository root (defaults to current directory)
- `include_metadata`: Whether to include metadata like date and time

### 3. add_task

Add a new task to an existing task list.

Parameters:
- `description`: The description identifier of the task list file
- `task_text`: Text for the new task
- `repo_path`: Path to the repository root (defaults to current directory)
- `section`: Which section to add the task to (defaults to "Tasks")

### 4. mark_task_complete

Mark a specific task as completed.

Parameters:
- `description`: The description identifier of the task list file
- `task_number`: The number of the task to mark as complete
- `repo_path`: Path to the repository root (defaults to current directory)
- `section`: Which section the task is in (defaults to "Tasks")

### 5. check_all_tasks_complete

Check if all tasks are complete and mark the task list as completed by renaming with ✅ prefix.

Parameters:
- `description`: The description identifier of the task list file
- `repo_path`: Path to the repository root (defaults to current directory)

### 6. list_task_files

List all task files in the .tasks directory.

Parameters:
- `repo_path`: Path to the repository root (defaults to current directory)
- `include_completed`: Whether to include completed task lists in the output

## How it Works

1. The server creates a `.tasks` folder in your repository root
2. Task lists are stored with descriptive filenames based on 2-3 word descriptions
3. When all tasks in a list are completed, the file is renamed with a ✅ prefix
4. The server parses the input text from Cursor's agent to extract tasks
5. It extracts tasks using various pattern matching techniques:
   - Numbered steps (1. First step)
   - Bullet points (* Item one)
   - Task-like sentences containing keywords like "should", "must", "need to"
6. If no clear tasks are found, it organizes the content into logical sections
7. The result can be tracked and updated as tasks progress

## Example Workflow

1. An agent proposes changes to your authentication system
2. You convert this plan to a task list: `convert_plan_to_tasks(plan_text, "Auth System Refactor", "auth-refactor")`
3. The tasks are saved to `.tasks/auth-refactor.md`
4. As you complete tasks, mark them: `mark_task_complete("auth-refactor", 1)`
5. When all tasks are done: `check_all_tasks_complete("auth-refactor")`
6. The file is renamed to `.tasks/✅auth-refactor.md`

## License

MIT 