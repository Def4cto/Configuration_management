import tkinter as tk
import shlex


class ConsoleLogic:
    def __init__(self):
        self.vfs_name = "docker$ "
        self.exit_cmd = "exit"

    def process_command(self, command: str) -> str:
        if not command.strip():
            return ""

        if command == self.exit_cmd:
            return "__EXIT__"

        try:
            command_shlexed = shlex.split(command)
        except ValueError as e:
            return f"Ошибка парсинга: {e}"

        if not command_shlexed:
            return ""

        cmd = command_shlexed[0]

        if cmd == "ls":
            return f"ls {command_shlexed[1:]}"
        elif cmd == "cd":
            if len(command_shlexed) > 1:
                return f"cd {command_shlexed[1:]}"
            else:
                return "cd: missing operand"
        else:
            return f"{cmd}: command not found"


class MiniShellGUI:
    def __init__(self, root, console_logic: ConsoleLogic):
        self.root = root
        self.logic = console_logic

        self.root.title("MiniShell")

        # окно вывода
        self.text = tk.Text(root, height=20, width=80,
                            bg="black", fg="lime", insertbackground="white")
        self.text.pack(padx=5, pady=5)

        # строка ввода
        self.entry = tk.Entry(root, width=80,
                              bg="black", fg="white", insertbackground="white")
        self.entry.pack(padx=5, pady=5)

        # биндинг Enter
        self.entry.bind("<Return>", self.execute_command)

        # вывести первый промпт
        self.append_text(self.logic.vfs_name)

        # курсор в строке ввода
        self.entry.focus_set()

    def append_text(self, msg: str):
        self.text.insert(tk.END, msg)
        self.text.see(tk.END)

    def execute_command(self, event=None):
        command = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        # показать введённую команду
        self.append_text(command + "\n")

        result = self.logic.process_command(command)

        if result == "__EXIT__":
            self.root.quit()
            return

        if result:
            self.append_text(result + "\n")

        # новый промпт
        self.append_text(self.logic.vfs_name)

        # вернуть курсор в строку ввода
        self.entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    console_logic = ConsoleLogic()
    app = MiniShellGUI(root, console_logic)
    root.mainloop()