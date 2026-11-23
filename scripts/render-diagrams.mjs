import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {execFileSync} from 'node:child_process';
const root='examples/caseflow/design/caseflow/architecture/diagrams';fs.mkdirSync(root+'/rendered',{recursive:true});
const sources=['entity-model.mmd','data-flow.mmd','process-flows/current-process.mmd','process-flows/agentic-process.mmd'];
const config=path.resolve('node_modules/.puppeteer-designkit.json');fs.writeFileSync(config,JSON.stringify({executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}));
const records=[];
for(const source of sources){const output='rendered/'+path.basename(source,'.mmd')+'.svg';execFileSync('node_modules/.bin/mmdc',['-i',root+'/'+source,'-o',root+'/'+output,'-p',config,'-b','white'],{stdio:'inherit'});records.push({source:'architecture/diagrams/'+source,output:'architecture/diagrams/'+output,sha256:crypto.createHash('sha256').update(fs.readFileSync(root+'/'+source)).digest('hex')});}
fs.writeFileSync(root+'/rendered/sources.json',JSON.stringify(records,null,2)+'\n');
