import networkx as nx

class CommandGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_command(self, command, depends_on=None):
        self.graph.add_node(command)
        if depends_on:
            self.graph.add_edge(depends_on, command)

    def visualize_graph(self):
        # This function is a placeholder for graph visualization
        return nx.drawing.nx_pydot.to_pydot(self.graph)

    def get_execution_order(self):
        return list(nx.topological_sort(self.graph))
