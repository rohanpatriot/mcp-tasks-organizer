#!/usr/bin/env python3
"""
A simple test script to verify the task extraction and task management functionality.
"""

import os
import shutil
from tasks_organizer.server import (
    extract_tasks, format_plan_sections, 
    convert_plan_to_tasks, create_task_list, 
    add_task, mark_task_complete,
    check_all_tasks_complete, list_task_files
)
import asyncio

# Sample Cursor agent plans for testing
SAMPLE_PLANS = [
    """
    Let's build a simple web application with Flask. Here's the plan:
    
    1. Set up a new virtual environment
    2. Install Flask and other dependencies
    3. Create the basic application structure
    4. Implement user authentication
    5. Add database models
    6. Create the frontend templates
    7. Test the application
    8. Deploy to a hosting service
    """,
    
    """
    To fix this bug, we need to:
    * Check the database connection parameters
    * Verify the SQL query syntax
    • Add proper error handling
    • Write tests to reproduce the issue
    * Update the documentation
    """,
    
    """
    I've analyzed your code and found several issues. We should refactor the authentication module. The current implementation has security vulnerabilities. We need to implement proper password hashing. Also, the session management needs improvement.
    
    The database layer should be optimized. Connection pooling would improve performance.
    
    To do all this, we'll need to update the dependencies first.
    """
]

async def test_parser():
    """Test the task parsing and formatting functionality."""
    print("\n=== TESTING TASK PARSER ===\n")
    
    for i, plan in enumerate(SAMPLE_PLANS):
        print(f"\n--- Test Case {i+1} ---")
        print("Original Plan:")
        print(plan)
        
        # Test task extraction
        tasks = extract_tasks(plan)
        print("\nExtracted Tasks:")
        for task in tasks:
            print(f"- {task}")
        
        # Test full conversion
        result = await convert_plan_to_tasks(
            plan, 
            f"Test Plan {i+1}", 
            f"test-plan-{i+1}",
            ".",
            True
        )
        print("\nSaved To:")
        print(result)
        
        print("\n" + "-" * 50)

async def test_task_management():
    """Test the task management functionality."""
    print("\n=== TESTING TASK MANAGEMENT ===\n")
    
    # Create a test directory
    test_dir = "test_repo"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    try:
        # 1. Create a new task list
        print("\n1. Creating a new task list...")
        result = await create_task_list(
            "Project Refactoring", 
            "code-refactor",
            test_dir,
            True
        )
        print(result)
        
        # 2. Add tasks to the list
        print("\n2. Adding tasks...")
        
        tasks = [
            "Refactor authentication module",
            "Update database schema",
            "Create unit tests",
            "Update documentation"
        ]
        
        for task in tasks:
            result = await add_task("code-refactor", task, test_dir)
            print(result)
        
        # 3. Mark some tasks as complete
        print("\n3. Marking tasks as complete...")
        result = await mark_task_complete("code-refactor", 1, test_dir)
        print(result)
        
        result = await mark_task_complete("code-refactor", 3, test_dir)
        print(result)
        
        # 4. List all task files
        print("\n4. Listing all task files...")
        result = await list_task_files(test_dir)
        print(result)
        
        # 5. Try to mark all tasks as complete (should fail as not all are done)
        print("\n5. Attempting to mark all tasks as complete (should fail)...")
        result = await check_all_tasks_complete("code-refactor", test_dir)
        print(result)
        
        # 6. Mark remaining tasks as complete
        print("\n6. Marking remaining tasks as complete...")
        result = await mark_task_complete("code-refactor", 2, test_dir)
        print(result)
        
        result = await mark_task_complete("code-refactor", 4, test_dir)
        print(result)
        
        # 7. Now check all tasks complete (should succeed)
        print("\n7. Checking all tasks complete again...")
        result = await check_all_tasks_complete("code-refactor", test_dir)
        print(result)
        
        # 8. List all task files again
        print("\n8. Listing all task files again...")
        result = await list_task_files(test_dir)
        print(result)
        
    finally:
        # Clean up test directory
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            print("\nCleaned up test directory")

if __name__ == "__main__":
    asyncio.run(test_parser())
    asyncio.run(test_task_management()) 