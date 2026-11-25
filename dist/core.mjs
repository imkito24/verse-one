export const normalize=s=>String(s).normalize('NFC').replace(/[ൺൻർൽൾൿ]/g,c=>({'ൺ':'ണ്','ൻ':'ന്','ർ':'ര്','ൽ':'ല്','ൾ':'ള്','ൿ':'ക്'}[c])).toLocaleLowerCase().replace(/[\u200c\u200d]/g,'').replace(/\s+/g,' ').trim();
export const tokens=s=>normalize(s).match(/[\p{L}\p{M}\p{N}]+/gu)||[];
const aliasKey=s=>normalize(s).replace(/[\s.\-]/g,'');
const extra={GEN:['gen','ge'],EXO:['ex','exod'],LEV:['lev'],NUM:['num'],DEU:['deut'],JOS:['josh'],JDG:['judg'],PSA:['ps','psalm','psalms'],PRO:['prov'],ECC:['eccl'],SNG:['song','song of songs','song of solomon','sos'],ISA:['isa'],JER:['jer'],EZK:['ezek'],DAN:['dan'],MAT:['mt','matt'],MRK:['mk','mark'],LUK:['lk','luke'],JHN:['jn','jhn','john'],ACT:['acts'],ROM:['rom'],PHP:['phil','philippians'],PHM:['phlm','philemon'],REV:['rev','revelation'],'1SA':['1sam'],'2SA':['2sam'],'1CO':['1cor'],'2CO':['2cor'],'1JN':['1jn'],'2JN':['2jn'],'3JN':['3jn']};
export function makeEngine(pack){
 const rows=[], refs=new Map(),chapterRows=new Map(),aliases=new Map();
 for(const b of pack.books){for(const a of [b.id,b.name,b.longName,b.english,...b.aliases,...(extra[b.id]||[])]){const k=aliasKey(a);if(!aliases.has(k))aliases.set(k,new Set());aliases.get(k).add(b.id)}for(const c of b.chapters){refs.set(b.id+':'+c.label,c);const local=c.verses.map(v=>({...v,book:b.id,bookName:b.name,chapter:c.label}));chapterRows.set(b.id+':'+c.label,local);rows.push(...local)}}
 const index=pack.index||{};if(!pack.index)rows.forEach((r,i)=>{for(const t of new Set(tokens(r.text)))(index[t]??=[]).push(i)});
 function resolve(q){
  let s=normalize(q).replace(/^(first|i)\s+/,'1 ').replace(/^(second|ii)\s+/,'2 ').replace(/^(third|iii)\s+/,'3 ');
  s=s.replace(/[०-९]/g,c=>String(c.charCodeAt(0)-2406)).replace(/[–—]/g,'-');
  const m=s.match(/^(.+?)\s*(\d{1,3})(?:[:.](\d{1,3})(?:-(\d{1,3}))?)?$/);
  if(!m)return null;
  const key=aliasKey(m[1]);let candidates=aliases.get(key);
  if(!candidates&&key.length>=3){candidates=new Set();for(const [a,ids] of aliases)if(a.startsWith(key))for(const id of ids)candidates.add(id)}
  if(!candidates?.size) return {error:'Book name not recognized. Choose a book or use its full name.'};
  if(candidates.size!==1)return {error:'Ambiguous book abbreviation. Please use the full book name.'};
  const book=[...candidates][0],ch=refs.get(book+':'+Number(m[2]));
  if(!ch)return {error:'That chapter is not present in this edition.'};
  const start=m[3]?Number(m[3]):null,end=m[4]?Number(m[4]):start;
  if(start!==null&&(start<1||end<start))return {error:'Invalid verse range.'};
  const result=chapterRows.get(book+':'+ch.label).filter(r=>start===null||(r.end>=start&&r.start<=end));
  if(start!==null){for(let n=start;n<=end;n++)if(!result.some(v=>v.start<=n&&v.end>=n))return {error:'One or more requested verse numbers are absent in this edition. No text has been substituted.'}}
  return {kind:'reference',book,chapter:ch.label,rows:result,total:result.length};
 }
 function search(q,mode='words',offset=0,limit=100){
  const reference=resolve(q);if(reference)return reference;
  const needle=normalize(q).replace(/^"|"$/g,'');const terms=[...new Set(tokens(needle))];
  if(!terms.length)return {error:'Enter a reference, word or phrase.'};
  const lists=terms.map(t=>Object.hasOwn(index,t)?index[t]:[]).sort((a,b)=>a.length-b.length);let ids=lists[0];
  for(const list of lists.slice(1)){const set=new Set(list);ids=ids.filter(i=>set.has(i))}
  if(mode==='phrase'||/^".*"$/.test(q.trim()))ids=ids.filter(i=>normalize(rows[i].text).includes(needle));
  return {kind:'text',total:ids.length,rows:ids.slice(offset,offset+limit).map(i=>rows[i]),offset};
 }
 return {rows,search,resolve,refs,index};
}
