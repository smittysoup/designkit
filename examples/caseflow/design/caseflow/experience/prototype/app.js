const key='designkit-caseflow-v1';
const seed=()=>({state:'question',version:1,answer:'',package:null,decision:null,runs:1,retries:0,events:['Simulated evidence scan: workshop purpose known; participant count missing.','Question Q-104 persisted. Preparation waits for requester.']});
let data;try{data=JSON.parse(localStorage.getItem(key))||seed()}catch{data=seed()}
let role='Requester';
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function save(){localStorage.setItem(key,JSON.stringify(data));render()}
function notice(s){$('toast').textContent=s}
function action(id,handler){$(id)?.addEventListener('click',()=>{notice('');handler()})}
function transition(state,event){data.state=state;data.version++;data.events.push(event);save()}
function render(){
 $('status').textContent=({question:'Waiting for requester',resumed:'Agent work resumed',error:'Intervention required',package:'Specialist review',reviewed:'Approver decision',complete:'Decision recorded',cancelled:'Cancelled'})[data.state];
 $('revision').textContent='v'+data.version;$('saved-answer').textContent=data.answer||'Not yet answered';$('decision').textContent=data.decision||'Reserved for approver';$('run').textContent=`RUN-${data.runs} · Preparation definition TASK-Prepare · case work WORK-104`;
 $('events').innerHTML=data.events.map(e=>`<div class="event">${esc(e)}</div>`).join('');
 $('fail').disabled=!['question','resumed'].includes(data.state);
 let html='';
 if(data.state==='question')html=`<h2>How many participants should the package cover?</h2><p>The preparation agent needs the participant count before it can gather sufficient evidence. Only the assigned requester can answer.</p><label for="answer">Your answer</label><textarea id="answer" placeholder="For example: 24 participants" ${role!=='Requester'?'disabled':''}></textarea><button id="answer-submit" ${role!=='Requester'?'disabled':''}>Submit answer & resume</button>`;
 if(data.state==='resumed')html=`<h2>The agent has resumed preparation</h2><p>Your attributed answer is saved. The simulated agent can now assemble the package using the permitted evidence tool.</p><button id="prepare">Run simulated preparation</button>`;
 if(['package','reviewed'].includes(data.state))html=`<h2>Reviewable package · v${data.package.version}</h2><p><strong>Recommendation:</strong> Review workshop supply needs for ${esc(data.answer)}. No purchase or commitment has been made.</p><p class="muted">Evidence: synthetic case brief + requester response Q-104. Prepared by RUN-${data.runs}. Human approval remains required.</p>${data.state==='package'?`<button id="review" ${role!=='Specialist'?'disabled':''}>Mark specialist review complete</button>`:`<button id="approve" ${role!=='Approver'?'disabled':''}>Approve package</button> <button id="reject" class="secondary" ${role!=='Approver'?'disabled':''}>Return for clarification</button>`}<details><summary>Propose a requirement change</summary><p>A requester revision invalidates the package and specialist review.</p><label for="change">Revised participant requirement</label><textarea id="change"></textarea><button id="revise" ${role!=='Requester'?'disabled':''}>Submit revised requirement</button></details>`;
 if(data.state==='error')html=`<div class="notice">Simulated tool error TOOL_UNAVAILABLE. The answer is preserved; no package or decision was produced.</div><h2>Specialist intervention needed</h2><p>One explicit retry is permitted in this demonstration. Further failure requires cancellation and investigation.</p><div class="actions"><button id="retry" ${role!=='Specialist'||data.retries>=1?'disabled':''}>Retry simulated tool</button><button id="cancel" class="secondary" ${role!=='Specialist'?'disabled':''}>Cancel preparation</button></div>`;
 if(data.state==='complete')html='<h2>The human decision is recorded</h2><p>The approver accepted the reviewable package. The agent prepared evidence; the human retained the final judgment. No real-world action has been taken.</p>';
 if(data.state==='cancelled')html='<h2>Preparation cancelled</h2><p>Existing evidence is retained. No agent run continues. Reset to start a separate synthetic exercise.</p>';
 $('work').innerHTML=html;
 action('answer-submit',()=>{if(role!=='Requester'||data.state!=='question')return notice('Not authorized for this state');const answer=$('answer').value.trim();if(!answer)return notice('Enter an answer before resuming.');data.answer=answer;data.runs++;transition('resumed','Requester response saved; dependent preparation resumed.');});
 action('prepare',()=>{if(data.state!=='resumed')return;data.package={version:data.version+1,answer:data.answer};transition('package','Simulated tool receipt stored. Package ready for specialist review.');});
 action('review',()=>{if(role==='Specialist'&&data.state==='package')transition('reviewed','Specialist reviewed this package revision. Approver decision requested.');});
 action('approve',()=>{if(role==='Approver'&&data.state==='reviewed'){data.decision='Approved by fictional approver';transition('complete','Human decision recorded. Preparation outcome complete.');}});
 action('reject',()=>{if(role==='Approver'&&data.state==='reviewed'){data.package=null;transition('question','Approver returned package for clarification; review invalidated.');}});
 action('revise',()=>{if(role!=='Requester')return;const a=$('change').value.trim();if(!a)return notice('Describe the revised requirement.');data.answer=a;data.package=null;data.runs++;transition('resumed','Requester revised requirement. Prior package/review invalidated; preparation resumed.');});
 action('retry',()=>{if(role==='Specialist'&&data.state==='error'&&data.retries<1){data.retries++;data.runs++;transition(data.answer?'resumed':'question','Specialist authorized one simulated retry; saved context restored.');}});
 action('cancel',()=>{if(role==='Specialist'&&data.state==='error')transition('cancelled','Specialist cancelled preparation; no further retries.');});
}
$('role').addEventListener('change',()=>{role=$('role').value;notice('');render()});
$('reset').onclick=()=>{data=seed();notice('');save()};
$('fail').onclick=()=>{if(['question','resumed'].includes(data.state))transition('error','Simulated evidence tool unavailable. Work stopped for intervention.');};
document.querySelectorAll('[data-phase]').forEach(b=>b.onclick=()=>{$('phase').textContent=`Inspecting ${b.dataset.phase} · Navigation does not advance work.`});
render();
