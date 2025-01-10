import streamlit as st
import requests
from datetime import datetime

# Configure the API URL
API_URL = "http://localhost:8000"

st.title("📝 Todo App")

# Create new todo
st.subheader("Create New Todo")
with st.form("todo_form", clear_on_submit=True):
    title = st.text_input("Title")
    description = st.text_area("Description")
    submitted = st.form_submit_button("Add Todo")
    
    if submitted and title:
        response = requests.post(
            f"{API_URL}/todos/",
            json={"title": title, "description": description, "completed": False}
        )
        if response.status_code == 200:
            st.success("Todo added successfully!")
        else:
            st.error("Failed to add todo")

# Display todos
st.subheader("Your Todos")
response = requests.get(f"{API_URL}/todos/")
if response.status_code == 200:
    todos = response.json()
    for todo in todos:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            if todo["completed"]:
                st.markdown(f"~~{todo['title']}~~")
            else:
                st.markdown(todo["title"])
            if todo["description"]:
                st.caption(todo["description"])
        
        with col2:
            if st.button("Toggle", key=f"toggle_{todo['id']}"):
                response = requests.put(
                    f"{API_URL}/todos/{todo['id']}",
                    json={
                        "title": todo["title"],
                        "description": todo["description"],
                        "completed": not todo["completed"]
                    }
                )
                if response.status_code == 200:
                    st.rerun()
        
        with col3:
            if st.button("Delete", key=f"delete_{todo['id']}"):
                response = requests.delete(f"{API_URL}/todos/{todo['id']}")
                if response.status_code == 200:
                    st.rerun()
        
        st.divider()
else:
    st.error("Failed to fetch todos") 