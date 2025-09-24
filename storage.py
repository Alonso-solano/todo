# storage.py
import json
from typing import List, Dict, Any, Optional
from .constants import STORE_FILE
from .models import Task

def load_tasks() -> List[Dict[str, Any]]:
    if not STORE_FILE.exists():
        return []
    try:
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("tasks", []) if isinstance(data, dict) else data
    except Exception:
        return []

def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    payload = {"tasks": tasks}
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def list_tasks() -> List[Dict[str, Any]]:
    return load_tasks()

def next_id(tasks: List[Dict[str, Any]]) -> int:
    return max((t["id"] for t in tasks), default=0) + 1

def get(task_id: int) -> Optional[Dict[str, Any]]:
    for t in load_tasks():
        if t["id"] == task_id:
            return t
    return None

def upsert(task: Task) -> Task:
    tasks = load_tasks()
    for i, t in enumerate(tasks):
        if t["id"] == task.id:
            tasks[i] = task.to_dict()
            break
    else:
        tasks.append(task.to_dict())
    save_tasks(tasks)
    return task

def delete(task_id: int) -> bool:
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    changed = len(new_tasks) != len(tasks)
    if changed:
        save_tasks(new_tasks)
    return changed

def toggle_done(task_id: int, value: bool = True) -> Optional[Dict[str, Any]]:
    tasks = load_tasks()
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            t["done"] = value
            tasks[i] = t
            save_tasks(tasks)
            return t
    return None
