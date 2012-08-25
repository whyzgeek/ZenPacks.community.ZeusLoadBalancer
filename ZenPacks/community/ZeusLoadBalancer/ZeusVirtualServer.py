from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class ZeusVirtualServer(DeviceComponent, ManagedEntity):
    "Zeus Virtual Server Information"
    
    portal_type = meta_type = 'ZeusVirtualServer'
    collectors = ('zeuscollector', 'zencommand',
                                              'zenping')
    vsName = ""
    vsPort = 0
    vsProtocol = -1
    snmpindex = -1
    vsDefaultTrafficPool = ""

    _properties = (
        dict(id='vsName', type='string',  **_kw),
        dict(id='vsPort', type='int',  **_kw),
        dict(id='vsProtocol', type='int',  **_kw),
        dict(id='vsDefaultTrafficPool', type='string',  **_kw)
    )

    _relations = (
        ('zeus', ToOne(ToManyCont, 'ZenPacks.community.ZeusLoadBalancer.ZeusLoadBalancer', 'virtualServers')),
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
        d = self.getDmdRoot("Devices").findDevice(self.vsName)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0

    def manage_deleteComponent(self, REQUEST=None):
        """
        Delete VS
        """
        url = None
        if REQUEST is not None:
            url = self.device().virtualServers.absolute_url()
        self.getPrimaryParent()._delObject(self.id)
        if REQUEST is not None:
                REQUEST['RESPONSE'].redirect(url)


InitializeClass(ZeusVirtualServer)
