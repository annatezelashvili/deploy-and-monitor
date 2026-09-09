from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

class TaskCreate(BaseModel):
    title: str

tasks= {}
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return list(tasks.values())

@app.post("/tasks")
def create_task(task: TaskCreate):
    new_id = max(tasks.keys(), default=0) + 1
    new_task = {"id":new_id, "title": task.title, "done":False}
    tasks[new_id]= new_task
    return new_task

@app.put("/tasks/{task_id}")
def mark_done(task_id: int):
    if task_id in tasks:
        tasks[task_id]["done"]= True 
        return tasks[task_id]
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete(task_id: int):
    if task_id in tasks:
        deleted_item= tasks[task_id]
        del tasks[task_id]
        return {"message": "Task deleted", "task": deleted_item}
    else:
        raise HTTPException(status_code=404, detail="Task not found")
