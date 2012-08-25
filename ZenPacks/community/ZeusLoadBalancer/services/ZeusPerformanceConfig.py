__doc__ = '''ZeusPerformanceConfig

Provides configuration to zeuscollector clients.
'''

###########################################################################
#
# This program heavily borrows code from Zenoss Core code which is 
# distributed under following GPL license.
# 
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################


from pprint import pformat
import logging
log = logging.getLogger('zen.HubService.ZeusPerformanceConfig')

import Globals
from twisted.spread import pb
from Products.ZenCollector.services.config import DeviceProxy, CollectorConfigService

def get_component_manage_ip(component, default=None):
    get_manage_ip = getattr(component, "getManageIp", None)
    if get_manage_ip is None:
        return default
    return get_manage_ip()

class SnmpDeviceProxy(DeviceProxy, pb.Copyable, pb.RemoteCopy):

    def __repr__(self):
        sci = getattr(self, "snmpConnInfo", None)
        scimi = None if (sci is None) else sci.manageIp
        return pformat({"id": self.id,
                        "_config_id": getattr(self, "_config_id", None),
                        "manageIp": self.manageIp,
                        "snmpConnInfo.manageIp": scimi,
                        "dses": getattr(self, "dses", None)})

pb.setUnjellyableForClass(SnmpDeviceProxy, SnmpDeviceProxy)


class ZeusPerformanceConfig(CollectorConfigService):
    def __init__(self, dmd, instance):
        deviceProxyAttributes = ('zMaxOIDPerRequest',
                                 'zSnmpMonitorIgnore',
                                 'zSnmpAuthPassword',
                                 'zSnmpAuthType',
                                 'zSnmpCommunity',
                                 'zSnmpPort',
                                 'zSnmpPrivPassword',
                                 'zSnmpPrivType',
                                 'zSnmpSecurityName',
                                 'zSnmpTimeout',
                                 'zSnmpTries',
                                 'zSnmpVer',
                                 'zSnmpCollectionInterval',
                                )
        CollectorConfigService.__init__(self, dmd, instance, 
                                        deviceProxyAttributes)

    def _filterDevice(self, device):
        include = CollectorConfigService._filterDevice(self, device)

        if getattr(device, 'zSnmpMonitorIgnore', False):
            self.log.debug("Device %s skipped because zSnmpMonitorIgnore is True",
                           device.id)
            include = False

        if getattr(device, 'meta_type') != 'ZeusLoadBalancer':
            self.log.debug("Device %s skipped because it is not a ZXTM",
                           device.id)
            include = False

        if not device.getManageIp():
            self.log.debug("Device %s skipped because its management IP address is blank.",
                           device.id)
            include = False

        return include

    def _getComponentConfig(self, comp, perfServer, dses):
        """
        Returns all datasources and datapoints of a Zeus 
        component
        """
        if comp.snmpIgnore():
            return None

        basepath = comp.rrdPath()
        for templ in comp.getRRDTemplates():
            for ds in templ.getRRDDataSources('Built-In'):
                if not ds.enabled:
                    continue

                for dp in ds.getRRDDataPoints():
                    # Everything under ZenModel *should* use titleOrId but it doesn't
                    cname = comp.viewName() if comp.meta_type != "ZeusLoadBalancer" else dp.id
                    dpData = (cname, 
                                 "/".join((basepath, dp.name())),
                                 dp.rrdtype,
                                 dp.getRRDCreateCommand(perfServer).strip(),
                                 dp.rrdmin, dp.rrdmax,
                                 comp.snmpindex, comp.snmpindex_dct)

                    dses.setdefault(ds.id, []).append(dpData)

        return comp.getThresholdInstances('Built-In')

    def _createDeviceProxies(self, device):
        manage_ips = {device.manageIp: ([], False)}
        components = device.getMonitoredComponents(collector="zeuscollector")
        for component in components:
            manage_ip = get_component_manage_ip(component, device.manageIp)
            if manage_ip not in manage_ips:
                log.debug("Adding manage IP %s from %r" % (manage_ip, component))
                manage_ips[manage_ip] = ([], True)
            manage_ips[manage_ip][0].append(component)
        proxies = []
        for manage_ip, (components, components_only) in manage_ips.items():
            proxy = self._createDeviceProxy(device, manage_ip, components, components_only)
            if proxy is not None:
                proxies.append(proxy)
        return proxies

    def _createDeviceProxy(self, device, manage_ip=None, components=(), components_only=False):
        proxy = SnmpDeviceProxy()
        proxy = CollectorConfigService._createDeviceProxy(self, device, proxy)
        proxy.snmpConnInfo = device.getSnmpConnInfo()
        if manage_ip is not None and manage_ip != device.manageIp:
            proxy._config_id = device.id + "_" + manage_ip
            proxy.snmpConnInfo.manageIp = manage_ip
        proxy.configCycleInterval = self._prefs.perfsnmpCycleInterval
        proxy.cycleInterval = getattr(device, 'zSnmpCollectionInterval', 300)
        proxy.name = device.id
        proxy.device = device.id
        proxy.lastmodeltime = device.getLastChangeString()
        proxy.lastChangeTime = float(device.getLastChange())

        # Gather the datapoints to retrieve
        perfServer = device.getPerformanceServer()
        proxy.dses = {}
        proxy.thresholds = []
        if not components_only:
            # First for the device....
            threshs = self._getComponentConfig(device, perfServer, proxy.dses)
            if threshs:
                proxy.thresholds.extend(threshs)
        # And now for its components
        for comp in components:
            threshs = self._getComponentConfig(comp, perfServer, proxy.dses)
            if threshs:
                proxy.thresholds.extend(threshs)

        if proxy.dses:
            return proxy


if __name__ == '__main__':
    from Products.ZenHub.ServiceTester import ServiceTester
    tester = ServiceTester(ZeusPerformanceConfig)
    def printer(proxy):
        print proxy.dses
        print [x for x in proxy.thresholds]
    tester.printDeviceProxy = printer
    tester.showDeviceInfo()

