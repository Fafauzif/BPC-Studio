#!/usr/bin/env python3
"""Find editorial review candidates, never certify persuasive writing."""
import argparse,json,re
from pathlib import Path
PATTERNS={
 'automatic_weakening':r'(?i)merely a prototype|remains hypothetical|only a proposed pilot|further validation is required|may potentially be promising|masih sebatas (?:ide|prototipe)|hanya (?:sebuah )?prototipe|masih diperlukan validasi',
 'generic_setup':r'(?i)di era (?:digital|globalisasi)|seiring (?:dengan )?perkembangan zaman|revolutionary solution|solusi (?:yang )?revolusioner',
 'unsupported_achievement_candidate':r'(?i)telah terbukti|telah bermitra|sudah memperoleh pendanaan|guaranteed returns|proven to',
}
def review(text):
 found=[]
 for category,pattern in PATTERNS.items():
  for m in re.finditer(pattern,text): found.append({'category':category,'line':text.count('\n',0,m.start())+1,'text':m.group(),'context':text[max(0,m.start()-60):m.end()+100]})
 return {'status':'editorial_review_required','findings':found,'scope':'Candidates require contextual judgment. Legitimate material qualifications and quoted weak examples may match. This tool cannot verify sources, argument, cadence or human authorship.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();r=review(a.input.read_text(encoding='utf-8'));s=json.dumps(r,ensure_ascii=False,indent=2)+'\n'
 if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s,encoding='utf-8')
 print(s)
if __name__=='__main__':main()
