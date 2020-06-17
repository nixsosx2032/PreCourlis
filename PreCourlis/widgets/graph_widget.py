import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class GraphWidget(FigureCanvas):
    def __init__(self, parent=None):
        figure = plt.figure(figsize=(15, 7))
        super().__init__(figure)

        self.graph = plt.subplot(111)

        self.previous_section = None
        self.current_section = None
        self.next_section = None

    def set_sections(self, previous_section, current_section, next_section):
        self.previous_section = previous_section
        self.current_section = current_section
        self.next_section = next_section
        self.refresh()

    def refresh(self):
        self.graph.clear()

        if self.current_section is not None:
            self.graph.plot(
                self.current_section.distances,
                self.current_section.z,
                color="red",
                label=self.current_section.name,
            )

        if self.previous_section is not None:
            self.graph.plot(
                self.previous_section.distances,
                self.previous_section.z,
                color="green",
                label=self.previous_section.name,
            )

        if self.next_section is not None:
            self.graph.plot(
                self.next_section.distances,
                self.next_section.z,
                color="blue",
                label=self.next_section.name,
            )

        self.graph.grid(True)
        self.graph.set_ylabel("Z (m)")
        self.graph.set_xlabel("Abscisse en travers (m)")
        self.draw()
