# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 22:22:12 2022

@author: Brale
"""

relrms = ERTManager.inv.relrms()
model = np.array(ERTManager.inv.model)
response = np.array(ERTManager.inv.response)

absrms = ERTManager.inv.absrms()