# MCP Tasks Organizer
# Converts Cursor agent plans to markdown task lists and organizes them in a repository

from .server import (
    mcp, 
    convert_plan_to_tasks, 
    create_task_list,
    add_task,
    mark_task_complete,
    check_all_tasks_complete,
    list_task_files,
    extract_tasks,
    format_plan_sections,
    TASKS_FOLDER,
    COMPLETED_PREFIX
)

__version__ = "0.1.0" 