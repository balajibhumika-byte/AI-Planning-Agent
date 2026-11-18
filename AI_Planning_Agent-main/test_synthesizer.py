from agents.synthesizer import Synthesizer


# Sample original task
user_task = """
Organize a two-day technical fest in an
engineering college with a budget of Rs. 50000.
"""


# Sample Executor results
execution_results = [
    {
        "subtask_id": 1,
        "title": "Prepare Budget",
        "status": "Completed",
        "result": """
        Total budget: Rs. 50000.

        Speakers: Rs. 10000
        Prizes: Rs. 15000
        Marketing: Rs. 5000
        Logistics: Rs. 10000
        Equipment: Rs. 5000
        Contingency: Rs. 5000
        """
    },
    {
        "subtask_id": 2,
        "title": "Arrange Venue",
        "status": "Completed",
        "result": """
        Use the college auditorium and
        laboratories for the two-day fest.
        Arrange projectors, sound systems
        and internet facilities.
        """
    },
    {
        "subtask_id": 3,
        "title": "Promote Event",
        "status": "Failed",
        "result": None,
        "error": "API connection unavailable."
    }
]


print("\n===== SYNTHESIZER AGENT TEST =====")

try:
    synthesizer = Synthesizer()

    final_output = synthesizer.synthesize(
        user_task,
        execution_results
    )

    print("\nTASK:")
    print(final_output["task"])

    print("\nEXECUTION SUMMARY:")
    print("Total subtasks:", final_output["total_subtasks"])
    print("Successful:", final_output["successful"])
    print("Failed:", final_output["failed"])

    print("\n===== FINAL COMBINED SOLUTION =====")
    print(final_output["final_result"])

    print("\nSYNTHESIZER TEST SUCCESSFUL!")

except Exception as error:
    print("\nSYNTHESIZER TEST FAILED!")
    print("Error:", error)