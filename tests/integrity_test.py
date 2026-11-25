import sys,json,hashlib,zipfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from build_library import parse_usfm,parse_usfx,CANON,ET
class SourceIntegrity(unittest.TestCase):
 def test_locked_source_archives(self):
  for name,h in json.loads((ROOT/'sources/source-lock.json').read_text()).items():self.assertEqual(hashlib.sha256((ROOT/'sources'/name).read_bytes()).hexdigest(),h)
 def test_all_shipped_passages_against_usfm(self):
  catalog=json.loads((ROOT/'dist/catalog.json').read_text());self.assertEqual(len(catalog['editions']),6)
  for e in catalog['editions']:
   with self.subTest(edition=e['id']):
    z=zipfile.ZipFile(ROOT/'sources'/f'{e["id"]}_usfm.zip');expected=parse_usfm(z);pack=json.loads((ROOT/'dist'/e['file']).read_text())
    self.assertEqual(set(expected),set(CANON));self.assertEqual([b['id'] for b in pack['books']],CANON)
    for b in pack['books']:
     actual={c['label']+':'+v['label']:v['text'] for c in b['chapters'] for v in c['verses']};self.assertEqual(actual,expected[b['id']])
 def test_negative_duplicate_label(self):
  import io
  buf=io.BytesIO()
  with zipfile.ZipFile(buf,'w') as z:z.writestr('test.usfm','\\id GEN\n\\c 1\n\\v 1 SYNTHETIC TEST ONLY\n\\v 1 SYNTHETIC TEST ONLY')
  buf.seek(0)
  with self.assertRaises(ValueError):parse_usfm(zipfile.ZipFile(buf))
 def test_negative_unknown_xml(self):
  with self.assertRaises(ValueError):parse_usfx(ET.fromstring('<usfx><book id="GEN"><c id="1"/><v id="1"/><unknown>NOT SCRIPTURE</unknown><ve/></book></usfx>'))
 def test_no_unexplained_differences(self):
  for r in json.loads((ROOT/'reports/validation.json').read_text()):self.assertEqual(r['errors'],[]);self.assertEqual(r['textDifferences'],0)
if __name__=='__main__':unittest.main(verbosity=2)
