# -*- coding: utf-8 -*-
"""Recebe a arte gerada e produz os dois arquivos que o site usa.

    python _ferramentas/receber.py <motivo> <arquivo-deitada> <arquivo-em-pe>
    python _ferramentas/receber.py vidro "C:\\Users\\Hardt\\Downloads\\a.jpg" "...\\b.jpg"

A foto e o unico insumo do site que vem de fora - de um gerador, pelo prompt de
_doc/PROMPTS.md. Ela chega grande: 2 a 4 MB, no tamanho que o gerador entrega. A
lamina da capa e o LCP da pagina, e 3 MB de LCP e uma capa que nao pinta em rede
ruim, que e onde a maior parte da audiencia esta.

Encolher a mao seria mais um passo manual que nada executa e nada documenta. Este
script existe para que a recepcao seja reprodutivel, como e o resto: a montagem
monta e verifica, o og.py fotografa, e este recebe.

O QUE ELE FAZ, e por que:

  - **Redimensiona em tres.** A deitada vira `-media` (1200px) e `-larga`
    (2400px), que sao os dois candidatos do `srcset` da lamina; a `-media`
    sozinha atende a faixa do artigo e o cartao da grade. A em pe vira `-alta`
    (1800px), que NAO e servida a ninguem: so o og.py a usa, para fotografar a
    chapa de feed a 1080x1350.
  - **Recomprime em JPEG progressivo.** Progressivo porque a lamina sangra a tela
    inteira: melhor a foto aparecer inteira e grosseira e depois afinar do que
    descer por uma tarja.
  - **Apaga o metadado.** O que sai do gerador carrega EXIF que nao diz nada e
    ocupa espaco; e o que sai de camera carrega data e as vezes coordenada.
    Publicar coordenada por descuido e o tipo de vazamento que nao da sintoma.
  - **Nao recorta e nao clareia.** Enquadramento e luz sao decisao do prompt. Se
    a foto voltou errada, quem se corrige e o prompt - imagem retocada a mao nao
    se reproduz na proxima.

Depois de rodar, `python _ferramentas/montar.py` mede o resultado e recusa o que nao servir.
"""
import io, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # a ferramenta mora em _ferramentas/; a raiz e um andar acima
IMG = os.path.join(RAIZ, "ativos", "img")

# TRES arquivos por motivo, e cada um serve um trabalho:
#
#   -media  1200px  o que o telefone baixa, e o que a faixa do artigo e o cartao
#                   usam sempre. A maior parte da audiencia vem do Instagram, no
#                   telefone: mandar 2400px para pintar uma faixa de 390 CSS px
#                   e o desperdicio que espremer qualidade nao conserta.
#   -larga  2400px  o candidato grande do srcset da lamina, para tela larga em
#                   retina, e a fonte do og.py.
#   -alta   1800px  em pe, NAO servida: so o og.py a usa, para fotografar a
#                   chapa de feed. Teto de higiene de repositorio, nao de rede.
#
# A qualidade NAO e fixa, e o teto e que manda. Textura fina - as bordas de papel
# sao milhares de linhas paralelas, a ardosia e grao mineral de ponta a ponta - e
# o pior caso do JPEG e custa o dobro de uma foto lisa no mesmo tamanho. Fixar a
# qualidade faria o peso variar com o assunto; fixar o teto faz variar a
# qualidade, que e o lado certo para variar.
EIXOS = {
    "media": dict(largura=1200, teto_kb=190, de="deitada"),
    "larga": dict(largura=2400, teto_kb=640, de="deitada"),
    "alta":  dict(largura=1800, teto_kb=900, de="em_pe"),
}
# Abaixo de 64 o artefato aparece na area lisa, que e justamente a metade escura
# onde o titulo vai. Foto que so cabe no orcamento abaixo disso e foto errada
# para o lugar, e quem se corrige e o prompt.
QUALIDADES = (86, 82, 78, 74, 70, 66, 64)


def receber(motivo, caminho, eixo):
    from PIL import Image

    regra = EIXOS[eixo]
    im = Image.open(caminho)
    larg, alt = im.size
    if regra["de"] == "deitada" and larg <= alt:
        sys.exit(u"%s: e para ser deitada e veio %dx%d" % (caminho, larg, alt))
    if regra["de"] == "em_pe" and alt <= larg:
        sys.exit(u"%s: e para ser em pe e veio %dx%d" % (caminho, larg, alt))

    im = im.convert("RGB")
    if larg > regra["largura"]:
        nova = (regra["largura"],
                int(round(alt * regra["largura"] / float(larg))))
        im = im.resize(nova, Image.LANCZOS)

    destino = os.path.join(IMG, "%s-%s.jpg" % (motivo, eixo))
    for q in QUALIDADES:
        buf = io.BytesIO()
        # sem `exif=` e sem `icc_profile=`: o metadado nao viaja
        im.save(buf, "JPEG", quality=q, optimize=True, progressive=True,
                subsampling=1)
        kb = buf.tell() / 1024.0
        if kb <= regra["teto_kb"]:
            break
    io.open(destino, "wb").write(buf.getvalue())

    aviso = u"" if kb <= regra["teto_kb"] else (
        u"   ACIMA DO TETO de %d KB mesmo em q%d" % (regra["teto_kb"], q))
    print(u"  %-22s %5dx%-5d %7.0f KB  q%d   (de %.1f MB)%s"
          % (os.path.basename(destino), im.size[0], im.size[1], kb, q,
             os.path.getsize(caminho) / 1048576.0, aviso))
    return kb <= regra["teto_kb"]


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__.split(u"\n\n")[1].strip())
    motivo, deitada, em_pe = sys.argv[1], sys.argv[2], sys.argv[3]
    for c in (deitada, em_pe):
        if not os.path.isfile(c):
            sys.exit(u"nao achei: %s" % c)
    try:
        import PIL  # noqa: F401
    except ImportError:
        sys.exit(u"Pillow ausente: pip install -r _ferramentas/requirements.txt")

    if not os.path.isdir(IMG):
        os.makedirs(IMG)
    ok = True
    for eixo, regra in sorted(EIXOS.items()):
        origem = deitada if regra["de"] == "deitada" else em_pe
        ok = receber(motivo, origem, eixo) and ok
    print(u"\n  %s recebido. Rode `python _ferramentas/og.py` e depois `python _ferramentas/montar.py`."
          % motivo)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
