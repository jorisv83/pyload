# -*- coding: utf-8 -*-
"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.
    
    @author: mkaay
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ConnectionManager(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        mainLayout = QHBoxLayout()
        buttonLayout = QVBoxLayout()
        
        connList = QListWidget()
        
        new = QPushButton("New")
        edit = QPushButton("Edit")
        remove = QPushButton("Remove")
        connect = QPushButton("Connect")
        
        mainLayout.addWidget(connList)
        mainLayout.addLayout(buttonLayout)
        
        buttonLayout.addWidget(new)
        buttonLayout.addWidget(edit)
        buttonLayout.addWidget(remove)
        buttonLayout.addStretch()
        buttonLayout.addWidget(connect)
        
        self.setLayout(mainLayout)
        
        self.new = new
        self.connectb = connect
        self.remove = remove
        self.editb = edit
        self.connList = connList
        self.edit = self.EditWindow()
        self.connectSignals()
    
    def connectSignals(self):
        self.connect(self, SIGNAL("setConnections(connections)"), self.setConnections)
        self.connect(self.new, SIGNAL("clicked()"), self.slotNew)
        self.connect(self.editb, SIGNAL("clicked()"), self.slotEdit)
        self.connect(self.remove, SIGNAL("clicked()"), self.slotRemove)
        self.connect(self.connectb, SIGNAL("clicked()"), self.slotConnect)
        self.connect(self.edit, SIGNAL("save"), self.slotSave)
    
    def setConnections(self, connections):
        self.connList.clear()
        for conn in connections:
            item = QListWidgetItem()
            item.setData(Qt.DisplayRole, QVariant(conn["name"]))
            item.setData(Qt.UserRole, QVariant(conn))
            self.connList.addItem(item)
            if conn["default"]:
                self.connList.setCurrentItem(item)
    
    def slotNew(self):
        data = {"id":uuid().hex, "type":"remote", "default":False, "name":"", "host":"", "ssl":False, "port":"7227", "user":"admin"}
        self.edit.setData(data)
        self.edit.show()
    
    def slotEdit(self):
        item = self.connList.currentItem()
        data = item.data(Qt.UserRole).toPyObject()
        tmp = {}
        for k, d in data.items():
            tmp[str(k)] = d
        data = tmp
        self.edit.setData(data)
        self.edit.show()
    
    def slotRemove(self):
        item = self.connList.currentItem()
        data = item.data(Qt.UserRole).toPyObject()
        tmp = {}
        for k, d in data.items():
            tmp[str(k)] = d
        data = tmp
        self.emit(SIGNAL("removeConnection"), data)
    
    def slotConnect(self):
        item = self.connList.currentItem()
        data = item.data(Qt.UserRole).toPyObject()
        tmp = {}
        for k, d in data.items():
            tmp[str(k)] = d
        data = tmp
        self.emit(SIGNAL("connect"), data)
    
    def slotSave(self, data):
        self.emit(SIGNAL("saveConnection"), data)
        
    class EditWindow(QWidget):
        def __init__(self):
            QWidget.__init__(self)
            
            grid = QGridLayout()
            
            nameLabel = QLabel("Name:")
            hostLabel = QLabel("Host:")
            sslLabel = QLabel("SSL:")
            localLabel = QLabel("Local:")
            userLabel = QLabel("User:")
            portLabel = QLabel("Port:")
            
            name = QLineEdit()
            host = QLineEdit()
            ssl = QCheckBox()
            local = QCheckBox()
            user = QLineEdit()
            port = QSpinBox()
            port.setRange(1,10000)
            
            save = QPushButton("Save")
            cancel = QPushButton("Cancel")
            
            grid.addWidget(nameLabel,  0, 0)
            grid.addWidget(name,       0, 1)
            grid.addWidget(localLabel, 1, 0)
            grid.addWidget(local,      1, 1)
            grid.addWidget(hostLabel,  2, 0)
            grid.addWidget(host,       2, 1)
            grid.addWidget(sslLabel,   4, 0)
            grid.addWidget(ssl,        4, 1)
            grid.addWidget(userLabel,  5, 0)
            grid.addWidget(user,       5, 1)
            grid.addWidget(portLabel,  3, 0)
            grid.addWidget(port,       3, 1)
            grid.addWidget(cancel,     6, 0)
            grid.addWidget(save,       6, 1)
            
            self.setLayout(grid)
            self.controls = {}
            self.controls["name"] = name
            self.controls["host"] = host
            self.controls["ssl"] = ssl
            self.controls["local"] = local
            self.controls["user"] = user
            self.controls["port"] = port
            self.controls["save"] = save
            self.controls["cancel"] = cancel
            
            self.connect(cancel, SIGNAL("clicked()"), self.hide)
            self.connect(save, SIGNAL("clicked()"), self.slotDone)
            self.connect(local, SIGNAL("stateChanged(int)"), self.slotLocalChanged)
            
            self.id = None
            self.default = None
        
        def setData(self, data):
            self.id = data["id"]
            self.default = data["default"]
            self.controls["name"].setText(data["name"])
            if data["type"] == "local":
                data["local"] = True
            else:
                data["local"] = False
            self.controls["local"].setChecked(data["local"])
            if not data["local"]:
                self.controls["ssl"].setChecked(data["ssl"])
                self.controls["user"].setText(data["user"])
                self.controls["port"].setValue(int(data["port"]))
                self.controls["host"].setText(data["host"])
                self.controls["ssl"].setDisabled(False)
                self.controls["user"].setDisabled(False)
                self.controls["port"].setDisabled(False)
                self.controls["host"].setDisabled(False)
            else:
                self.controls["ssl"].setChecked(False)
                self.controls["user"].setText("")
                self.controls["port"].setValue(1)
                self.controls["host"].setText("")
                self.controls["ssl"].setDisabled(True)
                self.controls["user"].setDisabled(True)
                self.controls["port"].setDisabled(True)
                self.controls["host"].setDisabled(True)
        
        def slotLocalChanged(self, val):
            if val == 2:
                self.controls["ssl"].setDisabled(True)
                self.controls["user"].setDisabled(True)
                self.controls["port"].setDisabled(True)
                self.controls["host"].setDisabled(True)
            elif val == 0:
                self.controls["ssl"].setDisabled(False)
                self.controls["user"].setDisabled(False)
                self.controls["port"].setDisabled(False)
                self.controls["host"].setDisabled(False)
        
        def getData(self):
            d = {}
            d["id"] = self.id
            d["default"] = self.default
            d["name"] = self.controls["name"].text()
            d["local"] = self.controls["local"].isChecked()
            d["ssl"] = str(self.controls["ssl"].isChecked())
            d["user"] = self.controls["user"].text()
            d["host"] = self.controls["host"].text()
            d["port"] = self.controls["port"].value()
            if d["local"]:
                d["type"] = "local"
            else:
                d["type"] = "remote"
            return d
        
        def slotDone(self):
            data = self.getData()
            self.hide()
            self.emit(SIGNAL("save"), data)