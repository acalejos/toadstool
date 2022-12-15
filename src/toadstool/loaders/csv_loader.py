import csv

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class CsvLoader(Loader):
    """
    Used to import csv files into a Python dict
    """
    file_exts="csv"

    def exec_module(self, module):
        """Executing the module means reading the csv file"""
        with self.path.open() as f:
            sniffer = csv.Sniffer()
            sample = f.read(1024)
            f.seek(0)
            dialect = sniffer.sniff(sample)
            has_header = sniffer.has_header(sample)
            if has_header:
                rows_dict = csv.DictReader(f,dialect)
            data = list(csv.reader(f,dialect))
        if has_header:
            module.__dict__["headers"] = data[0]
            module.__dict__["rows"] = data[1:]
        else:
            module.__dict__["rows"] = data
        fieldnames = tuple(identifier(key) for key in data.keys())
        fields = dict(zip(fieldnames, data.values()))
        module.__dict__.update(fields)
        super().exec_module(module)
