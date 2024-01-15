class IncidenceListReader:
    @staticmethod
    def read_incidents_from_file(file_path):
        incidents = []

        with open(file_path, 'r') as file:
            for line in file:
                # Split line into two parts by ":"
                parts = line.strip().split(':')

                # Extract left and right side of incyfency list
                left_side = parts[0].strip()
                right_side = parts[1].strip()

                # Split the right side into individual elements using "," as a separator
                right_side_elements = [element.strip() for element in right_side.split(',')]

                # Tuple representing the incident and add it to the list
                incident = (left_side, right_side_elements)
                incidents.append(incident)

            return incidents

    @staticmethod
    def read_incidents_from_text_widget(text_widget, tk):
        text_content = text_widget.get("1.0", tk.END)
        incidents = [line.strip().split(':') for line in text_content.splitlines() if line]
        incidents_data = [(left.strip(), [element.strip() for element in right.split(',')]) for left, right in incidents]
        return incidents_data