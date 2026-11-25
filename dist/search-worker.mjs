import {makeEngine} from './core.mjs';
let engine,edition;
self.onmessage=({data})=>{try{if(data.type==='load'){engine=makeEngine(data.pack);edition=data.pack.id;self.postMessage({type:'ready',edition});return}if(data.type==='search'&&engine){const start=performance.now();self.postMessage({type:'results',requestId:data.requestId,edition,result:engine.search(data.query,data.mode,data.offset),ms:performance.now()-start})}}catch(e){self.postMessage({type:'error',requestId:data.requestId,edition,message:e.message})}};
