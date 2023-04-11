# -*- coding: utf-8 -*-

from qgis.core import QgsProject
from qgis.PyQt.QtCore import QSettings


class UserSetting(object):
    def __init__(self, name, type=str, default=None):
        self.name = name
        self.type = type
        self.default = default

    def __get__(self, instance, owner):
        return instance._qsettings.value(self.name, self.default, type=self.type)

    def __set__(self, instance, value):
        instance._qsettings.setValue(self.name, value)

    def __delete__(self, instance):
        instance._qsettings.remove(self.name)


class ProjectSetting(object):
    def __init__(self, name, type=[str, float, bool], default=None):
        self.name = name
        self.type = type
        self.default = default

    def __get__(self, instance, owner):
        if self.type == str:
            value, ok = QgsProject.instance().readEntry(
                instance.project_scope, self.name
            )
        elif self.type == float:
            value, ok = QgsProject.instance().readDoubleEntry(
                instance.project_scope, self.name
            )
        elif self.type == bool:
            value, ok = QgsProject.instance().readBoolEntry(
                instance.project_scope, self.name
            )
        else:
            raise NotImplementedError(f"Type not supported: {self.type}")
        return value if ok else self.default

    def __set__(self, instance, value):
        QgsProject.instance().writeEntry(instance.project_scope, self.name, value)

    def __delete__(self, instance):
        QgsProject.instance().removeEntry(instance.project_scope, self.name)


class Settings(object):
    group = "PreCourlis"
    project_scope = "PreCourlis"
    spin_box_min = -999999.0

    def __init__(self):
        self._qsettings = QSettings()
        self._qsettings.beginGroup(self.group)

    def get_spin_box_min(self):
        return self.spin_box_min

    default_elevation = ProjectSetting("default_elevation", float, spin_box_min)


settings = Settings()
