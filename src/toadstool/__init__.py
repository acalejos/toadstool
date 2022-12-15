"""
Runs on first import of toadstool package

Loads all loaders which can be loaded

Raises:
    ImportError, ModuleNotFoundError: Modules that do not have supported optional dependencies installed will raise this
    AttributeError, NotImplementedError: Loader modules will raised this when they do not override all necessary methods of the base Loader class
"""

import sys
import logging
from importlib import import_module

LOG = logging.getLogger("toadstool")
all_loaders = [
    ('toadstool.loaders.gql_loader', 'GqlLoader', 'gql'),
    ('toadstool.loaders.yaml_loader', 'YamlLoader', 'yaml'),
    ('toadstool.loaders.json_loader', 'JsonLoader', None),
    ('toadstool.loaders.toml_loader', 'TomlLoader', 'toml'),
    ('toadstool.loaders.csv_loader', 'CsvLoader', None),
    ('toadstool.loaders.config_loader', 'ConfigLoader', None)
]

loaded = []

for loader_mod, loader_class, extra_option in all_loaders:
    try:
        module = import_module(loader_mod)
        cls = getattr(module, loader_class)
    except (ImportError, ModuleNotFoundError) as e:
        if extra_option is not None:
            LOG.info(
                f"Running without {extra_option} support. Install with `pip install {__name__}[{extra_option}]")
    except (AttributeError, NotImplementedError) as e:
        raise e
    else:
        loaded.append(cls)
        if cls not in sys.meta_path:
            sys.meta_path.append(cls)
