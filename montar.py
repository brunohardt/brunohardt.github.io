# -*- coding: utf-8 -*-
"""Montador do site.

    python montar.py

Fonte em `_fonte/` e `_conteudo/`, saída na raiz. Nada de monolito:

  _fonte/partes/     a casca (cabeça, barra, rodapé), uma vez só
  _fonte/paginas/    o miolo de cada página fixa
  _conteudo/escritos/*.md   UM arquivo por escrito — e só ele
  ativos/estilo/     um módulo de CSS por assunto

A regra 4 da ESPEC vive aqui: **escrito novo não toca em HTML**. De um único
Markdown saem três coisas — a página do artigo, a entrada do índice e o cartão
da capa. Acrescentar um texto é acrescentar um arquivo.

REQUISITO: python-markdown (`pip install -r requirements.txt`).
"""
import io, os, re, sys, unicodedata

try:
    import markdown
except ImportError:
    sys.exit("falta a dependencia: pip install -r requirements.txt")

RAIZ = os.path.dirname(os.path.abspath(__file__))
PARTES = os.path.join(RAIZ, "_fonte", "partes")
PAGINAS = os.path.join(RAIZ, "_fonte", "paginas")
ESCRITOS = os.path.join(RAIZ, "_conteudo", "escritos")
ESTILO = os.path.join(RAIZ, "ativos", "estilo")
SITE = "https://brunohardt.github.io/"

MES = ["", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
       "agosto", "setembro", "outubro", "novembro", "dezembro"]


def ler(p):
    return io.open(p, encoding="utf-8", newline="\n").read()


def escrever(p, s):
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def por_extenso(iso):
    a, m, d = iso.split("-")
    return u"%d de %s de %s" % (int(d), MES[int(m)], a)


# ============================================================== metadados
CAB = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
CAB_PAG = re.compile(r"^<!--@\s*\n(.*?)\n@-->\s*\n", re.S)


def metadados(bruto, padrao):
    m = padrao.match(bruto)
    if not m:
        return None, bruto
    meta = {}
    for linha in m.group(1).split(u"\n"):
        if u":" in linha:
            k, v = linha.split(u":", 1)
            meta[k.strip()] = v.strip()
    return meta, bruto[m.end():]


# ============================================================== o verbete
# Bloco de prova, escrito por citar.py e congelado dentro do escrito:
#
#   :::verbete 41-dobro-independe-do-elemento-volitivo
#   fonte: TJSC, Apelação n. ...
#   inteiro_teor_conferido: nao
#   ---
#   <ementa literal, byte a byte>
#   :::
VERBETE = re.compile(
    r"^:::verbete[ \t]+(?P<id>[\w\-]+)[ \t]*\n(?P<meta>.*?)\n---[ \t]*\n(?P<corpo>.*?)\n:::[ \t]*$",
    re.S | re.M)


def render_verbetes(md, slug, rascunho, problemas):
    """Troca cada bloco :::verbete por HTML, e reclama do que não foi conferido."""
    def troca(m):
        vid = m.group("id")
        meta = {}
        for linha in m.group("meta").split(u"\n"):
            if u":" in linha:
                k, v = linha.split(u":", 1)
                meta[k.strip()] = v.strip()
        conferido = meta.get("inteiro_teor_conferido", "nao").strip().lower()
        if conferido != "sim" and not rascunho:
            problemas.append(
                u"%s cita o verbete %s com inteiro_teor_conferido: %s" % (slug, vid, conferido))
        selo = u"" if conferido == "sim" else \
            u'\n    <p class="pendente">Inteiro teor ainda n&#227;o conferido na fonte.</p>'
        return (u'<figure class="verbete" id="v-%s">\n'
                u'    <blockquote>%s</blockquote>\n'
                u'    <figcaption>%s</figcaption>%s\n'
                u'  </figure>') % (
            esc(vid),
            u"\n".join(u"<p>%s</p>" % esc(p.strip())
                       for p in m.group("corpo").strip().split(u"\n\n") if p.strip()),
            esc(meta.get("fonte", vid)),
            selo)
    return VERBETE.sub(troca, md)


# ============================================================== escritos
def carregar_escritos(problemas):
    if not os.path.isdir(ESCRITOS):
        return []
    saida = []
    for nome in sorted(os.listdir(ESCRITOS)):
        if not nome.endswith(".md"):
            continue
        slug = nome[:-3]
        meta, corpo = metadados(ler(os.path.join(ESCRITOS, nome)), CAB)
        if meta is None:
            problemas.append(u"%s: faltou o bloco de metadados" % nome)
            continue
        for exigido in ("titulo", "dek", "categoria", "data", "guilhoche"):
            if not meta.get(exigido):
                problemas.append(u"%s: falta o campo '%s'" % (nome, exigido))
        rascunho = meta.get("rascunho", "nao").lower() == "sim"
        corpo = render_verbetes(corpo, slug, rascunho, problemas)
        meta.update({
            "slug": slug,
            "rascunho": rascunho,
            "destaque": meta.get("destaque", "nao").lower() == "sim",
            "data_extenso": por_extenso(meta["data"]) if meta.get("data") else u"",
            "html": markdown.markdown(corpo, extensions=["extra", "smarty"],
                                      output_format="html5"),
        })
        saida.append(meta)
    saida.sort(key=lambda e: e.get("data", ""), reverse=True)
    return saida


# ============================================================== fragmentos
def cartao(e, raiz=u""):
    return u'''      <li class="cartao">
        <div class="dentro">
          <p class="rotulo">%s</p>
          <h3><a href="%sescritos/%s.html">%s</a></h3>
          <p class="dek">%s</p>
          <span class="data">%s</span>
        </div>
        <img class="figura" src="%sativos/guilhoche-%s.svg" alt="" width="1000" height="1000">
      </li>''' % (esc(e["categoria"]), raiz, e["slug"], esc(e["titulo"]),
                  esc(e["dek"]), e["data_extenso"], raiz, e["guilhoche"])


def lamina(e, i):
    return u'''      <article class="lamina" id="e%d">
        <div class="lamina-interna">
          <img class="guilhoche" src="ativos/guilhoche-%s.svg" alt="" width="1000" height="1000">
          <div>
            <p class="rotulo">%s</p>
            <h2><a href="escritos/%s.html">%s</a></h2>
            <p class="dek">%s</p>
            <span class="data">%s</span>
          </div>
        </div>
      </article>''' % (i, e["guilhoche"], esc(e["categoria"]), e["slug"],
                       esc(e["titulo"]), esc(e.get("chamada") or e["dek"]),
                       e["data_extenso"])


def montar_capa(escritos):
    """A capa: as laminas em destaque, e a grade com o resto.
    Com poucos textos a grade some — cartao solitario denuncia falta."""
    destaques = [e for e in escritos if e["destaque"]] or escritos[:1]
    resto = [e for e in escritos if e not in destaques]
    partes = []
    if destaques:
        partes.append(u'''  <section class="vitrine" aria-labelledby="vit">
    <h2 class="so-leitor" id="vit">Em destaque</h2>
    <div class="trilho" tabindex="0" role="region" aria-label="Escritos em destaque, rol&#225;vel na horizontal">
%s
    </div>%s
  </section>''' % (
            u"\n".join(lamina(e, i + 1) for i, e in enumerate(destaques)),
            (u'\n    <nav class="reguas" aria-label="Escolher o escrito em destaque">\n%s\n    </nav>'
             % u"\n".join(u'      <a href="#e%d">%d</a>' % (i + 1, i + 1)
                          for i in range(len(destaques)))) if len(destaques) > 1 else u""))
    if resto:
        partes.append(u'''  <section class="secao" aria-labelledby="esc">
    <div class="cabeca">
      <h2 class="rotulo" id="esc">Mais escritos</h2>
      <a class="mais" href="escritos.html">Ver todos</a>
    </div>
    <ul class="grade">
%s
    </ul>
  </section>''' % u"\n".join(cartao(e) for e in resto))
    return u"\n\n".join(partes)


def montar_indice(escritos):
    """O índice. O h2 não aparece na tela, mas existe: os cartões são h3, e
    h3 direto sob h1 é degrau quebrado para quem navega por títulos."""
    return u'''  <h2 class="so-leitor">Todos os escritos</h2>
  <ul class="grade">
%s
  </ul>''' % u"\n".join(cartao(e) for e in escritos)


# ============================================================== JSON-LD
def jsonld_pessoa():
    return u'''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "%(s)s#bruno-hardt",
  "name": "Bruno Hardt", "givenName": "Bruno", "familyName": "Hardt",
  "jobTitle": "Advogado", "url": "%(s)s",
  "email": "hardtbruno@hotmail.com", "telephone": "+5547992261494",
  "identifier": { "@type": "PropertyValue", "propertyID": "OAB/SC", "value": "79.648" },
  "knowsAbout": ["Direito público", "Direito criminal", "Direito cível"],
  "knowsLanguage": "pt-BR",
  "areaServed": [
    { "@type": "City", "name": "Blumenau", "addressRegion": "SC", "addressCountry": "BR" },
    { "@type": "City", "name": "Pomerode", "addressRegion": "SC", "addressCountry": "BR" }
  ],
  "affiliation": { "@type": "Organization",
    "name": "Ordem dos Advogados do Brasil, Seccional de Santa Catarina",
    "alternateName": "OAB/SC" },
  "sameAs": ["https://www.instagram.com/hardt.adv/"],
  "worksFor": { "@type": "Organization", "@id": "https://ordir.com.br/#ordir",
    "name": "Ordir", "url": "https://ordir.com.br",
    "founder": { "@id": "%(s)s#bruno-hardt" } }
}
</script>''' % {"s": SITE}


def jsonld_artigo(e):
    return u'''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "%s",
  "description": "%s",
  "datePublished": "%s",
  "inLanguage": "pt-BR",
  "author": { "@type": "Person", "@id": "%s#bruno-hardt", "name": "Bruno Hardt" },
  "publisher": { "@id": "%s#bruno-hardt" },
  "mainEntityOfPage": "%sescritos/%s.html"
}
</script>''' % (esc(e["titulo"]), esc(e["dek"]), e["data"], SITE, SITE, SITE, e["slug"])


# ============================================================== montagem
def casca(miolo, meta, saida_rel, jsonld=u""):
    profundidade = saida_rel.count("/")
    raiz = u"../" * profundidade if profundidade else u"./"
    canonical = SITE + (u"" if saida_rel == "index.html" else saida_rel)
    doc = u"\n".join([
        ler(os.path.join(PARTES, "cabeca.html")).rstrip(u"\n"), u"",
        ler(os.path.join(PARTES, "topo.html")).rstrip(u"\n"), u"",
        miolo.rstrip(u"\n"), u"",
        ler(os.path.join(PARTES, "rodape.html")).rstrip(u"\n"), u"",
        u"</body>", u"</html>"])
    doc = (doc.replace(u"{{titulo}}", esc(meta.get("titulo", u"Bruno Hardt")))
              .replace(u"{{descricao}}", esc(meta.get("descricao", u"")))
              .replace(u"{{canonical}}", canonical)
              .replace(u"{{ogtipo}}", meta.get("ogtipo", u"website"))
              .replace(u"{{jsonld}}", jsonld)
              .replace(u"{{raiz}}", raiz))
    ativo = meta.get("ativo", u"")
    for nome in (u"escritos", u"atuacao", u"sobre"):
        doc = doc.replace(u"{{ativo-%s}}" % nome,
                          u' aria-current="page"' if nome == ativo else u"")
    sobrou = re.findall(r"\{\{[a-z-]+\}\}", doc)
    if sobrou:
        sys.exit(u"marcador nao substituido em %s: %s" % (saida_rel, sorted(set(sobrou))))
    escrever(os.path.join(RAIZ, saida_rel), doc + u"\n")
    return len(doc.encode("utf-8"))


def juntar_estilo():
    partes = sorted(f for f in os.listdir(ESTILO) if f.endswith(".css"))
    corpo = [u'@charset "utf-8";',
             u"/* GERADO por montar.py a partir de ativos/estilo/*.css.",
             u"   Não edite: a próxima montagem sobrescreve.",
             u"   Módulos: %s */" % u", ".join(partes), u""]
    for p in partes:
        corpo.append(ler(os.path.join(ESTILO, p)).rstrip(u"\n"))
        corpo.append(u"")
    saida = os.path.join(RAIZ, "ativos", "estilo.css")
    escrever(saida, u"\n".join(corpo) + u"\n")
    return len(partes), os.path.getsize(saida)


def pagina_escrito(e):
    miolo = u'''<main id="miolo" class="envelope leitura">
  <article>
    <header class="abertura">
      <p class="rotulo">%s</p>
      <h1>%s</h1>
      <p class="dek">%s</p>
      <p class="creditos"><span class="data">%s</span><span class="autor">Bruno Hardt</span></p>
    </header>
    <img class="guilhoche guilhoche--artigo" src="../ativos/guilhoche-%s.svg" alt="" width="1000" height="1000">
    <div class="corpo">
%s
    </div>
  </article>
  <nav class="volta"><a href="../escritos.html">Todos os escritos</a></nav>
</main>''' % (esc(e["categoria"]), esc(e["titulo"]), esc(e["dek"]),
              e["data_extenso"], e["guilhoche"],
              u"\n".join(u"      " + l for l in e["html"].split(u"\n")))
    return casca(miolo, {"titulo": u"%s — Bruno Hardt" % e["titulo"],
                         "descricao": e["dek"], "ativo": "escritos",
                         "ogtipo": "article"},
                 u"escritos/%s.html" % e["slug"], jsonld_artigo(e))


def main():
    problemas = []
    n, tam = juntar_estilo()
    print(u"  estilo.css        %2d modulos  %5.1f KB" % (n, tam / 1024.0))

    escritos = carregar_escritos(problemas)
    for e in escritos:
        t = pagina_escrito(e)
        print(u"  escritos/%-24s %5.1f KB%s" % (e["slug"] + ".html", t / 1024.0,
                                                u"   [RASCUNHO]" if e["rascunho"] else u""))

    for nome in sorted(os.listdir(PAGINAS)):
        if not nome.endswith(".html"):
            continue
        meta, miolo = metadados(ler(os.path.join(PAGINAS, nome)), CAB_PAG)
        if meta is None:
            sys.exit(u"faltou o bloco de metadados em %s" % nome)
        miolo = (miolo.replace(u"{{capa}}", montar_capa(escritos))
                      .replace(u"{{indice-escritos}}", montar_indice(escritos)))
        jl = jsonld_pessoa() if meta.get("jsonld") == "pessoa" else u""
        rel = meta.get("saida", nome)
        t = casca(miolo, meta, rel, jl)
        print(u"  %-33s %5.1f KB" % (rel, t / 1024.0))

    if problemas:
        print(u"\n  A MONTAGEM RECUSA PUBLICAR:")
        for p in problemas:
            print(u"    - %s" % p)
        sys.exit(1)
    print(u"\n  %d escrito(s), tudo conferido." % len(escritos))


if __name__ == "__main__":
    main()
