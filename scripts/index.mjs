import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {makeEngine} from '../dist/core.mjs';
const root=path.resolve(import.meta.dirname,'..');const catalog=JSON.parse(fs.readFileSync(root+'/dist/catalog.json'));
for(const e of catalog.editions){const p=root+'/dist/'+e.file,pack=JSON.parse(fs.readFileSync(p));pack.index=makeEngine({...pack,index:undefined}).index;const bytes=JSON.stringify(pack);fs.writeFileSync(p,bytes);e.sha256=crypto.createHash('sha256').update(bytes).digest('hex');e.bytes=Buffer.byteLength(bytes);console.log(e.id,e.bytes,Object.keys(pack.index).length)}
fs.writeFileSync(root+'/dist/catalog.json',JSON.stringify(catalog));
