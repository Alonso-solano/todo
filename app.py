# app.py
import argparse
from .storage import (
    list_tasks, next_id, upsert, delete, toggle_done, get
)
from .models import Task
from .render import render_list, render_task

def cmd_list(_: argparse.Namespace) -> None:
    print(render_list(list_tasks()))

def cmd_add(args: argparse.Namespace) -> None:
    tasks = list_tasks()
    tid = next_id(tasks)
    t = Task(
        id=tid,
        title=args.title,
        priority=(args.priority or ""),
        due=args.due
    )
    upsert(t)
    print("Añadida:")
    print(render_task(t))

def cmd_done(args: argparse.Namespace) -> None:
    t = toggle_done(args.id, True)
    print("Marcada como hecha:" if t else "No encontrada.")
    if t: print(render_task(t))

def cmd_undone(args: argparse.Namespace) -> None:
    t = toggle_done(args.id, False)
    print("Marcada como pendiente:" if t else "No encontrada.")
    if t: print(render_task(t))

def cmd_delete(args: argparse.Namespace) -> None:
    ok = delete(args.id)
    print("Eliminada." if ok else "No encontrada.")

def cmd_show(args: argparse.Namespace) -> None:
    t = get(args.id)
    if t:
        print(render_task(t))
    else:
        print("No encontrada.")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo", description="Gestor de tareas")
    sub = p.add_subparsers(required=True)

    sp = sub.add_parser("list", help="Listar tareas")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("add", help="Agregar tarea")
    sp.add_argument("title", help="Título de la tarea")
    sp.add_argument("--priority", "-p", choices=["low","med","high"])
    sp.add_argument("--due", help="Fecha límite YYYY-MM-DD")
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser("done", help="Marcar como hecha")
    sp.add_argument("id", type=int)
    sp.set_defaults(func=cmd_done)

    sp = sub.add_parser("undone", help="Marcar como pendiente")
    sp.add_argument("id", type=int)
    sp.set_defaults(func=cmd_undone)

    sp = sub.add_parser("delete", help="Eliminar tarea")
    sp.add_argument("id", type=int)
    sp.set_defaults(func=cmd_delete)

    sp = sub.add_parser("show", help="Ver una tarea")
    sp.add_argument("id", type=int)
    sp.set_defaults(func=cmd_show)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
