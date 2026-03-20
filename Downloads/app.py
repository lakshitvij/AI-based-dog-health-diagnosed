
import streamlit as st
import importlib

st.set_page_config(page_title="Automation Panel", layout="centered")
st.title("🛠️ Menu-Based Automation Panel")

# Menu
task_category = st.sidebar.selectbox("Select Technology", [
    "Python Automation", "Linux Tasks", "JavaScript Tasks", "Docker Tasks", "Git Tasks"
])

task_map = {
    "Python Automation": [
        "send_email", "send_sms", "make_call", "post_to_linkedin",
        "post_to_twitter", "post_to_facebook", "send_whatsapp_msg"
    ],
    "Linux Tasks": [
        "disk_usage", "list_processes", "system_info"
    ],
    "JavaScript Tasks": [
        "color_changer", "shortcut_keys", "todo_list"
    ],
    "Docker Tasks": [
        "build_image", "run_container", "stop_container"
    ],
    "Git Tasks": [
        "clone_repo", "commit_push", "create_branch"
    ]
}

selected_task = st.sidebar.selectbox("Select Task", task_map[task_category])

module_path = f"{task_category.lower().replace(' ', '_').replace('automation', 'tasks')}.{selected_task}"

try:
    module = importlib.import_module(module_path)
    module.run()
except Exception as e:
    st.error(f"⚠️ Unable to load task '{selected_task}': {e}")
