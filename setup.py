from pkg_resources import parse_version
from configparser import ConfigParser
import itertools
import os.path
import setuptools
from distutils.command.build import build
from setuptools.command.develop import develop
from setuptools.command.easy_install import easy_install
from setuptools.command.install_lib import install_lib
assert parse_version(setuptools.__version__)>=parse_version('36.2')

LOVELY_TENSORS_HOOK_SRC = "lovely_tensors_hook.py"
LOVELY_TENSORS_HOOK = "lovely_tensors_hook.pth"


def create_hook(src_path, dest_path):
    with open(src_path, 'r') as f:
        src_code = f.read()
    with open(dest_path, 'w') as f:
        print(f"import os; exec({src_code!r})", file=f)


class BuildWithHook(build):
    def run(self):
        build.run(self)
        path = os.path.join(os.path.dirname(__file__), LOVELY_TENSORS_HOOK_SRC)
        dest = os.path.join(self.build_lib, LOVELY_TENSORS_HOOK)
        self.make_file([path], dest, create_hook, [path, dest])


class EasyInstallWithHook(easy_install):
    def run(self):
        easy_install.run(self)
        path = os.path.join(self.build_directory, LOVELY_TENSORS_HOOK)
        dest = os.path.join(self.install_dir, LOVELY_TENSORS_HOOK)
        self.copy_file(path, dest)


class InstallLibWithHook(install_lib):
    def run(self):
        install_lib.run(self)
        path = os.path.join(self.build_dir, LOVELY_TENSORS_HOOK)
        dest = os.path.join(self.install_dir, LOVELY_TENSORS_HOOK)
        self.copy_file(path, dest)
        self.outputs = [dest]

    def get_outputs(self):
        return itertools.chain(install_lib.get_outputs(self), self.outputs)


class DevelopWithHook(develop):
    def run(self):
        develop.run(self)
        path = os.path.join(self.build_directory, LOVELY_TENSORS_HOOK)
        dest = os.path.join(self.install_dir, LOVELY_TENSORS_HOOK)
        self.copy_file(path, dest)


# note: all settings are in settings.ini; edit there, not here
config = ConfigParser(delimiters=['='])
config.read('settings.ini', encoding="utf-8")
cfg = config['DEFAULT']

cfg_keys = 'version description keywords author author_email'.split()
expected = cfg_keys + "lib_name user branch license status min_python audience language".split()
for o in expected: assert o in cfg, "missing expected setting: {}".format(o)
setup_cfg = {o:cfg[o] for o in cfg_keys}

licenses = {
    'apache2': ('Apache Software License 2.0','OSI Approved :: Apache Software License'),
    'mit': ('MIT License', 'OSI Approved :: MIT License'),
    'gpl2': ('GNU General Public License v2', 'OSI Approved :: GNU General Public License v2 (GPLv2)'),
    'gpl3': ('GNU General Public License v3', 'OSI Approved :: GNU General Public License v3 (GPLv3)'),
    'bsd3': ('BSD License', 'OSI Approved :: BSD License'),
}
statuses = [ '1 - Planning', '2 - Pre-Alpha', '3 - Alpha',
    '4 - Beta', '5 - Production/Stable', '6 - Mature', '7 - Inactive' ]
py_versions = '3.6 3.7 3.8 3.9 3.10'.split()

requirements = cfg.get('requirements','').split()
if cfg.get('pip_requirements'): requirements += cfg.get('pip_requirements','').split()
min_python = cfg['min_python']
lic = licenses.get(cfg['license'].lower(), (cfg['license'], None))
dev_requirements = (cfg.get('dev_requirements') or '').split()

setuptools.setup(
    name = cfg['lib_name'],
    license = lic[0],
    classifiers = [
        'Development Status :: ' + statuses[int(cfg['status'])],
        'Intended Audience :: ' + cfg['audience'].title(),
        'Natural Language :: ' + cfg['language'].title(),
    ] + ['Programming Language :: Python :: '+o for o in py_versions[py_versions.index(min_python):]] + (['License :: ' + lic[1] ] if lic[1] else []),
    url = cfg['git_url'],
    packages = setuptools.find_packages(),
    include_package_data = True,
    install_requires = requirements,
    extras_require={ 'dev': dev_requirements },
    dependency_links = cfg.get('dep_links','').split(),
    python_requires  = '>=' + cfg['min_python'],
    long_description = open('README.md', encoding="utf-8").read(),
    long_description_content_type = 'text/markdown',
    zip_safe = False,
    entry_points = {
        'console_scripts': cfg.get('console_scripts','').split(),
        'nbdev': [f'{cfg.get("lib_path")}={cfg.get("lib_path")}._modidx:d']
    },
    # The import hooks mechanism is inspired by the one used in better_exceptions
    # https://github.com/Qix-/better-exceptions/blob/f7f1476e57129dc74d241b4377b0df39c37bc8a7/setup.py
    cmdclass = {
        'build': BuildWithHook,
        'easy_install': EasyInstallWithHook,
        'install_lib': InstallLibWithHook,
        'develop': DevelopWithHook,
    },
    **setup_cfg)


