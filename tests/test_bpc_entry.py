import unittest,subprocess,tempfile,shutil,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Entry(unittest.TestCase):
 def test_clean_project_from_relocated_cli(self):
  with tempfile.TemporaryDirectory() as t:
   dest=Path(t)/'relocated';dest.mkdir();shutil.copy2(ROOT/'studio.py',dest/'studio.py')
   r=subprocess.run(['python',str(dest/'studio.py'),'new','fresh'],cwd=t,capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stderr)
   p=dest/'projects/fresh/project-record.json';record=json.loads(p.read_text())
   self.assertEqual(record['language'],'id');self.assertIsNone(record['venture']['name']);self.assertEqual(record['canonical_numbers'],[])
   self.assertNotIn('JejakBalik',p.read_text());self.assertNotIn('ReFeel',p.read_text())
   r=subprocess.run(['python',str(dest/'studio.py'),'handoff','fresh'],cwd=t,capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr)
 def test_no_overwrite(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'studio.py';shutil.copy2(ROOT/'studio.py',p)
   for expected in [0,2]:self.assertEqual(subprocess.run(['python',str(p),'new','fresh'],capture_output=True).returncode,expected)
if __name__=='__main__':unittest.main()
