# -*- coding: utf-8 -*-
"""Cola um bloco de prova dentro de um escrito.

Do corpus da advocacia (tipo `ementa` ou `enunciado`, inferido pela classe):

    python citar.py <escrito> <verbete>
    python citar.py sumula-479 10-sumula-479-fortuito-interno
    python citar.py sumula-479 10            # o prefixo basta

De uma consulta a fonte oficial (tipo `consulta`) — andamento de tema
repetitivo, texto de lei, enunciado que não está no corpus:

    python citar.py <escrito> --consulta <arquivo> --url <URL> [--titulo "..."]
    python citar.py tema-929 --consulta trecho.txt --url https://processo.stj.jus.br/...

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


def do_corpus(alvo, escrito, chave):
    nome = achar_verbete(chave)
    campos, ementa = extrair(ler(os.path.join(CORPUS, nome)))
    vid = nome[:-3]
    tipo = inferir_tipo(campos, vid)
    conferido = str(campos.get("inteiro_teor_conferido", "nao")).strip().lower()
    fonte = campos.get("fonte") or campos.get("origem") or campos.get("tribunal") or vid

    colar(alvo, escrito, vid, [(u"tipo", tipo),
                               (u"fonte", fonte),
                               (u"inteiro_teor_conferido", conferido)], ementa)

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
                               (u"fonte", titulo),
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
    if resto[0].startswith("--"):
        args = {}
        i = 0
        while i < len(resto):
            if not resto[i].startswith("--") or i + 1 >= len(resto):
                sys.exit(u"argumento solto: %s" % resto[i])
            args[resto[i]] = resto[i + 1]
            i += 2
        do_consulta(alvo, escrito, args)
    else:
        do_corpus(alvo, escrito, resto[0])


if __name__ == "__main__":
    main()
