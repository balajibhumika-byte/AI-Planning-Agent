from core.llm_client import get_ai_response


class Synthesizer:

    def __init__(self):
        self.system_prompt = """
        You are an intelligent AI Synthesizer Agent.

        Your responsibility is to combine multiple
        subtask results into one final solution.

        Rules:
        1. Understand the original task.
        2. Combine successful subtask results.
        3. Organize information using clear headings.
        4. Remove repeated information.
        5. Mention failed or incomplete subtasks.
        6. Do not invent information.
        7. Provide a useful conclusion.
        """

    def synthesize(self, task, execution_results):

        if not isinstance(task, str) or not task.strip():
            raise ValueError("Original task is missing.")

        if not isinstance(execution_results, list):
            raise ValueError("Invalid execution results.")

        if not execution_results:
            raise ValueError("No execution results provided.")

        successful = []
        failed = []

        for item in execution_results:
            if item.get("status") == "Completed":
                successful.append(item)
            else:
                failed.append(item)

        if not successful:
            raise ValueError(
                "No successfully completed subtasks."
            )

        result_text = ""

        for index, item in enumerate(successful, start=1):
            result_text += f"""
            SUBTASK {index}: {item.get('title')}

            RESULT:
            {item.get('result')}
            """

        failed_text = ""

        for item in failed:
            failed_text += f"""
            SUBTASK: {item.get('title')}
            STATUS: {item.get('status')}
            ERROR: {item.get('error', 'Not available')}
            """

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": f"""
                ORIGINAL TASK:
                {task}

                SUCCESSFUL RESULTS:
                {result_text}

                FAILED SUBTASKS:
                {failed_text if failed_text else 'None'}

                Combine everything into one
                comprehensive final solution.
                """
            }
        ]

        response = get_ai_response(
            messages,
            temperature=0.3,
            max_tokens=3000
        )

        if not response or not response.strip():
            raise ValueError(
                "Synthesizer received an empty AI response."
            )

        return {
            "task": task,
            "total_subtasks": len(execution_results),
            "successful": len(successful),
            "failed": len(failed),
            "final_result": response.strip()
        }