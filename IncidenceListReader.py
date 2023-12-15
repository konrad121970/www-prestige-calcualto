class IncidenceListReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.incidents = []

    def read_incidents_from_file(self):
        with open(self.file_path, 'r') as file:
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
                self.incidents.append(incident)

    def get_incidents(self):
        return self.incidents
