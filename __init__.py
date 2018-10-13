# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CurrentLocationTest
                                 A QGIS plugin
 Current Location Test plugin
                             -------------------
        begin                : 2018-10-09
        copyright            : (C) 2018 by Kevin Ng'eno
        email                : kngeno.kevin@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CurrentLocationTest class from file CurrentLocationTest.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .current_location_test import CurrentLocationTest
    return CurrentLocationTest(iface)
