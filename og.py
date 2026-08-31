# -*- coding: utf-8 -*-
"""Gera as imagens de compartilhamento — uma por escrito, mais a do site.

    python og.py

Link compartilhado sem `og:image` renderiza caixa cinza, e todo o tráfego
previsto vem do Instagram: são justamente as semanas de divulgação que rodariam
com o link feio (ESPEC §7).

Sem dependência nova. O cartão é uma página HTML com as fontes, a paleta e o
guilhoché do próprio site, fotografada a 1200×630 pelo Chromium que o
`verificar.py` já traz. Nada é redesenhado num editor de imagem: a imagem de
compartilhamento é o site, no formato do card.

Roda quando um escrito nasce ou muda de título. O `verificar.py` reclama se
faltar imagem, ou se ela for mais velha que o Markdown que a originou.
"""
import io, os, re, sys, glob

RAIZ = os.path.dirname(os.path.abspath(__file__))
ESCRITOS = os.path.join(RAIZ, "_conteudo", "escritos")
ATIVOS = os.path.join(RAIZ, "ativos")
SAIDA = os.path.join(ATIVOS, "og")

# Duas chapas por escrito, do mesmo guilhoche (ESPEC 7): a previa de link, que
# e deitada, e o post do Instagram, que e em pe. Sao trabalhos diferentes e um
# nao substitui o outro -- recortar a deitada em quadrado perde o titulo pelas
# bordas, porque ela foi desenhada deitada. So a primeira e exigida pela
# montagem; a de feed nao afeta o site e por isso nao derruba o build.
# A arte e uma so, reaproveitada em todo escrito -- e o que a Sullivan &
# Cromwell faz na peca editorial: forma abstrata neutra, dois tons, contraste
# baixo, sem relacao com o assunto do texto. Quem carrega o sentido e o titulo.
#
# Cada formato usa a arte cortada no proprio eixo longo: a em pe na tarja
# vertical da previa, a deitada na faixa do feed. Cortar contra o eixo esmaga
# o desenho e some com o movimento das linhas.
#
# A tipografia nunca fica POR CIMA da arte: fica ao lado, no marfim. E assim
# na referencia, e e o que mantem o titulo legivel.
FORMATOS = (
    dict(sufixo=u"", larg=1200, alt=630,
         pad=u"74px 78px", alto=u"100%",
         arte=u"onda-alta.jpg",
         tarja=u"right:0;top:0;width:504px;height:100%",
         caixa=u"inset:0 504px 0 0",
         regua=6, rotulo_px=19, gap=26, marca_px=30, oab_px=17,
         corpos=(64, 54, 46)),
    dict(sufixo=u"-feed", larg=1080, alt=1350,
         pad=u"104px 92px", alto=u"100%",
         arte=u"onda-larga.jpg",
         tarja=u"left:0;top:0;width:100%;height:700px",
         caixa=u"inset:700px 0 0 0",
         regua=8, rotulo_px=23, gap=34, marca_px=38, oab_px=21,
         corpos=(96, 82, 68)),
)

CAB = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def ler(p):
    return io.open(p, encoding="utf-8", newline="\n").read()


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def metadados(bruto):
    m = CAB.match(bruto)
    if not m:
        return None
    meta = {}
    for linha in m.group(1).split(u"\n"):
        if u":" in linha:
            k, v = linha.split(u":", 1)
            meta[k.strip()] = v.strip()
    return meta


def uri(nome):
    return "file:///" + os.path.join(ATIVOS, nome).replace("\\", "/")


# O cartão. Tudo em pixel absoluto — não é página responsiva, é uma chapa de
# tamanho fixo, fotografada uma vez. A geometria vem do formato: o que muda
# entre a prévia de link e o post do feed é proporção, nunca desenho.
CARTAO = u"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<style>
  @font-face{font-family:"Marca";src:url("%(marca)s") format("woff2");font-display:block}
  @font-face{font-family:"Serifada";src:url("%(serif)s") format("woff2-variations");font-display:block}
  @font-face{font-family:"Grotesca";src:url("%(sans)s") format("woff2-variations");font-display:block}
  *{margin:0;padding:0;box-sizing:border-box}
  body{
    width:%(larg)dpx;height:%(alt)dpx;overflow:hidden;position:relative;
    background:#FBF9F2;color:#14181A;
  }
  /* a arte ocupa uma tarja inteira e sangra: presença, não ilustração */
  .figura{position:absolute;%(tarja)s;object-fit:cover;display:block}
  .regua{position:absolute;left:0;top:0;width:100%%;height:%(regua)dpx;background:#245C53}
  .caixa{
    position:absolute;%(caixa)s;padding:%(pad)s;
    display:flex;flex-direction:column;justify-content:space-between;
  }
  .alto{max-width:%(alto)s}
  .rotulo{
    font-family:"Grotesca",sans-serif;font-size:%(rotulo_px)dpx;font-weight:600;
    letter-spacing:.15em;text-transform:uppercase;color:#245C53;
    margin-bottom:%(gap)dpx;
  }
  h1{
    font-family:"Serifada",Georgia,serif;font-weight:500;
    font-size:%(corpo)dpx;line-height:1.08;letter-spacing:-.006em;
    color:#14181A;text-wrap:balance;
  }
  .baixo{display:flex;align-items:baseline;gap:20px}
  .marca{
    font-family:"Marca","Serifada",Georgia,serif;font-size:%(marca_px)dpx;
    letter-spacing:.095em;text-transform:uppercase;color:#14181A;
  }
  .oab{font-family:"Grotesca",sans-serif;font-size:%(oab_px)dpx;font-weight:450;color:#5F686C}
</style></head><body>
  <img class="figura" src="%(figura)s" alt="">
  <div class="regua"></div>
  <div class="caixa">
    <div class="alto">
      <p class="rotulo">%(rotulo)s</p>
      <h1>%(titulo)s</h1>
    </div>
    <div class="baixo">
      <span class="marca">Bruno Hardt</span>
      <span class="oab">Advogado &#183; OAB/SC 79.648</span>
    </div>
  </div>
</body></html>"""


def corpo_do_titulo(titulo, corpos):
    """Título longo encolhe para caber em três linhas sem estourar a chapa."""
    n = len(titulo)
    if n <= 34:
        return corpos[0]
    if n <= 52:
        return corpos[1]
    return corpos[2]


def cartao(rotulo, titulo, figura, f):
    d = dict(f)
    d.update({
        "marca": uri("marca.woff2"), "serif": uri("serif.woff2"),
        "sans": uri("sans.woff2"), "figura": figura,
        "rotulo": esc(rotulo), "titulo": esc(titulo),
        "corpo": corpo_do_titulo(titulo, f["corpos"]),
    })
    return CARTAO % d


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit(u"playwright ausente: pip install -r requirements.txt "
                 u"&& playwright install")

    if not os.path.isdir(SAIDA):
        os.makedirs(SAIDA)

    chapas = []
    for caminho in sorted(glob.glob(os.path.join(ESCRITOS, "*.md"))):
        slug = os.path.basename(caminho)[:-3]
        meta = metadados(ler(caminho))
        if not meta:
            print(u"  %s: sem metadados, pulado" % slug)
            continue
        chapas.append((slug,
                       meta.get("categoria", u"Escrito"),
                       meta.get("titulo", slug)))

    # a chapa do site: capa, atuação, sobre e índice compartilham esta
    chapas.append((u"site", u"Escritos", u"Bruno Hardt"))

    temp = os.path.join(SAIDA, "_chapa.html")
    with sync_playwright() as pw:
        navegador = pw.chromium.launch()
        for f in FORMATOS:
            pag = navegador.new_page(
                viewport={"width": f["larg"], "height": f["alt"]},
                device_scale_factor=1)
            arte = uri(os.path.join("img", f["arte"]))
            for slug, rotulo, titulo in chapas:
                io.open(temp, "w", encoding="utf-8", newline="\n").write(
                    cartao(rotulo, titulo, arte, f))
                pag.goto("file:///" + temp.replace("\\", "/"))
                pag.wait_for_timeout(120)      # as fontes terminam de assentar
                nome = slug + f["sufixo"] + ".png"
                destino = os.path.join(SAIDA, nome)
                pag.screenshot(path=destino)
                print(u"  og/%-28s %6.1f KB  %d\u00d7%d"
                      % (nome, os.path.getsize(destino) / 1024.0,
                         f["larg"], f["alt"]))
            pag.close()
        navegador.close()
    os.remove(temp)


if __name__ == "__main__":
    main()
