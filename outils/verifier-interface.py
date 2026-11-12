from pathlib import Path
from playwright.sync_api import sync_playwright
import subprocess,json,re,argparse
parser=argparse.ArgumentParser(description="Vérifie l’interface dans une instance Obsidian isolée, sans plugin communautaire. Nécessite Playwright et un port CDP.")
parser.add_argument('--cdp',required=True)
parser.add_argument('--coffre',required=True,type=Path)
parser.add_argument('--sortie',required=True,type=Path)
args=parser.parse_args()
root=args.sortie;root.mkdir(parents=True,exist_ok=True);repo=Path(__file__).resolve().parent.parent;vault=args.coffre.resolve()
baseline=subprocess.check_output(['git','show','5653884:theme.css'],cwd=repo,text=True);candidate=(repo/'theme.css').read_text()
# La palette et les primitives typographiques ne changent pas dans la source.
def type_tokens(s):return dict(re.findall(r'(--tasogare-(?:type-[a-z-]+|police(?:-code)?))\s*:\s*([^;]+);',s))
assert type_tokens(baseline)==type_tokens(candidate)
colors_start=baseline.index('  /* Graphite */');colors_end=baseline.index('Couche 2 : rôles')
assert baseline[colors_start:colors_end]==candidate[candidate.index('  /* Graphite */'):candidate.index('Couche 2 : rôles')]
refs=list((vault/'References').glob('*.md'));assert len(refs)==155
originals={f:f.read_bytes() for f in refs}
report={'app':'Obsidian 1.15.0 Linux','theme':'Tasogare, essai isolé','source_typographique_identique':True,'palettes_source_identiques':True,'fiches_preservees':155,'palettes':[],'dispositions':[]}
metric_js='''()=>{const s=getComputedStyle(document.body);const p=document.querySelector('.markdown-rendered p');const h=document.querySelector('.markdown-rendered h3');const font=e=>{const c=getComputedStyle(e);return Object.fromEntries(['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing'].map(k=>[k,c[k]]))};return {colors:Object.fromEntries(['--background-primary','--background-secondary','--text-normal','--text-muted','--interactive-accent'].map(k=>[k,s.getPropertyValue(k).trim()])),paragraph:font(p),heading:font(h)}}'''
geometry_js='''()=>{const r=e=>e.getBoundingClientRect().toJSON(),visible=q=>[...document.querySelectorAll(q)].find(e=>e.getBoundingClientRect().width>0);const main=visible('.mod-root .workspace-leaf'),right=visible('.mod-right-split .workspace-leaf');const header=document.querySelector('.mod-root .workspace-tab-header-container'),tab=document.querySelector('.mod-root .workspace-tab-header.is-active');return {main:r(document.querySelector('.mod-root')),mainCard:r(main),right:r(document.querySelector('.mod-right-split')),rightCard:right?r(right):null,header:r(header),tab:r(tab),overflow:document.documentElement.scrollWidth>innerWidth,mainRadius:getComputedStyle(main).borderRadius,rightRadius:right?getComputedStyle(right).borderRadius:null}}'''
with sync_playwright() as p:
 b=p.chromium.connect_over_cdp(args.cdp);pg=next(pg for c in b.contexts for pg in c.pages if 'obsidian.md' in pg.url)
 pg.reload();pg.wait_for_function('()=>window.app?.workspace?.layoutReady&&window.app?.plugins',timeout=30000)
 pg.set_viewport_size({'width':1136,'height':812})
 config=pg.evaluate('''()=>({theme:app.vault.getConfig('cssTheme'),size:app.vault.getConfig('baseFontSize'),plugins:Object.keys(app.plugins.plugins),snippets:app.customCss.enabledSnippets instanceof Set?[...app.customCss.enabledSnippets]:app.customCss.enabledSnippets})''')
 assert config['theme']=='Tasogare' and config['size']==15 and config['plugins']==[],config
 assert pg.evaluate('()=>app.vault.adapter.basePath')==str(vault), 'Utiliser uniquement le coffre de test désigné.'
 assert not pg.evaluate('()=>[...document.body.classList].some(c=>c.startsWith("hider-"))')
 report['configuration']=config
 assert pg.locator('.status-bar').evaluate('e=>getComputedStyle(e).display')=='none'
 assert pg.locator('.workspace-leaf-content[data-type="file-explorer"] .nav-header').evaluate('e=>getComputedStyle(e).display')=='none'
 pg.evaluate('''async()=>{await app.workspace.openLinkText('Notes/Exemple — Une bibliothèque lisible','',false);await app.workspace.getMostRecentLeaf().setViewState({type:'markdown',state:{file:'Notes/Exemple — Une bibliothèque lisible.md',mode:'preview'}});app.workspace.leftSplit.expand();app.workspace.rightSplit.expand();app.workspace.getLeavesOfType('localgraph')[0].parent.selectTab(app.workspace.getLeavesOfType('localgraph')[0])}''')
 for palette in ['graphite','crepuscule','gres','the','lac','porte','galet']:
  pg.evaluate('''value=>{for(const c of [...document.body.classList])if(c.startsWith('tasogare-'))document.body.classList.remove(c);document.body.classList.add('tasogare-'+value)}''',palette)
  for mode in ['dark','light']:
   pg.evaluate("m=>{app.vault.setConfig('theme',m==='light'?'moonstone':'obsidian');app.setTheme()}",mode)
   pg.wait_for_function("m=>document.body.classList.contains('theme-'+m)",arg=mode);pg.wait_for_timeout(80)
   current=pg.evaluate(metric_js)
   pg.evaluate("css=>{[...document.querySelectorAll('style')].find(s=>s.textContent.includes('Tasogare : thème')).textContent=css}",baseline)
   before=pg.evaluate(metric_js)
   pg.evaluate("css=>{[...document.querySelectorAll('style')].find(s=>s.textContent.includes('Tasogare : thème')).textContent=css}",candidate)
   assert current==before,{'palette':palette,'mode':mode,'avant':before,'apres':current}
   g=pg.evaluate(geometry_js)
   assert abs(g['mainCard']['top']-g['rightCard']['top'])<1,g
   assert abs(g['right']['right']-g['rightCard']['right']-10)<1,g
   assert g['mainRadius']=='16px' and g['rightRadius']=='16px',g
   report['palettes'].append({'palette':palette,'mode':mode,'couleurs_et_typographie_identiques':True,'mesures':current})
 # Configurer le rendu partagé, sans changer les palettes disponibles.
 pg.evaluate("()=>{for(const c of [...document.body.classList])if(c.startsWith('tasogare-'))document.body.classList.remove(c)}")
 for width in [1136,900]:
  pg.set_viewport_size({'width':width,'height':812})
  for mode in ['dark','light']:
   pg.evaluate("m=>{app.vault.setConfig('theme',m==='light'?'moonstone':'obsidian');app.setTheme()}",mode)
   pg.wait_for_function("m=>document.body.classList.contains('theme-'+m)",arg=mode)
   for left,right in [(True,True),(False,True),(True,False),(False,False)]:
    pg.evaluate("s=>{app.workspace.leftSplit[s[0]?'expand':'collapse']();app.workspace.rightSplit[s[1]?'expand':'collapse']()}",[left,right]);pg.wait_for_timeout(350)
    g=pg.evaluate(geometry_js)
    assert not g['overflow'],g
    assert abs(g['main']['right']-g['mainCard']['right']-10)<1,g
    assert abs(g['main']['bottom']-g['mainCard']['bottom']-10)<1,g
    assert g['tab']['top']>=g['header']['top']+9,g
    assert g['tab']['bottom']<=g['header']['bottom']-9,g
    if right:
     assert abs(g['right']['right']-g['rightCard']['right']-10)<1,g
     assert abs(g['right']['bottom']-g['rightCard']['bottom']-10)<1,g
     assert abs(g['mainCard']['top']-g['rightCard']['top'])<1,g
    report['dispositions'].append({'largeur':width,'mode':mode,'gauche':left,'droite':right,'geometrie':g})
    if width==1136 and left and right:
     pg.mouse.move(500,760);pg.screenshot(path=str(root/f'note-{mode}.png'))
 # Panneau redimensionnable : aucun décalage fixe dépendant de sa largeur.
 pg.evaluate('()=>app.workspace.rightSplit.expand()')
 for size in [280,360]:
  pg.evaluate('n=>app.workspace.rightSplit.setSize(n)',size);pg.wait_for_timeout(350);g=pg.evaluate(geometry_js)
  assert abs(g['right']['right']-g['rightCard']['right']-10)<1 and abs(g['mainCard']['top']-g['rightCard']['top'])<1,g
 pg.set_viewport_size({'width':1136,'height':812});pg.evaluate('()=>{app.workspace.leftSplit.expand();app.workspace.rightSplit.setSize(320)}')
 # Les cinq icônes ouvrent les vrais panneaux ; les boutons latéraux les replient.
 expected=['localgraph','backlink','outgoing-link','all-properties','outline']
 actual=pg.evaluate('()=>app.workspace.getLayout().right.children[0].children.map(l=>l.state.type)');assert actual==expected,actual
 for i,t in enumerate(expected):
  pg.locator('.mod-right-split .workspace-tab-header').nth(i).click()
  assert pg.locator(f'.mod-right-split .workspace-leaf-content[data-type="{t}"]').is_visible(),t
 pg.locator('.mod-right-split .workspace-tab-header').nth(0).click()
 for sel,split in [('.sidebar-toggle-button.mod-secondary','rightSplit'),('.sidebar-toggle-button.mod-primary','leftSplit')]:
  pg.locator(sel+':visible').click();pg.wait_for_timeout(350);assert pg.evaluate('s=>app.workspace[s].collapsed',split)
  pg.locator(sel+':visible').click();pg.wait_for_timeout(350);assert not pg.evaluate('s=>app.workspace[s].collapsed',split)
 report['panneaux_natifs']=expected
 pg.evaluate('''async()=>{await app.workspace.openLinkText('Notes/Exemple — Propriétés structurées','',false);await app.workspace.getMostRecentLeaf().setViewState({type:'markdown',state:{file:'Notes/Exemple — Propriétés structurées.md',mode:'preview'}})}''')
 assert pg.locator('.metadata-property-icon').first.evaluate('e=>getComputedStyle(e).display')=='none'
 assert pg.locator('.metadata-container').evaluate('e=>getComputedStyle(e).backgroundColor')=='rgba(0, 0, 0, 0)'
 pg.locator('.metadata-add-button').focus();pg.wait_for_timeout(150)
 assert pg.locator('.metadata-add-button').evaluate('e=>getComputedStyle(e).opacity')=='1'
 report['ajouter_propriete_au_clavier']=True
 pg.evaluate("()=>document.body.classList.add('tasogare-barre-etat','tasogare-actions-fichiers','tasogare-icones-proprietes')")
 assert pg.locator('.status-bar').evaluate('e=>getComputedStyle(e).display')!='none'
 assert pg.locator('.workspace-leaf-content[data-type="file-explorer"] .nav-header').evaluate('e=>getComputedStyle(e).display')!='none'
 assert pg.locator('.metadata-property-icon').first.evaluate('e=>getComputedStyle(e).display')!='none'
 pg.evaluate("()=>document.body.classList.remove('tasogare-barre-etat','tasogare-actions-fichiers','tasogare-icones-proprietes')")
 report['options_facultatives']=True
 for mode in ['dark','light']:
  pg.evaluate("m=>{app.vault.setConfig('theme',m==='light'?'moonstone':'obsidian');app.setTheme()}",mode);pg.wait_for_function("m=>document.body.classList.contains('theme-'+m)",arg=mode)
  pg.locator('.metadata-add-button').evaluate('e=>e.blur()');pg.mouse.move(500,760);pg.screenshot(path=str(root/f'proprietes-{mode}.png'))
 # Le module Bases continue à lire toutes les fiches.
 for view,count in [('Tout · tableau',155),('Œuvres · cartes',35)]:
  pg.evaluate("async v=>{await app.workspace.getMostRecentLeaf().setViewState({type:'bases',state:{file:'Templates/Bases/Bibliothèque.base',viewName:v}});app.workspace.rightSplit.collapse()}",view)
  pg.wait_for_function("n=>[...document.querySelectorAll('.text-button-label')].some(e=>e.textContent.trim()===n+' results')",arg=count,timeout=15000)
  if count==35:
   ratio=pg.locator('.bases-cards-cover').first.evaluate('e=>{const r=e.getBoundingClientRect();return r.height/r.width}')
   assert abs(ratio-2/3)<0.02, 'Le cadre des cartes ne correspond pas aux couvertures paysage du coffre de test.'
   report['ratio_cartes']=ratio
  pg.screenshot(path=str(root/('tableau.png' if count==155 else 'cartes.png')))
 report['bases']={'tableau':155,'oeuvres_cartes':35}
 # État d'ouverture livré : note avec graphe, Graphite sombre.
 pg.evaluate('''async()=>{app.vault.setConfig('theme','obsidian');app.setTheme();await app.workspace.openLinkText('Notes/Exemple — Une bibliothèque lisible','',false);await app.workspace.getMostRecentLeaf().setViewState({type:'markdown',state:{file:'Notes/Exemple — Une bibliothèque lisible.md',mode:'preview'}});app.workspace.rightSplit.expand();app.workspace.getLeavesOfType('localgraph')[0].parent.selectTab(app.workspace.getLeavesOfType('localgraph')[0]);await app.workspace.saveLayout()}''')
assert all(f.read_bytes()==content for f,content in originals.items())
(root/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'palettes_et_modes':len(report['palettes']),'dispositions':len(report['dispositions']),'fiches_preservees':155,'plugins_communautaires':config['plugins'],'bases':report['bases'],'typographie':'identique au Tasogare de départ','resultat':'réussi'},ensure_ascii=False))
