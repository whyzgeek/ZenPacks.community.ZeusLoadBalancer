from zope.component import adapts
from zope.interface import implements

from Products.ZenUtils.Utils import convToUnits
from Products.Zuul.decorators import info
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.device import DeviceInfo
from Products.Zuul.infos.component import ComponentInfo
import logging
log = logging.getLogger('zeus.info')

from .ZeusLoadBalancer import ZeusLoadBalancer
from .ZeusPool import ZeusPool
from .ZeusVirtualServer import ZeusVirtualServer

from .interfaces import IZeusLoadBalancerInfo, IZeusVirtualServerInfo, IZeusPoolInfo

algorithmMap = {
    1 :  'roundrobin',
    2 :  'weightedRoundRobin',
    3 :  'perceptive',
    4 :  'leastConnections',
    5 :  'fastestResponseTime',
    6 :  'random',
    7 :  'weightedLeastConnections',
    -1:  'not collected'
    }

persistenceMap = {
    1 : 'none',
    2 : 'ip',
    3 : 'rule',
    4 : 'transparent',
    5 : 'applicationCookie',
    6 : 'xZeusBackend',
    7 : 'ssl',
    -1: 'not collected'   
    }

poolStateMap = {
        1 : 'active',
        2 : 'disabled',
        3 : 'draining',
        4 : 'unused',
        5 : 'unknown',
        -1: 'not collected'
        }

vsProtocolMap = {
        1 : 'http',
        2 : 'https',
        3 : 'ftp',
        4 : 'imaps',
        5 : 'imapv2',
        6 : 'imapv3',
        7 : 'imapv4',
        8 : 'pop3',
        9 : 'pop3s',
        10: 'smtp',
        11: 'ldap',
        12: 'ldaps',
        13: 'telnet',
        14: 'sslforwarding',
        15: 'udpstreaming',
        16: 'udp',
        17: 'dns',
        18: 'genericserverfirst',
        19: 'genericclientfirst',
        20: 'dnstcp',
        21: 'sipudp',
        22: 'siptcp',
        23: 'rtsp',
        -1: 'not collected'
        }


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
    vsDefaultTrafficPool = ProxyProperty('vsDefaultTrafficPool')

    @property
    @info
    def vsProtocol(self):
        return vsProtocolMap[self._object.vsProtocol]


class ZeusPoolInfo(ZeusLoadBalancerComponentInfo):
    implements(IZeusPoolInfo)
    adapts(ZeusPool)

    poolName = ProxyProperty('poolName')
    poolNodes = ProxyProperty('poolNodes')
    poolFailPool = ProxyProperty('poolFailPool')

    @property
    @info
    def poolAlgorithm(self):
        return algorithmMap[self._object.poolAlgorithm]

    @property
    @info
    def poolPersistence(self):
        return persistenceMap[self._object.poolPersistence]

    @property
    @info
    def poolDraining(self):
        try:
            value = self._object.poolDraining()
        except Exception, e:
            log.warning('Couldnt read RRD file for poolDraining:%s' % str(e))
            value = -1
        return value

    @property
    @info
    def poolState(self):
        return poolStateMap[self._object.poolState]

    @property
    @info
    def poolActiveNodes(self):
        try:
            value = self._object.poolActiveNodes()
        except Exception, e:
            log.warning('Couldnt read RRD file for poolActiveNodes: %s' % str(e))
            value = -1
        return value

