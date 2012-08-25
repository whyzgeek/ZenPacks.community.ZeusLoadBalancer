import Globals
import json
import os
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

JSONFILENAME = 'zeuspoolnodes.json'

class pools(SnmpPlugin):

    relname = "pools"
    modname = 'ZenPacks.community.ZeusLoadBalancer.ZeusPool'

    pool_columns = {
    '.1': 'poolName',
    '.2': 'poolAlgorithm',
    '.3': 'poolNodes',
    '.5': 'poolFailPool',
    '.11': 'poolPersistence',
    '.14': 'poolState',
    }

    node_columns = {
    '.1': 'perPoolNodePoolName',
    '.5': 'perPoolNodeNodeHostName',
    '.4': 'perPoolNodeNodePort',
    '.6': 'perPoolNodeState',
    }

    snmpGetTableMaps = (
    GetTableMap('poolinfo', '.1.3.6.1.4.1.7146.1.2.3.2.1', pool_columns),
    GetTableMap('nodeinfo', '.1.3.6.1.4.1.7146.1.2.4.6.1', node_columns),
    )

    def process(self, device, results, log):
        """collect snmp information from this zxtm"""



        # log that we are processing device
        log.info('processing %s for device %s', self.name(), device.id)
        log.debug("SNMP results: %r", results)

        poolCount = 0

        rm = self.relMap()

        # We do this manually to grab the OID suffix which becomes
        # the snmpindex, ascii encoded into OID's is horrible!
        for suffix, data in results[1]['poolinfo'].iteritems():

            om = self.objectMap(data)

            # Remove the extra " characters out of the pool names
            newName = om.poolName.replace('"', '')
            om.poolName = newName

            om.id = self.prepId(om.poolName)

            log.debug("Found Pool: %s" % om.poolName)

            om.snmpindex = suffix
            rm.append(om)
            poolCount = poolCount + 1

        log.info("Finished processing %s, %i pools found", self.name(), poolCount)
        jsonPath = os.path.join(os.environ['ZENHOME'], 'perf', 'Devices', device.id)
        if not os.path.exists(jsonPath):
            try:
                os.makedirs(jsonPath)
            except Exception, e:
                log.error("Couldn't create the device folder hirarachy because"
                          "%s" % str(e))
        try:
            jsonFile = open(jsonPath + '/' + JSONFILENAME, 'w')
        except:
            log.error("failed to create json storage file %s" % jsonPath + '/' + JSONFILENAME)
        else:
            json.dump(results[1]['nodeinfo'], jsonFile)
            log.info("Node info successfully writen to %s/%s" % (jsonPath, JSONFILENAME))
        finally:
            jsonFile.close()
        return [rm]

