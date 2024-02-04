from Core.core.models import Vertex, Graph, Edge, Forest
from Core.core.services.loading import LoadingService
import xml.etree.ElementTree as ET


class XMLLoader(LoadingService):
    def __init__(self):
        pass

    def name(self):
        return 'XML Loader'

    def id(self):
        return 'XML_Loader_plugin'

    def load(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                print(content)
                root = ET.fromstring(content)
                return root
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
        except IOError as e:
            print(f"Error: Unable to open file - {e}")

    def create_graph(self, root, graph=None, parent=None):
        if graph is None:
            graph = Graph()

        id_generator = 0
        object_name = ""

        def process_node(node, parent_vertex=None):
            v = None

            # Napravi vertex za potreban objekat
            if node.tag == object_name:
                nonlocal id_generator
                v = Vertex(id_generator)
                id_generator += 1
                for attr in node.attrib:
                    v.add_attribute(attr, node.attrib[attr])

            if node.text.strip() != "" and parent_vertex != None:       #uvek ce biti prazno za pocetak objekta
                node.text = " ".join(node.text.split())
                parent_vertex.add_attribute(node.tag, node.text)
                return

            if v is not None:
                graph.add_vertex(v)

            # Create an edge to the parent, if applicable
            if parent_vertex and node.tag == object_name:
                e = Edge(parent_vertex.id, v.id)
                parent_vertex.add_edge(e)

            # Process child nodes recursively
            for child in node:
                if v is None:
                    process_node(child, parent_vertex)
                else:
                    process_node(child, parent_vertex=v)

        # Start processing from the root node
        for item in root:
            object_name = item.tag
            process_node(item)

        self.handle_duplicates(graph)
        return graph

    def handle_duplicates(self, graph: Graph):
        set_of_vertices = []
        map_to_be_changed = {}
        for vertex in graph.vertices.values():
            is_duplicate = False
            for temp in set_of_vertices:
                if vertex == temp:
                    map_to_be_changed[vertex.id] = temp.id
                    is_duplicate = True
                    break
            if is_duplicate:
                continue
            set_of_vertices.append(vertex)

        for vertex in set_of_vertices:
            for edge in vertex.edges:
                if edge.end in map_to_be_changed.keys():
                    edge.end = map_to_be_changed[edge.end]

        graph.vertices = set_of_vertices


if __name__ == "__main__":
    loader = XMLLoader()
    # root = loader.load("D:\\FAKS\\SOFT. OBRASCI I KOMPONENTE\\Projekat 2023\\Software-patterns-and-components\\data\\test_bidirectional.xml")
    # root = loader.load("D:\\FAKS\\SOFT. OBRASCI I KOMPONENTE\\Projekat 2023\\Software-patterns-and-components\\data\\test_normal.xml")
    root = loader.load("D:\\FAKS\\SOFT. OBRASCI I KOMPONENTE\\Projekat 2023\\Software-patterns-and-components\\data\\test_cyclic.xml")
    graph = loader.create_graph(root)
    print(graph)
    f = Forest(graph)
    print(f)


