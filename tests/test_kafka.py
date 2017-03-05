import sys

from pathlib import Path


sys.path.append(Path(__file__).parent.parent)

import fixture


class InstallTest(fixture.DockerTest):
    def test_install_kafka(self):
        self.stuff(['contrib.kafka.Install("0.10.0.0")'])
        self.assertRegex(self.container_run(['ls', '/opt/kafka_2.11-0.10.0.0/bin']), r'kafka-server-start\.sh')
