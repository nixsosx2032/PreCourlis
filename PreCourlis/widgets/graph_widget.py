from qgis.core import (
    QgsPoint,
    QgsGeometry,
)

from PreCourlis.core.precourlis_file import PreCourlisFileLine

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class GraphWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = plt.figure(figsize=(15, 7))
        super().__init__(self.figure)

        self.graph = plt.subplot(111)

        self.file = None
        self.feature = None
        self.previous_section = None
        self.current_section = None
        self.next_section = None

        self.position = None
        self.pointing_line = None
        self.current_section_line = None
        self.layers_lines = []
        self.layers_fills = []

    def close_figure(self):
        plt.close(self.figure)

    def set_sections(
        self, layer, feature, previous_section, current_section, next_section
    ):
        self.position = None
        self.file = PreCourlisFileLine(layer)
        self.feature = feature
        self.previous_section = previous_section
        self.current_section = current_section
        self.next_section = next_section
        self.refresh()

    def set_position(self, position):
        self.position = position
        self.refresh_pointing_line()

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
        if section.distances[0] is None:
            return
        return self.graph.plot(
            [d + offset for d in section.distances],
            section.z,
            label=section.name,
            **kwargs,
        )

    def draw_layer(self, section, layer, **kwargs):
        if section.distances[0] is None:
            return
        layer_index = section.layer_names.index(layer)

        if layer_index == 0:
            previous_values = self.current_section.z
        else:
            previous_values = section.layers_elev[layer_index]
        current_values = section.layers_elev[layer_index]

        self.layers_fills.append(
            self.graph.fill_between(
                section.distances,
                previous_values,
                current_values,
                where=current_values <= previous_values,
                facecolor=kwargs.get("color"),
                alpha=0.3,
            )
        )

        return self.graph.plot(
            section.distances, current_values, label=layer, **kwargs,
        )

    def clear(self):
        self.graph.clear()
        self.pointing_line = None
        self.current_section_line = None
        self.layers_lines = []
        self.layers_fills = []

    def refresh(self):
        self.clear()

        axis_pos = self.axis_position(self.current_section)

        if self.previous_section:
            self.draw_section(
                self.previous_section,
                axis_pos - self.axis_position(self.previous_section),
                color="green",
                linewidth=0.5,
            )

        self.refresh_current_section(False)

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
            lines,
            labels,
            loc="upper center",
            fancybox=True,
            shadow=True,
            ncol=4,
            prop={"size": 10},
        )

        self.draw()

    def refresh_current_section(self, draw=True):
        if self.current_section_line is not None:
            [line.remove() for line in self.current_section_line]
            self.current_section_line = None

            [line.remove() for col in self.layers_lines for line in col]
            self.layers_lines = []

            [poly.remove() for poly in self.layers_fills]
            self.layers_fills = []

        if self.current_section is None:
            return
        self.current_section_line = self.draw_section(
            self.current_section, 0, color="red", marker=".", zorder=10,
        )

        for layer in self.file.layers():
            self.layers_lines.append(
                self.draw_layer(
                    self.current_section,
                    layer,
                    color=self.file.layer_color(layer),
                    zorder=1,
                )
            )

        if draw:
            self.draw()

    def refresh_pointing_line(self, draw=True):
        if self.pointing_line is not None:
            self.pointing_line.remove()
            self.pointing_line = None
        if self.position is not None:
            self.pointing_line = self.graph.axvline(self.position, color="purple")
        if draw:
            self.draw()
