from graph_builder import GraphBuilder
from incidence_list_reader import IncidenceListReader
from prestige_calculator import MatrixProcessor

incidence_list_path = 'data/incidence_list.txt'

incidence_list_reader = IncidenceListReader(incidence_list_path)
incidence_list_reader.read_incidents_from_file()
incidence_list = incidence_list_reader.get_incidents()





graph_builder = GraphBuilder(incidence_list)
graph_builder.draw_graph()




processor = MatrixProcessor(graph_builder.adjacency_matrix)
prestige_value = processor.calculate_prestige(specific_column=1)