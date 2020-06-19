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

        self.position = None
        self.pointing_line = None

    def set_sections(self, previous_section, current_section, next_section):
        self.position = None
        self.previous_section = previous_section
        self.current_section = current_section
        self.next_section = next_section
        self.refresh()

    def set_position(self, position):
        self.position = position
        self.refresh_pointing_line()

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

    def draw_section(self, section, offset, **kwargs):
        self.graph.plot(
            [d + offset for d in section.distances],
            section.z,
            label=section.name,
            **kwargs,
        )

    def refresh(self):
        self.clear()
        self.pointing_line = None

        axis_pos = self.axis_position(self.current_section)

        if self.previous_section:
            self.draw_section(
                self.previous_section,
                axis_pos - self.axis_position(self.previous_section),
                color="green",
                linewidth=0.5,
            )

        self.draw_section(
            self.current_section,
            0,
            color="red",
            marker=".",
            zorder=10,
        )

        if self.next_section:
            self.draw_section(
                self.next_section,
                axis_pos - self.axis_position(self.next_section),
                color="blue",
                linewidth=0.5,
            )

        # Draw axis position
        self.graph.axvline(axis_pos, color="black")

        self.graph.grid(True)
        self.graph.set_ylabel("Z (m)")
        self.graph.set_xlabel("Abscisse en travers (m)")

        lines, labels = self.graph.get_legend_handles_labels()
        self.graph.legend(
            lines, labels, loc="upper center", fancybox=True, shadow=True, ncol=4, prop={"size": 10}
        )

        self.draw()

    def refresh_pointing_line(self):
        if self.pointing_line != None:
            self.pointing_line.remove()
            self.pointing_line = None
        if self.position is not None:
            self.pointing_line = self.graph.axvline(self.position, color="purple")
        self.draw()
