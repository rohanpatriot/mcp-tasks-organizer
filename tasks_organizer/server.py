#!/usr/bin/env python3
import re
import json
import asyncio
import os
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("tasks-organizer")

# Constants
TASKS_FOLDER = ".tasks"
COMPLETED_PREFIX = "✅"

@mcp.tool()
async def create_task_list(
    title: str,
    description: str,
    repo_path: str = ".",
    include_metadata: bool = True
) -> str:
    """Create a new task list and save it to the .tasks folder.
    
    Args:
        title: Title for the task list
        description: Short 2-3 word description for the filename (e.g., "refactor-authentication")
        repo_path: Path to the repository root (defaults to current directory)
        include_metadata: Whether to include creation date/time
    
    Returns:
        Path to the created task list file
    """
    # Sanitize the description for filename use
    safe_description = description.lower().replace(" ", "-")
    safe_description = re.sub(r'[^a-z0-9\-]', '', safe_description)
    
    # Create .tasks directory if it doesn't exist
    tasks_dir = os.path.join(repo_path, TASKS_FOLDER)
    if not os.path.exists(tasks_dir):
        os.makedirs(tasks_dir)
    
    # Generate markdown content
    markdown = f"# {title}\n\n"
    
    if include_metadata:
        markdown += f"*Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    markdown += "## Tasks\n\n"
    markdown += "*No tasks yet*\n"
    
    # Save to file
    filename = f"{safe_description}.md"
    file_path = os.path.join(tasks_dir, filename)
    
    with open(file_path, 'w') as file:
        file.write(markdown)
    
    return f"Created task list at {file_path}"

@mcp.tool()
async def convert_plan_to_tasks(
    plan_text: str,
    title: str,
    description: str,
    repo_path: str = ".",
    include_metadata: bool = True
) -> str:
    """Convert a Cursor agent's plan text into a formatted Markdown task list and save it.
    
    Args:
        plan_text: The plan text from the Cursor agent
        title: Title for the task list
        description: Short 2-3 word description for the filename (e.g., "refactor-authentication")
        repo_path: Path to the repository root (defaults to current directory)
        include_metadata: Whether to include metadata like date and time
        
    Returns:
        Path to the created task list file
    """
    # Sanitize the description for filename use
    safe_description = description.lower().replace(" ", "-")
    safe_description = re.sub(r'[^a-z0-9\-]', '', safe_description)
    
    # Create .tasks directory if it doesn't exist
    tasks_dir = os.path.join(repo_path, TASKS_FOLDER)
    if not os.path.exists(tasks_dir):
        os.makedirs(tasks_dir)
    
    # Basic structure for our markdown
    markdown = f"# {title}\n\n"
    
    # Add metadata if requested
    if include_metadata:
        markdown += f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    # Extract tasks from the plan text
    tasks = extract_tasks(plan_text)
    
    # Format tasks as markdown
    if tasks:
        markdown += "## Tasks\n\n"
        for i, task in enumerate(tasks):
            markdown += f"{i+1}. [ ] {task.strip()}\n"
    else:
        # If no specific tasks were found, format the entire plan
        sections = format_plan_sections(plan_text)
        markdown += sections
    
    # Save to file
    filename = f"{safe_description}.md"
    file_path = os.path.join(tasks_dir, filename)
    
    with open(file_path, 'w') as file:
        file.write(markdown)
    
    return f"Created task list at {file_path}"

@mcp.tool()
async def add_task(
    description: str,
    task_text: str,
    repo_path: str = ".",
    section: str = "Tasks"
) -> str:
    """Add a new task to an existing task list.
    
    Args:
        description: The description identifier of the task list file
        task_text: Text for the new task
        repo_path: Path to the repository root (defaults to current directory)
        section: Which section to add the task to (defaults to "Tasks")
    
    Returns:
        Updated markdown task list
    """
    # Find the task file
    task_file, content = find_task_file(description, repo_path)
    if not task_file:
        return f"Error: Could not find task list with description '{description}'"
    
    lines = content.split('\n')
    section_header = f"## {section}"
    
    # Find the section
    section_index = -1
    for i, line in enumerate(lines):
        if line.strip() == section_header:
            section_index = i
            break
    
    if section_index == -1:
        # Section doesn't exist, add it
        lines.append("")
        lines.append(section_header)
        lines.append("")
        section_index = len(lines) - 1
    
    # Find where to insert the task
    task_start = section_index + 1
    task_count = 0
    
    # Count existing tasks
    i = task_start
    while i < len(lines) and not lines[i].startswith('#'):
        if re.match(r'^\d+\.\s+\[[ x]\]', lines[i]):
            task_count += 1
        i += 1
    
    # Remove "No tasks yet" if it exists
    if task_count == 0 and task_start < len(lines) and "*No tasks yet*" in lines[task_start]:
        lines[task_start] = f"{task_count + 1}. [ ] {task_text}"
    else:
        # Insert the new task
        insert_index = task_start
        while insert_index < len(lines) and not lines[insert_index].startswith('#'):
            insert_index += 1
        
        lines.insert(insert_index, f"{task_count + 1}. [ ] {task_text}")
    
    updated_content = '\n'.join(lines)
    
    # Save updated content
    with open(task_file, 'w') as file:
        file.write(updated_content)
    
    return f"Added task '{task_text}' to {os.path.basename(task_file)}"

@mcp.tool()
async def mark_task_complete(
    description: str,
    task_number: int,
    repo_path: str = ".",
    section: str = "Tasks"
) -> str:
    """Mark a specific task as completed.
    
    Args:
        description: The description identifier of the task list file
        task_number: The number of the task to mark as complete
        repo_path: Path to the repository root (defaults to current directory)
        section: Which section the task is in (defaults to "Tasks")
    
    Returns:
        Updated markdown task list
    """
    # Find the task file
    task_file, content = find_task_file(description, repo_path)
    if not task_file:
        return f"Error: Could not find task list with description '{description}'"
    
    lines = content.split('\n')
    section_header = f"## {section}"
    
    # Find the section
    section_index = -1
    for i, line in enumerate(lines):
        if line.strip() == section_header:
            section_index = i
            break
    
    if section_index == -1:
        return f"Error: Section '{section}' not found in task list"
    
    # Find the task
    task_index = -1
    current_task = 0
    
    for i in range(section_index + 1, len(lines)):
        if lines[i].startswith('#'):
            break
            
        task_match = re.match(r'^(\d+)\.\s+\[[ x]\]', lines[i])
        if task_match:
            current_task += 1
            if current_task == task_number:
                task_index = i
                break
    
    if task_index == -1:
        return f"Error: Task {task_number} not found in section '{section}'"
    
    # Update the task status
    lines[task_index] = re.sub(r'^\d+\.\s+\[ \]', f"{task_number}. [x]", lines[task_index])
    
    updated_content = '\n'.join(lines)
    
    # Save updated content
    with open(task_file, 'w') as file:
        file.write(updated_content)
    
    return f"Marked task {task_number} as complete in {os.path.basename(task_file)}"

@mcp.tool()
async def check_all_tasks_complete(
    description: str,
    repo_path: str = ".",
) -> str:
    """Check if all tasks are complete and mark the task list as completed.
    
    Args:
        description: The description identifier of the task list file
        repo_path: Path to the repository root (defaults to current directory)
        
    Returns:
        Message indicating if the task list was marked as completed
    """
    # Find the task file
    task_file, content = find_task_file(description, repo_path)
    if not task_file:
        return f"Error: Could not find task list with description '{description}'"
    
    # Check if all tasks are complete
    all_tasks_complete = True
    incomplete_task_count = 0
    
    # Find all task lines
    task_matches = re.finditer(r'^\d+\.\s+\[([ x])\]', content, re.MULTILINE)
    for match in task_matches:
        if match.group(1) == ' ':  # Unchecked box
            all_tasks_complete = False
            incomplete_task_count += 1
    
    if not all_tasks_complete:
        return f"Task list has {incomplete_task_count} incomplete tasks. Cannot mark as completed."
    
    # If all tasks are complete, rename the file with the ✅ prefix
    filename = os.path.basename(task_file)
    if not filename.startswith(COMPLETED_PREFIX):
        task_dir = os.path.dirname(task_file)
        new_filename = f"{COMPLETED_PREFIX}{filename}"
        new_file_path = os.path.join(task_dir, new_filename)
        
        os.rename(task_file, new_file_path)
        return f"All tasks complete! Renamed task list to {new_filename}"
    else:
        return "All tasks are already complete and the list is marked as completed."

@mcp.tool()
async def list_task_files(
    repo_path: str = ".",
    include_completed: bool = True
) -> str:
    """List all task files in the .tasks directory.
    
    Args:
        repo_path: Path to the repository root (defaults to current directory)
        include_completed: Whether to include completed task lists
        
    Returns:
        List of task files with their completion status
    """
    tasks_dir = os.path.join(repo_path, TASKS_FOLDER)
    if not os.path.exists(tasks_dir):
        return "No .tasks directory exists yet."
    
    # Get list of markdown files
    task_files = []
    for file in os.listdir(tasks_dir):
        if file.endswith('.md'):
            is_completed = file.startswith(COMPLETED_PREFIX)
            if include_completed or not is_completed:
                task_files.append((file, is_completed))
    
    if not task_files:
        return "No task lists found."
    
    # Format the output
    result = "## Task Lists\n\n"
    for filename, is_completed in sorted(task_files):
        status = "✅ Complete" if is_completed else "⏳ In Progress"
        description = filename.replace(COMPLETED_PREFIX, "").replace(".md", "")
        result += f"- **{description}**: {status}\n"
    
    return result

def find_task_file(description: str, repo_path: str) -> Tuple[Optional[str], Optional[str]]:
    """Find a task file by its description.
    
    Args:
        description: The description identifier of the task list file
        repo_path: Path to the repository root
        
    Returns:
        Tuple of (file_path, content) or (None, None) if not found
    """
    tasks_dir = os.path.join(repo_path, TASKS_FOLDER)
    if not os.path.exists(tasks_dir):
        return None, None
    
    # Normalize description for comparison
    safe_description = description.lower().replace(" ", "-")
    safe_description = re.sub(r'[^a-z0-9\-]', '', safe_description)
    
    # Look for files that match the description
    for file in os.listdir(tasks_dir):
        if file.endswith('.md'):
            # Remove completion prefix and extension for comparison
            file_desc = file.replace(COMPLETED_PREFIX, "").replace(".md", "")
            if file_desc == safe_description:
                file_path = os.path.join(tasks_dir, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                return file_path, content
    
    return None, None

def extract_tasks(text: str) -> List[str]:
    """Extract tasks from the plan text.
    
    Looks for common patterns that indicate tasks in the text.
    
    Args:
        text: The plan text to parse
        
    Returns:
        A list of extracted tasks
    """
    tasks = []
    
    # Try to find numbered steps (1. Step one, 2. Step two)
    numbered_steps = re.findall(r'\b(\d+\.?\s*[A-Z].*?)(?=\b\d+\.|\n\n|$)', text, re.DOTALL)
    if numbered_steps:
        # Clean up the steps
        tasks = [re.sub(r'^\d+\.?\s*', '', step).strip() for step in numbered_steps]
        return tasks
    
    # Try to find bullet points
    bullet_points = re.findall(r'(?:^|\n)[*\-•]\s*(.*?)(?=\n[*\-•]|\n\n|$)', text, re.DOTALL)
    if bullet_points:
        tasks = [point.strip() for point in bullet_points]
        return tasks
    
    # Try to find sentences that contain task-like keywords
    task_sentences = re.findall(r'(?:need to|should|must|will|going to|let\'s|we can|I\'ll|can|todo|to-do|task)\s+([^\.]+\.)', text, re.IGNORECASE)
    if task_sentences:
        tasks = [sentence.strip() for sentence in task_sentences]
        return tasks
    
    # If all else fails, split by paragraphs and treat each as a potential task
    paragraphs = re.split(r'\n\s*\n', text)
    if paragraphs:
        # Filter out very short paragraphs and headers
        tasks = [p.strip() for p in paragraphs if len(p.strip()) > 10 and not p.strip().startswith('#')]
        return tasks
    
    return tasks

def format_plan_sections(text: str) -> str:
    """Format the plan into structured sections if no clear tasks were found.
    
    Args:
        text: The plan text to format
        
    Returns:
        Formatted markdown with sections
    """
    # Look for markdown headers already in the text
    has_headers = bool(re.search(r'^#+\s+', text, re.MULTILINE))
    
    if has_headers:
        # If the text already has headers, preserve them
        return text
    
    # Otherwise try to identify sections
    sections = {
        "## Overview": [],
        "## Implementation Details": [],
        "## Next Steps": []
    }
    
    lines = text.split('\n')
    current_section = "## Overview"
    
    for line in lines:
        # Simple heuristic: Try to identify section breaks
        if re.match(r'^.*(overview|summary|about).*$', line, re.IGNORECASE):
            current_section = "## Overview"
            continue
        elif re.match(r'^.*(implementation|details|how to|approach).*$', line, re.IGNORECASE):
            current_section = "## Implementation Details"
            continue
        elif re.match(r'^.*(next steps|future|todo|to do).*$', line, re.IGNORECASE):
            current_section = "## Next Steps"
            continue
        
        # Add the line to the current section
        if line.strip():
            sections[current_section].append(line)
    
    # Build the final markdown
    result = ""
    for section, content in sections.items():
        if content:
            result += f"{section}\n\n"
            # Format as a list if it's the "Next Steps" section
            if section == "## Next Steps":
                for i, line in enumerate(content):
                    result += f"{i+1}. [ ] {line.strip()}\n"
            else:
                result += "\n".join(content) + "\n\n"
    
    return result

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio') 