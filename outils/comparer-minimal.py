"""Compare les interactions natives de Bases entre Minimal et Tasogare sur les mêmes données temporaires."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import argparse,json,shutil
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cdp',required=True);p.add_argument('--coffre',required=True,type=Path);p.add_argument('--minimal',required=True,type=Path);p.add_argument('--sortie',required=True,type=Path);a=p.parse_args();a.sortie.mkdir(parents=True,exist_ok=True)
folder='Notes/Contrôle Minimal';base=folder+'/Comparaison.base'
base_text='''filters:
  and:
    - file.inFolder("Notes/Contrôle Minimal")
    - file.ext == "md"
properties:
  file.name:
    displayName: Fiche
  note.prix:
    displayName: Prix
  note.achete:
    displayName: Acheté
views:
  - type: table
    name: Tableau
    order: [file.name, prix, achete]
    sort:
      - property: file.name
        direction: ASC
  - type: cards
    name: Cartes
    order: [file.name, prix, achete]
  - type: table
    name: Filtrés
    order: [file.name, prix, achete]
    filters: note.achete == true
'''
refs={f:f.read_bytes() for f in (a.coffre/'References').glob('*.md')}
minimal_target=a.coffre/'.obsidian/themes/Minimal';existed=minimal_target.exists()
if not existed:shutil.copytree(a.minimal,minimal_target)
report={'minimal':json.loads((a.minimal/'manifest.json').read_text())['version'],'resultats':{}}
with sync_playwright() as p:
 b=p.chromium.connect_over_cdp(a.cdp);pg=next(pg for c in b.contexts for pg in c.pages if 'obsidian.md' in pg.url);pg.set_default_timeout(6000);pg.set_viewport_size({'width':1136,'height':812})
 assert pg.evaluate('()=>app.vault.adapter.basePath')==str(a.coffre.resolve())
 assert pg.evaluate('()=>Object.keys(app.plugins.plugins)')==[]
 assert not pg.evaluate('f=>!!app.vault.getAbstractFileByPath(f)',folder),'Le dossier de test existe déjà.'
 report['user_agent']=pg.evaluate('()=>navigator.userAgent');report['plugins_communautaires']=[]
 layout=pg.evaluate('()=>app.workspace.getLayout()');old_theme=pg.evaluate("()=>app.vault.getConfig('cssTheme')")
 def count(n):pg.wait_for_function("n=>[...document.querySelectorAll('.text-button-label')].some(e=>e.textContent.trim()===n+' result'+(n===1?'':'s'))",arg=n)
 def rows():return pg.locator('.bases-tr .internal-link').all_text_contents()
 def switch(old,new):
  pg.locator('.mod-root').get_by_text(old,exact=True).click();pg.get_by_text(new,exact=True).click();pg.wait_for_function('n=>app.workspace.getMostRecentLeaf().getViewState().state.viewName===n',arg=new)
 try:
  pg.evaluate('async()=>app.customCss.readThemes()');pg.wait_for_timeout(250)
  for theme in ['Minimal','Tasogare']:
   pg.evaluate('''async arg=>{if(!app.vault.getAbstractFileByPath(arg.folder))await app.vault.createFolder(arg.folder);for(const [name,price,bought] of [['Alpha',10,false],['Bêta',20,true],['Gamma',30,false]]){const path=arg.folder+'/'+name+'.md',text='---'+String.fromCharCode(10)+'prix: '+price+String.fromCharCode(10)+'achete: '+bought+String.fromCharCode(10)+'---'+String.fromCharCode(10);const f=app.vault.getAbstractFileByPath(path);if(f)await app.vault.modify(f,text);else await app.vault.create(path,text)}const existing=app.vault.getAbstractFileByPath(arg.base);if(existing)await app.vault.modify(existing,arg.content);else await app.vault.create(arg.base,arg.content);app.customCss.setTheme(arg.theme);await app.workspace.getMostRecentLeaf().setViewState({type:'bases',state:{file:arg.base,viewName:'Tableau'}});app.workspace.rightSplit.collapse()}''',{'folder':folder,'base':base,'content':base_text,'theme':theme})
   pg.wait_for_timeout(400);count(3);r={'initial':rows()};assert r['initial']==['Alpha','Bêta','Gamma'],r
   pg.locator('.mod-root').get_by_text('Sort',exact=True).click();pg.locator('.bases-sort-direction').click();pg.get_by_text('Z → A',exact=True).click();pg.keyboard.press('Escape')
   pg.wait_for_function("()=>document.querySelector('.bases-tr .internal-link')?.textContent==='Gamma'")
   r['tri']=rows();assert r['tri']==['Gamma','Bêta','Alpha']
   pg.locator('.mod-root').get_by_text('Search',exact=True).click();search=pg.get_by_placeholder('Find...',exact=True);search.fill('Alpha');pg.wait_for_timeout(200)
   r['recherche']={'saisie':search.input_value(),'lignes':rows()};search.fill('');pg.keyboard.press('Escape')
   switch('Tableau','Cartes');count(3);r['cartes']=3
   switch('Cartes','Filtrés');count(1);r['filtre']=rows();assert r['filtre']==['Bêta']
   pg.locator('.mod-root').get_by_text('Filter',exact=True).click();r['editeur_filtre']=pg.locator('.bases-toolbar-menu').inner_text();pg.keyboard.press('Escape')
   switch('Filtrés','Tableau');count(3)
   row=pg.locator('.bases-tr').filter(has=pg.locator('.internal-link[data-href="'+folder+'/Alpha.md"]'))
   row.locator('input[type=number]').fill('42');row.locator('input[type=number]').press('Tab');row.locator('input[type=checkbox]').check()
   pg.wait_for_function("f=>{const m=app.metadataCache.getFileCache(app.vault.getAbstractFileByPath(f))?.frontmatter;return m?.prix===42&&m?.achete===true}",arg=folder+'/Alpha.md');r['edition']={'prix':42,'achete':True}
   switch('Tableau','Cartes');count(3);pg.locator('.bases-cards-item').filter(has_text='Alpha').first.click()
   pg.wait_for_function('f=>app.workspace.getMostRecentLeaf().getViewState().state.file===f',arg=folder+'/Alpha.md');r['ouverture_fiche']=True
   r['collections_originales']={}
   for name,n in [('Tout · tableau',155),('Œuvres · cartes',35)]:
    pg.evaluate("async name=>app.workspace.getMostRecentLeaf().setViewState({type:'bases',state:{file:'Templates/Bases/Bibliothèque.base',viewName:name}})",name);count(n);r['collections_originales'][name]=n
   pg.evaluate("async f=>app.workspace.getMostRecentLeaf().setViewState({type:'markdown',state:{file:f,mode:'preview'}})",folder+'/Alpha.md')
   pg.evaluate("async()=>{const l=app.workspace.getLeaf('tab');await l.setViewState({type:'markdown',state:{file:'Notes/Exemple — Une bibliothèque lisible.md',mode:'preview'}});app.workspace.setActiveLeaf(l);app.commands.executeCommandById('workspace:toggle-stacked-tabs');app.workspace.rightSplit.expand()}");pg.wait_for_timeout(400)
   stacked=pg.evaluate('''()=>{const t=document.querySelector('.mod-root .workspace-tabs');return {actif:t.classList.contains('mod-stacked'),headers:[...t.querySelectorAll('.workspace-tab-header')].map(e=>e.getBoundingClientRect().height)}}''')
   assert stacked['actif'] and all(h>500 for h in stacked['headers']),stacked
   r['onglets_empiles']=True
   pg.mouse.move(40,700);pg.screenshot(path=str(a.sortie/f'empiles-{theme}.png'))
   report['resultats'][theme]=r;print(json.dumps({'theme':theme,'resultat':r},ensure_ascii=False),flush=True)
   pg.evaluate('async l=>app.workspace.changeLayout(l)',layout)
  assert report['resultats']['Minimal']==report['resultats']['Tasogare'],report
 finally:
  pg.keyboard.press('Escape');pg.evaluate('async l=>app.workspace.changeLayout(l)',layout)
  pg.evaluate('''async arg=>{app.customCss.setTheme(arg.theme);const f=app.vault.getAbstractFileByPath(arg.folder);if(f)await app.vault.adapter.rmdir(arg.folder,true);await app.workspace.saveLayout()}''',{'theme':old_theme,'folder':folder})
  if not existed:shutil.rmtree(minimal_target)
assert all(f.read_bytes()==old for f,old in refs.items())
report['fiches_preservees']=len(refs);(a.sortie/'parite-minimal.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Parité vérifiée sur les interactions testées ; aucun plugin communautaire.',flush=True)
