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
      title: 'Code Health Report',
      href: 'CODE_HEALTH_REPORT.html',
      description: 'Indicadores de qualidade de codigo e manutencao dos repositorios.',
      category: 'auditoria',
      tag: 'code-health',
      audience: 'engenharia',
      updatedAt: '2026-03-18'
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
      title: 'Blackbox Ambiente de Desenvolvimento',
      href: 'BLACKBOX_AMBIENTE_DESENVOLVIMENTO.html',
      description: 'Panorama tecnico do ambiente de desenvolvimento e pontos criticos.',
      category: 'governanca',
      tag: 'ambiente',
      audience: 'engenharia',
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
      href: 'b2b_export/index.html',
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
      title: 'Contexto Sessao IA',
      href: 'CONTEXTO_SESSAO_IA.html',
      description: 'Registro de contexto e alinhamento de operacao assistida por IA.',
      category: 'governanca',
      tag: 'ia',
      audience: 'operacao',
      updatedAt: '2026-03-10'
    },
    {
      title: 'Validacao Memorias IA',
      href: 'VALIDACAO_MEMORIAS_IA_ECOSSISTEMA_2026_03_10.html',
      description: 'Checklist de validacao de memoria e consistencia de contexto.',
      category: 'governanca',
      tag: 'ia',
      audience: 'operacao',
      updatedAt: '2026-03-10'
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
    var cardsRoot = qs('#documentos');
    if (!cardsRoot) {
      return;
    }

    var searchInput = qs('#searchInput');
    var categorySelect = qs('#categorySelect');
    var resultLine = qs('#resultLine');
    var emptyState = qs('#emptyState');
    var statDocs = qs('#statDocs');
    var statCategories = qs('#statCategories');
    var statUpdated = qs('#statUpdated');

    function render() {
      var filtered = filterDocs(searchInput.value, categorySelect.value);
      cardsRoot.innerHTML = filtered.map(cardHtml).join('');

      if (resultLine) {
        resultLine.textContent =
          'Mostrando ' + filtered.length + ' de ' + docs.length + ' documentos em ' + categoryLabel(categorySelect.value) + '.';
      }

      if (emptyState) {
        emptyState.style.display = filtered.length === 0 ? 'block' : 'none';
      }

      updateChips(categorySelect.value);
    }

    qsa('.chip').forEach(function (chip) {
      chip.addEventListener('click', function () {
        categorySelect.value = chip.getAttribute('data-category');
        render();
      });
    });

    searchInput.addEventListener('input', render);
    categorySelect.addEventListener('change', render);

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

    render();
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

  window.CaraCoreDocs = {
    docs: docs
  };

  initPortalHome();
  initCatalogPage();
})();
