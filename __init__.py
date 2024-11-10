# -*- coding: utf-8 -*-
"""
/***************************************************************************
 pec
                                 A QGIS plugin
 software cientifico para avaliação da acurácia posicional de dados espaciais
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-02-08
        copyright            : (C) 2024 by UFV
        email                : afonso.santos@ufv.br
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
    """Load pec class from file pec.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .GeoPEC import pec
    return pec(iface)
