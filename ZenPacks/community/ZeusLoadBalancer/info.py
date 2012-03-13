from zope.component import adapts
from zope.interface import implements

from Products.ZenUtils.Utils import convToUnits
from Products.Zuul.decorators import info
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.device import DeviceInfo
from Products.Zuul.infos.component import ComponentInfo

from .ZeusLoadBalancer import ZeusLoadBalancer
from .ZeusPool import ZeusPool
from .ZeusVirtualServer import ZeusVirtualServer

from .interfaces import IZeusLoadBalancerInfo, IZeusVirtualServerInfo, IZeusPoolInfo


class ZeusLoadBalancerComponentInfo(ComponentInfo):
        @property
        def entity(self):
            return {
                    'uid': self._object.getPrimaryUrlPath(),
                    'name': self._object.titleOrId(),
                    }

class ZeusLoadBalancerInfo(DeviceInfo):
    implements(IZeusLoadBalancerInfo)
    adapts(ZeusLoadBalancer)
    pass
class ZeusVirtualServerInfo(ZeusLoadBalancerComponentInfo):
    implements(IZeusVirtualServerInfo)
    adapts(ZeusVirtualServer)

    vsName = ProxyProperty('vsName')
    vsPort = ProxyProperty('vsPort')
    vsProtocol = ProxyProperty('vsProtocol')

class ZeusPoolInfo(ZeusLoadBalancerComponentInfo):
    implements(IZeusPoolInfo)
    adapts(ZeusPool)

    poolName = ProxyProperty('poolName')
    poolAlgorithm = ProxyProperty('poolAlgorithm')
    poolNodes = ProxyProperty('poolNodes')
    poolDraining = ProxyProperty('poolDraining')
    poolFailPool = ProxyProperty('poolFailPool')
    poolPersistence = ProxyProperty('poolPersistence')

