from qgis.core import (
    QgsPoint,
    QgsGeometry,
)

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

    def clear(self):
        self.graph.clear()

    def axis_position(self, section):
        """
        Return linear referencing of axis intersection for passed section.
        """
        f = section.feature
        intersection = QgsGeometry(
            QgsPoint(f.attribute("axis_x"), f.attribute("axis_y"))
        )
        return f.geometry().lineLocatePoint(intersection)

    def refresh(self):
        self.clear()

        axis_pos = self.axis_position(self.current_section)

        for section, color in (
            (self.previous_section, "green"),
            (self.next_section, "blue"),
        ):
            if section is not None:
                offset = axis_pos - self.axis_position(section)
                self.graph.plot(
                    [d + offset for d in section.distances],
                    section.z,
                    color=color,
                    label=section.name,
                )

        self.graph.plot(
            self.current_section.distances,
            self.current_section.z,
            color="red",
            label=self.current_section.name,
        )

        # Draw axis position
        self.graph.axvline(axis_pos, color="black")

        self.graph.grid(True)
        self.graph.set_ylabel("Z (m)")
        self.graph.set_xlabel("Abscisse en travers (m)")
        self.draw()
