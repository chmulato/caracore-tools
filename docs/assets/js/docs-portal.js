(function () {
  'use strict';

  var docs = [
    {
      title: 'Sistema de Governanca do Ecossistema',
      href: 'SISTEMA_GOVERNANCA_ECOSSISTEMA.html',
      description: 'Diretrizes formais, papeis e modelo operacional do ecossistema Cara Core.',
      category: 'governanca',
      tag: 'governanca',
      audience: 'operacao',
      updatedAt: '2026-03-12'
    },
    {
      title: 'Mapeamento do Ecossistema',
      href: 'MAPEAMENTO_ECOSSISTEMA_PRODUCTOS.html',
      description: 'Inventario de produtos, dependencias e relacionamento entre frentes.',
      category: 'governanca',
      tag: 'mapa',
      audience: 'estrategia',
      updatedAt: '2026-03-14'
    },
    {
      title: 'Padrao de Lojas do Ecossistema',
      href: 'PADRAO_LOJAS_ECOSSISTEMA.html',
      description: 'Padroes de estrutura e experiencia para lojas e repositorios de releases.',
      category: 'governanca',
      tag: 'padrao',
      audience: 'publicacao',
      updatedAt: '2026-03-20'
    },
    {
      title: 'Plano de Vitrine Padrao 2026',
      href: 'PLANO_VITRINE_PADRAO_2026.html',
      description: 'Plano de apresentacao online para produtos com foco comercial.',
      category: 'campanha',
      tag: 'vitrine',
      audience: 'marketing',
      updatedAt: '2026-03-22'
    },
    {
      title: 'Template Vitrine Padrao',
      href: 'TEMPLATE_VITRINE_PADRAO.html',
      description: 'Modelo base para pagina de vitrine de produto no ecossistema.',
      category: 'campanha',
      tag: 'template',
      audience: 'marketing',
      updatedAt: '2026-03-22'
    },
    {
      title: 'Template Download Padrao',
      href: 'TEMPLATE_DOWNLOAD_PADRAO.html',
      description: 'Modelo padrao para pagina de download e distribuicao de artefatos.',
      category: 'campanha',
      tag: 'template',
      audience: 'publicacao',
      updatedAt: '2026-03-22'
    },
    {
      title: 'Template Instalacao (HTML)',
      href: 'TEMPLATE_INSTALACAO.html',
      description: 'Guia em HTML para instrucoes de instalacao em Windows e validacao de checksum.',
      category: 'campanha',
      tag: 'instalacao',
      audience: 'suporte',
      updatedAt: '2026-04-09'
    },
    {
      title: 'Relatorio de Seguranca do Ecossistema',
      href: 'RELATORIO_SEGURANCA_ECOSSISTEMA.html',
      description: 'Controles implementados, riscos identificados e recomendacoes tecnicas.',
      category: 'seguranca',
      tag: 'seguranca',
      audience: 'governanca',
      updatedAt: '2026-03-15'
    },
    {
      title: 'Auditoria de Seguranca das Lojas Releases',
      href: 'AUDITORIA_SEGURANCA_LOJAS_RELEASES.html',
      description: 'Verificacao da postura de seguranca nas lojas de release.',
      category: 'auditoria',
      tag: 'seguranca',
      audience: 'compliance',
      updatedAt: '2026-03-14'
    },
    {
      title: 'Auditoria de Licencas Repositorios',
      href: 'AUDITORIA_LICENCAS_REPOSITORIOS_2026_03_14.html',
      description: 'Relatorio de conformidade e rastreabilidade de licencas.',
      category: 'auditoria',
      tag: 'compliance',
      audience: 'juridico',
      updatedAt: '2026-03-14'
    },
    {
      title: 'Code Health Report Final',
      href: 'CODE_HEALTH_REPORT_FINAL.html',
      description: 'Consolidado final do estado tecnico de saude de codigo.',
      category: 'auditoria',
      tag: 'code-health',
      audience: 'engenharia',
      updatedAt: '2026-03-19'
    },
    {
      title: 'GATE Publicacao Antiabutre',
      href: 'GATE_PUBLICACAO_ANTIABUTRE_ECOSSISTEMA.html',
      description: 'Gate de publicacao e controles de protecao operacional.',
      category: 'seguranca',
      tag: 'gate',
      audience: 'publicacao',
      updatedAt: '2026-03-16'
    },
    {
      title: 'Analise de Honestidade Cronologica',
      href: 'ANALISE_HONESTIDADE_CRONOLOGICA_PRODUTOS.html',
      description: 'Analise de coerencia temporal em entregas e trilha de evidencias.',
      category: 'auditoria',
      tag: 'analise',
      audience: 'governanca',
      updatedAt: '2026-03-17'
    },
    {
      title: 'Governance Reports',
      href: 'governance-reports/index.html',
      description: 'Colecao cronologica de relatorios de gate e evidencias operacionais.',
      category: 'governanca',
      tag: 'relatorios',
      audience: 'operacao',
      updatedAt: '2026-04-04'
    },
    {
      title: 'Campanha B2B Export',
      href: 'b2b/index.html',
      description: 'Hub editorial com 12 artigos em ingles, filtragem por assunto e assets.',
      category: 'campanha',
      tag: 'b2b',
      audience: 'marketing',
      updatedAt: '2026-04-01'
    },
    {
      title: 'Checklist de Publicacao Web',
      href: 'PUBLICACAO_CHECKLIST.html',
      description: 'Checklist operacional para validar navegacao, links e consistencia antes de publicar online.',
      category: 'governanca',
      tag: 'checklist',
      audience: 'operacao',
      updatedAt: '2026-04-09'
    },
    {
      title: 'Politica de Publicacao HTML-Only',
      href: 'POLITICA_PUBLICACAO_HTML_ONLY.html',
      description: 'Regra institucional para manter o docs com documentos publicados em HTML e sem artefatos crus na superficie web.',
      category: 'governanca',
      tag: 'html-only',
      audience: 'publicacao',
      updatedAt: '2026-04-10'
    },
    {
      title: 'Guia de Publicacao: Shell x Identidade',
      href: 'GUIA_PUBLICACAO_SHELL_IDENTIDADE.html',
      description: 'Guia curto para separar componentes compartilhados do portal e identidade propria por assunto.',
      category: 'governanca',
      tag: 'publicacao',
      audience: 'publicacao',
      updatedAt: '2026-04-10'
    },
    {
      title: 'Checklist QA Visual do Portal',
      href: 'CHECKLIST_QA_VISUAL_PORTAL.html',
      description: 'Roteiro de validacao visual desktop/mobile com foco em ritmo, contraste, hierarquia e consistencia Shell x Identidade.',
      category: 'governanca',
      tag: 'qa-visual',
      audience: 'publicacao',
      updatedAt: '2026-04-10'
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

  function categoryLabel(value) {
    var labels = {
      all: 'todas as categorias',
      governanca: 'governanca',
      seguranca: 'seguranca',
      auditoria: 'auditoria',
      campanha: 'campanha e comunicacao'
    };
    return labels[value] || value;
  }

  function streamLabel(value) {
    var labels = {
      governanceOps: 'Governance Ops',
      publicationPipeline: 'Publication Pipeline',
      riskAndSecurity: 'Risk and Security',
      marketEnablement: 'Market Enablement'
    };
    return labels[value] || value;
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
      '<small>' + doc.category + ' · ' + doc.tag + ' · ' + doc.updatedAt + '</small>' +
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
        doc.href
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
    var businessModel = computeBusinessModel();

    if (!statDocs && !businessKpis) {
      return;
    }

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
      statUpdated.textContent = sorted[0] ? sorted[0].updatedAt : 'n/a';
    }

    if (businessKpis) {
      businessKpis.innerHTML = '' +
        '<div class="business-kpi"><strong>' + businessModel.kpis.hot + '</strong><span>documentos quentes</span></div>' +
        '<div class="business-kpi"><strong>' + businessModel.kpis.stale + '</strong><span>desatualizados +30d</span></div>' +
        '<div class="business-kpi"><strong>' + businessModel.kpis.streams + '</strong><span>fluxos de valor</span></div>' +
        '<div class="business-kpi"><strong>' + businessModel.priorityQueue[0].title + '</strong><span>prioridade #1</span></div>';
    }

    if (businessHotlist) {
      businessHotlist.innerHTML = businessModel.priorityQueue.slice(0, 5).map(function (doc) {
        return '<li class="business-item">' +
          '<a href="' + doc.href + '">' + doc.title + '</a>' +
          '<div class="business-meta"><span class="pill ' + statusClass(doc.status) + '">' + doc.status + '</span>' +
          'score ' + doc.priorityScore + ' · ' + streamLabel(doc.stream) + ' · ' + doc.ageInDays + 'd</div>' +
          '</li>';
      }).join('');
    }

    if (businessStreams) {
      businessStreams.innerHTML = Object.keys(businessModel.streams).map(function (stream) {
        return '<article class="stream-card">' +
          '<h3>' + streamLabel(stream) + '</h3>' +
          '<p>' + businessModel.streams[stream] + ' ativos neste fluxo de negocio.</p>' +
          '</article>';
      }).join('');
    }
  }

  function catalogCardHtml(doc) {
    return '<article class="catalog-card anim-in" data-category="' + doc.category + '">' +
      '<h3><a href="' + doc.href + '">' + doc.title + '</a></h3>' +
      '<div class="meta-line">' + doc.category + ' · ' + doc.tag + ' · ' + doc.updatedAt + '</div>' +
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
        countNode.textContent = 'Total visivel: ' + filtered.length + ' de ' + docs.length + ' documentos.';
      }

      if (emptyNode) {
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
      '<td>' + doc.category + '</td>' +
      '<td>' + doc.audience + '</td>' +
      '<td><span class="pill ' + statusClass(doc.status) + '">' + doc.status + '</span></td>' +
      '<td>' + doc.ageInDays + 'd</td>' +
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
        '<div class="business-kpi"><strong>' + model.kpis.total + '</strong><span>ativos mapeados</span></div>' +
        '<div class="business-kpi"><strong>' + model.kpis.hot + '</strong><span>quentes</span></div>' +
        '<div class="business-kpi"><strong>' + model.kpis.stale + '</strong><span>desatualizados +30d</span></div>' +
        '<div class="business-kpi"><strong>' + model.priorityQueue[0].priorityScore + '</strong><span>maior score</span></div>';
    }

    function render() {
      var selectedStream = streamFilter.value;
      var selectedStatus = statusFilter.value;
      var term = normalize(searchInput.value).trim();

      var filtered = model.priorityQueue.filter(function (doc) {
        var streamMatch = selectedStream === 'all' || doc.stream === selectedStream;
        var statusMatch = selectedStatus === 'all' || doc.status === selectedStatus;
        var text = normalize(doc.title + ' ' + doc.description + ' ' + doc.tag + ' ' + doc.category + ' ' + doc.audience);
        var termMatch = !term || text.indexOf(term) !== -1;
        return streamMatch && statusMatch && termMatch;
      });

      tableBody.innerHTML = filtered.map(businessRowHtml).join('');
      countLine.textContent = 'Itens visiveis: ' + filtered.length + ' de ' + model.priorityQueue.length + '.';
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
