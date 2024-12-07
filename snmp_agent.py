from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity import config
from pysnmp.entity.engine import SnmpEngine
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.proto.api.v1 import ObjectIdentifier
from pysnmp.smi import exval


class SNMPAgent(object):
    def __init__(self, args, config):
        self.args = args
        self.config = config
        self.snmpEngine = SnmpEngine()
        config.addTransport(
            self.snmpEngine,
            udp.domainName,
            udp.UdpTransport().openServerMode(('0.0.0.0', args.port))
        )
        config.addV1System(self.snmpEngine, 'my-area', 'public')
        config.addVacmUser(self.snmpEngine,
                           2,
                           'my-area',
                           'noAuthNoPriv',
                           ObjectIdentifier("1.3.6.1.2.1.25.4"),
                           ObjectIdentifier("1.3.6.1.2.1.25.4"))

        snmp_context = context.SnmpContext(self.snmpEngine)
        mib_builder = snmp_context.getMibInstrum().getMibBuilder()
        mib_builder.loadModules('HOST-RESOURCES-MIB')
        mib_instrum = snmp_context.getMibInstrum()

        # see http://www.oidview.com/mibs/0/HOST-RESOURCES-MIB.html
        host_run_table, = mib_builder.importSymbols('HOST-RESOURCES-MIB', 'hrSWRunEntry')
        instance_id = host_run_table.getInstIdFromIndices(1)

        enterprise_mib = (ObjectIdentifier(config.enterprise_mib))

        var_binds = mib_instrum.writeVars((
            (host_run_table.name + (1,) + instance_id, 1),
            (host_run_table.name + (2,) + instance_id, 'TradeLoader'),  # <=== Must match OpenNMS service-name variable
            (host_run_table.name + (3,) + instance_id, enterprise_mib),  #
            (host_run_table.name + (4,) + instance_id, 'All is well'),
            (host_run_table.name + (5,) + instance_id, 'If this was not the case it would say so here'),
            (host_run_table.name + (6,) + instance_id, 4),
            # Values are ==> unknown(1), operatingSystem(2), deviceDriver(3), application(4)
            (host_run_table.name + (7,) + instance_id, 1)
            # <<=== This is the status number OpenNMS looks at Values are ==> running(1), runnable(2), notRunnable(3), invalid(4)
        ))

        # --- end of  table population ---
        oid, val = (), None
        while True:
            oid, val = mib_instrum.readNextVars(((oid, val),))[0]
            if exval.endOfMib.isSameTypeWith(val):
                break
            print('%s = %s' % ('.'.join([str(x) for x in oid]), val.prettyPrint()))

        # Register SNMP Applications at the SNMP engine for particular SNMP context
        cmdrsp.GetCommandResponder(self.snmpEngine, snmp_context)
        cmdrsp.SetCommandResponder(self.snmpEngine, snmp_context)
        cmdrsp.NextCommandResponder(self.snmpEngine, snmp_context)
        cmdrsp.BulkCommandResponder(self.snmpEngine, snmp_context)

        # Register an imaginary never-ending job to keep I/O dispatcher running forever
        self.snmpEngine.transportDispatcher.jobStarted(1)
        return

    def run(self):
        # Run I/O dispatcher which would receive queries and send responses
        try:
            self.snmpEngine.transportDispatcher.runDispatcher()
        except:
            self.snmpEngine.transportDispatcher.closeDispatcher()
            raise
        return
