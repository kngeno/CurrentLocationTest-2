# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CurrentLocationTest
                                 A QGIS plugin
 Current Location Test plugin
                              -------------------
        begin                : 2018-10-09
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Kevin Ng'eno
        email                : kngeno.kevin@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os.path
import datetime
import time
import ogr
from PyQt4.QtCore import *
from PyQt4.QtGui import QAction, QIcon
from qgis.core import (
    QgsFeature, QgsField, QgsFields,
    QgsGeometry, QgsPoint, QgsVectorFileWriter,
    QgsCoordinateReferenceSystem, QgsMapLayerRegistry,
    QgsProject, QgsVectorLayer
    )
from qgis.gui import QgsMessageBar
from qgis.utils import QGis, iface
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from current_location_test_dialog import CurrentLocationTestDialog


class CurrentLocationTest:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CurrentLocationTest_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Current Location Test')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'CurrentLocationTest')
        self.toolbar.setObjectName(u'CurrentLocationTest')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CurrentLocationTest', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = CurrentLocationTestDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/CurrentLocationTest/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Current Location Test'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Current Location Test'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.

            # current user home path
            filename = os.path.abspath("current_point_feature.shp")

            # load to map canvas
            layer = iface.activeLayer()        

            # Export a vector layer directly from features
            # define fields for feature attributes. A QgsFields object is needed
            fields = QgsFields()
            fields.append(QgsField("DATE", QVariant.String))

            writer = QgsVectorFileWriter(
                filename, "UTF8", fields, QGis.WKBPoint, QgsCoordinateReferenceSystem(4326), "ESRI Shapefile")

            iface.messageBar().pushMessage("Shapefile attributes successfully created.", QgsMessageBar.INFO)
            # create shapefile to disk
            layers = QgsVectorLayer(filename, "Current Location", "ogr")

            if not layers.isValid():
                print "Layers %s did not load" % layers.name()
                iface.messageBar().pushMessage("Error creating shapefile.", QgsMessageBar.CRITICAL)
            iface.messageBar().pushMessage("Shapefile successfully created.", QgsMessageBar.INFO)
            # style option
            
            # add layer to map canvas
            QgsMapLayerRegistry.instance().addMapLayers([layers])
            iface.messageBar().pushMessage("Shapefile added to map canvas.", QgsMessageBar.INFO)

            # check the attributes have been added
            if writer.hasError() != QgsVectorFileWriter.NoError:
                print("Error when creating shapefile: ", writer.errorMessage())
                iface.messageBar().pushMessage("Feature addition failed.", QgsMessageBar.CRITICAL)

            # Add a feature
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry().fromPoint(QgsPoint(36.5, -0.43)))
            
            # variable for date attribute
            value = time.strftime("%Y-%m-%d")
           
            # Add date value to date attribute
            fet.setAttributes([value])
            writer.addFeature(fet)

            # set datetime variable
            d = datetime.datetime.now()
            dt = d.strftime("%Y-%m-%d-%H:%M:%S")
            file =QFileInfo(os.path.abspath('Current Location_'+dt+'.qgs'))
            project = QgsProject.instance()
            project.write(file)
            # Delete the writer to flush features to disk
            # del writer

            # Load project
            # project.read(file)
