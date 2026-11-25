#!/usr/bin/env python3
"""Deterministic, fail-closed importer. Never generates or repairs Scripture text."""
from pathlib import Path
import json, re, zipfile, hashlib, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
IDS=['engwebp','mal','hin2017','mar','tam2017','tel2017']
CANON='GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO ECC SNG ISA JER LAM EZK DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE 2PE 1JN 2JN 3JN JUD REV'.split()
ENGLISH='Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1 Samuel|2 Samuel|1 Kings|2 Kings|1 Chronicles|2 Chronicles|Ezra|Nehemiah|Esther|Job|Psalms|Proverbs|Ecclesiastes|Song of Solomon|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|1 Corinthians|2 Corinthians|Galatians|Ephesians|Philippians|Colossians|1 Thessalonians|2 Thessalonians|1 Timothy|2 Timothy|Titus|Philemon|Hebrews|James|1 Peter|2 Peter|1 John|2 John|3 John|Jude|Revelation'.split('|')
SPACE=re.compile(r'\s+')
def clean(s):return SPACE.sub(' ',s).strip()
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
def parse_usfm(z):
 out={}; inventories={}
 for name in z.namelist():
  if not name.endswith('.usfm'):continue
  src=z.read(name).decode('utf-8-sig');bid=re.search(r'\\id\s+(\S+)',src)[1]
  if bid not in CANON:continue
  entries={};ch=None
  # Split at chapter/verse markers, independently of the XML traversal.
  parts=re.split(r'\\(c|v)\s+(\S+)\s*',src)
  for i in range(1,len(parts),3):
   kind,label,body=parts[i:i+3]
   if kind=='c':ch=label;continue
   if ch is None:raise ValueError('Verse before chapter')
   key=f'{ch}:{label}'
   if key in entries:raise ValueError(f'Duplicate source label {bid} {key}')
   # Notes and cross-references are separate content, not verse-body words.
   body=re.sub(r'\\(f|x)\s.*?\\\1\*','',body,flags=re.S)
   # Section titles, psalm titles, speaker labels and chapter labels are separate.
   body=re.sub(r'(?m)^\\(?:s\d*|ms\d*|mr|r|d|qa|sp|cl|cp)\b[^\n]*','',body)
   body=re.sub(r'\\\+?w\s+([^|\\]*)(?:\|[^\\]*)?\\\+?w\*',r'\1',body)
   body=re.sub(r'\\\+?[a-zA-Z0-9]+(?:\*|[ \t]?)', '',body)
   entries[key]=clean(body)
  out[bid]=entries
 return out

def parse_usfx(root):
 books=[];unknown=set()
 allowed={'book','id','h','toc','ide','p','q','b','s','d','cl','cp','c','v','ve','f','x','w','wj','qs','wh','k','bk','it','bdit','tl','bd','ref'}
 for source in root.findall('book'):
  bid=source.get('id')
  if bid not in CANON:continue
  book={'id':bid,'chapters':[]};chapter=None;cur=None;pending=[]
  def text(s):
   if cur is not None and s:cur['_text'].append(s)
  def walk(e):
   nonlocal chapter,cur,pending
   tag=e.tag
   if tag not in allowed:unknown.add(tag)
   if tag=='c':
    cur=None;pending=[];chapter={'label':e.get('id'),'verses':[],'headings':[]};book['chapters'].append(chapter);return
   if tag=='v':
    if chapter is None:raise ValueError('XML verse before chapter')
    cur={'label':e.get('id'),'_text':[],'notes':[],'headings':pending};pending=[];chapter['verses'].append(cur);return
   if tag=='ve':cur=None;return
   if tag in {'id','h','toc','ide','cl','cp'}:return
   if tag in {'s','d'} or (tag=='p' and e.get('sfm') not in {None,'p','m','mi','pi','li','nb'}):
    value=clean(''.join(e.itertext()))
    if value and chapter is not None:
     item={'kind':e.get('sfm',tag),'text':value};pending.append(item);chapter['headings'].append(item)
    return
   if tag in {'f','x'}:
    if cur is not None:cur['notes'].append({'kind':tag,'text':clean(''.join(e.itertext()))})
    return
   text(e.text)
   for child in e:
    walk(child);text(child.tail)
  walk(source)
  for ch in book['chapters']:
   for v in ch['verses']:v['text']=clean(''.join(v.pop('_text')))
  books.append(book)
 if unknown:raise ValueError(f'Unhandled XML tags {unknown}')
 return books

def build():
 lockpath=ROOT/'sources'/'source-lock.json'
 if lockpath.exists():
  for name,expected in json.loads(lockpath.read_text()).items():
   if sha((ROOT/'sources'/name).read_bytes())!=expected:raise ValueError('Source fingerprint changed: '+name+'; review before repinning')
 manifest=[];reports=[]
 for id in IDS:
  paths={fmt:ROOT/'sources'/f'{id}_{fmt}.zip' for fmt in ['usfm','usfx']}
  z=zipfile.ZipFile(paths['usfx']);xml=z.read(f'{id}_usfx.xml');root=ET.fromstring(xml)
  meta=ET.fromstring(z.read(f'{id}metadata.xml'));names={b.get('code'):b.attrib for b in ET.fromstring(z.read('BookNames.xml'))}
  books=parse_usfx(root);usfm=parse_usfm(zipfile.ZipFile(paths['usfm']))
  errors=[];differences=[];exceptions=[];inventory={}
  if set(b['id'] for b in books)!=set(CANON) or set(usfm)!=set(CANON):errors.append('Canon inventory mismatch')
  for b in books:
   bid=b['id'];n=names[bid];b.update(name=n['short'],longName=n['long'],english=ENGLISH[CANON.index(bid)],aliases=list(dict.fromkeys([bid,n['short'],n['long'],n['abbr'],*([n['alt']] if n['alt'] else [])])))
   inventory[bid]={}; seen=set();flat={}
   for c in b['chapters']:
    if c['label'] in seen:errors.append(f'Duplicate chapter {bid}.{c["label"]}')
    seen.add(c['label']);labels=[];covered=set()
    for v in c['verses']:
     label=v['label'];key=f'{c["label"]}:{label}'
     if key in flat:errors.append(f'Duplicate verse {bid}.{key}')
     flat[key]=v['text'];labels.append(label)
     m=re.fullmatch(r'(\d+)(?:-(\d+))?',label)
     if not m:errors.append(f'Unsupported label {bid}.{key}');continue
     a=int(m[1]);end=int(m[2] or m[1]);v['start']=a;v['end']=end
     for num in range(a,end+1):
      if num in covered:exceptions.append({'reference':f'{bid}.{c["label"]}.{num}','type':'overlap','sourceLabel':label})
      covered.add(num)
     if end!=a:exceptions.append({'reference':f'{bid}.{key}','type':'bridge','sourceLabel':label})
     if not v['text']:exceptions.append({'reference':f'{bid}.{key}','type':'empty-source-verse','sourceLabel':label})
    inventory[bid][c['label']]=labels
    gaps=sorted(set(range(1,max(covered,default=0)+1))-covered)
    if gaps:exceptions.append({'reference':f'{bid}.{c["label"]}','type':'source-numbering-gaps','numbers':gaps})
   if set(flat)!=set(usfm.get(bid,{})):errors.append(f'USFM/USFX label mismatch {bid}')
   for key,value in flat.items():
    if usfm.get(bid,{}).get(key)!=value:differences.append({'reference':bid+'.'+key,'usfx':value,'usfm':usfm.get(bid,{}).get(key)})
  info={'id':id,'title':meta.findtext('identification/name'),'nativeTitle':meta.findtext('identification/nameLocal'),'language':meta.findtext('language/name'),'lang':{'engwebp':'en','mal':'ml','hin2017':'hi','mar':'mr','tam2017':'ta','tel2017':'te'}[id],'abbreviation':meta.findtext('identification/abbreviationLocal'),'scope':'66-book Protestant collection','source':f'https://ebible.org/Scriptures/details.php?id={id}','license':'Public domain' if id=='engwebp' else 'CC BY-SA 4.0','licenseUrl':'https://worldenglish.bible/' if id=='engwebp' else 'https://creativecommons.org/licenses/by-sa/4.0/','copyright': 'World English Bible, eBible.org. Public domain.' if id=='engwebp' else ('Copyright © 2017, 2019 Bridge Communication Systems. Contributor: Bridge Connectivity Solutions Pvt. Ltd.' if id=='mal' else 'Copyright © 2017, '+('2018, ' if id=='hin2017' else '')+'2019 Bridge Connectivity Solutions. Contributor: Bridge Connectivity Solutions Pvt. Ltd.'),'retrieved':'2026-11-15','sources':[{ 'url':f'https://ebible.org/Scriptures/{id}_{fmt}.zip','sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for fmt,p in paths.items()]}
  report={**info,'books':len(books),'chapters':sum(len(b['chapters']) for b in books),'verseUnits':sum(len(c['verses']) for b in books for c in b['chapters']),'errors':errors,'textDifferences':len(differences),'exceptions':exceptions,'excludedSourceBooks':[b.get('id') for b in root.findall('book') if b.get('id') not in CANON],'status':'source-compared' if not errors and not differences else 'blocked','limitations':['USFM and USFX are two publisher exports, not independent manuscripts.','Whitespace collapsed for presentation; notes and headings separated; lexical attributes and typography not reproduced.','No independent theological or printed-edition certification.','Cross-translation passage alignment is not certified.']}
  outdir=ROOT/'dist'/'licenses'/id;outdir.mkdir(parents=True,exist_ok=True)
  for n in ['copr.htm',f'{id}metadata.xml','BookNames.xml']: (outdir/n).write_bytes(z.read(n))
  dump(ROOT/'reports'/f'{id}-inventory.json',inventory);dump(ROOT/'reports'/f'{id}-differences.json',differences);dump(ROOT/'reports'/f'{id}-validation.json',report)
  if report['status']=='source-compared':
   pack={**info,'validation':{'status':report['status'],'books':report['books'],'chapters':report['chapters'],'verseUnits':report['verseUnits'],'exceptionCount':len(exceptions)},'books':books}
   path=ROOT/'dist'/'data'/f'{id}.json';dump(path,pack);manifest.append({**info,**pack['validation'],'file':f'data/{id}.json','sha256':sha(path.read_bytes()),'bytes':path.stat().st_size})
  reports.append(report);print(id,report['status'],report['books'],report['chapters'],report['verseUnits'],'diffs',len(differences),'exceptions',len(exceptions),errors)
 dump(ROOT/'dist'/'catalog.json',{'schema':1,'editions':manifest,'blocked':[r['id'] for r in reports if r['status']=='blocked']});dump(ROOT/'reports'/'validation.json',reports)
if __name__=='__main__':build()
