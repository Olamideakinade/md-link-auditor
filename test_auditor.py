import unittest
import os
from main import LinkAuditor

class TestLinkAuditor(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_sandbox'
        os.makedirs(self.test_dir, exist_ok=True)
        self.valid_md = os.path.join(self.test_dir, 'valid.md')
        with open(self.valid_md, 'w') as f:
            f.write('[Local Link](valid.md)\n[External](https://httpbin.org/status/200)')

    def tearDown(self):
        for f in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, f))
        os.rmdir(self.test_dir)

    def test_local_resolution(self):
        auditor = LinkAuditor(self.test_dir)
        valid, msg = auditor.validate_link(self.valid_md, 'valid.md')
        self.assertTrue(valid)

    def test_broken_local_resolution(self):
        auditor = LinkAuditor(self.test_dir)
        valid, msg = auditor.validate_link(self.valid_md, 'nonexistent.md')
        self.assertFalse(valid)

    def test_ignore_pattern(self):
        auditor = LinkAuditor(self.test_dir, ignore_patterns=['example.com'])
        self.assertTrue(auditor.is_ignored('https://example.com/path'))

if __name__ == '__main__':
    unittest.main()
