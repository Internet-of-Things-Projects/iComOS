#===============================================================================
# @brief    Scons Target Definitions File
# Copyright (c) 2019 QUECTEL LIMITED
#===============================================================================
# 
import os
import copy
from EnvironmentUtils import BuildType

target_quectel_opencpu_bc28 = {
    'platform':         'BC28',
    'binary_name':      'application',
    'chip':             'Hi2115',
    'core':             'application_core',
    'image_slot':       'apps_a',
    'type':             BuildType.ARM,
    'memory_config':    'standard',
    'os':               'LiteOS',
    'drivers_set':      'LiteOS',
    'optimisation':     '-Os',
    'unwind':           'on',   #Enable backtrace
    'support_libs':     [],
    'support_libs_whole': [],
    'defines':          [
                         '_QUECTEL_OPEN_CPU_',
                         '_MODULE_BC28_',
                        ]
}

target_quectel_opencpu_bc35g = {
    'platform':         'BC35G',
    'binary_name':      'application',
    'chip':             'Hi2115',
    'core':             'application_core',
    'image_slot':       'apps_a',
    'type':             BuildType.ARM,
    'memory_config':    'standard',
    'os':               'LiteOS',
    'drivers_set':      'LiteOS',
    'optimisation':     '-Os',
    'unwind':           'on',  
    'support_libs':     [],
    'support_libs_whole': [],
    'defines':          [
                         '_QUECTEL_OPEN_CPU_',
                         '_MODULE_BC35_G_',
                        ]
}

#===============================================================================
# Target names
#===============================================================================

# Target names to call by scons target=target_name
configs = {
    'opencpu_bc28':          target_quectel_opencpu_bc28,
    'opencpu_bc35g':         target_quectel_opencpu_bc35g,
}

# Alias names, group several targets under an alias
aliases = {
    'all':        configs.keys(),
}