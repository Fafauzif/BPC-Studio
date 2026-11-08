#!/usr/bin/env python3
"""Validate active routes, archived bytes, syntax and portable package paths."""
from pathlib import Path
import argparse,ast,hashlib,json,re,sys
from urllib.parse import unquote

def validate(root):
 root=Path(root).resolve();fail=[];checks={};warn=[]
 required=['AGENTS.md','START.md','README.md','studio.py','library/source-manifest.json','library/catalog.md','library/reading-routes.md','library/bpc-synthesis.md','skills/build-bpc-proposals/SKILL.md']
 for rel in required:
  if not (root/rel).is_file():fail.append('Missing '+rel)
 active=[*root.glob('*.md'),*root.glob('docs/*.md'),*root.glob('skills/build-bpc-proposals/**/*.md'),*root.glob('library/*.md'),*root.glob('library/lessons/*.md'),*root.glob('library/bpc-lessons/*.md'),*root.glob('examples/*/README.md')]
 count=0
 for p in active:
  t=re.sub(r'(?ms)^`{3,}.*?^`{3,}\s*$','',p.read_text(encoding='utf-8'))
  for m in re.finditer(r'!?\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+"[^"]*")?\)',t):
   target=(m.group(1)or m.group(2)).split('#',1)[0]
   if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
   dest=(p.parent/unquote(target)).resolve();count+=1
   if not dest.is_relative_to(root)or not dest.exists():fail.append(f'Broken local link {p.relative_to(root)} -> {target}')
 checks['active_links']=count
 manifest=root/'library/source-manifest.json';n=0
 if manifest.exists():
  for row in json.loads(manifest.read_text())['files']:
   p=(root/row['path']).resolve()
   if not p.is_relative_to(root)or not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:fail.append('Source hash/path mismatch '+row['path'])
   n+=1
 checks['source_hashes']=n
 for p in root.rglob('*.py'):
  try:ast.parse(p.read_text(encoding='utf-8'))
  except SyntaxError as e:fail.append(str(e))
 names={};largest=0
 for p in root.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(root);key=str(rel).casefold()
  if key in names:fail.append('Case collision '+str(rel))
  names[key]=1;largest=max(largest,p.stat().st_size)
  if p.is_symlink()or any(x in {'.git','.venv','node_modules','__pycache__'}for x in rel.parts):fail.append('Excluded path '+str(rel))
  if p.name=='.env' or p.suffix=='.pyc':fail.append('Excluded file '+str(rel))
  if any(re.search(r'[<>:"|?*]',s)or s.endswith((' ','.'))or re.fullmatch(r'(?i:con|prn|aux|nul|conin\$|conout\$|com[1-9¹²³]|lpt[1-9¹²³])',s.split('.',1)[0])for s in rel.parts):fail.append('Nonportable path '+str(rel))
  if p.stat().st_size>=100*1024**2:fail.append('GitHub file limit exceeded '+str(rel))
 checks.update(files=len(names),largest_file_bytes=largest)
 return {'status':'pass' if not fail else 'fail','checks':checks,'failures':fail,'warnings':warn,'scope':'Mechanical structure/hash/path checks. Functional, financial and visual review recorded separately.'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',nargs='?',type=Path,default=Path(__file__).resolve().parents[3]);p.add_argument('--output',type=Path);a=p.parse_args();r=validate(a.root);s=json.dumps(r,indent=2)+'\n'
 if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(s);sys.exit(r['status']!='pass')
