"""Windows device names must be rejected on every host before packaging."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
studio=load('path_test_studio',ROOT/'studio.py')
validator=load('path_test_validator',ROOT/'skills/build-bpc-proposals/scripts/validate_package.py')

class PortablePaths(unittest.TestCase):
 def test_project_names_reject_windows_devices_and_allow_normal_word(self):
  oldroot=studio.ROOT
  try:
   with tempfile.TemporaryDirectory() as d:
    studio.ROOT=Path(d)
    for name in ['con','prn','aux','nul','com1','com9','lpt1','lpt9']:
     with self.subTest(name=name),self.assertRaisesRegex(ValueError,'reserved'):studio.new_project(name,'id')
     self.assertFalse((Path(d)/'projects'/name).exists())
    self.assertEqual(studio.new_project('console','id'),0)
  finally:studio.ROOT=oldroot
 def test_package_detects_reserved_filenames_and_parent_components(self):
  with tempfile.TemporaryDirectory() as d:
   base=Path(d);(base/'CON.txt').write_text('fixture');(base/'aux').mkdir();(base/'aux'/'ordinary.md').write_text('fixture')
   result=validator.validate(base)
   self.assertIn('Nonportable path CON.txt',result['failures'])
   self.assertIn('Nonportable path aux/ordinary.md',result['failures'])

if __name__=='__main__':unittest.main()
