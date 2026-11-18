from core.state_manager import StateManager

sample_plan = {
    "task": "Organize a technical fest",
    "summary": "Plan and organize a two-day technical fest.",
    "subtasks": [
        {
            "id": 1,
            "title": "Prepare Budget",
            "description": "Create a budget.",
            "expected_output": "Budget sheet"
        },
        {
            "id": 2,
            "title": "Arrange Venue",
            "description": "Select a venue.",
            "expected_output": "Venue confirmation"
        },
        {
            "id": 3,
            "title": "Promote Event",
            "description": "Promote the fest.",
            "expected_output": "Promotion plan"
        }
    ]
}

print("\n===== STATE MANAGER TEST =====")

manager = StateManager(sample_plan)

manager.update_status(
    1,
    "Completed",
    result="Budget prepared successfully."
)

manager.update_status(
    2,
    "Running"
)

print("\nTASK PROGRESS:")
print(manager.get_progress())

manager.save_state()

print("\nState saved successfully!")

loaded_manager = StateManager.load_state()

print("\nLOADED TASK STATE:")
print(loaded_manager.get_state())

print("\nSTATE MANAGER TEST SUCCESSFUL!")