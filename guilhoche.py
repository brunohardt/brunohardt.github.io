# -*- coding: utf-8 -*-
"""Gera os guilhochés — as curvas gravadas de certificado e apólice.

Nada é desenhado à mão: são epitrocoides e interferências de senoides, a mesma
família de curvas que a impressão de segurança usa desde o século XIX. Cada
escrito ganha uma marca própria, determinada por parâmetros diferentes.

Cada SVG carrega o próprio <style> com media query, para responder ao tema
mesmo sendo carregado por <img> — o mesmo truque do favicon.
"""
import io, math, os

SAIDA = r"C:\Users\Hardt\Dev\site-bruno-hardt\ativos"
W = H = 1000
CX = CY = 500

CABECA = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000" role="img" aria-label="%s">
<title>%s</title>
<style>
  .f{fill:none;stroke:#245C53;stroke-width:%s;stroke-linecap:round;opacity:%s}
  @media (prefers-color-scheme:dark){ .f{stroke:#7FCFBD} }
</style>
"""
RODAPE = "</svg>\n"


def caminho(pontos):
    d = "M%d %d" % (round(pontos[0][0]), round(pontos[0][1]))
    ax, ay = round(pontos[0][0]), round(pontos[0][1])
    for x, y in pontos[1:]:
        x, y = round(x), round(y)
        if x == ax and y == ay:      # ponto repetido nao desenha nada
            continue
        d += "l%d %d" % (x - ax, y - ay)   # relativo: numeros menores
        ax, ay = x, y
    return d


def epitrocoide(R, r, d, escala, passos=560, giro=0.0):
    """x = (R+r)cos t - d cos((R+r)/r t);  y = idem com sen."""
    pts = []
    voltas = r / math.gcd(int(R), int(r)) if float(r).is_integer() else 12
    tmax = 2 * math.pi * max(1, int(voltas))
    for i in range(passos + 1):
        t = tmax * i / passos
        k = (R + r) / r
        x = (R + r) * math.cos(t) - d * math.cos(k * t)
        y = (R + r) * math.sin(t) - d * math.sin(k * t)
        xr = x * math.cos(giro) - y * math.sin(giro)
        yr = x * math.sin(giro) + y * math.cos(giro)
        pts.append((CX + xr * escala, CY + yr * escala))
    return pts


def marca_roseta(nome, R, r, d, n=7, base=0.86, passo=0.045, sw="1.6", op=".85"):
    """Rosetas concêntricas — a marca clássica de apólice."""
    partes = [CABECA % (nome, nome, sw, op)]
    for i in range(n):
        e = base - i * passo
        pts = epitrocoide(R, r, d, e * 500 / (R + r + d), giro=i * 0.16)
        partes.append('<path class="f" d="%s"/>\n' % caminho(pts))
    partes.append(RODAPE)
    return "".join(partes)


def marca_interferencia(nome, linhas=46, amp=118, ciclos=2.4, torcao=1.7, sw="1.5", op=".8"):
    """Feixe de senoides com fase progressiva: a onda gravada."""
    partes = [CABECA % (nome, nome, sw, op)]
    for i in range(linhas):
        y0 = 90 + (820.0 * i / (linhas - 1))
        fase = torcao * math.pi * i / linhas
        a = amp * math.sin(math.pi * i / (linhas - 1)) ** 1.15
        pts = []
        for j in range(97):
            x = 70 + (860.0 * j / 96)
            t = 2 * math.pi * ciclos * (j / 96.0)
            pts.append((x, y0 + a * math.sin(t + fase)))
        partes.append('<path class="f" d="%s"/>\n' % caminho(pts))
    partes.append(RODAPE)
    return "".join(partes)


def marca_trama(nome, n=34, sw="1.4", op=".78"):
    """Duas famílias de arcos cruzando — a trama de fundo de certificado."""
    partes = [CABECA % (nome, nome, sw, op)]
    for fam, sinal in ((0, 1), (1, -1)):
        for i in range(n):
            u = i / (n - 1.0)
            pts = []
            for j in range(65):
                v = j / 64.0
                x = 70 + 860 * v
                curva = math.sin(math.pi * v) * (150 * (u - .5)) * sinal
                base = 110 + 780 * u
                pts.append((x, base + curva))
            partes.append('<path class="f" d="%s"/>\n' % caminho(pts))
    partes.append(RODAPE)
    return "".join(partes)


marcas = {
    # tres caracteres distintos: uma roseta cheia, uma onda, uma estrela aberta
    "guilhoche-1.svg": marca_roseta(u"Guilhoché — roseta", 7, 3, 5, n=6, passo=.058),
    "guilhoche-2.svg": marca_interferencia(u"Guilhoché — interferência"),
    "guilhoche-3.svg": marca_roseta(u"Guilhoché — estrela", 11, 4, 9, n=5, base=.92, passo=.072, sw="1.5", op=".82"),
}

for nome, conteudo in marcas.items():
    p = os.path.join(SAIDA, nome)
    io.open(p, "w", encoding="utf-8", newline="\n").write(conteudo)
    print("  %-18s %6.1f KB" % (nome, os.path.getsize(p) / 1024.0))
