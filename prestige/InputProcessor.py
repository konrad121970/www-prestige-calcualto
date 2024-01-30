from tkinter import filedialog

import tk


class InputProcessor:
    @staticmethod
    def transform_input_to_dict(input_str):
        relationships = {}

        lines = input_str.strip().split('\n')

        for line in lines:
            parts = line.split(':')
            key = parts[0].strip().split()[-1]
            values = [v.strip().split()[-1] for v in parts[1].split(',')] if parts[1].strip() != '' else []
            relationships[key] = values

        return relationships

    @staticmethod
    def load_from_file(self):
        file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Text Files", "*.txt")])

        if file_path:
            with open(file_path, 'r') as file:
                incidence_list = file.read()

            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, incidence_list)

            # Trigger processing after loading from the file
            self.process_input()


