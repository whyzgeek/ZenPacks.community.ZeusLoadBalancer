
__doc__="ZXTM Load Balancer Zen Pack"

import Globals
import os
import logging

log = logging.getLogger("zen.zenpack")

from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.DeviceClass import manage_addDeviceClass

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

import ZenPacks.community.ZeusLoadBalancer
def initialize(registrar):
    registrar.registerClass(
    ZeusPool.ZeusPool,
    permission='Add DMD Objects',
    )


class ZenPack(ZenPackBase):
    """ Zeus loader
    """

    def install(self, app):
        log.info("Installing ZXTM Zenpack...")
        if not hasattr(app.zport.dmd.Devices.Server, 'Zeus'):
            manage_addDeviceClass(app.zport.dmd.Devices.Server, 'Zeus')
        dc = app.zport.dmd.Devices.getOrganizer('Server/Zeus')
        dc.description = 'Zeus Load Balancers'
        # Do some cleanup for old properties to make
        # ZenPack upgrade safe
        flag = False
        for dev in dc.getSubDevices():
            for comp in dev.pools():
                if hasattr(comp, 'poolDraining') and \
                        type(comp.poolDraining) == type(1):
                    flag = True
                    try:    
                        del comp.poolDraining
                    except Exception, e:
                        log.warning("Couldn't clean %s/%s because %s" % \
                                                      (dev.id, comp.id, str(e)))
            if flag:
                log.info("Device %s has been successfully cleaned" % dev.id)
                flag = False
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        log.info("Upgrading ZXTM Zenpack...")
        if not hasattr(app.zport.dmd.Devices.Server, 'Zeus'):
            manage_addDeviceClass(app.zport.dmd.Devices.Server, 'Zeus')
        dc = app.zport.dmd.Devices.getOrganizer('Server/Zeus')
        dc.description = 'Zeus Load Balancers'
        # Do some cleanup for old properties to make
        # ZenPack upgrade safe
        flag = False
        for dev in dc.getSubDevices():
            for comp in dev.pools():
                if hasattr(comp, 'poolDraining') and \
                        type(comp.poolDraining) == type(1):
                    flag = True
                    try:    
                        del comp.poolDraining
                    except Exception, e:
                        log.warning("Couldn't clean %s/%s because %s" % \
                                                      (dev.id, comp.id, str(e)))
            if flag:
                log.info("Device %s has been successfully cleaned" % dev.id)
                flag = False
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        ZenPackBase.remove(self, app, leaveObjects)
