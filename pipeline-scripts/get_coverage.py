from lxml import etree
import fire
import os
from json import dump


class GetCoverage:

    def __init__(self, source_path, source_type, write_path):
        self.default_parser = etree.HTMLParser()
        self.source_path = source_path
        self.source_type = source_type
        self.write_path = write_path
        self.root = self.get_root_node()
        self.source_xpath = {
            "Scala": "//table[@class='coverage']//td[contains(text(), 'Total')]/following-sibling::td[@class='ctr2'][1]/text()",
            "React": "//span[contains(text(), 'Statements')]/preceding-sibling::span/text()"
        }
        self.default_coverage = "0%"
               
    def get_root_node(self):
        with open(self.source_path) as tempFile:
            root = etree.fromstring(tempFile.read().encode("utf-8"), self.default_parser)
        return root

    def set_coverage(self, coverage):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        final_path = os.path.join(current_dir, self.write_path)
        with open(final_path, "w") as tempfile:
            dump({"coverageValue": coverage, 
            "source_path": self.source_path, 
            "source_type": self.source_type}, tempfile)

    def run(self):
        coverage = self.root.xpath(self.source_xpath[self.source_type])
        coverage = coverage[0] if coverage else self.default_coverage
        self.set_coverage(coverage)

if __name__ == '__main__':
   fire.Fire(GetCoverage)