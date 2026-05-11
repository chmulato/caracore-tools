(function () {
  'use strict';

  var docs = [
    {
      title: 'Linhas mestras da Cara Core Informática',
      href: 'linhas_mestras_cara_core.html',
      description: 'Explica a direção da Cara Core e os princípios que orientam o ecossistema.',
      category: 'governanca',
      tag: 'linhas-mestras',
      audience: 'estrategia',
      updatedAt: '2026-05-11'
    },
    {
      title: 'Matriz pública do portfólio Cara Core',
      href: 'matriz_produto_status_expectativa_gate.html',
      description: 'Apresenta cada frente do portfólio com estágio atual e expectativa pública.',
      category: 'governanca',
      tag: 'matriz',
      audience: 'estrategia',
      updatedAt: '2026-05-10'
    },
    {
      title: 'Como a Cara Core organiza o ecossistema',
      href: 'sistema_governanca_ecossistema.html',
      description: 'Mostra como a Cara Core organiza revisão, coerência e publicação no ecossistema.',
      category: 'governanca',
      tag: 'governanca',
      audience: 'operacao',
      updatedAt: '2026-03-12'
    },
    {
      title: 'Visão geral do ecossistema Cara Core',
      href: 'mapeamento_ecossistema_productos.html',
      description: 'Resume os principais produtos, áreas de atuação e papéis do ecossistema.',
      category: 'governanca',
      tag: 'mapa',
      audience: 'estrategia',
      updatedAt: '2026-03-14'
    },
    {
      title: 'Campanha B2B',
      href: 'b2b/index.html',
      description: 'Reúne textos em inglês voltados à apresentação institucional e ao mercado.',
      category: 'campanha',
      tag: 'b2b',
      audience: 'marketing',
      updatedAt: '2026-04-01'
    },
    {
      title: 'Checklist de publicação',
      href: 'publicacao_checklist.html',
      description: 'Traz uma revisão curta para confirmar clareza, links e leitura antes da publicação.',
      category: 'governanca',
      tag: 'checklist',
      audience: 'operacao',
      updatedAt: '2026-04-09'
    },
    {
      title: 'Regras de publicação do portal',
      href: 'politica_publicacao_html_only.html',
      description: 'Resume o que pode entrar na área pública e o que deve ficar fora dela.',
      category: 'governanca',
      tag: 'html-only',
      audience: 'publicacao',
      updatedAt: '2026-04-10'
    },
    {
      title: 'Guia de linguagem e identidade das páginas',
      href: 'guia_publicacao_shell_identidade.html',
      description: 'Mostra o que deve permanecer igual no portal e o que cada página pode adaptar ao seu assunto.',
      category: 'governanca',
      tag: 'publicacao',
      audience: 'publicacao',
      updatedAt: '2026-05-11'
    },
    {
      title: 'Checklist visual do portal',
      href: 'checklist_qa_visual_portal.html',
      description: 'Ajuda a revisar leitura, contraste, hierarquia e conforto de navegação das páginas.',
      category: 'governanca',
      tag: 'qa-visual',
      audience: 'publicacao',
      updatedAt: '2026-05-11'
    }
  ];

  function qs(selector) {
    return document.querySelector(selector);
  }

  function qsa(selector) {
    return Array.prototype.slice.call(document.querySelectorAll(selector));
  }

  function normalize(text) {
    return String(text || '').toLowerCase();
  }

  function categoryPt(value) {
    var labels = {
      governanca: 'Governança',
      seguranca: 'Segurança',
      auditoria: 'Auditoria',
      campanha: 'Campanha'
    };
    return labels[value] || value;
  }

  function categoryLabel(value) {
    var labels = {
      all: 'Todas as categorias',
      governanca: 'Governança',
      seguranca: 'Segurança',
      auditoria: 'Auditoria',
      campanha: 'Campanha e comunicação'
    };
    return labels[value] || value;
  }

  function streamLabel(value) {
    var labels = {
      governanceOps: 'Operação e governança',
      publicationPipeline: 'Publicação e modelos',
      riskAndSecurity: 'Risco e segurança',
      marketEnablement: 'Campanha e mercado'
    };
    return labels[value] || value;
  }

  function audiencePt(value) {
    var labels = {
      operacao: 'Operação',
      publicacao: 'Publicação',
      governanca: 'Governança',
      engenharia: 'Engenharia',
      compliance: 'Compliance',
      juridico: 'Jurídico',
      marketing: 'Marketing',
      estrategia: 'Estratégia',
      suporte: 'Suporte'
    };
    return labels[value] || value;
  }

  function statusLabel(status) {
    var labels = {
      quente: 'Quente',
      morno: 'Morno',
      saudavel: 'Saudável'
    };
    return labels[status] || status;
  }

  function daysSince(dateString) {
    var today = new Date();
    var source = new Date(dateString + 'T00:00:00');
    var diff = today.getTime() - source.getTime();
    return Math.max(0, Math.floor(diff / 86400000));
  }

  function businessStatus(days) {
    if (days >= 28) {
      return 'quente';
    }
    if (days >= 14) {
      return 'morno';
    }
    return 'saudavel';
  }

  function statusClass(status) {
    if (status === 'quente') {
      return 'hot';
    }
    if (status === 'morno') {
      return 'warm';
    }
    return 'ok';
  }

  function criticalityWeight(category) {
    var map = {
      seguranca: 5,
      auditoria: 4,
      governanca: 3,
      campanha: 2
    };
    return map[category] || 2;
  }

  function audienceWeight(audience) {
    var map = {
      operacao: 4,
      publicacao: 3,
      governanca: 4,
      engenharia: 3,
      compliance: 4,
      juridico: 2,
      marketing: 2,
      estrategia: 3,
      suporte: 3
    };
    return map[audience] || 2;
  }

  function streamFromDoc(doc) {
    if (doc.category === 'seguranca' || doc.tag === 'seguranca' || doc.tag === 'gate') {
      return 'riskAndSecurity';
    }
    if (doc.category === 'auditoria') {
      return 'governanceOps';
    }
    if (doc.tag === 'template' || doc.tag === 'instalacao' || doc.tag === 'checklist' || doc.tag === 'padrao') {
      return 'publicationPipeline';
    }
    if (doc.category === 'campanha' || doc.tag === 'b2b' || doc.tag === 'vitrine') {
      return 'marketEnablement';
    }
    return 'governanceOps';
  }

  function businessEnrichedDocs() {
    return docs.map(function (doc) {
      var ageInDays = daysSince(doc.updatedAt);
      var status = businessStatus(ageInDays);
      var stream = streamFromDoc(doc);
      var priorityScore = (criticalityWeight(doc.category) * 10) + (audienceWeight(doc.audience) * 6) + Math.min(30, ageInDays);

      return {
        title: doc.title,
        href: doc.href,
        description: doc.description,
        category: doc.category,
        tag: doc.tag,
        audience: doc.audience,
        updatedAt: doc.updatedAt,
        ageInDays: ageInDays,
        status: status,
        stream: stream,
        priorityScore: priorityScore
      };
    });
  }

  function computeBusinessModel() {
    var enriched = businessEnrichedDocs();
    var streamBuckets = {
      governanceOps: 0,
      publicationPipeline: 0,
      riskAndSecurity: 0,
      marketEnablement: 0
    };
    var stale = 0;
    var hot = 0;

    enriched.forEach(function (doc) {
      streamBuckets[doc.stream] += 1;
      if (doc.ageInDays >= 30) {
        stale += 1;
      }
      if (doc.status === 'quente') {
        hot += 1;
      }
    });

    var priorityQueue = enriched.slice().sort(function (a, b) {
      return b.priorityScore - a.priorityScore;
    });

    return {
      docs: enriched,
      kpis: {
        total: enriched.length,
        stale: stale,
        hot: hot,
        streams: Object.keys(streamBuckets).length
      },
      streams: streamBuckets,
      priorityQueue: priorityQueue
    };
  }

  function cardHtml(doc) {
    return '<a class="card anim-in" href="' + doc.href + '">' +
      '<h3>' + doc.title + '</h3>' +
      '<p>' + doc.description + '</p>' +
      '<small>' + categoryPt(doc.category) + ' · atualizado em ' + doc.updatedAt + '</small>' +
      '</a>';
  }

  function filterDocs(term, category) {
    var safeTerm = normalize(term).trim();
    return docs.filter(function (doc) {
      var categoryMatch = category === 'all' || doc.category === category;
      var searchable = normalize([
        doc.title,
        doc.description,
        doc.tag,
        doc.category,
        doc.audience,
        doc.updatedAt,
        doc.href,
        categoryPt(doc.category),
        audiencePt(doc.audience)
      ].join(' '));
      var termMatch = !safeTerm || searchable.indexOf(safeTerm) !== -1;
      return categoryMatch && termMatch;
    });
  }

  function updateChips(category) {
    qsa('.chip').forEach(function (chip) {
      var chipCategory = chip.getAttribute('data-category');
      chip.classList.toggle('active', chipCategory === category);
    });
  }

  function initPortalHome() {
    var statDocs = qs('#statDocs');
    var statCategories = qs('#statCategories');
    var statUpdated = qs('#statUpdated');
    var businessKpis = qs('#businessKpis');
    var businessHotlist = qs('#businessHotlist');
    var businessStreams = qs('#businessStreams');

    if (!statDocs && !statUpdated && !statCategories && !businessKpis && !businessHotlist && !businessStreams) {
      return;
    }

    var needBusiness = !!(businessKpis || businessHotlist || businessStreams);
    var businessModel = needBusiness ? computeBusinessModel() : null;

    if (statDocs) {
      statDocs.textContent = String(docs.length);
    }

    if (statCategories) {
      var count = {};
      docs.forEach(function (doc) {
        count[doc.category] = true;
      });
      statCategories.textContent = String(Object.keys(count).length);
    }

    if (statUpdated) {
      var sorted = docs.slice().sort(function (a, b) {
        return a.updatedAt < b.updatedAt ? 1 : -1;
      });
      statUpdated.textContent = sorted[0] ? sorted[0].updatedAt : '—';
    }

    if (businessModel && businessKpis) {
      businessKpis.innerHTML = '' +
        '<div class="business-kpi"><strong>' + businessModel.kpis.hot + '</strong><span>Documentos prioritários</span></div>' +
        '<div class="business-kpi"><strong>' + businessModel.kpis.stale + '</strong><span>Sem atualização há 30+ dias</span></div>' +
        '<div class="business-kpi"><strong>' + businessModel.kpis.streams + '</strong><span>Fluxos de trabalho</span></div>' +
        '<div class="business-kpi"><strong>' + businessModel.priorityQueue[0].title + '</strong><span>Maior prioridade hoje</span></div>';
    }

    if (businessModel && businessHotlist) {
      businessHotlist.innerHTML = businessModel.priorityQueue.slice(0, 5).map(function (doc) {
        return '<li class="business-item">' +
          '<a href="' + doc.href + '">' + doc.title + '</a>' +
          '<div class="business-meta"><span class="pill ' + statusClass(doc.status) + '">' + statusLabel(doc.status) + '</span>' +
          ' · ' + streamLabel(doc.stream) + ' · ' + doc.ageInDays + ' dias</div>' +
          '</li>';
      }).join('');
    }

    if (businessModel && businessStreams) {
      businessStreams.innerHTML = Object.keys(businessModel.streams).map(function (stream) {
        return '<article class="stream-card">' +
          '<h3>' + streamLabel(stream) + '</h3>' +
          '<p>' + businessModel.streams[stream] + ' documento(s) neste grupo.</p>' +
          '</article>';
      }).join('');
    }
  }

  function catalogCardHtml(doc) {
    return '<article class="catalog-card anim-in" data-category="' + doc.category + '">' +
      '<h3><a href="' + doc.href + '">' + doc.title + '</a></h3>' +
      '<div class="meta-line">' + categoryPt(doc.category) + ' · atualizado em ' + doc.updatedAt + '</div>' +
      '<p>' + doc.description + '</p>' +
      '</article>';
  }

  function initCatalogPage() {
    var catalogRoot = qs('#catalogGrid');
    if (!catalogRoot) {
      return;
    }

    var searchInput = qs('#catalogSearch');
    var categorySelect = qs('#catalogCategory');
    var countNode = qs('#catalogCount');
    var emptyNode = qs('#catalogEmpty');

    function render() {
      var category = categorySelect.value;
      var term = searchInput.value;
      var filtered = filterDocs(term, category).sort(function (a, b) {
        return a.title.localeCompare(b.title);
      });

      catalogRoot.innerHTML = filtered.map(catalogCardHtml).join('');

      if (countNode) {
        countNode.textContent = 'Mostrando ' + filtered.length + ' de ' + docs.length + ' documento(s).';
      }

      if (emptyNode) {
        emptyNode.textContent = 'Nenhum documento corresponde à busca ou ao filtro.';
        emptyNode.style.display = filtered.length === 0 ? 'block' : 'none';
      }
    }

    searchInput.addEventListener('input', render);
    categorySelect.addEventListener('change', render);

    render();
  }

  function businessRowHtml(doc) {
    return '<tr>' +
      '<td><a href="' + doc.href + '">' + doc.title + '</a></td>' +
      '<td>' + streamLabel(doc.stream) + '</td>' +
      '<td>' + categoryPt(doc.category) + '</td>' +
      '<td>' + audiencePt(doc.audience) + '</td>' +
      '<td><span class="pill ' + statusClass(doc.status) + '">' + statusLabel(doc.status) + '</span></td>' +
      '<td>' + doc.ageInDays + ' d</td>' +
      '<td>' + doc.priorityScore + '</td>' +
      '</tr>';
  }

  function initBusinessPage() {
    var tableBody = qs('#businessTableBody');
    if (!tableBody) {
      return;
    }

    var streamFilter = qs('#bizStreamFilter');
    var statusFilter = qs('#bizStatusFilter');
    var searchInput = qs('#bizSearch');
    var countLine = qs('#bizCount');
    var kpisRoot = qs('#bizKpis');
    var model = computeBusinessModel();

    if (kpisRoot) {
      kpisRoot.innerHTML = '' +
        '<div class="business-kpi"><strong>' + model.kpis.total + '</strong><span>Documentos no painel</span></div>' +
        '<div class="business-kpi"><strong>' + model.kpis.hot + '</strong><span>Prioritários (recência)</span></div>' +
        '<div class="business-kpi"><strong>' + model.kpis.stale + '</strong><span>+30 dias sem revisão</span></div>' +
        '<div class="business-kpi"><strong>' + model.priorityQueue[0].priorityScore + '</strong><span>Maior pontuação</span></div>';
    }

    function render() {
      var selectedStream = streamFilter.value;
      var selectedStatus = statusFilter.value;
      var term = normalize(searchInput.value).trim();

      var filtered = model.priorityQueue.filter(function (doc) {
        var streamMatch = selectedStream === 'all' || doc.stream === selectedStream;
        var statusMatch = selectedStatus === 'all' || doc.status === selectedStatus;
        var text = normalize(doc.title + ' ' + doc.description + ' ' + doc.tag + ' ' + doc.category + ' ' + doc.audience +
          ' ' + categoryPt(doc.category) + ' ' + audiencePt(doc.audience) + ' ' + streamLabel(doc.stream));
        var termMatch = !term || text.indexOf(term) !== -1;
        return streamMatch && statusMatch && termMatch;
      });

      tableBody.innerHTML = filtered.map(businessRowHtml).join('');
      countLine.textContent = 'Exibindo ' + filtered.length + ' de ' + model.priorityQueue.length + ' documento(s).';
    }

    streamFilter.addEventListener('change', render);
    statusFilter.addEventListener('change', render);
    searchInput.addEventListener('input', render);

    render();
  }

  window.CaraCoreDocs = {
    docs: docs,
    computeBusinessModel: computeBusinessModel
  };

  initPortalHome();
  initCatalogPage();
  initBusinessPage();
})();
