import importlib
import os
import sys
import tkinter as tk
from subprocess import run
from tkinter import NSEW, DISABLED, NORMAL, END

# Insertion du dossier /src dans le path pour pouvoir utiliser parse_program et ses imports
sys.path.insert(0, './src/')
from src.utils import parse_program


def get_scripts():
    """Returns the list of every executables in ./src, except the ones in the given_by_uni list"""
    given_by_uni = ["jsast.py", "utils.py"]
    src_dir = os.path.join(os.getcwd(), "src")
    return [file for file in os.listdir(src_dir)
            if os.path.isfile(os.path.join(src_dir, file))
            and file.endswith(".py")
            and file not in given_by_uni]


def get_examples():
    """Returns the list of every 'compact' examples in ./exemples"""
    examples_dir = os.path.join(os.getcwd(), "exemples")
    return [file for file in os.listdir(examples_dir)
            if os.path.isfile(os.path.join(examples_dir, file))
            and file.endswith("-compact.json")]


def read_matching_source(file_path):
    """Returns the content of the source file (.js) that matches the passed file-compact (.json)"""
    file_path = file_path.removesuffix('-compact.json')
    file_path += '.js'
    with open(file_path, "r") as f:
        content = f.read()
    return content


class App:
    def __init__(self, root_frame: tk.Tk):
        self.executable = ""
        self.example = ""
        self.executables_list: tk.Listbox = None
        self.examples_list: tk.Listbox = None
        self.__init_gui(root_frame)

    def __init_gui(self, root_frame: tk.Tk):
        # Create the main window
        root_frame.title("Sélectionnez un exécutable et un fichier exemple à lui passer en argument")
        root_frame.columnconfigure(0, weight=1)
        root_frame.columnconfigure(1, weight=1)
        root_frame.rowconfigure(0, weight=1)
        root_frame.rowconfigure(1, weight=1)

        self.__init_top_left_panel(root_frame)
        self.__init_top_right_panel(root_frame)
        self.__init_bottom_left_panel(root_frame)
        self.__init_bottom_right_panel(root_frame)

    def __init_top_left_panel(self, root_frame):
        # Create the first panel with 2 listboxes
        lists_panel = tk.Frame(root_frame, relief="solid", bd=1, pady=10, padx=20)
        lists_panel.grid(row=0, column=0, sticky=NSEW)
        inner_frame = tk.Frame(lists_panel)
        inner_frame.grid(row=0, column=0, sticky=NSEW)

        lists_panel.columnconfigure(0, weight=1)
        lists_panel.rowconfigure(0, weight=1)
        inner_frame.columnconfigure(0, weight=1)
        inner_frame.columnconfigure(1, weight=1)
        inner_frame.rowconfigure(0, weight=1)

        executables_panel = tk.Frame(inner_frame)
        executables_panel.grid(row=0, column=0, sticky=NSEW)
        examples_panel = tk.Frame(inner_frame)
        examples_panel.grid(row=0, column=1, sticky=NSEW)

        executables_panel.columnconfigure(0, weight=1)
        executables_panel.rowconfigure(0, weight=1)
        examples_panel.columnconfigure(0, weight=1)
        examples_panel.rowconfigure(0, weight=1)

        self.executables_list = tk.Listbox(executables_panel, font=("Consolas", 13))
        self.executables_list.grid(row=0, column=0, sticky=NSEW)
        self.examples_list = tk.Listbox(examples_panel, font=("Consolas", 13))
        self.examples_list.grid(row=0, column=0, sticky=NSEW)
        self.__init_lists()

        # Create the "Run" button
        self.run_button = tk.Button(lists_panel, text="Sélectionnez un exécutable et un fichier .json",
                                    command=self.run_selection)
        self.run_button.grid(row=1, column=0, sticky=NSEW)
        self.run_button.config(font=("Arial", 12, "bold"), bg="grey", relief="solid", bd=2, padx=10, pady=5,
                               state=DISABLED)

    def __init_top_right_panel(self, root_frame):
        # Create the file reader panel that will be used to display the source code matching the selected file
        file_reader_frame = tk.Frame(root_frame, relief="solid", bd=1, pady=10, padx=20)
        file_reader_frame.grid(row=0, column=1, sticky=NSEW)
        self.file_text = tk.Text(file_reader_frame)
        self.file_text.pack(fill=tk.BOTH, expand=True)
        self.file_text.config(background="grey82")
        self.file_text.insert(tk.END, "Lecture du code source correspondant")
        self.file_text.config(state=DISABLED)

    def __init_bottom_left_panel(self, root_frame):
        # Create the AST display panel that will be used to display the AST (named tuples) matching the selected file
        ast_frame = tk.Frame(root_frame, relief="solid", bd=1, pady=10, padx=20)
        ast_frame.grid(row=1, column=0, sticky=NSEW)
        self.ast_text = tk.Text(ast_frame)
        self.ast_text.pack(fill=tk.BOTH, expand=True)
        self.ast_text.config(background="grey87", font=('Arial', 11))
        self.ast_text.insert(tk.END, "named_tuples correspondant à l'AST interprété")
        self.ast_text.config(state=DISABLED)

    def __init_bottom_right_panel(self, root_frame):
        # Create the output panel
        output_frame = tk.Frame(root_frame, relief="solid", bd=1, pady=10, padx=20)
        output_frame.grid(row=1, column=1, sticky=NSEW)
        self.output_text = tk.Text(output_frame)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.config(background="grey87")
        self.output_text.insert(tk.END, "Résultat de l'exécution du programme")
        self.output_text.config(state=DISABLED)

    def __init_lists(self):
        scripts = get_scripts()
        scripts.sort()
        for script in scripts:
            self.executables_list.insert(tk.END, script)
        examples = get_examples()
        examples.sort()
        for example in examples:
            self.examples_list.insert(tk.END, example)
        self.executables_list.bind("<<ListboxSelect>>", self.on_executable_select)
        self.examples_list.bind("<<ListboxSelect>>", self.on_example_select)

    def on_executable_select(self, _):
        selected_index = self.executables_list.curselection()
        if len(selected_index) > 0:
            selected_index = selected_index[0]
            self.executable = self.executables_list.get(selected_index)

            # Clear background of all other indices
            for index in range(self.executables_list.size()):
                if index != selected_index:
                    self.executables_list.itemconfig(index, background='white')
            self.executables_list.itemconfig(selected_index, background='lightblue')
        if self.executable and self.example:
            self.__enable_run()

    def on_example_select(self, _):
        selected_index = self.examples_list.curselection()
        if len(selected_index) > 0:
            selected_index = selected_index[0]
            self.example = self.examples_list.get(selected_index)

            # Cleaning the previous file's content display before displaying the currently selected one
            self.file_text.config(state=NORMAL)
            self.file_text.delete("1.0", tk.END)
            self.file_text.insert(tk.END, read_matching_source(f"exemples/{self.example}"))
            self.file_text.config(state=DISABLED)

            # Clear background of all other indices
            for index in range(self.examples_list.size()):
                if index != selected_index:
                    self.examples_list.itemconfig(index, background='white')
            self.examples_list.itemconfig(selected_index, background='lightblue')
        if self.executable and self.example:
            self.__enable_run()

    def __enable_run(self):
        self.run_button.config(bg="light sky blue", text=f"Exécuter {self.executable} sur {self.example}", state=NORMAL)

    def run_selection(self):
        # Cleaning the displays between each run
        self.ast_text.config(state=NORMAL)
        self.output_text.config(state=NORMAL)
        self.ast_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

        command = f"python3 src/{self.executable} exemples/{self.example}"
        print(f"######\nEXECUTING\t {self.executable}\t ON\t {self.example}\t :\n>> {command}\n######\n")

        self.__handle_ast_text()

        result = run(command, shell=True, capture_output=True)

        self.__display_std_from_exe(result)
        self.ast_text.config(state=DISABLED)
        self.output_text.config(state=DISABLED)

    def __display_std_from_exe(self, result):
        output = result.stdout  # Redirecting any outputs from the executed program into the output text panel
        errors = result.stderr
        self.output_text.insert(tk.END, output)
        print(output)
        print("\n")
        if errors:
            self.output_text.insert(tk.END, errors)
            print(errors)

    def __handle_ast_text(self):
        """Puts in bold every named tuples found in jsast.py from the ast when displaying the ast in self.ast_text"""
        ast = parse_program(f"exemples/{self.example}")
        print(str(ast))
        print("\n")
        named_tuples = importlib.import_module("src.jsast")
        str_ast = str(ast)
        self.ast_text.insert(tk.END, str_ast)
        for name in dir(named_tuples):
            self.ast_text.tag_configure('bold', font=('Arial', 11, 'bold'))
            start = '1.0'
            while True:
                start = self.ast_text.search(name, start, END)
                if not start:
                    break
                start = self.ast_text.index(start)
                end = f'{start}+{len(name)}c'
                self.ast_text.tag_add('bold', start, end)
                start = end


if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.attributes('-zoomed', True)
    except:
        print("Couldn't start zoomed in")
    app = App(root)
    root.mainloop()
