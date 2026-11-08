#!/usr/bin/env python3
"""Portable entry point; no package installation or remote writes on import."""
from pathlib import Path
import argparse, importlib.util, json, os, re, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parent
TOOLS=ROOT/'skills'/'build-bpc-proposals'/'scripts'

def doctor():
    commands={n:shutil.which(n)for n in ['xelatex','lualatex','pdflatex','pdftoppm','soffice','libreoffice','fc-match','tesseract','git']}
    configured=os.environ.get('LIBREOFFICE_BIN')
    if configured:commands['configured_libreoffice']=configured if Path(configured).is_file()else None
    modules={n:importlib.util.find_spec(n)is not None for n in ['docx','fitz','PIL','numpy','yaml','qrcode','cv2']}
    font=None
    if commands['fc-match']:
        r=subprocess.run(['fc-match','Times New Roman','--format','%{family}'],capture_output=True,text=True)
        font=r.stdout.strip()if r.returncode==0 else None
    report={'python':sys.version.split()[0],'executable':sys.executable,'modules':modules,'commands':commands,'requested_font':'Times New Roman','resolved_font_family':font,'checks':{'planning_and_reading':True,'docx_build_dependency_available':modules['docx'],'pdf_converter_binary_available':bool(commands['soffice']or commands['libreoffice']or commands.get('configured_libreoffice')),'pdf_inspection_dependency_available':modules['fitz'],'unicode_tex_binary_available':bool(commands['xelatex']or commands['lualatex']),'chart_rasterizer_available':bool(commands['pdftoppm']or modules['fitz']),'optional_qr_decode_dependency_available':modules['cv2']},'note':'Availability inventory only. Compile/render representative actual files to test functional capability; an installed binary can still lack packages.'}
    print(json.dumps(report,indent=2));return 0

def new_project(name,language):
    if not name or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_'for c in name):raise ValueError('Use lowercase letters, digits, hyphens and underscores for project names.')
    if re.fullmatch(r'(?i:con|prn|aux|nul|com[1-9]|lpt[1-9])',name):raise ValueError('Project name is reserved on Windows; choose another name.')
    dest=ROOT/'projects'/name
    if dest.exists():raise ValueError('Project already exists; no files overwritten.')
    dest.mkdir(parents=True)
    for part in ['inputs','assets','evidence','output','render']:(dest/part).mkdir()
    record={'project':name,'language':language,'mode':'discussion','requirements':{'competition':None,'organizer':None,'round':None,'prompt':None,'rubric':[],'deadline':None,'timezone':None,'limits':{},'guidebook_path':None,'missing_material':[]},'venture':{'name':None,'customer':None,'payer':None,'offer':None,'revenue_unit':None,'operation':None,'first_market':None,'growth':None},'decisions':[],'protected_content':[],'latest_artifacts':[],'canonical_numbers':[],'sources':[],'claims':[],'assumptions':[],'open_issues':[],'actual_checks':[],'next_action':None}
    (dest/'project-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
    (dest/'brief.md').write_text('# '+name+'\n\nRecord the actual customer, offer, earning unit, fulfillment, current competition requirements and requested scope. Describe the chosen business confidently; source observed achievements accurately.\n',encoding='utf-8')
    print(str(dest));return 0

def verify_library():
    manifest=ROOT/'library'/'source-manifest.json'
    if not manifest.exists():raise ValueError('library/source-manifest.json is missing.')
    import hashlib
    data=json.loads(manifest.read_text(encoding="utf-8"));items=data.get('files',data.get('items',[]))if isinstance(data,dict)else data
    failures=[];checked=0
    for item in items:
        rel=item.get('path',item.get('relative_path'))
        if not rel or not item.get('sha256'):continue
        p=(ROOT/rel).resolve()
        if not p.is_relative_to(ROOT):failures.append({'path':rel,'error':'outside repository'});continue
        if not p.is_file():failures.append({'path':rel,'error':'missing'});continue
        actual=hashlib.sha256(p.read_bytes()).hexdigest();checked+=1
        if actual!=item['sha256']:failures.append({'path':rel,'error':'SHA-256 mismatch'})
    print(json.dumps({'checked':checked,'failures':failures,'scope':'Stored supplied-file bytes only, not source validity or rights.'},indent=2))
    return 1 if failures or checked==0 else 0

def main():
    parser=argparse.ArgumentParser(description='BPC Studio — portable business proposal production and verification')
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor',help='Report actual local capabilities without installing anything')
    n=sub.add_parser('new',help='Create a new local project record');n.add_argument('name');n.add_argument('--language',choices=['id','en'],default='id')
    h=sub.add_parser('handoff',help='Write a portable handoff from a project record');h.add_argument('name')
    sub.add_parser('verify-library',help='Verify archived supplied files by SHA-256')
    routes={'build':'build_docx.py','render':'render_document.py','audit':'audit_document.py','comments':'extract_comments.py','chart':'charts.py','analyze':'analysis.py','read':'read_documents.py','check':'validate_package.py','finance':'finance.py','voice':'voice_review.py'}
    # Delegate all remaining arguments intact, including --help.
    if len(sys.argv)>1 and sys.argv[1]in routes:
        tool=TOOLS/routes[sys.argv[1]]
        if not tool.is_file():parser.error(f'Tool missing: {tool.relative_to(ROOT)}')
        return subprocess.call([sys.executable,str(tool),*sys.argv[2:]])
    for name,tool in routes.items():sub.add_parser(name,add_help=False,help=f'Delegate to {tool}; use {name} --help')
    args=parser.parse_args()
    if args.command=='doctor':return doctor()
    if args.command=='new':return new_project(args.name,args.language)
    if args.command=='handoff':
        if not args.name or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in args.name): raise ValueError('Invalid project name')
        dest=ROOT/'projects'/args.name; record=json.loads((dest/'project-record.json').read_text(encoding='utf-8'))
        lines=['# BPC project handoff','', 'Read AGENTS.md, the latest guidebook and accepted artifacts before changing this case.','']
        for key,value in record.items(): lines.extend(['## '+key.replace('_',' ').title(),'','```json',json.dumps(value,ensure_ascii=False,indent=2),'```',''])
        (dest/'HANDOFF.md').write_text('\n'.join(lines),encoding='utf-8');print(dest/'HANDOFF.md');return 0
    if args.command=='verify-library':return verify_library()
    return 2

if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError)as exc:print(f'Error: {exc}',file=sys.stderr);raise SystemExit(2)
