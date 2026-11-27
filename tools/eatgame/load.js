// loads the EATG script out of an index.html (default: the worktree) into node, exposing internals for tuning/tests
const fs=require('fs');
module.exports=function(file){ file=file||require('path').join(__dirname,'..','..','index.html');
 const html=fs.readFileSync(file,'utf8'); const a=html.indexOf('<script id="eatg-src">'), b=html.indexOf('</script>',a);
 let src=html.slice(a+'<script id="eatg-src">'.length,b);
 src=src.replace(/^root\.EATG = \{ /m,'root.EATG = { _sim: simulate, _items: ITEMS, _newRun: newRun, _step: stepLogic, _in: inDown, _up: inUp, _bot: makeBot, ');
 const g={}; g.window=g; g.document={createElement(){return{getContext(){return new Proxy({},{get:()=>()=>({})})},style:{}}},addEventListener(){},body:{appendChild(){}}};
 g.requestAnimationFrame=()=>0; g.cancelAnimationFrame=()=>0; g.Image=function(){};
 new Function('window','document','requestAnimationFrame','cancelAnimationFrame','Image',src)(g,g.document,g.requestAnimationFrame,g.cancelAnimationFrame,g.Image);
 return g.EATG; };
