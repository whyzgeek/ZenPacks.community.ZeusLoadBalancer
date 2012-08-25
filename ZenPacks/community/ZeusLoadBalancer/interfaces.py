from Products.Zuul.form import schema
from Products.Zuul.interfaces import IFacade
from Products.Zuul.interfaces import IDeviceInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t


class IZeusLoadBalancerInfo(IDeviceInfo):
    pass

class IZeusPoolInfo(IComponentInfo):
    pass

class IZeusVirtualServerInfo(IComponentInfo):
    vsName =  schema.Text(title=_t(u"Name"))
    vsPort = schema.Int(title=_t(u"Port"))
    vsProtocol = schema.Text(title=_t(u"Protocol"))
    vsDefaultTrafficPool =  schema.Text(title=_t(u"Default Traffic Pool"))
