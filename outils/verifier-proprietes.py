"""Teste les propriétés dans le coffre isolé romā. Nécessite Playwright et CDP."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cdp',required=True);parser.add_argument('--coffre',required=True,type=Path);parser.add_argument('--sortie',required=True,type=Path)
a=parser.parse_args();a.sortie.mkdir(parents=True,exist_ok=True)
refs={f:f.read_bytes() for f in (a.coffre/'References').glob('*.md')}
file='Notes/Essai technique des propriétés.md'
fields={'type':'Source','domaine':'Connaissance','mots-clés':['Obsidian','Écriture','Gestion des connaissances','Une valeur de liste particulièrement longue à vérifier'],'source':'https://www.thethinkers.club/p/how-to-build-a-commonplace-in-obsidian?contexte='+('connaissance-transverse-'*8),'Critère de sélection particulièrement important':'Une description longue, lisible et modifiable. '*8,'vide':'','achete':True,'prix':39}
content='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in fields.items())+'---\n\n# Essai des propriétés\n\nNote temporaire de vérification.\n'
report={'editions':{},'dispositions':[]}
with sync_playwright() as p:
 b=p.chromium.connect_over_cdp(a.cdp);pg=next(pg for c in b.contexts for pg in c.pages if 'obsidian.md' in pg.url)
 assert pg.evaluate('()=>app.vault.adapter.basePath')==str(a.coffre.resolve())
 assert pg.evaluate('()=>Object.keys(app.plugins.plugins)')==[]
 pg.evaluate("()=>app.customCss.setTheme('Tasogare')")
 assert not pg.evaluate('f=>!!app.vault.getAbstractFileByPath(f)',file),'Le fichier de test existe déjà.'
 try:
  pg.evaluate('''async arg=>{await app.vault.create(arg.file,arg.content);await app.workspace.getMostRecentLeaf().setViewState({type:'markdown',state:{file:arg.file,mode:'preview'}})}''',{'file':file,'content':content})
  pg.wait_for_selector('[data-property-key="type"]')
  for width in [1136,900,760]:
   pg.set_viewport_size({'width':width,'height':900})
   for right in [True,False]:
    pg.evaluate("r=>{app.workspace.rightSplit[r?'expand':'collapse']();app.workspace.leftSplit.expand()}",right);pg.wait_for_timeout(400)
    r=pg.evaluate('''()=>{const rows=[...document.querySelectorAll('.metadata-property')];return {overflow:document.documentElement.scrollWidth>innerWidth,rows:rows.map(e=>{const k=e.querySelector('.metadata-property-key'),i=e.querySelector('input'),v=e.querySelector('.metadata-property-value');return {key:i.value,width:e.getBoundingClientRect().width,keyWidth:k.getBoundingClientRect().width,valueX:v.getBoundingClientRect().x,valueRight:v.getBoundingClientRect().right,right:e.getBoundingClientRect().right,top:e.getBoundingClientRect().top,bottom:e.getBoundingClientRect().bottom,colon:getComputedStyle(k,'::after').content}})}}''')
    assert not r['overflow'],r
    assert all(x['valueRight']<=x['right']+1 and x['keyWidth']<=x['width']/2+1 for x in r['rows']),r
    short=[x for x in r['rows'] if x['key'] in ['type','domaine','mots-clés','source']]
    if r['rows'][0]['width']>350:assert len({round(x['valueX']) for x in short})>=3,r
    assert all(y['top']>=x['bottom']-1 for x,y in zip(r['rows'],r['rows'][1:])),r
    assert all(x['colon']=='":"' for x in r['rows']),r
    report['dispositions'].append({'largeur':width,'droite':right,'mesures':r})
  # Une édition réelle et un renommage doivent atteindre le fichier YAML.
  pg.set_viewport_size({'width':1136,'height':900})
  pg.locator('[data-property-key="type"] .metadata-input-longtext').fill('Article');pg.locator('[data-property-key="type"] .metadata-input-longtext').press('Tab')
  pg.wait_for_function("f=>app.metadataCache.getFileCache(app.vault.getAbstractFileByPath(f))?.frontmatter?.type==='Article'",arg=file)
  report['editions']['valeur_enregistree']=True
  pg.locator('[data-property-key="domaine"] .metadata-property-key-input').fill('champ temporaire');pg.locator('[data-property-key="domaine"] .metadata-property-key-input').press('Enter')
  pg.wait_for_function("f=>app.metadataCache.getFileCache(app.vault.getAbstractFileByPath(f))?.frontmatter?.['champ temporaire']==='Connaissance'",arg=file)
  report['editions']['cle_renommee']=True
  # Les notes existantes gardent les clés minuscules et restent inchangées.
 finally:
  pg.evaluate('''async f=>{await app.workspace.getMostRecentLeaf().setViewState({type:'markdown',state:{file:'Notes/Exemple — Propriétés structurées.md',mode:'preview'}});const temp=app.vault.getAbstractFileByPath(f);if(temp)await app.vault.delete(temp)}''',file)
  pg.set_viewport_size({'width':1136,'height':812});pg.evaluate('()=>app.workspace.rightSplit.expand()');pg.wait_for_timeout(400)
 for mode in ['dark','light']:
  pg.evaluate("m=>{app.vault.setConfig('theme',m==='dark'?'obsidian':'moonstone');app.setTheme()}",mode);pg.wait_for_function("m=>document.body.classList.contains('theme-'+m)",arg=mode)
  pg.mouse.move(1050,750);pg.locator('.metadata-container').screenshot(path=str(a.sortie/f'proprietes-inline-{mode}.png'))
assert all(f.read_bytes()==before for f,before in refs.items())
(a.sortie/'verification-proprietes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'dispositions':len(report['dispositions']),'edition':report['editions'],'fiches_preservees':len(refs)},ensure_ascii=False))
