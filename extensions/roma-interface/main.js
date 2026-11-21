const {
  Component, getFrontMatterInfo, MarkdownRenderer,
  Notice, Plugin, PluginSettingTab, setIcon, TFile,
} = require('obsidian');

const visibilityOptions = [
  { value: 'etat', label: 'Barre d’état complète', legacy: 'tasogare-barre-etat' },
  { value: 'fichiers', label: 'Commandes des fichiers', legacy: 'tasogare-actions-fichiers' },
  { value: 'proprietes', label: 'Icônes des propriétés', legacy: 'tasogare-icones-proprietes' },
];

class NoteSheet extends Component {
  constructor(app, file, leaf, trigger, close) {
    super();
    this.app = app;
    this.file = file;
    this.leaf = leaf;
    this.host = leaf.view.containerEl;
    this.source = leaf.getViewState().state?.file;
    this.trigger = trigger;
    this.close = close;
  }

  async onload() {
    const sheet = this.host.createEl('aside', { cls: 'roma-note-sheet', attr: { 'aria-label': this.file.basename } });
    const header = sheet.createEl('header', { cls: 'roma-note-sheet-header' });
    header.createEl('h2', { cls: 'roma-note-sheet-title', text: this.file.basename });
    const closeButton = header.createEl('button', {
      cls: 'clickable-icon', attr: { type: 'button', 'aria-label': 'Fermer le tiroir' },
    });
    setIcon(closeButton, 'x');
    this.registerDomEvent(closeButton, 'click', () => this.close());
    this.registerDomEvent(sheet, 'keydown', event => {
      if (event.key === 'Escape' && !event.defaultPrevented) {
        event.preventDefault();
        event.stopPropagation();
        this.close();
      }
    });
    this.register(() => {
      const hadFocus = sheet.contains(sheet.ownerDocument.activeElement);
      sheet.remove();
      if (hadFocus && this.trigger?.isConnected) this.trigger.focus({ preventScroll: true });
    });
    closeButton.focus({ preventScroll: true });

    const toolbar = sheet.createDiv({ cls: 'roma-note-sheet-toolbar' });
    const properties = this.app.metadataCache.getFileCache(this.file)?.frontmatter;
    for (const key of ['statut', 'priorité']) {
      if (typeof properties?.[key] === 'string' && properties[key]) {
        const badge = toolbar.createSpan({ text: properties[key], cls: 'roma-note-sheet-badge' });
        badge.setAttribute('aria-label', `${key} ${properties[key]}`);
      }
    }
    const editButton = toolbar.createEl('button', { text: 'Ouvrir dans l’éditeur' });
    this.registerDomEvent(editButton, 'click', async () => {
      this.close();
      try {
        await this.leaf.openFile(this.file, { active: true, state: { mode: 'source' } });
      } catch {
        new Notice('Impossible d’ouvrir la fiche.');
      }
    });

    const content = sheet.createDiv({ cls: 'markdown-rendered roma-note-sheet-content' });
    try {
      const markdown = await this.app.vault.cachedRead(this.file);
      if (!sheet.isConnected) return;
      const { contentStart } = getFrontMatterInfo(markdown);
      const body = markdown.slice(contentStart);
      if (body.trim()) {
        await MarkdownRenderer.render(this.app, body, content, this.file.path, this);
      } else {
        content.createEl('p', { text: 'Cette fiche contient uniquement des propriétés.' });
      }
    } catch {
      if (sheet.isConnected) content.setText('Impossible de lire cette fiche.');
    }
  }

  isMounted() {
    return this.host.isConnected && this.leaf.view.containerEl === this.host
      && this.leaf.getViewState().state?.file === this.source;
  }
}

class InterfaceSettings extends PluginSettingTab {
  constructor(plugin) {
    super(plugin.app, plugin);
    this.plugin = plugin;
  }

  display() {
    this.containerEl.empty();
    const field = this.containerEl.createEl('details', { cls: 'roma-visibility-field' });
    const summary = field.createEl('summary');
    const selected = new Set(this.plugin.currentVisibility());
    const reset = this.containerEl.createEl('button', { text: 'Revenir aux réglages du thème' });
    reset.addEventListener('click', () => {
      this.plugin.setVisibility(null);
      this.display();
    });
    const updateSummary = () => {
      const labels = visibilityOptions.filter(option => selected.has(option.value)).map(option => option.label);
      summary.setText(`Éléments visibles · ${labels.join(', ') || 'Aucun élément supplémentaire'}`);
      reset.hidden = this.plugin.visibility === null;
    };
    for (const option of visibilityOptions) {
      const row = field.createEl('label');
      const checkbox = row.createEl('input', { type: 'checkbox' });
      checkbox.checked = selected.has(option.value);
      row.createSpan({ text: option.label });
      checkbox.addEventListener('change', () => {
        if (checkbox.checked) selected.add(option.value);
        else selected.delete(option.value);
        this.plugin.setVisibility([...selected]);
        updateSummary();
      });
    }
    updateSummary();
  }
}

module.exports = class RomaInterface extends Plugin {
  async onload() {
    const stored = (await this.loadData())?.visibility;
    this.visibility = Array.isArray(stored)
      ? visibilityOptions.filter(option => stored.includes(option.value)).map(option => option.value)
      : null;
    this.applyVisibility();
    this.addSettingTab(new InterfaceSettings(this));
    this.registerDomEvent(document, 'click', event => {
      if (event.button === 0) this.handleActivation(event);
    }, { capture: true });
    this.registerDomEvent(document, 'keydown', event => {
      if (event.key === 'Enter' && !event.repeat) this.handleActivation(event);
    }, { capture: true });
    this.registerEvent(this.app.workspace.on('file-menu', (menu, file) => {
      if (file instanceof TFile && file.extension === 'md') {
        menu.addItem(item => item.setTitle('Aperçu à droite').setIcon('panel-right').onClick(() => {
          const workspace = this.app.workspace;
          const leaf = workspace.getMostRecentLeaf(workspace.rootSplit);
          if (leaf) this.openSheet(file, leaf, document.activeElement);
        }));
      }
    }));
    const detachSheet = () => {
      if (this.sheet && !this.sheet.isMounted()) this.closeSheet();
    };
    this.registerEvent(this.app.workspace.on('layout-change', detachSheet));
    this.registerEvent(this.app.workspace.on('file-open', detachSheet));
  }

  onunload() {
    this.closeSheet();
    document.body.removeAttribute('data-roma-visibilite');
  }

  applyVisibility() {
    if (this.visibility === null) document.body.removeAttribute('data-roma-visibilite');
    else document.body.setAttribute('data-roma-visibilite', this.visibility.join(' '));
  }

  currentVisibility() {
    return this.visibility ?? visibilityOptions.filter(option => document.body.classList.contains(option.legacy)).map(option => option.value);
  }

  setVisibility(values) {
    this.visibility = values;
    this.applyVisibility();
    // Preserve the order of writes when several options are selected quickly.
    this.pendingSave = (this.pendingSave ?? Promise.resolve())
      .then(() => this.saveData({ visibility: values }))
      .catch(() => new Notice('Impossible d’enregistrer les options d’Interface romā.'));
  }

  handleActivation(event) {
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    const target = event.target;
    if (!(target instanceof Element) || !target.closest('.mod-root .bases-view')) return;
    if (target.isContentEditable || target.closest('button, input, select, textarea, .external-link')) return;

    const card = target.closest('.bases-kanban-card, .bases-cards-item');
    const link = target.closest('.internal-link[data-href]')
      ?? card?.querySelector('.mod-title .internal-link[data-href]');
    if (!link) return;
    const reference = link.getAttribute('data-href');
    if (!reference || reference.includes('#')) return;
    let leaf;
    this.app.workspace.iterateRootLeaves(candidate => {
      if (candidate.view.containerEl.contains(target)) leaf = candidate;
    });
    if (!leaf) return;
    const source = leaf.getViewState().state?.file ?? '';
    const file = this.app.metadataCache.getFirstLinkpathDest(reference, source);
    if (!(file instanceof TFile) || file.extension !== 'md') return;

    event.preventDefault();
    event.stopPropagation();
    this.openSheet(file, leaf, target.closest('[tabindex="0"]') ?? document.activeElement);
  }

  closeSheet() {
    if (!this.sheet) return;
    const sheet = this.sheet;
    this.sheet = null;
    this.removeChild(sheet);
  }

  openSheet(file, leaf, trigger) {
    this.closeSheet();
    this.sheet = this.addChild(new NoteSheet(this.app, file, leaf, trigger, () => this.closeSheet()));
  }
};
