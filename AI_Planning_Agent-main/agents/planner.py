import json
import re

from core.llm_client import get_ai_response


class Planner:
    """
    Planner Agent:
    Converts a complex user task into smaller,
    structured and manageable subtasks.
    """

    def __init__(self):
        self.system_prompt = """
        You are an intelligent Planning Agent.

        Your job is to break a complex user task into
        smaller, logical and actionable subtasks.

        Follow these rules:

        1. Understand the main task carefully.
        2. Generate between 3 and 8 subtasks.
        3. Arrange subtasks in a logical order.
        4. Each subtask must be specific and actionable.
        5. Avoid unnecessary or repeated subtasks.
        6. Make subtasks suitable for independent execution
           wherever possible.
        7. Do not execute the tasks. Only create the plan.
        8. Keep descriptions and expected outputs concise.
        9. Return complete JSON with all closing brackets and braces.
        10. Never stop in the middle of a subtask.
        11. Do not include Markdown code fences.

        Return ONLY valid JSON.

        Use exactly this structure:

        {
            "task": "Original main task",
            "summary": "Brief explanation of the plan",
            "subtasks": [
                {
                    "title": "Subtask title",
                    "description": "What needs to be done",
                    "expected_output": "Expected result"
                }
            ]
        }
        """

    def create_plan(self, user_task):
        """
        Takes the user's task and generates a plan.
        """

        # Check user input
        if not user_task or not user_task.strip():
            raise ValueError("Please enter a valid task.")

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": (
                    "Create a detailed execution plan for "
                    "the following task:\n\n" + user_task.strip()
                )
            }
        ]

        # Get response from OpenRouter
        ai_response = get_ai_response(
            messages,
            temperature=0.2,
            max_tokens=3500
        )

        if not ai_response:
            raise ValueError("The AI returned an empty response.")

        # Convert AI response into JSON
        print("\n========== RAW AI RESPONSE ==========")
        print(ai_response)
        print("========== END AI RESPONSE ==========\n")
        plan = self._parse_json(ai_response)

        # Validate the generated plan
        return self._validate_plan(plan, user_task.strip())

    def _parse_json(self, response):
        """
        Extracts JSON even if the model adds code fences
        or introductory text.
        """

        cleaned = response.strip()

        # Remove Markdown JSON code fences
        cleaned = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE
        )

        cleaned = re.sub(r"\s*```$", "", cleaned)

        # Find the JSON object
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "The AI did not return valid JSON."
            )

        json_text = cleaned[start:end + 1]

        try:
            return json.loads(json_text)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"Could not parse the AI plan: {error}"
            ) from error

    def _validate_plan(self, plan, original_task):
        """
        Checks and standardizes the generated plan.
        """

        if not isinstance(plan, dict):
            raise ValueError("The generated plan must be a JSON object.")

        subtasks = plan.get("subtasks")

        if not isinstance(subtasks, list):
            raise ValueError("The plan must contain a subtasks list.")

        if not 3 <= len(subtasks) <= 8:
            raise ValueError(
                "The Planner must generate between 3 and 5 subtasks. "
                "Please try again."
               
            )

        validated_subtasks = []

        for index, subtask in enumerate(subtasks, start=1):

            if not isinstance(subtask, dict):
                raise ValueError("Each subtask must be an object.")

            title = subtask.get("title")
            description = subtask.get("description")
            expected_output = subtask.get("expected_output")

            if not all(
                isinstance(value, str) and value.strip()
                for value in [title, description, expected_output]
            ):
                raise ValueError(
                    f"Subtask {index} is missing required information."
                )

            validated_subtasks.append({
                "id": index,
                "title": title.strip(),
                "description": description.strip(),
                "expected_output": expected_output.strip(),
                "status": "Pending",
                "result": None
            })

        return {
            "task": original_task,
            "summary": str(plan.get("summary", "")).strip(),
            "subtasks": validated_subtasks
        }