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
QUADRADO = (1000, 1000)
FAIXA = (1600, 500)          # 16:5, a proporção da abertura do artigo

CABECA = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s">
<title>%s</title>
<style>
  .f{fill:none;stroke:#245C53;stroke-width:%s;stroke-linecap:round;opacity:%s}
  @media (prefers-color-scheme:dark){ .f{stroke:#7FCFBD} }
</style>
"""
RODAPE = "</svg>\n"


def cabeca(nome, w, h, sw, op):
    return CABECA % (w, h, w, h, nome, nome, sw, op)


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


def epitrocoide(R, r, d, escala, cx, cy, passos=560, giro=0.0):
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
        pts.append((cx + xr * escala, cy + yr * escala))
    return pts


def marca_roseta(nome, R, r, d, n=7, base=0.86, passo=0.045, sw="1.6", op=".85",
                 caixa=QUADRADO):
    """Rosetas concêntricas — a marca clássica de apólice.

    Só serve em caixa quadrada: a roseta é radial, e numa faixa 16:5 ela sai
    cortada em cima e embaixo — foi o que motivou a família horizontal abaixo.
    """
    w, h = caixa
    partes = [cabeca(nome, w, h, sw, op)]
    raio = min(w, h) / 2.0
    for i in range(n):
        e = base - i * passo
        pts = epitrocoide(R, r, d, e * raio / (R + r + d), w / 2.0, h / 2.0,
                          giro=i * 0.16)
        partes.append('<path class="f" d="%s"/>\n' % caminho(pts))
    partes.append(RODAPE)
    return "".join(partes)


def marca_interferencia(nome, linhas=46, amp=.118, ciclos=2.4, torcao=1.7,
                        sw="1.5", op=".8", caixa=QUADRADO, passos=96):
    """Feixe de senoides com fase progressiva: a onda gravada.

    Tudo em fração da caixa, e é por isso que esta família atravessa formato:
    a onda é horizontal por natureza, então ela cresce para os lados sem
    perder o desenho. `amp` é fração da altura.
    """
    w, h = caixa
    partes = [cabeca(nome, w, h, sw, op)]
    for i in range(linhas):
        y0 = .09 * h + (.82 * h * i / (linhas - 1))
        fase = torcao * math.pi * i / linhas
        # o envelope não zera nas pontas: linha reta encostada na borda vira
        # um filete duplicado, que lê como engano em vez de gravura
        a = amp * h * (.16 + .84 * math.sin(math.pi * i / (linhas - 1)) ** 1.15)
        pts = []
        for j in range(passos + 1):
            x = .07 * w + (.86 * w * j / float(passos))
            t = 2 * math.pi * ciclos * (j / float(passos))
            pts.append((x, y0 + a * math.sin(t + fase)))
        partes.append('<path class="f" d="%s"/>\n' % caminho(pts))
    partes.append(RODAPE)
    return "".join(partes)


marcas = {
    # O CARTÃO e o ÍNDICE — quadrados, três caracteres distintos
    "guilhoche-1.svg": marca_roseta(u"Guilhoché — roseta", 7, 3, 5, n=6, passo=.058),
    "guilhoche-2.svg": marca_interferencia(u"Guilhoché — interferência"),
    "guilhoche-3.svg": marca_roseta(u"Guilhoché — estrela", 11, 4, 9, n=5, base=.92,
                                    passo=.072, sw="1.5", op=".82"),

    # A FAIXA do artigo — 16:5 nativo. Três variantes da mesma curva de
    # interferência, separadas por ciclo e torção: variante nova é parâmetro
    # novo, não arquivo novo (ESPEC §3).
    "faixa-1.svg": marca_interferencia(u"Guilhoché — faixa, onda longa",
                                       linhas=26, amp=.145, ciclos=1.7, torcao=1.3,
                                       sw="1.5", op=".8", caixa=FAIXA, passos=150),
    "faixa-2.svg": marca_interferencia(u"Guilhoché — faixa, interferência",
                                       linhas=34, amp=.115, ciclos=3.1, torcao=2.1,
                                       sw="1.4", op=".78", caixa=FAIXA, passos=150),
    "faixa-3.svg": marca_interferencia(u"Guilhoché — faixa, torção",
                                       linhas=22, amp=.165, ciclos=2.3, torcao=3.0,
                                       sw="1.6", op=".82", caixa=FAIXA, passos=150),
}

for nome, conteudo in marcas.items():
    p = os.path.join(SAIDA, nome)
    io.open(p, "w", encoding="utf-8", newline="\n").write(conteudo)
    print("  %-18s %6.1f KB" % (nome, os.path.getsize(p) / 1024.0))
