const { Component, MarkdownView, Notice, Plugin, setIcon, TFile, WorkspaceLeaf } = require('obsidian');

class NoteSheet extends Component {
  constructor(app, leaf, trigger, close, size) {
    super();
    this.app = app;
    this.leaf = leaf;
    this.host = leaf.view.containerEl;
    this.source = leaf.getViewState().state?.file;
    this.trigger = trigger;
    this.close = close;
    this.size = size;
  }

  onload() {
    this.sheet = this.host.createEl('aside', { cls: 'bases-reading-pane' });
    const grip = this.host.createDiv({
      cls: 'bases-reading-pane-resize',
      attr: { role: 'separator', tabindex: '0', 'aria-label': 'Largeur du panneau',
        'aria-orientation': 'vertical', 'aria-valuemin': '30', 'aria-valuemax': '65' },
    });
    this.host.classList.add('bases-reading-pane-host');
    this.register(() => {
      const active = this.sheet.ownerDocument.activeElement;
      const hadFocus = this.sheet.contains(active) || grip === active;
      grip.remove();
      this.sheet.remove();
      this.host.classList.remove('bases-reading-pane-host');
      this.host.style.removeProperty('--bases-reading-pane-width');
      if (hadFocus && this.trigger?.isConnected) this.trigger.focus({ preventScroll: true });
    });
    this.registerResize(grip);

    this.closeButton = this.sheet.createEl('button', {
      cls: 'clickable-icon bases-reading-pane-close',
      attr: { type: 'button', 'aria-label': 'Fermer le panneau' },
    });
    setIcon(this.closeButton, 'x');
    this.registerDomEvent(this.closeButton, 'click', () => this.close());
    this.registerDomEvent(this.sheet, 'keydown', event => {
      if (event.key === 'Escape' && !event.defaultPrevented) {
        event.preventDefault();
        event.stopPropagation();
        this.close();
      }
    });

    // A standalone workspace leaf hosts the native editor outside the tab tree.
    // Obsidian exports WorkspaceLeaf, but its constructor is not a public API.
    this.editorLeaf = new WorkspaceLeaf(this.app);
    this.sheet.appendChild(this.editorLeaf.containerEl);
    this.closeButton.focus({ preventScroll: true });
  }

  async open(file) {
    await this.editorLeaf.openFile(file, { active: false, state: { mode: 'source', source: false } });
    const { view } = this.editorLeaf;
    if (!(view instanceof MarkdownView) || view.file !== file) throw new Error('Native editor unavailable');
    this.sheet.setAttribute('aria-label', file.basename);
  }

  async disposeEditor() {
    if (!this.editorLeaf) return;
    if (this.editorLeaf.containerEl.contains(this.sheet.ownerDocument.activeElement)) {
      this.closeButton.focus({ preventScroll: true });
    }
    try {
      // Await native close so it flushes pending edits before releasing the leaf.
      await this.editorLeaf.open(null);
    } finally {
      this.editorLeaf.detach();
    }
  }

  registerResize(grip) {
    let drag;
    const resize = next => {
      const width = Math.min(65, Math.max(30, Math.round(next)));
      this.size.width = width;
      this.host.style.setProperty('--bases-reading-pane-width', `${width}%`);
      grip.setAttribute('aria-valuenow', String(width));
      grip.setAttribute('aria-valuetext', `${width} %`);
    };
    const direction = () => getComputedStyle(this.host).direction === 'rtl' ? -1 : 1;
    resize(this.size.width);
    this.registerDomEvent(grip, 'pointerdown', event => {
      if (event.button !== 0 || drag) return;
      const span = this.host.getBoundingClientRect().width;
      if (!span) return;
      drag = { id: event.pointerId, x: event.clientX, width: this.size.width, span };
      grip.setPointerCapture(event.pointerId);
      grip.focus({ preventScroll: true });
    });
    this.registerDomEvent(grip, 'pointermove', event => {
      if (drag?.id !== event.pointerId) return;
      resize(drag.width + direction() * 100 * (drag.x - event.clientX) / drag.span);
    });
    this.registerDomEvent(grip, 'lostpointercapture', () => { drag = undefined; });
    this.registerDomEvent(grip, 'keydown', event => {
      const { width } = this.size;
      const positions = { ArrowLeft: width + 3 * direction(), ArrowRight: width - 3 * direction(), Home: 30, End: 65 };
      if (event.key === 'Escape') {
        event.preventDefault();
        this.close();
      } else if (Object.hasOwn(positions, event.key)) {
        event.preventDefault();
        resize(positions[event.key]);
      }
    });
  }

  isMounted() {
    return this.host.isConnected && this.leaf.view.containerEl === this.host
      && this.leaf.getViewState().state?.file === this.source;
  }
}

module.exports = class BasesReadingPane extends Plugin {
  onload() {
    this.panelSize = { width: 42 };
    this.pending = Promise.resolve();
    this.registerDomEvent(document, 'click', event => {
      if (event.button === 0) this.handleActivation(event);
    }, { capture: true });
    this.registerDomEvent(document, 'keydown', event => {
      if (event.key === 'Enter' && !event.repeat) this.handleActivation(event);
    }, { capture: true });
    this.registerEvent(this.app.workspace.on('file-menu', (menu, file) => {
      if (file instanceof TFile && file.extension === 'md') {
        menu.addItem(item => item.setTitle('Ouvrir dans le tiroir').setIcon('panel-right').onClick(() => {
          const workspace = this.app.workspace;
          const leaf = workspace.getMostRecentLeaf(workspace.rootSplit);
          if (leaf?.view.containerEl.querySelector(':scope > .view-content')) {
            this.openSheet(file, leaf, document.activeElement);
          }
        }));
      }
    }));
    const detachSheet = () => {
      if (this.sheet && !this.sheet.isMounted()) this.closeSheet(this.sheet);
    };
    this.registerEvent(this.app.workspace.on('layout-change', detachSheet));
    this.registerEvent(this.app.workspace.on('file-open', detachSheet));
  }

  onunload() {
    this.unloaded = true;
    if (this.sheet) this.closeSheet(this.sheet);
  }

  handleActivation(event) {
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    const target = event.target;
    if (!(target instanceof Element) || !target.closest('.mod-root .bases-view')
      || target.closest('.bases-reading-pane')) return;
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
    if (!leaf?.view.containerEl.querySelector(':scope > .view-content')) return;
    const source = leaf.getViewState().state?.file ?? '';
    const file = this.app.metadataCache.getFirstLinkpathDest(reference, source);
    if (!(file instanceof TFile) || file.extension !== 'md') return;

    event.preventDefault();
    event.stopPropagation();
    this.openSheet(file, leaf, target.closest('[tabindex="0"]') ?? document.activeElement);
  }

  enqueue(action) {
    this.pending = this.pending.then(action).catch(error => {
      console.warn('Yoi : erreur du tiroir.', error);
      new Notice('Impossible d’utiliser l’éditeur du tiroir.');
    });
  }

  async removeSheet(sheet) {
    if (this.sheet !== sheet) return;
    this.sheet = undefined;
    try {
      await sheet.disposeEditor();
    } finally {
      this.removeChild(sheet);
    }
  }

  closeSheet(sheet) {
    this.enqueue(() => this.removeSheet(sheet));
  }

  openSheet(file, leaf, trigger) {
    const sheet = new NoteSheet(this.app, leaf, trigger, () => this.closeSheet(sheet), this.panelSize);
    this.enqueue(async () => {
      if (this.unloaded || !sheet.isMounted()) return;
      if (this.sheet) await this.removeSheet(this.sheet);
      if (this.unloaded || !sheet.isMounted()) return;
      this.sheet = sheet;
      try {
        this.addChild(sheet);
        await sheet.open(file);
      } catch (error) {
        await this.removeSheet(sheet);
        throw error;
      }
    });
  }
};
