import csv

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class CsvLoader(Loader):
    """
    Used to import csv files into a Python dict
    """
    file_exts="csv"

    def exec_module(self, module):
        rows_dict = None
        with self.path.open() as f:
            sniffer = csv.Sniffer()
            sample = f.read(1024)
            f.seek(0)
            dialect = sniffer.sniff(sample)
            has_header = sniffer.has_header(sample)
            if has_header:
                dict_reader = csv.DictReader(f, dialect=dialect)
                module.__dict__["fieldnames"] = dict_reader.fieldnames
                data = list(dict_reader.reader)
                rows_dict = list(dict_reader)
                module.__dict__["rows"] = data[1:]
                module.__dict__["named_rows"] = rows_dict
            else:
                data = list(csv.reader(f,dialect))
                module.__dict__["rows"] = data
        module.__dict__["columns"] = [list(x) for x in zip(*module.__dict__["rows"])]
        if has_header and module.__dict__["fieldnames"] is not None:
            module.__dict__["named_columns"] = {header: column for header, column in zip(module.__dict__["fieldnames"],module.__dict__["columns"])}
            fieldnames = tuple(identifier(key) for key in module.__dict__["named_columns"].keys())
            fields = dict(zip(fieldnames, module.__dict__["named_columns"].values()))
        module.__dict__.update(fields)
        super().exec_module(module)
