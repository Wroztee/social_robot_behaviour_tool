import base64
from requests import get


class GraphHandler():
    def __init__(self, type: str = "graph LR"):
        self.type = type
        self.connections = {}
        self.string = f"{type};\n"

        self.save_graph_png()


    def add_connection(self, nodes : dict):
        for source_node in nodes:
            if nodes[source_node] == {}:
                if not source_node in self.connections:
                    self.string += f"{source_node.replace(" ", "_")}({source_node});\n"
                    self.connections[source_node] = []
                continue

            for target_node in nodes[source_node]:
                if source_node in self.connections and target_node in self.connections[source_node]:
                    if nodes[source_node][target_node] != {}:
                        self.add_connection({target_node : nodes[source_node][target_node]})
                    continue

                source_string = f"{source_node.replace(" ", "_")}"
                if not source_node in self.connections:
                    source_string += f"({source_node})"
                    self.connections[source_node] = []

                target_string = f"{target_node.replace(" ", "_")}"
                if not target_node in self.connections:
                    target_string += f"({target_node})"
                    self.connections[target_node] = []

                self.string += f"{source_string} --> {target_string};\n"
                self.connections[source_node].append(target_node)

                if nodes[source_node][target_node] != {}:
                    self.add_connection({target_node : nodes[source_node][target_node]})


    def save_graph_png(self, path: str = "graph.png"):
        graphbytes = self.string.encode("utf8")
        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")
        img = get("https://mermaid.ink/img/" + base64_string).content
        with open(path, "wb") as png:
            png.write(img)
