# Import built-in modules
import os
import sys
from functools import partial

# Import third-party modules
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from pymxs import runtime as rt

# Import local modules
maxscirpt_path = rt.GetDir(rt.Name("userScripts"))
if maxscirpt_path not in sys.path:
    sys.path.append(maxscirpt_path)

from max_shelves.paths import get_script_search_paths
from max_shelves.paths import resolve_paths
from max_shelves.paths import resolve_tools

SHELVE_ICON_SIZE = 32


def get_layout(main_window):
    widget = filter_widget(main_window, QtWidgets.QWidget,
                           "QmaxTimeSliderDockWidget")
    return filter_widget(widget, QtWidgets.QLayout, "QVBoxLayout")


def filter_widget(widget, filter_type, filter_name):
    for w in widget.findChildren(filter_type):
        if w.metaObject().className() == filter_name:
            return w
    raise RuntimeError('Could not find {} instance.'.format(filter_name))


def execute_script(item):
    file_path = item['script']
    if file_path.endswith(".py"):
        rt.python.executeFile(file_path)
    else:
        rt.filein(file_path)


def create_tabs(data):
    tab_info = {}
    main_tab = QtWidgets.QTabWidget()
    for key, value in data.items():
        widget = script_plane(value)
        main_tab.addTab(widget, key)
        tab_info[key] = widget
    return main_tab


def set_icon(button, icon_file):
    """Set the icon to script item."""
    icon = QtGui.QIcon(icon_file)
    button.setIcon(icon)


def script_plane(items):
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout()
    for item in items:
        button = QtWidgets.QPushButton(item["name"])
        button.clicked.connect(partial(execute_script, item))
        button.setMinimumSize(SHELVE_ICON_SIZE, SHELVE_ICON_SIZE)
        button.setMaximumSize(SHELVE_ICON_SIZE, SHELVE_ICON_SIZE)
        button.setIconSize(QtCore.QSize(SHELVE_ICON_SIZE, SHELVE_ICON_SIZE))
        button.setToolTip(item.get("description", item["name"]))
        icon = item['icon']
        if os.path.isfile(icon):
            set_icon(button, item['icon'])
        layout.addWidget(button)
    layout.addStretch()
    widget.setLayout(layout)
    return widget


def get_main_widget():
    """Get 3dsmax main window."""
    return QtWidgets.QWidget.find(rt.windows.getMAXHWND())


def main():
    main_window = get_main_widget()
    layout = get_layout(main_window)
    paths = get_script_search_paths()
    tools = resolve_paths(paths)
    data = resolve_tools(tools)
    main_tab = create_tabs(data)
    layout.insertWidget(0, main_tab)


if __name__ == '__main__':
    main()
