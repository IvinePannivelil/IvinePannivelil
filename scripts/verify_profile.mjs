// Local browser verification. Requires Node.js and Playwright.
// Default: use installed Google Chrome. Override PROFILE_CHROMIUM_EXECUTABLE if needed.
// Optional PROFILE_QA_DIR chooses the output directory; PROFILE_QA_SCREENSHOTS=1 captures images.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=process.env.PROFILE_QA_DIR || path.join(root,'profile-polish','verification');
import {pathToFileURL} from 'node:url';
const playwrightModule = process.env.PROFILE_PLAYWRIGHT_MODULE
  ? (process.env.PROFILE_PLAYWRIGHT_MODULE.startsWith('file:') ? process.env.PROFILE_PLAYWRIGHT_MODULE : pathToFileURL(path.resolve(process.env.PROFILE_PLAYWRIGHT_MODULE)).href)
  : 'playwright';
const {chromium}=await import(playwrightModule);
await fs.mkdir(output,{recursive:true});
const mime={'.html':'text/html; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.ico':'image/x-icon','.md':'text/plain; charset=utf-8'};
const server=http.createServer(async(req,res)=>{
  try{
    const p=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
    if(!p.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
    const data=await fs.readFile(p);res.writeHead(200,{'Content-Type':mime[path.extname(p)]||'application/octet-stream'});res.end(data);
  }catch{res.writeHead(404);res.end('Not found');}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const origin=`http://127.0.0.1:${server.address().port}`;
const failures=[],errors=[];
const assert=(condition,message)=>{if(!condition)failures.push(message);};
let browser;
const result={checkedAt:new Date().toISOString(),scope:'Local browser only; no live GitHub test',viewports:[],reducedMotion:[],assets:[],motionSamples:[],failures,errors};
try{
  const options={headless:true};
  if(process.env.PROFILE_CHROMIUM_EXECUTABLE)options.executablePath=process.env.PROFILE_CHROMIUM_EXECUTABLE;
  else options.channel='chrome';
  if(process.env.PROFILE_BROWSER_ARGS)options.args=JSON.parse(process.env.PROFILE_BROWSER_ARGS);
  browser=await chromium.launch(options);result.browserVersion=browser.version();
  const ctx=await browser.newContext({deviceScaleFactor:1,reducedMotion:'no-preference'});
  const page=await ctx.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${new URL(r.url()).pathname}`);});

  // Verify approved master PNG SHA-256
  const crypto = await import('node:crypto');
  const masterBuf = await fs.readFile(path.join(root, 'v4/motion-proof/assets/ivine-approved-arms-folded.png'));
  const masterDigest = crypto.createHash('sha256').update(masterBuf).digest('hex');
  assert(masterDigest === 'a9885b2629713ef3048b98fe9ded0b749c080dd06b4e8ac1e6f4fe0220d52101', 'Approved master PNG hash mismatch');
  result.masterPngSha256 = masterDigest;

  for(const [width,height] of [[1440,1000],[1024,900],[390,844],[360,780]]){
    await page.setViewportSize({width,height});
    await page.goto(origin+'/preview.html',{waitUntil:'networkidle'});
    await page.evaluate(()=>Promise.all([...document.images].map(img=>img.decode())));
    const metrics=await page.evaluate(()=>{
      const d=document.documentElement;
      return {width:innerWidth,height:innerHeight,dpr:devicePixelRatio,clientWidth:d.clientWidth,scrollWidth:d.scrollWidth,
        pictures:[...document.querySelectorAll('#readme-article picture img')].map(img=>{const r=img.getBoundingClientRect();return{source:new URL(img.currentSrc).pathname,x:r.x,y:r.y,width:r.width,height:r.height,loaded:img.complete&&img.naturalWidth>0};}),
        overflowing:[...document.querySelectorAll('#readme-article *')].filter(el=>{const r=el.getBoundingClientRect();return r.width>0&&(r.left<-.5||r.right>innerWidth+.5)}).map(el=>el.tagName).slice(0,10)};
    });
    result.viewports.push(metrics);
    assert(metrics.width===width,'Viewport mismatch '+width);
    assert(metrics.scrollWidth<=metrics.clientWidth,'Page overflow '+width);
    assert(!metrics.overflowing.length,'Content outside viewport '+width);
    assert(metrics.pictures.every(x=>x.loaded),'Unloaded image '+width);
    assert(metrics.pictures[0].source.endsWith(width<=600?'hero-mobile.svg':'hero-desktop.svg'),'Wrong hero source '+width);
    if(process.env.PROFILE_QA_SCREENSHOTS==='1')await page.screenshot({path:path.join(output,`profile-${width}.png`),fullPage:true});
  }

  // Check expandable academic section and links
  await page.setViewportSize({width:1024,height:900});
  await page.goto(origin+'/preview.html',{waitUntil:'networkidle'});
  const linkAndDetailsCheck = await page.evaluate(async () => {
    const details = document.querySelector('details');
    const summary = details ? details.querySelector('summary') : null;
    const initialOpen = details ? details.open : null;
    if (summary) summary.click();
    const afterClickOpen = details ? details.open : null;
    const links = [...document.querySelectorAll('#readme-article a')].map(a => ({
      text: a.textContent.trim(),
      href: a.getAttribute('href')
    }));
    return { hasDetails: !!details, initialOpen, afterClickOpen, links };
  });
  assert(linkAndDetailsCheck.hasDetails, 'Details element missing');
  assert(linkAndDetailsCheck.afterClickOpen === true, 'Expandable details did not open on click');
  assert(linkAndDetailsCheck.links.some(l => l.href.includes('JIVA')), 'JIVA link missing');
  assert(linkAndDetailsCheck.links.some(l => l.href.includes('linkedin.com')), 'LinkedIn link missing');
  assert(linkAndDetailsCheck.links.some(l => l.href.includes('mailto:')), 'Email link missing');
  assert(linkAndDetailsCheck.links.some(l => l.href.includes('Industrial-Conveyor-Vision-Analytics')), 'Conveyor vision link missing');
  result.linksAndDetails = linkAndDetailsCheck;

  await page.emulateMedia({reducedMotion:'reduce'});
  for(const width of [1440,390]){
    await page.setViewportSize({width,height:900});
    await page.goto(origin+'/preview.html',{waitUntil:'networkidle'});
    const m=await page.evaluate(()=>({matches:matchMedia('(prefers-reduced-motion: reduce)').matches,source:new URL(document.querySelector('#readme-article picture img').currentSrc).pathname}));
    result.reducedMotion.push({width,...m});
    assert(m.matches&&m.source.endsWith(width===390?'hero-mobile-static.svg':'hero-desktop-static.svg'),'Reduced-motion source '+width);
  }
  await page.setViewportSize({width:1100,height:1200});
  for(const name of (await fs.readdir(path.join(root,'profile-polish/assets'))).filter(n=>n.endsWith('.svg'))){
    await page.goto(origin+'/profile-polish/assets/'+name,{waitUntil:'load'});
    const m=await page.evaluate(()=>{
      const svg=document.querySelector('svg'),box=svg.getBoundingClientRect();
      return{outOfBounds:[...svg.querySelectorAll('text')].filter(el=>{const r=el.getBoundingClientRect();return r.left<box.left-1||r.right>box.right+1||r.top<box.top-1||r.bottom>box.bottom+1}).map(el=>el.textContent)};
    });
    result.assets.push({name,...m});assert(!m.outOfBounds.length,'Text clipped in '+name);
  }
  await page.goto(origin+'/v4/motion-proof/assets/hero-desktop.svg',{waitUntil:'load'});
  const reduced=await page.evaluate(()=>Object.fromEntries(['.entrance','.head-idle','.trace'].map(s=>[s,getComputedStyle(document.querySelector(s)).animationName])));
  result.directSvgReducedMotion=reduced;
  assert(Object.values(reduced).every(v=>v==='none'),'Direct SVG reduced motion');
  await page.emulateMedia({reducedMotion:'no-preference'});
  await page.reload({waitUntil:'load'});
  await page.waitForTimeout(1300);
  for(let i=0;i<17;i++){
    result.motionSamples.push(await page.evaluate(()=>{
      const head=document.querySelector('.head-idle'),body=document.querySelector('#body'),r=body.getBoundingClientRect();
      return{time:performance.now(),headTransform:getComputedStyle(head).transform,bodyTransform:getComputedStyle(body).transform,bodyRect:[r.x,r.y,r.width,r.height]};
    }));
    if(i<16)await page.waitForTimeout(500);
  }
  const samples=result.motionSamples;
  assert(new Set(samples.map(x=>x.headTransform)).size>2,'Head did not move over a full cycle');
  assert(samples.every(x=>x.bodyTransform==='none'),'Unexpected body transform');
  const reference=samples[0].bodyRect;
  assert(samples.every(x=>x.bodyRect.every((v,i)=>Math.abs(v-reference[i])<.01)),'Body moved during head idle');
  result.motionObservedSeconds=(samples.at(-1).time-samples[0].time)/1000;
  assert(!errors.length,'Browser resource or script errors');
}catch(e){failures.push(String(e.stack||e));}
finally{
  if(browser)await browser.close();
  await new Promise(resolve=>server.close(resolve));
  result.passed=failures.length===0;
  await fs.writeFile(path.join(output,'browser-results.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({passed:result.passed,browser:result.browserVersion,viewports:result.viewports.map(v=>v.width),motionObservedSeconds:result.motionObservedSeconds,failures},null,2));
  if(!result.passed)process.exitCode=1;
}
