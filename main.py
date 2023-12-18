from graph_builder import GraphBuilder
from incidence_list_reader import IncidenceListReader

incidence_list_path = 'resources/incidence_list.txt'

incidence_list_reader = IncidenceListReader(incidence_list_path)
incidence_list_reader.read_incidents_from_file()

incidence_list = incidence_list_reader.get_incidents()

print(incidence_list)

graph_builder = GraphBuilder(incidence_list)
graph_builder.draw_graph()
