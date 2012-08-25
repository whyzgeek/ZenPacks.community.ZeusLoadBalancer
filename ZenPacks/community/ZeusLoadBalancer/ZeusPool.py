from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits
from math import isnan
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class ZeusPool(DeviceComponent, ManagedEntity):
    "Zeus Pool Information"
    
    portal_type = meta_type = 'ZeusPool'
    collectors = ('zeuscollector', 'zencommand', 
                              'zenping')

    poolName = ""
    poolAlgorithm = -1
    poolNodes = -1
    poolState = -1
    poolDisabled = -1
    poolFailPool = ""
    poolPersistence = -1
    poolActiveNodes = -1
    poolDraining = -1
    snmpindex = -1

    _properties = (
        dict(id='poolName', type='string',  **_kw),
        dict(id='poolAlgorithm', type='int',  **_kw),
        dict(id='poolNodes', type='int',  **_kw),
        dict(id='poolState', type='int',  **_kw),
        dict(id='poolFailPool', type='string',  **_kw),
        dict(id='poolPersistence',type='int',  **_kw)
    )

    _relations = (
        ('zeus', ToOne(ToManyCont, 'ZenPacks.community.ZeusLoadBalancer.ZeusLoadBalancer', 'pools')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = ({
                'actions': ({
                    'id': 'perfConf',
                    'name': 'Template',
                    'action': 'objTemplates',
                    'permissions': (ZEN_CHANGE_SETTINGS,),
                    },),
                    },)

    def device(self):
        return self.zeus()

    def managedDeviceLink(self):
        from Products.ZenModel.ZenModelRM import ZenModelRM
        d = self.getDmdRoot("Devices").findDevice(self.poolName)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0

    def poolDraining(self):
        poolDraining = self.cacheRRDValue("poolDraining")
        if poolDraining is not None and not isnan(poolDraining):
            return int(poolDraining)
        return -1

    def poolDisabled(self):
        poolDisabled = self.cacheRRDValue("poolDisabled")
        if poolDisabled is not None and not isnan(poolDisabled):
            return int(poolDisabled)
        return -1

    def poolActiveNodes(self):
        poolActiveNodes = self.cacheRRDValue("poolActiveNodes")
        if poolActiveNodes is not None and not isnan(poolActiveNodes):
            return int(poolActiveNodes)
        return -1

    def manage_deleteComponent(self, REQUEST=None):
        """
        Delete Pool
        """
        url = None
        if REQUEST is not None:
            url = self.device().pools.absolute_url()
        self.getPrimaryParent()._delObject(self.id)
        if REQUEST is not None:
                REQUEST['RESPONSE'].redirect(url)


InitializeClass(ZeusPool)
