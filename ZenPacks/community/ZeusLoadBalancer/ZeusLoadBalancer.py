from Globals import InitializeClass
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import *

import copy

class ZeusLoadBalancer(Device):
    "Zeus Load Balancer Device"

    portal_type = meta_type = 'ZeusLoadBalancer'

    _relations = Device._relations + (
    ('pools', ToManyCont(ToOne, "ZenPacks.community.ZeusLoadBalancer.ZeusPool", "zeus")),
    ) + (
    ('virtualServers', ToManyCont(ToOne, "ZenPacks.community.ZeusLoadBalancer.ZeusVirtualServer", "zeus")),
    ) 
    

    

InitializeClass(ZeusLoadBalancer)
