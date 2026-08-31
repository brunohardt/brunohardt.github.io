# -*- coding: utf-8 -*-
"""Cola um bloco de prova dentro de um escrito.

Do corpus da advocacia (tipo `ementa` ou `enunciado`, inferido pela classe):

    python _ferramentas/citar.py <escrito> <verbete>
    python _ferramentas/citar.py sumula-479 10-sumula-479-fortuito-interno
    python _ferramentas/citar.py sumula-479 10            # o prefixo basta

Ementa longa entra recortada, e o corte aparece. Primeiro se olha o que ha:

    python _ferramentas/citar.py sumula-479 29 --ver      # lista os trechos numerados
    python _ferramentas/citar.py sumula-479 29 --manter 0,6-8

Os trechos sao os itens numerados do proprio acordao -- a divisao e do
relator, nao minha. Cada corte vira [...] no texto colado, posto pelo script.

De uma consulta a fonte oficial (tipo `consulta`) — andamento de tema
repetitivo, texto de lei, enunciado que não está no corpus:

    python _ferramentas/citar.py <escrito> --consulta <arquivo> --url <URL> [--titulo "..."]
    python _ferramentas/citar.py tema-929 --consulta trecho.txt --url https://processo.stj.jus.br/...

O arquivo é lido verbatim e vai inteiro para o bloco: o trecho se copia da
página e se salva num arquivo, nunca se redigita na linha de comando.

Por que congelar em vez de referenciar: a fonte do escrito mora no repo do
site, e o corpus mora no repo da advocacia. Referência entre repositórios
quebra em silêncio — no dia em que o site publicar de outra máquina, ou de um
CI, o verbete simplesmente não está lá. Copiando o texto e o campo de
conferência para dentro do escrito, ele carrega a própria prova, e o
`montar.py` consegue recusar a publicação sozinho.

Extração programática nos três tipos, nunca redigitação — é a RED LINE 2 do
repositório da advocacia, aplicada ao que vai a público (ESPEC §2.2).
"""
import io, os, re, sys, datetime

CORPUS = r"C:\Users\Hardt\Dev\HARDT - ADVOCACIA\conhecimento\jurisprudencia"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # a ferramenta mora em _ferramentas/; a raiz e um andar acima
ESCRITOS = os.path.join(RAIZ, "_conteudo", "escritos")


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


def data_br(iso):
    p = (iso or u"").strip().split(u"-")
    return u"%s/%s/%s" % (p[2], p[1], p[0]) if len(p) == 3 else (iso or u"").strip()


def credito_do_verbete(campos, nome):
    """A linha que sai impressa embaixo da citacao.

    Ela e montada dos campos do proprio julgado -- tribunal, classe, numero,
    orgao e data --, e nunca do campo `fonte`. O `fonte` do corpus e nota de
    trabalho: guarda como a pesquisa comecou, e as vezes o caminho da pasta do
    caso, que nomeia cliente e parte contraria. Isso nao credita nada e nao
    pode ir a publico (ESPEC 2.2).

    O relator fica de fora de proposito: o credito existe para o leitor achar o
    julgado, e tribunal + classe + numero + orgao + data ja o acham. Nome de
    magistrado esta gravado no corpus sem acento em parte dos verbetes, e
    adivinhar acento de nome proprio e inventar.
    """
    trib = (campos.get("tribunal") or u"").strip()
    classe = (campos.get("classe") or u"").strip()
    numero = (campos.get("numero") or u"").strip()
    orgao = (campos.get("orgao") or u"").strip()
    jul = (campos.get("julgamento") or u"").strip()

    partes = []
    if trib:
        partes.append(trib)
    if classe and numero:
        # "Sumula 479" com numero "Sumula 479" nao vira "Sumula 479 n. Sumula 479"
        if numero in classe:
            partes.append(classe)
        elif classe in numero:
            partes.append(numero)
        else:
            partes.append(u"%s n. %s" % (classe, numero))
    elif classe or numero:
        partes.append(classe or numero)
    if orgao and not orgao.startswith(u"("):
        partes.append(orgao)
    if jul:
        partes.append(u"j. %s" % data_br(jul))

    credito = u", ".join(partes)
    if not credito or not trib:
        sys.exit(u"o verbete %s nao tem campos para um credito publicavel; "
                 u"faltam tribunal, classe, numero, orgao ou julgamento" % nome)
    return credito


# Ementa civel numera "1. ", "2. "; ementa penal costuma numerar "I - ", "II - "
# (as vezes com meia-risca). Nos dois casos a divisao e do relator, nao minha.
ITEM = re.compile(r"(?=\b\d{1,2}\.\s+[A-ZÀ-Ú])|(?=\b[IVX]{1,5}\s*[-–]\s+[A-ZÀ-Ú])")
CORTE = u"[…]"


def segmentar(ementa):
    """Quebra a ementa nos itens numerados do proprio acordao.

    Nao inventa divisao: usa a que o relator escreveu. Onde nao ha item
    numerado, a ementa e um bloco so, e ou entra inteira ou nao entra."""
    partes = [t.strip() for t in ITEM.split(ementa) if t.strip()]
    return partes or [ementa.strip()]


def recortar(partes, manter):
    """Junta so os trechos pedidos, marcando cada corte com [...].

    O texto nunca e redigitado: cada pedaco sai do proprio arquivo. O que a
    marca promete e simples -- entre um trecho e o seguinte havia mais ementa,
    e voce esta vendo um recorte, nao o acordao inteiro."""
    fora = [i for i in manter if i < 0 or i >= len(partes)]
    if fora:
        sys.exit(u"trecho inexistente: %s (a ementa tem %d)"
                 % (u", ".join(str(i) for i in fora), len(partes)))
    manter = sorted(set(manter))
    saida = []
    if manter[0] > 0:
        saida.append(CORTE)
    anterior = None
    for i in manter:
        if anterior is not None and i > anterior + 1:
            saida.append(CORTE)
        saida.append(partes[i])
        anterior = i
    if manter[-1] < len(partes) - 1:
        saida.append(CORTE)
    return u" ".join(saida)


def ler_intervalos(spec):
    """'0,3-5,9' -> [0, 3, 4, 5, 9]"""
    numeros = []
    for pedaco in spec.split(u","):
        pedaco = pedaco.strip()
        if not pedaco:
            continue
        if u"-" in pedaco:
            a, b = pedaco.split(u"-", 1)
            numeros.extend(range(int(a), int(b) + 1))
        else:
            numeros.append(int(pedaco))
    return numeros


def inferir_tipo(campos, vid):
    """Súmula e enunciado não têm inteiro teor a conferir: o enunciado é o
    próprio texto. O resto é ementa de acórdão."""
    classe = (campos.get("classe") or u"").strip().lower()
    if classe.startswith(u"súmula") or classe.startswith(u"sumula") \
            or classe.startswith(u"enunciado"):
        return u"enunciado"
    if re.match(r"^\d+-(sumula|enunciado)", vid):
        return u"enunciado"
    return u"ementa"


def colar(alvo, escrito, vid, linhas, corpo):
    texto = ler(alvo)
    if (u":::verbete %s\n" % vid) in texto:
        sys.exit(u"o escrito ja cita %s — nada a fazer" % vid)
    bloco = u"\n:::verbete %s\n%s---\n%s\n:::\n" % (
        vid, u"".join(u"%s: %s\n" % (k, v) for k, v in linhas), corpo)
    io.open(alvo, "a", encoding="utf-8", newline="\n").write(bloco)
    print(u"  bloco %s colado em %s" % (vid, escrito))
    for k, v in linhas:
        print(u"  %s: %s" % (k, v))


def do_corpus(alvo, escrito, chave, ver=False, manter=None):
    nome = achar_verbete(chave)
    campos, ementa = extrair(ler(os.path.join(CORPUS, nome)))
    vid = nome[:-3]
    partes = segmentar(ementa)

    if ver:
        print(u"%s  --  %d trecho(s), %d palavras" % (vid, len(partes), len(ementa.split())))
        for i, t in enumerate(partes):
            uma_linha = u" ".join(t.split())
            print(u"  [%2d] %4d p.  %s%s" % (i, len(t.split()), uma_linha[:96],
                                             u"..." if len(uma_linha) > 96 else u""))
        print(u"\n  para colar um recorte:  python _ferramentas/citar.py %s %s --manter 0,3-5" % (escrito, chave))
        return

    tipo = inferir_tipo(campos, vid)
    conferido = str(campos.get("inteiro_teor_conferido", "nao")).strip().lower()
    credito = credito_do_verbete(campos, nome)

    linhas = [(u"tipo", tipo), (u"credito", credito)]
    if manter:
        corpo = recortar(partes, manter)
        linhas.append((u"recorte", u"sim"))
    else:
        corpo = ementa
    linhas.append((u"inteiro_teor_conferido", conferido))

    colar(alvo, escrito, vid, linhas, corpo)

    if conferido != u"sim":
        print(u"\n  ATENCAO: a montagem vai RECUSAR publicar este escrito enquanto\n"
              u"  este verbete nao for conferido. E a conferencia no primeiro uso\n"
              u"  (ESPEC 2.2): abra o julgado na pagina de jurisprudencia do\n"
              u"  JusBrasil -- a base, nao a resposta da Jus IA -- confira numero,\n"
              u"  orgao, relator e datas, e mude o campo no verbete de origem\n"
              u"  (%s) e aqui." % os.path.join(CORPUS, nome))


def do_consulta(alvo, escrito, args):
    """Consulta a fonte oficial. Aqui o Bruno esteve na fonte ele mesmo — não
    há intermediário para conferir depois, então o bloco já nasce conferido."""
    arquivo = args.get("--consulta")
    url = args.get("--url")
    if not arquivo or not url:
        sys.exit(u"--consulta exige o arquivo do trecho e --url da pagina")
    if not os.path.isfile(arquivo):
        sys.exit(u"arquivo do trecho nao encontrado: %s" % arquivo)
    trecho = ler(arquivo).strip()
    if not trecho:
        sys.exit(u"o arquivo do trecho esta vazio: %s" % arquivo)

    vid = args.get("--id") or re.sub(r"[^a-z0-9]+", "-",
                                     os.path.splitext(os.path.basename(arquivo))[0].lower()).strip("-")
    titulo = args.get("--titulo") or url
    hoje = datetime.date.today().isoformat()

    colar(alvo, escrito, vid, [(u"tipo", u"consulta"),
                               (u"credito", titulo),
                               (u"url", url),
                               (u"acesso", hoje),
                               (u"inteiro_teor_conferido", u"sim")], trecho)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    escrito = sys.argv[1]
    alvo = os.path.join(ESCRITOS, escrito if escrito.endswith(".md") else escrito + ".md")
    if not os.path.isfile(alvo):
        sys.exit(u"escrito nao encontrado: %s" % alvo)

    resto = sys.argv[2:]
    if not resto[0].startswith("--"):
        chave = resto[0]
        flags = {}
        i = 1
        while i < len(resto):
            if resto[i] == u"--ver":
                flags["ver"] = True
                i += 1
            elif resto[i] == u"--manter" and i + 1 < len(resto):
                flags["manter"] = ler_intervalos(resto[i + 1])
                i += 2
            else:
                sys.exit(u"argumento solto: %s" % resto[i])
        do_corpus(alvo, escrito, chave, **flags)
        return

    if resto[0].startswith("--"):
        args = {}
        i = 0
        while i < len(resto):
            if not resto[i].startswith("--") or i + 1 >= len(resto):
                sys.exit(u"argumento solto: %s" % resto[i])
            args[resto[i]] = resto[i + 1]
            i += 2
        do_consulta(alvo, escrito, args)


if __name__ == "__main__":
    main()
