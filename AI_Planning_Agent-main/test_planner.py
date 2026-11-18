from agents.planner import Planner

# Create Planner object
planner = Planner()

# Sample complex task
user_task = """
Organize a two-day technical fest in an engineering
college with a budget of Rs. 50000.
Include event planning, budget management,
venue arrangements and student participation.
"""

print("\n====================================")
print("       PLANNING AGENT TEST")
print("====================================")

try:
    # Generate execution plan
    plan = planner.create_plan(user_task)

    print("\nMAIN TASK:")
    print(plan["task"])

    print("\nPLAN SUMMARY:")
    print(plan["summary"])

    print("\nGENERATED SUBTASKS:")
    print("------------------------------------")

    for subtask in plan["subtasks"]:

        print(f"\nSubtask {subtask['id']}")
        print("Title:", subtask["title"])
        print("Description:", subtask["description"])
        print("Expected Output:", subtask["expected_output"])
        print("Status:", subtask["status"])

    print("\n====================================")
    print("PLANNER TEST SUCCESSFUL!")
    print("====================================")

except Exception as error:

    print("\nPLANNER TEST FAILED!")
    print("Error:", error)