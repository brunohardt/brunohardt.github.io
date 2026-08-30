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

LARG, ALT = 1200, 630

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
# 1200×630 que será fotografada uma vez.
CARTAO = u"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<style>
  @font-face{font-family:"Marca";src:url("%(marca)s") format("woff2");font-display:block}
  @font-face{font-family:"Serifada";src:url("%(serif)s") format("woff2-variations");font-display:block}
  @font-face{font-family:"Grotesca";src:url("%(sans)s") format("woff2-variations");font-display:block}
  *{margin:0;padding:0;box-sizing:border-box}
  body{
    width:%(w)dpx;height:%(h)dpx;overflow:hidden;position:relative;
    background:#FBF9F2;color:#14181A;
  }
  /* o guilhoché sangra pela direita: presença, não ilustração */
  .figura{
    position:absolute;right:-150px;top:50%%;transform:translateY(-50%%);
    width:660px;height:660px;opacity:.5;
  }
  .regua{position:absolute;left:0;top:0;width:100%%;height:6px;background:#245C53}
  .caixa{
    position:absolute;inset:0;padding:74px 78px;
    display:flex;flex-direction:column;justify-content:space-between;
  }
  .alto{max-width:720px}
  .rotulo{
    font-family:"Grotesca",sans-serif;font-size:19px;font-weight:600;
    letter-spacing:.15em;text-transform:uppercase;color:#245C53;
    margin-bottom:26px;
  }
  h1{
    font-family:"Serifada",Georgia,serif;font-weight:500;
    font-size:%(corpo)dpx;line-height:1.08;letter-spacing:-.006em;
    color:#14181A;text-wrap:balance;
  }
  .baixo{display:flex;align-items:baseline;gap:20px}
  .marca{
    font-family:"Marca","Serifada",Georgia,serif;font-size:30px;
    letter-spacing:.095em;text-transform:uppercase;color:#14181A;
  }
  .oab{font-family:"Grotesca",sans-serif;font-size:17px;font-weight:450;color:#5F686C}
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


def corpo_do_titulo(titulo):
    """Título longo encolhe para caber em três linhas sem estourar a chapa."""
    n = len(titulo)
    if n <= 34:
        return 76
    if n <= 52:
        return 64
    return 54


def cartao(rotulo, titulo, figura):
    return CARTAO % {
        "w": LARG, "h": ALT,
        "marca": uri("marca.woff2"), "serif": uri("serif.woff2"),
        "sans": uri("sans.woff2"), "figura": figura,
        "rotulo": esc(rotulo), "titulo": esc(titulo),
        "corpo": corpo_do_titulo(titulo),
    }


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
                       meta.get("titulo", slug),
                       uri("guilhoche-%s.svg" % meta.get("guilhoche", "1"))))

    # a chapa do site: capa, atuação, sobre e índice compartilham esta
    chapas.append((u"site", u"Escritos",
                   u"Bruno Hardt", uri("guilhoche-2.svg")))

    temp = os.path.join(SAIDA, "_chapa.html")
    with sync_playwright() as pw:
        navegador = pw.chromium.launch()
        pag = navegador.new_page(viewport={"width": LARG, "height": ALT},
                                 device_scale_factor=1)
        for slug, rotulo, titulo, figura in chapas:
            io.open(temp, "w", encoding="utf-8", newline="\n").write(
                cartao(rotulo, titulo, figura))
            pag.goto("file:///" + temp.replace("\\", "/"))
            pag.wait_for_timeout(120)          # as fontes terminam de assentar
            destino = os.path.join(SAIDA, slug + ".png")
            pag.screenshot(path=destino)
            print(u"  og/%-28s %6.1f KB" % (slug + ".png",
                                            os.path.getsize(destino) / 1024.0))
        navegador.close()
    os.remove(temp)


if __name__ == "__main__":
    main()
