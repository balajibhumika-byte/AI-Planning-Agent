from agents.planner import Planner
from agents.executor import Executor

# Sample task
user_task = """
Organize a two-day technical fest in an
engineering college with a budget of Rs. 50000.
"""

print("\n===== EXECUTOR AGENT TEST =====")

try:
    # First generate the plan
    planner = Planner()
    plan = planner.create_plan(user_task)

    print("\nPlanner generated", len(plan["subtasks"]), "subtasks.")

    # Execute only the first subtask for this test
    executor = Executor()

    first_subtask = plan["subtasks"][0]

    print("\nExecuting first subtask:")
    print(first_subtask["title"])

    result = executor.execute_subtask(
        first_subtask,
        plan["task"]
    )

    print("\n===== EXECUTION RESULT =====")
    print("Title:", result["title"])
    print("Status:", result["status"])
    print("Result:", result.get("result"))

    if result["status"] == "Completed":
        print("\nEXECUTOR TEST SUCCESSFUL!")
    else:
        print("\nEXECUTOR TEST FAILED!")
        print("Error:", result.get("error"))

except Exception as error:
    print("\nTEST FAILED!")
    print("Error:", error)