import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# List to store woodworking projects
projects = []

# Function to add a new project
def add_project():
    project_name = entry_project_name.get()
    materials_needed = entry_materials.get()
    estimated_duration = entry_duration.get()
    
    try:
        estimated_duration = int(estimated_duration)  # duration in days
    except ValueError:
        messagebox.showerror("Invalid Duration", "Please enter a valid number for estimated duration.")
        return
    
    project = {
        "name": project_name,
        "materials_needed": materials_needed,
        "estimated_duration": estimated_duration,
        "tasks": [],
        "progress": "Not Started",
        "deadline": None
    }
    
    projects.append(project)
    update_project_list()
    messagebox.showinfo("Project Added", f"Project '{project_name}' added successfully!")

# Function to add a task to the project
def add_task():
    task_name = entry_task_name.get()
    project_index = listbox_projects.curselection()
    
    if not task_name or not project_index:
        messagebox.showerror("Error", "Please select a project and provide a task name.")
        return
    
    project_index = project_index[0]
    task = {
        "name": task_name,
        "status": "Not Started",
        "deadline": None
    }
    
    projects[project_index]["tasks"].append(task)
    update_task_list(project_index)
    messagebox.showinfo("Task Added", f"Task '{task_name}' added successfully!")

# Function to update task status (Complete or In Progress)
def update_task_status(task_index, project_index):
    task = projects[project_index]["tasks"][task_index]
    if task["status"] == "Not Started":
        task["status"] = "In Progress"
    elif task["status"] == "In Progress":
        task["status"] = "Completed"
    else:
        task["status"] = "Not Started"
    
    update_task_list(project_index)

# Function to update the deadline of the project
def set_project_deadline(project_index):
    deadline = entry_deadline.get()
    
    try:
        deadline = datetime.strptime(deadline, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter a valid deadline in DD/MM/YYYY format.")
        return
    
    projects[project_index]["deadline"] = deadline
    update_project_list()

# Function to update the displayed list of projects
def update_project_list():
    listbox_projects.delete(0, tk.END)
    for i, project in enumerate(projects):
        project_info = f"{project['name']} - Duration: {project['estimated_duration']} days - Progress: {project['progress']}"
        if project["deadline"]:
            project_info += f" - Deadline: {project['deadline'].strftime('%d/%m/%Y')}"
        listbox_projects.insert(tk.END, project_info)

# Function to update the displayed task list for the selected project
def update_task_list(project_index):
    listbox_tasks.delete(0, tk.END)
    for i, task in enumerate(projects[project_index]["tasks"]):
        task_info = f"{task['name']} - Status: {task['status']}"
        listbox_tasks.insert(tk.END, task_info)

# Function to display selected project details in the entry fields
def display_project_details(event):
    selected_index = listbox_projects.curselection()
    if selected_index:
        project_index = selected_index[0]
        project = projects[project_index]
        
        entry_project_name.delete(0, tk.END)
        entry_project_name.insert(0, project["name"])
        
        entry_materials.delete(0, tk.END)
        entry_materials.insert(0, project["materials_needed"])
        
        entry_duration.delete(0, tk.END)
        entry_duration.insert(0, project["estimated_duration"])
        
        entry_deadline.delete(0, tk.END)
        
        update_task_list(project_index)

# Function to display selected task details
def display_task_details(event):
    selected_index = listbox_tasks.curselection()
    if selected_index:
        task_index = selected_index[0]
        project_index = listbox_projects.curselection()[0]
        
        update_task_status(task_index, project_index)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Woodworking Project Organizer")

# Project Input Fields
label_project_name = tk.Label(root, text="Project Name:")
label_project_name.grid(row=0, column=0)
entry_project_name = tk.Entry(root)
entry_project_name.grid(row=0, column=1)

label_materials = tk.Label(root, text="Materials Needed:")
label_materials.grid(row=1, column=0)
entry_materials = tk.Entry(root)
entry_materials.grid(row=1, column=1)

label_duration = tk.Label(root, text="Estimated Duration (in days):")
label_duration.grid(row=2, column=0)
entry_duration = tk.Entry(root)
entry_duration.grid(row=2, column=1)

button_add_project = tk.Button(root, text="Add Project", command=add_project)
button_add_project.grid(row=3, columnspan=2)

# Project List Box
listbox_projects = tk.Listbox(root, height=10, width=50)
listbox_projects.grid(row=4, columnspan=2)
listbox_projects.bind('<<ListboxSelect>>', display_project_details)

# Task Input Fields
label_task_name = tk.Label(root, text="Task Name:")
label_task_name.grid(row=5, column=0)
entry_task_name = tk.Entry(root)
entry_task_name.grid(row=5, column=1)

button_add_task = tk.Button(root, text="Add Task", command=add_task)
button_add_task.grid(row=6, columnspan=2)

# Task List Box
listbox_tasks = tk.Listbox(root, height=10, width=50)
listbox_tasks.grid(row=7, columnspan=2)
listbox_tasks.bind('<<ListboxSelect>>', display_task_details)

# Set Deadline for Project
label_deadline = tk.Label(root, text="Set Project Deadline (DD/MM/YYYY):")
label_deadline.grid(row=8, column=0)
entry_deadline = tk.Entry(root)
entry_deadline.grid(row=8, column=1)

button_set_deadline = tk.Button(root, text="Set Deadline", command=lambda: set_project_deadline(listbox_projects.curselection()[0]))
button_set_deadline.grid(row=9, columnspan=2)

# Start the Tkinter event loop
root.mainloop()
