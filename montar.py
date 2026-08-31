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
    # normaliza o fim de linha na leitura: as expressoes que acham os blocos
    # de prova casam com \n, e um checkout com autocrlf=true transforma o
    # arquivo em CRLF sem ninguem pedir (aconteceu no merge da estreia).
    return io.open(p, encoding="utf-8", newline="\n").read().replace("\r\n", "\n")


def escrever(p, s):
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def por_extenso(iso):
    """A data por extenso. A hora existe para desempatar a ordem, nao para o
    leitor: dois escritos publicados no mesmo dia empatam na ordenacao, e ele
    nao precisa saber qual saiu as oito e qual as nove."""
    a, m, d = iso.split(" ")[0].split("-")
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
#   tipo: ementa
#   fonte: TJSC, Apelação n. ...
#   inteiro_teor_conferido: nao
#   ---
#   <texto literal, byte a byte>
#   :::
VERBETE = re.compile(
    r"^:::verbete[ \t]+(?P<id>[\w\-]+)[ \t]*\n(?P<meta>.*?)\n---[ \t]*\n(?P<corpo>.*?)\n:::[ \t]*$",
    re.S | re.M)

# O leitor vê o rótulo e julga o peso: andamento de tema repetitivo não é
# ementa, e o site não finge que é (ESPEC §2.2).
ROTULO_PROVA = {
    u"ementa": u"Ementa",
    u"enunciado": u"Enunciado",
    u"consulta": u"Consulta &#224; fonte oficial",
}


def render_verbetes(md, slug, rascunho, problemas):
    """Troca cada bloco :::verbete por HTML, e reclama do que não foi conferido."""
    def troca(m):
        vid = m.group("id")
        meta = {}
        for linha in m.group("meta").split(u"\n"):
            if u":" in linha:
                k, v = linha.split(u":", 1)
                meta[k.strip()] = v.strip()

        tipo = meta.get("tipo", u"").strip().lower()
        if tipo not in ROTULO_PROVA:
            problemas.append(u"%s: o bloco %s tem tipo '%s' (esperado: %s)"
                             % (slug, vid, tipo, u", ".join(sorted(ROTULO_PROVA))))
            tipo = u"ementa"

        conferido = meta.get("inteiro_teor_conferido", "nao").strip().lower()
        if conferido != "sim" and not rascunho:
            problemas.append(
                u"%s cita o verbete %s com inteiro_teor_conferido: %s" % (slug, vid, conferido))
        selo = u"" if conferido == "sim" else \
            u'\n    <p class="pendente">Inteiro teor ainda n&#227;o conferido na fonte.</p>'

        # ementa longa entra recortada, e o rótulo diz isso: o leitor precisa
        # saber que está vendo um trecho antes de julgar o peso (ESPEC §2.2)
        rotulo = ROTULO_PROVA[tipo]
        if meta.get("recorte", u"").strip().lower() == u"sim":
            rotulo += u" (trecho)"

        # o crédito é o julgado, montado pelo citar.py dos campos do verbete.
        # O `fonte` do corpus não entra aqui: é nota de trabalho (ESPEC §2.2).
        # a consulta mostra onde e quando: sem isso ela não é verificável
        credito = esc(meta.get("credito", vid))
        if tipo == u"consulta" and meta.get("url"):
            credito = u'<a href="%s" rel="noopener">%s</a>' % (
                esc(meta["url"]), credito)
            if meta.get("acesso"):
                credito += u" &#183; consulta em %s" % por_extenso(meta["acesso"])

        return (u'<figure class="verbete verbete--%s" id="v-%s">\n'
                u'    <p class="rotulo-prova">%s</p>\n'
                u'    <blockquote>%s</blockquote>\n'
                u'    <figcaption>%s</figcaption>%s\n'
                u'  </figure>') % (
            tipo, esc(vid), rotulo,
            u"\n".join(u"<p>%s</p>" % esc(p.strip())
                       for p in m.group("corpo").strip().split(u"\n\n") if p.strip()),
            credito,
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
        rascunho = meta.get("rascunho", "nao").lower() == "sim"
        for exigido in ("titulo", "dek", "categoria", "guilhoche"):
            if not meta.get(exigido):
                problemas.append(u"%s: falta o campo '%s'" % (nome, exigido))
        # A data e a da PUBLICACAO (ESPEC 1.1). O escrito em estoque ainda nao
        # tem uma, e inventa-la seria datar ficcao; publicado sem data nao monta.
        if not rascunho and not meta.get("data"):
            problemas.append(u"%s: publicado sem 'data' \u2014 ela \u00e9 a da "
                             u"publica\u00e7\u00e3o, e falta" % nome)
        corpo = render_verbetes(corpo, slug, rascunho, problemas)
        meta.update({
            "slug": slug,
            "rascunho": rascunho,
            "data_extenso": por_extenso(meta["data"]) if meta.get("data") else u"",
            "data_iso": meta.get("data", u"").replace(u" ", u"T"),
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
    """A capa: o trilho em destaque, e a grade com o resto (ESPEC 4.1).

    O trilho e METADE do acervo, com teto de quatro: dois escritos dao uma
    lamina e um cartao; quatro dao duas e duas; oito ou mais dao quatro laminas
    e o resto na grade. A regra existe para a grade nunca ficar vazia. Na S&C,
    que e a referencia, o carrossel tem cinco laminas e a grade tem outros
    dezessete cartoes — o carrossel nunca e a pagina inteira, e la isso so
    funciona porque sobra acervo. Aqui a proporcao faz o mesmo com quatro textos.

    Nenhum campo marca destaque: e a recencia. Escolher a manchete a mao todo
    mes e um passo manual que nada verifica, e num sistema que ja depende
    inteiro da disciplina do autor, um passo manual a menos vale mais que a
    escolha que ele daria."""
    quantos = min(4, max(1, len(escritos) // 2))
    destaques = escritos[:quantos]
    resto = escritos[quantos:]
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
    { "@type": "City", "name": "Pomerode", "addressRegion": "SC", "addressCountry": "BR" },
    { "@type": "Country", "name": "Brasil" }
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
</script>''' % (esc(e["titulo"]), esc(e["dek"]), e["data_iso"], SITE, SITE, SITE,
                e["slug"])


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
    # og:image é URL absoluta, sempre: quem lê o card não resolve caminho
    # relativo. Escrito tem a sua; o resto do site divide a chapa geral.
    doc = (doc.replace(u"{{titulo}}", esc(meta.get("titulo", u"Bruno Hardt")))
              .replace(u"{{descricao}}", esc(meta.get("descricao", u"")))
              .replace(u"{{canonical}}", canonical)
              .replace(u"{{ogimagem}}",
                       SITE + u"ativos/og/%s.png" % meta.get("ogslug", u"site"))
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
    <img class="guilhoche guilhoche--artigo" src="../ativos/faixa-%s.svg" alt="" width="1600" height="500">
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
                         "ogtipo": "article", "ogslug": e["slug"]},
                 u"escritos/%s.html" % e["slug"], jsonld_artigo(e))


def main():
    problemas = []
    n, tam = juntar_estilo()
    print(u"  estilo.css        %2d modulos  %5.1f KB" % (n, tam / 1024.0))

    escritos = carregar_escritos(problemas)
    publicados = [e for e in escritos if not e["rascunho"]]
    for e in escritos:
        if e["rascunho"]:
            # Escrito em estoque nao vira pagina, nao entra na capa e nao entra
            # no indice. O estoque e o que sustenta a cadencia (ESPEC 1.1) e
            # precisa poder morar no repositorio com a montagem verde; publicar
            # rascunho sob o nome e a OAB do autor e caro sob o Provimento 205.
            # Se ele ja teve pagina, ela sai agora.
            velha = os.path.join(RAIZ, "escritos", e["slug"] + ".html")
            if os.path.exists(velha):
                os.remove(velha)
            print(u"  %-33s  em estoque" % (e["slug"] + ".md"))
            continue
        t = pagina_escrito(e)
        print(u"  escritos/%-24s %5.1f KB" % (e["slug"] + ".html", t / 1024.0))

    for nome in sorted(os.listdir(PAGINAS)):
        if not nome.endswith(".html"):
            continue
        meta, miolo = metadados(ler(os.path.join(PAGINAS, nome)), CAB_PAG)
        if meta is None:
            sys.exit(u"faltou o bloco de metadados em %s" % nome)
        miolo = (miolo.replace(u"{{capa}}", montar_capa(publicados))
                      .replace(u"{{indice-escritos}}", montar_indice(publicados)))
        jl = jsonld_pessoa() if meta.get("jsonld") == "pessoa" else u""
        rel = meta.get("saida", nome)
        t = casca(miolo, meta, rel, jl)
        print(u"  %-33s %5.1f KB" % (rel, t / 1024.0))

    if problemas:
        print(u"\n  A MONTAGEM RECUSA PUBLICAR:")
        for p in problemas:
            print(u"    - %s" % p)
        sys.exit(1)
    print(u"\n  %d escrito(s) publicado(s), %d em estoque.\n"
          % (len(publicados), len(escritos) - len(publicados)))

    # A montagem exige navegador (ESPEC §2.3): montar sem verificar não é uma
    # montagem, é um rascunho de HTML. Um comando só, sem disciplina no meio.
    import verificar
    verificar.main()


if __name__ == "__main__":
    main()
