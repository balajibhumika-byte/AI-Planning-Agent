import streamlit as st

from agents.planner import Planner
from agents.executor import Executor
from agents.synthesizer import Synthesizer
from core.state_manager import StateManager


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="AI Planning Agent",
    page_icon="🤖",
    layout="wide"
)


# -------------------------------------------------
# PAGE HEADER
# -------------------------------------------------

st.title("🤖 AI Planning Agent")
st.subheader("Intelligent Task Planning and Execution")

st.write(
    "Enter a complex task. The AI will break it into "
    "subtasks, execute them, track progress and generate "
    "a final combined solution."
)

st.divider()


# -------------------------------------------------
# USER INPUT
# -------------------------------------------------

user_task = st.text_area(
    "Enter your task:",
    placeholder=(
        "Example: Organize a two-day technical fest "
        "in an engineering college with a budget of Rs. 50000."
    ),
    height=130
)


# -------------------------------------------------
# RUN PLANNING AGENT
# -------------------------------------------------

if st.button("🚀 Generate Plan and Execute", type="primary"):

    if not user_task.strip():
        st.warning("Please enter a task first.")

    else:
        st.session_state.pop("run_data", None)

        try:
            planner = Planner()
            executor = Executor()
            synthesizer = Synthesizer()

            # STEP 1: GENERATE PLAN

            with st.spinner("Planner is generating subtasks..."):
                plan = planner.create_plan(user_task)

            st.success(
                f"Planner generated {len(plan['subtasks'])} subtasks!"
            )

            # STEP 2: INITIALIZE STATE MANAGER

            manager = StateManager(plan)

            execution_results = []

            # STEP 3: EXECUTE SUBTASKS

            st.subheader("⚙️ Subtask Execution")

            progress_bar = st.progress(0)
            progress_text = st.empty()

            total = len(plan["subtasks"])

            for index, subtask in enumerate(plan["subtasks"]):

                manager.update_status(
                    subtask["id"],
                    "Running"
                )

                progress_text.write(
                    f"Executing {index + 1} of {total}: "
                    f"{subtask['title']}"
                )

                with st.spinner(
                    f"Executing: {subtask['title']}"
                ):
                    result = executor.execute_subtask(
                        subtask,
                        plan["task"]
                    )

                execution_results.append(result)

                manager.record_result(result)

                percentage = int(
                    ((index + 1) / total) * 100
                )

                progress_bar.progress(percentage)

                if result["status"] == "Completed":
                    st.success(
                        f"Completed: {result['title']}"
                    )
                else:
                    st.error(
                        f"Failed: {result['title']}"
                    )

            progress_text.write("Execution finished!")

            # STEP 4: GET PROGRESS

            progress = manager.get_progress()

            # Save task state

            manager.save_state("task_state.json")

            # STEP 5: SYNTHESIZE RESULTS

            final_output = None

            if progress["completed"] > 0:

                with st.spinner(
                    "Synthesizer is combining the results..."
                ):
                    final_output = synthesizer.synthesize(
                        user_task,
                        execution_results
                    )

                st.success("Final solution generated!")

            # STORE RESULTS

            st.session_state["run_data"] = {
                "plan": plan,
                "results": execution_results,
                "progress": progress,
                "final_output": final_output
            }

        except Exception as error:
            st.error(f"Application Error: {error}")


# -------------------------------------------------
# DISPLAY GENERATED RESULTS
# -------------------------------------------------

if "run_data" in st.session_state:

    data = st.session_state["run_data"]

    st.divider()

    # PLAN

    st.header("📋 Generated Plan")

    st.write(data["plan"]["summary"])

    for subtask in data["plan"]["subtasks"]:

        with st.expander(
            f"Subtask {subtask['id']}: {subtask['title']}"
        ):
            st.write("**Description:**")
            st.write(subtask["description"])

            st.write("**Expected Output:**")
            st.write(subtask["expected_output"])

    # PROGRESS

    st.header("📊 Execution Progress")

    progress = data["progress"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", progress["total"])
    col2.metric("Completed", progress["completed"])
    col3.metric("Failed", progress["failed"])
    col4.metric("Pending", progress["pending"])

    st.progress(progress["percentage"] / 100)

    st.write(
        f"Overall completion: {progress['percentage']}%"
    )

    # INDIVIDUAL RESULTS

    st.header("📝 Individual Execution Results")

    for result in data["results"]:

        with st.expander(
            f"{result['title']} — {result['status']}"
        ):

            if result["status"] == "Completed":
                st.markdown(result["result"])
            else:
                st.error(
                    result.get("error", "Execution failed.")
                )

    # FINAL SOLUTION

    st.divider()

    st.header("🎯 Final Combined Solution")

    final_output = data["final_output"]

    if final_output:
        st.markdown(final_output["final_result"])

        st.download_button(
            label="⬇️ Download Final Solution",
            data=final_output["final_result"],
            file_name="AI_Planning_Agent_Result.md",
            mime="text/markdown"
        )
    else:
        st.warning(
            "No final solution was generated because "
            "no subtasks completed successfully."
        )

    # SAVE STATUS

    st.success("Task execution process finished!")