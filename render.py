# render.py
from typing import List, Dict, Any

def render_list(tasks: List[Dict[str, Any]]) -> str:
    if not tasks:
        return "No hay tareas. 🎉"
    lines = []
    for t in tasks:
        chk = "✔" if t.get("done") else "⟡"
        pr  = (t.get("priority") or "").upper()
        due = f"(due {t['due']})" if t.get("due") else ""
        lines.append(f"[{t['id']:>3}] {chk} {t['title']} {due} {pr}".rstrip())
    return "\n".join(lines)

def render_task(t: Dict[str, Any]) -> str:
    chk = "✔" if t.get("done") else "⟡"
    due = f"(due {t['due']})" if t.get("due") else ""
    pr  = (t.get("priority") or "").upper()
    return f"[{t['id']}] {chk} {t['title']} {due} {pr}".rstrip()
