"""Integration checks for document mechanics; no research/visual approval claim.

Run: python -m unittest discover -s tests -p 'test_document_tools.py' -v
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from docx import Document
from lxml import etree as ET

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skills/build-bpc-proposals/scripts'
def load(name):
    spec=importlib.util.spec_from_file_location(name,SCRIPTS/(name+'.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
build=load('build_docx');extract=load('extract_comments');audit=load('audit_document');render=load('render_document')

class DocumentMechanics(unittest.TestCase):
    def test_real_internal_links_without_self_linked_heading(self):
        p={'title':'Mechanics fixture','body':[{'type':'paragraph','text':'The calculation is in Appendix A.1.'}],'appendices':[{'id':'A.1','title':'Calculation','blocks':[]}]}
        with tempfile.TemporaryDirectory()as d:
            path=Path(d)/'fixture.docx';b=build.Builder(p,Path(d));build.save_docx(b.build(),path)
            r=audit.audit(path);self.assertEqual(r['errors'],[]);self.assertEqual(r['internal_links'],4)
            with zipfile.ZipFile(path)as z:
                x=ET.fromstring(z.read('word/document.xml'));ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                heads=x.xpath('//w:p[w:pPr/w:pStyle[starts-with(@w:val,"Heading")]]',namespaces=ns)
                self.assertFalse(any(h.xpath('.//w:hyperlink',namespaces=ns)for h in heads))

    def test_unknown_link_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'Unresolved'):
            build.Builder({'title':'Fixture','body':[{'text':'See Appendix Z.9.'}]},Path.cwd()).build()

    def test_table_cannot_overflow_text_region(self):
        with self.assertRaisesRegex(ValueError,'exceed'):
            build.Builder({'title':'Fixture','body':[{'type':'table','headers':['One','Two'],'rows':[['a','b']],'widths_cm':[12,12]}]},Path.cwd()).build()

    def test_comment_range_crosses_paragraphs_and_source_unchanged(self):
        with tempfile.TemporaryDirectory()as d:
            path=Path(d)/'review.docx';doc=Document();a=doc.add_paragraph().add_run('First selected paragraph');b=doc.add_paragraph().add_run('Second selected paragraph')
            doc.add_comment([a,b],text='Clarify this connection',author='Fixture reviewer');doc.save(path)
            before=hashlib.sha256(path.read_bytes()).hexdigest();result=extract.extract(path)
            self.assertEqual(result['comment_count'],1);self.assertEqual(result['comments'][0]['selection']['text'],'First selected paragraph\nSecond selected paragraph')
            self.assertEqual(before,hashlib.sha256(path.read_bytes()).hexdigest())

    def test_missing_converter_is_reported_as_failure(self):
        with tempfile.TemporaryDirectory()as d:
            path=Path(d)/'fixture.docx';build.save_docx(build.Builder({'title':'Fixture'},Path(d)).build(),path)
            r=render.render(path,Path(d)/'render',executable=str(Path(d)/'missing-converter'))
            self.assertEqual(r['status'],'failed');self.assertEqual(r['visual_review'],'not_performed_by_script')

    def test_neutral_template_has_no_author_or_comments(self):
        path=ROOT/'skills/build-bpc-proposals/assets/templates/neutral_proposal.docx'
        doc=Document(path);self.assertFalse(doc.core_properties.author);self.assertFalse(doc.core_properties.last_modified_by)
        r=audit.audit(path);self.assertEqual(r['comments'],0);self.assertEqual(r['tracked_changes'],0)

    def test_inherited_remote_template_removed_but_authored_link_retained(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);template=base/'source.docx';Document().save(template)
            with zipfile.ZipFile(template) as archive:
                parts={name:archive.read(name) for name in archive.namelist()}
            w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            r='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
            settings=ET.fromstring(parts['word/settings.xml'])
            attached=ET.SubElement(settings,'{'+w+'}attachedTemplate');attached.set('{'+r+'}id','rIdOldTemplate')
            parts['word/settings.xml']=ET.tostring(settings)
            parts['word/_rels/settings.xml.rels']=(
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rIdOldTemplate" Type="'+r+'/attachedTemplate" '
                'Target="https://example.invalid/old-private-template.dotm" TargetMode="External"/>'
                '</Relationships>').encode()
            with zipfile.ZipFile(template,'w') as archive:
                for name,raw in parts.items():archive.writestr(name,raw)
            project={'title':'New business','template':'source.docx','body':[
                {'runs':[{'text':'Current source','url':'https://example.org/current-source'}]}]}
            output=base/'output.docx';build.save_docx(build.Builder(project,base).build(),output)
            with zipfile.ZipFile(output) as archive:
                self.assertNotIn(b'attachedTemplate',archive.read('word/settings.xml'))
                for name in archive.namelist():self.assertNotIn(b'old-private-template',archive.read(name))
                self.assertIn(b'https://example.org/current-source',archive.read('word/_rels/document.xml.rels'))

    def test_physical_requirements_detect_changed_docx_and_pdf(self):
        from docx.shared import Cm
        import fitz
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);project={'title':'Physical fixture','format':{'page_width_cm':21,'page_height_cm':29.7,'margin_cm':2.5,'margins_cm':{'left':3}}}
            source=base/'source.json';source.write_text(json.dumps(project),encoding='utf-8')
            doc=build.Builder(project,base).build();path=base/'fixture.docx';build.save_docx(doc,path)
            self.assertEqual(audit.audit(path,project=source)['errors'],[])
            doc.sections[0].page_width=Cm(12);doc.sections[0].left_margin=Cm(1);build.save_docx(doc,path)
            pdf=base/'fixture.pdf'
            with fitz.open() as export:
                page=export.new_page(width=12/2.54*72,height=29.7/2.54*72);page.insert_text((30,50),'Physical fixture');export.save(pdf)
            errors=audit.audit(path,pdf=pdf,project=source)['errors']
            self.assertTrue(any('Section 1 page_width_cm' in e for e in errors),errors)
            self.assertTrue(any('Section 1 left margin' in e for e in errors),errors)
            self.assertTrue(any('PDF page 1 page_width_cm' in e for e in errors),errors)

if __name__=='__main__':unittest.main()
