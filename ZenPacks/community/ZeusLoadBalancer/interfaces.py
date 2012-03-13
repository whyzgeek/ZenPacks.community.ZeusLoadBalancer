from Products.Zuul.form import schema
from Products.Zuul.interfaces import IFacade
from Products.Zuul.interfaces import IDeviceInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t


class IZeusLoadBalancerInfo(IDeviceInfo):
    pass

class IZeusPoolInfo(IComponentInfo):
    poolName = schema.Text(title=_t(u"Name"))
    poolAlgorithm = schema.Text(title=_t(u"Algorithm"))
    poolNodes = schema.Int(title=_t(u"Nodes"))
    poolDraining = schema.Int(title=_t(u"Draining"))
    poolFailPool = schema.Text(title=_t(u"Failure Pool"))
    poolPersistence = schema.Text(title=_t(u"Persistence"))

class IZeusVirtualServerInfo(IComponentInfo):
    vsName =  schema.Text(title=_t(u"Name"))
    vsPort = schema.Int(title=_t(u"Port"))
    vsProtocol = schema.Text(title=_t(u"Protocol"))
