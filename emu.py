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
            return f"Ошибка парсинга"

        if not command_shlexed:
            return ""

        cmd = command_shlexed[0]

        if cmd == "ls":
            args = " ".join(command_shlexed[1:])
            return f"ls {args}".strip()
        elif cmd == "cd":
            if len(command_shlexed) > 1:
                args = " ".join(command_shlexed[1:])
                return f"cd {args}"
            else:
                return "cd: missing operand"
        else:
            return f"{cmd}: command not found"


class MiniShellGUI:
    def __init__(self, root, console_logic: ConsoleLogic):
        self.root = root
        self.logic = console_logic

        self.root.title("MiniShell")

        self.text = tk.Text(root, height=20, width=80,
                            bg="black", fg="lime", insertbackground="white")
        self.text.pack(padx=5, pady=5)

        self.entry = tk.Entry(root, width=80,
                              bg="black", fg="white", insertbackground="white")
        self.entry.pack(padx=5, pady=5)

        self.entry.bind("<Return>", self.execute_command)

        self.append_text(self.logic.vfs_name)

        self.entry.focus_set()

    def append_text(self, msg: str):
        self.text.insert(tk.END, msg)
        self.text.see(tk.END)

    def execute_command(self, event=None):
        command = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        self.append_text(command + "\n")

        result = self.logic.process_command(command)

        if result == "__EXIT__":
            self.root.quit()
            return

        if result:
            self.append_text(result + "\n")

        self.append_text(self.logic.vfs_name)

        self.entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    console_logic = ConsoleLogic()
    app = MiniShellGUI(root, console_logic)
    root.mainloop()