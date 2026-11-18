import json
from pathlib import Path
from copy import deepcopy


class StateManager:
    """
    Manages the state and progress of the Planning Agent.
    """

    def __init__(self, plan):
        if not isinstance(plan, dict):
            raise ValueError("Invalid plan provided.")

        self.state = {
            "task": plan.get("task", ""),
            "summary": plan.get("summary", ""),
            "subtasks": deepcopy(plan.get("subtasks", []))
        }

        for subtask in self.state["subtasks"]:
            subtask["status"] = "Pending"
            subtask["result"] = None
            subtask["error"] = None

    def update_status(self, subtask_id, status,
                      result=None, error=None):

        allowed_statuses = [
            "Pending", "Running", "Completed", "Failed"
        ]

        if status not in allowed_statuses:
            raise ValueError("Invalid subtask status.")

        for subtask in self.state["subtasks"]:
            if subtask.get("id") == subtask_id:
                subtask["status"] = status
                subtask["result"] = result
                subtask["error"] = error
                return

        raise ValueError("Subtask ID not found.")

    def record_result(self, execution_result):
        if not isinstance(execution_result, dict):
            raise ValueError("Invalid execution result.")

        self.update_status(
            execution_result.get("subtask_id"),
            execution_result.get("status"),
            result=execution_result.get("result"),
            error=execution_result.get("error")
        )

    def get_progress(self):
        subtasks = self.state["subtasks"]
        total = len(subtasks)

        completed = sum(
            s["status"] == "Completed" for s in subtasks
        )
        failed = sum(
            s["status"] == "Failed" for s in subtasks
        )
        running = sum(
            s["status"] == "Running" for s in subtasks
        )
        pending = sum(
            s["status"] == "Pending" for s in subtasks
        )

        percentage = (
            round((completed / total) * 100, 2)
            if total else 0
        )

        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "running": running,
            "pending": pending,
            "percentage": percentage
        }

    def get_state(self):
        return deepcopy(self.state)

    def save_state(self, file_path="task_state.json"):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                self.state,
                file,
                indent=4,
                ensure_ascii=False
            )

    @classmethod
    def load_state(cls, file_path="task_state.json"):
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError("Saved state file not found.")

        with open(path, "r", encoding="utf-8") as file:
            saved_state = json.load(file)

        manager = cls.__new__(cls)
        manager.state = saved_state

        return manager