# -*- coding: utf-8 -*-
"""Puxa um verbete do corpus da advocacia e congela dentro de um escrito.

    python citar.py <escrito> <verbete>
    python citar.py sumula-479 01-sumula-479-fortuito-interno
    python citar.py sumula-479 01            # o prefixo basta

Por que congelar em vez de referenciar: a fonte do escrito mora no repo do
site, e o corpus mora no repo da advocacia. Referência entre repositórios
quebra em silêncio — no dia em que o site publicar de outra máquina, ou de um
CI, o verbete simplesmente não está lá. Copiando a ementa e o campo de
conferência para dentro do escrito, o texto carrega a própria prova, e o
`montar.py` consegue recusar a publicação sozinho.

A ementa é copiada por extração programática, nunca redigitada — é a RED LINE 2
do repositório da advocacia, aplicada ao que vai a público.
"""
import io, os, re, sys

CORPUS = r"C:\Users\Hardt\Dev\HARDT - ADVOCACIA\conhecimento\jurisprudencia"
ESCRITOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_conteudo", "escritos")


def ler(p):
    return io.open(p, encoding="utf-8", newline="\n").read()


def achar_verbete(chave):
    if not os.path.isdir(CORPUS):
        sys.exit(u"corpus nao encontrado em %s\n"
                 u"(o repo da advocacia precisa estar clonado nesse caminho)" % CORPUS)
    achados = [f for f in sorted(os.listdir(CORPUS))
               if f.endswith(".md") and f[:-3].startswith(chave)]
    if not achados:
        achados = [f for f in sorted(os.listdir(CORPUS))
                   if f.endswith(".md") and chave.lower() in f.lower()]
    if not achados:
        sys.exit(u"nenhum verbete casa com '%s'" % chave)
    if len(achados) > 1:
        sys.exit(u"'%s' casa com %d verbetes:\n  %s" % (chave, len(achados),
                 u"\n  ".join(a[:-3] for a in achados)))
    return achados[0]


def extrair(texto):
    """Devolve (campos, ementa). A ementa e o bloco entre os marcadores
    LITERAL_BEGIN/END; se nao houver, cai para a primeira citacao em bloco."""
    campos = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", texto, re.S)
    if m:
        for linha in m.group(1).split(u"\n"):
            if u":" in linha:
                k, v = linha.split(u":", 1)
                campos[k.strip()] = v.strip().strip('"')
    # O corpus da advocacia marca a ementa com <!--EMENTA_BEGIN--> / <!--EMENTA_END-->.
    # LITERAL_* fica como alternativa: é o marcador que o resto daquele
    # repositório usa nas citações de peça.
    for ini, fim in (("<!--EMENTA_BEGIN-->", "<!--EMENTA_END-->"),
                     ("LITERAL_BEGIN", "LITERAL_END")):
        lit = re.search(re.escape(ini) + r"\s*\n(.*?)\n\s*" + re.escape(fim), texto, re.S)
        if lit:
            bruto = lit.group(1).strip()
            # a ementa costuma vir como citação em bloco; tira o "> " de cada linha
            if all(l.startswith(">") or not l.strip() for l in bruto.split("\n")):
                bruto = "\n".join(re.sub(r"^>\s?", "", l) for l in bruto.split("\n")).strip()
            return campos, bruto
    bloco = re.findall(r"(?:^>.*\n?)+", texto, re.M)
    if bloco:
        maior = max(bloco, key=len)
        return campos, u"\n".join(re.sub(r"^>\s?", "", l) for l in maior.split(u"\n")).strip()
    sys.exit(u"nao achei ementa literal no verbete (sem LITERAL_BEGIN/END nem citacao em bloco)")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    escrito, chave = sys.argv[1], sys.argv[2]
    alvo = os.path.join(ESCRITOS, escrito if escrito.endswith(".md") else escrito + ".md")
    if not os.path.isfile(alvo):
        sys.exit(u"escrito nao encontrado: %s" % alvo)

    nome = achar_verbete(chave)
    campos, ementa = extrair(ler(os.path.join(CORPUS, nome)))
    vid = nome[:-3]
    conferido = str(campos.get("inteiro_teor_conferido", "nao")).strip().lower()
    fonte = campos.get("fonte") or campos.get("origem") or campos.get("tribunal") or vid

    bloco = (u"\n:::verbete %s\n"
             u"fonte: %s\n"
             u"inteiro_teor_conferido: %s\n"
             u"---\n%s\n:::\n") % (vid, fonte, conferido, ementa)

    texto = ler(alvo)
    if (u":::verbete %s\n" % vid) in texto:
        sys.exit(u"o escrito ja cita %s — nada a fazer" % vid)
    io.open(alvo, "a", encoding="utf-8", newline="\n").write(bloco)

    print(u"  verbete %s colado em %s" % (vid, escrito))
    print(u"  fonte: %s" % fonte)
    print(u"  inteiro_teor_conferido: %s%s" % (
        conferido,
        u"" if conferido == "sim" else
        u"\n\n  ATENCAO: a montagem vai RECUSAR publicar este escrito enquanto o\n"
        u"  inteiro teor nao for conferido na fonte. Abra o acordao no site do\n"
        u"  tribunal, confira, e mude o campo no verbete de origem e aqui."))


if __name__ == "__main__":
    main()
