#!/usr/bin/env python
from pynagios import make_option, Response, CRITICAL, OK
from base_rabbit_check import BaseRabbitCheck


class RabbitNodesCheck(BaseRabbitCheck):
    """
    performs a nagios compliant check on partition status
    attempts to catch all errors. expected usage is with a critical threshold of 0
    """

    nodes = make_option("--nodes", dest="nodes", help="RabbitMQ nodes", type="int", default=1)

    def makeUrl(self):
        """
        forms self.url, a correct url to polling a rabbit queue
        """
        try:
            if self.options.use_ssl is True:
                self.url = "https://%s:%s/api/nodes" % (self.options.hostname, self.options.port)
            else:
                self.url = "http://%s:%s/api/nodes" % (self.options.hostname, self.options.port)
            return True
        except Exception, e:
            self.rabbit_error = 3
            self.rabbit_note = "problem forming api url:", e
        return False

    def testOptions(self):
        if not self.options.nodes:
            return False
        return True

    def setPerformanceData(self, data, result):
        result.set_perf_data("rabbit_error", self.rabbit_error)
        return result

    def parseResult(self, data):
        if len(data) == self.options.nodes:
            return Response(OK, "%i Nodes present" % self.options.nodes)
        return Response(CRITICAL, "Nodes expected %i, but found %i" % (self.options.nodes, len(data)))


if __name__ == "__main__":
    obj = RabbitNodesCheck()
    obj.check().exit()