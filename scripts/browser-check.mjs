import {chromium} from 'playwright';
import {createServer} from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root=path.resolve('examples/caseflow/design/caseflow');
const source='experience/prototype/app.js';
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const server=createServer((req,res)=>{const file=path.join(root,'experience/prototype',req.url==='/'?'index.html':req.url);if(!file.startsWith(path.join(root,'experience/prototype')+path.sep)){res.writeHead(403).end();return;}try{res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');res.end(fs.readFileSync(file));}catch{res.writeHead(404).end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const browser=await chromium.launch(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{});
const page=await browser.newPage({viewport:{width:1280,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
const screens=[];const observations=[];fs.mkdirSync(path.join(root,'experience/screenshots'),{recursive:true});fs.mkdirSync(path.join(root,'validation/evidence'),{recursive:true});
const assert=(v,msg)=>{if(!v)throw Error(msg);observations.push(msg)};
async function capture(state,mobile=false){const capture=`experience/screenshots/${state.toLowerCase()}${mobile?'-mobile':''}.png`;await page.screenshot({path:path.join(root,capture),fullPage:true});screens.push({id:`SCREEN-${state}`,state,route:'/',fixture:'CASE-104',viewport:page.viewportSize(),device:'emulated viewport',captured_at:new Date().toISOString(),capture,source,source_sha256:hash(path.join(root,source)),requirements:['FR-1'],html_source_sha256:hash(path.join(root,'experience/prototype/index.html'))});}
try{
 await page.goto(`http://127.0.0.1:${server.address().port}`);
 await capture('Question');
 await page.getByRole('button',{name:'Submit answer & resume'}).click();assert((await page.locator('#toast').innerText()).includes('Enter an answer'),'Empty answer rejected');
 await page.selectOption('#role','Approver');assert(await page.locator('#answer-submit').isDisabled(),'Wrong role cannot answer');
 await page.selectOption('#role','Requester');await page.fill('#answer','24 participants');await page.click('#answer-submit');await capture('Resumed');
 await page.reload();assert((await page.locator('#saved-answer').innerText())==='24 participants','Answer persists after reload');
 await page.click('[data-phase="Decision"]');assert((await page.locator('#status').innerText())==='Agent work resumed','Phase inspection does not advance state');
 await page.click('#prepare');await capture('Package');assert(await page.locator('#review').isDisabled(),'Requester cannot mark specialist review');
 await page.selectOption('#role','Specialist');await page.click('#review');await capture('Decision');assert(await page.locator('#approve').isDisabled(),'Specialist cannot approve');
 await page.selectOption('#role','Requester');await page.locator('#work summary').click();await page.fill('#change','30 participants');await page.click('#revise');assert((await page.locator('#status').innerText())==='Agent work resumed','Revision invalidates package review');
 await page.click('#prepare');await page.selectOption('#role','Specialist');await page.click('#review');await page.selectOption('#role','Approver');await page.click('#approve');await capture('Complete');assert((await page.locator('#decision').innerText()).includes('Approved'),'Human final decision recorded');
 await page.click('#reset');await page.selectOption('#role','Requester');await page.fill('#answer','24 participants');await page.click('#answer-submit');await page.click('#fail');await capture('Error');
 await page.selectOption('#role','Specialist');await page.click('#retry');assert((await page.locator('#status').innerText())==='Agent work resumed','Specialist retry restores saved context');await page.click('#fail');assert(await page.locator('#retry').isDisabled(),'Retry budget enforced');await page.click('#cancel');assert((await page.locator('#status').innerText())==='Cancelled','Cancellation stops preparation');
 await page.setViewportSize({width:390,height:844});await page.click('#reset');await page.selectOption('#role','Requester');await capture('Question',true);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Mobile viewport has no horizontal overflow');
 await page.locator('#answer').focus();await page.keyboard.type('24 participants');await page.keyboard.press('Tab');assert(await page.locator('#answer-submit').evaluate(el=>el===document.activeElement),'Keyboard reaches answer action');await page.keyboard.press('Enter');await page.click('#prepare');await capture('Package',true);
 assert(errors.length===0,'No browser JavaScript errors');
 fs.writeFileSync(path.join(root,'experience/screens.json'),JSON.stringify(screens,null,2)+'\n');
 fs.writeFileSync(path.join(root,'validation/evidence/browser.json'),JSON.stringify({executed_at:new Date().toISOString(),browser:browser.version(),level:'simulation',source_hashes:{[source]:hash(path.join(root,source)),'experience/prototype/index.html':hash(path.join(root,'experience/prototype/index.html'))},observations,limitations:['No live business agent','No production authorization or scheduling','No human stakeholder acceptance','Emulated mobile viewport, not physical device']},null,2)+'\n');
 console.log(JSON.stringify({passed:observations.length,captures:screens.length,browser:browser.version()}));
}finally{await browser.close();server.close();}
