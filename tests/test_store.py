import sys

from pathlib import Path


sys.path.append(str(Path(__file__).parents[1]))

import fixture


class StoreTest(fixture.DockerTest):
    def test_set_get(self):
        self.stuff(["store.Set('my_key', 'my_val')"])
        self.assertEquals('my_val', self.stuff(["print(store.get('my_key'), end='')"]))
