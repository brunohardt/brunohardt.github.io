# -*- coding: utf-8 -*-
"""Verificador do site.

    python verificar.py

A ESPEC não é boa intenção: as regras dela viram teste aqui, e teste que falha
derruba a publicação. O ciclo da §6 é emendar a espec, escrever a verificação,
implementar, provar.

São oito checagens (ESPEC §6). Cinco leem os arquivos; três precisam de
navegador e rodam com Playwright, porque contraste, movimento e estouro só
existem depois que o CSS foi aplicado.

REQUISITO: playwright (`pip install -r requirements.txt` e `playwright install`).
"""
import io, os, re, sys, glob

# O console do Windows abre em cp1252 e transforma "léxico" em "l?xico". O
# relatório é para ser lido.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

RAIZ = os.path.dirname(os.path.abspath(__file__))
ESCRITOS_MD = os.path.join(RAIZ, "_conteudo", "escritos")
ESTILO = os.path.join(RAIZ, "ativos", "estilo")

# As páginas geradas que se verifica. Descobertas, não listadas: página nova
# não toca no verificador, pela mesma razão que não toca no montador.
def paginas_geradas():
    saida = [p for p in sorted(glob.glob(os.path.join(RAIZ, "*.html")))]
    saida += sorted(glob.glob(os.path.join(RAIZ, "escritos", "*.html")))
    return saida


def ler(p):
    return io.open(p, encoding="utf-8", newline="\n").read()


def rel(p):
    return os.path.relpath(p, RAIZ).replace("\\", "/")


# ====================================================== 1. léxico regulatório
#
# O Provimento 205 proíbe a captação, não o assunto. A carteira do autor é
# consumidor bancário: "desconto", "cobrança" e "resultado" são o objeto dos
# escritos, e proibir a palavra solta encheria o verificador de falso positivo
# até alguém desligá-lo. Por isso os padrões são de FRASE, e miram a voz do
# site oferecendo serviço — nunca o vocabulário da matéria.
LEXICO = [
    (u"honorário na voz do site",
     r"\b(meus|nossos|os)\s+honor[áa]rios\b|\bhonor[áa]rios\s+a\s+combinar\b"),
    (u"forma de pagamento",
     r"\bforma[s]?\s+de\s+pagamento\b|\bparcelamos\b|\baceitamos\s+cart[ãa]o\b"),
    (u"consulta grátis",
     r"\b(primeira\s+)?consulta\s+(gr[áa]tis|gratuita|sem\s+compromisso)\b"),
    (u"orçamento",
     r"\bor[çc]amento\s+(gr[áa]tis|gratuito|sem\s+compromisso)\b"),
    (u"superlativo",
     r"\bo\s+melhor\s+(advogado|escrit[óo]rio)\b|\bmelhor[es]?\s+advogado[s]?\s+d[eoa]\b"
     r"|\bl[íi]der\s+em\b|\bexcel[êe]ncia\s+em\b|\breferência\s+em\b"),
    (u"especialista sem título",
     r"\bespecialista\s+em\b"),
    (u"depoimento ou resultado de cliente",
     r"\bdepoimento[s]?\s+de\s+cliente|\bo\s+que\s+dizem\s+(os\s+)?(nossos\s+)?clientes\b"
     r"\b|\bcaso[s]?\s+de\s+sucesso\b|\b[êe]xito[s]?\s+obtido[s]?\b"),
    (u"comparação com colega",
     r"\bdiferente\s+d[eo]s\s+(outros\s+)?(advogados|escrit[óo]rios)\b"
     r"|\bao\s+contr[áa]rio\s+d[eo]s\s+(outros\s+)?(advogados|escrit[óo]rios)\b"),
    (u"captação ativa",
     r"<form\b|\btype=[\"']hidden[\"'][^>]*campanha|\bfale\s+conosco\b"
     r"|\bagende\s+(sua\s+)?(consulta|hor[áa]rio)\b|\bsolicite\s+(um\s+)?or[çc]amento\b"),
    (u"símbolo da OAB",
     r"<img[^>]+(oab|brasao)[^>]*>"),
]

TAG = re.compile(r"<[^>]+>")
VERBETE_HTML = re.compile(r'<figure class="verbete".*?</figure>', re.S)
SCRIPT = re.compile(r"<script\b.*?</script>", re.S)


def texto_da_voz_do_site(html):
    """O HTML sem o que não é voz do site.

    Os blocos de prova saem antes de tudo: ementa fala de honorário
    sucumbencial, de êxito e de resultado o tempo todo, e o autor não responde
    pelo vocabulário de um desembargador. O JSON-LD sai porque é dado, não
    prosa."""
    html = VERBETE_HTML.sub(u" ", html)
    html = SCRIPT.sub(u" ", html)
    return re.sub(r"\s+", u" ", TAG.sub(u" ", html))


def checar_lexico(paginas):
    ruins = []
    for p in paginas:
        alvo = texto_da_voz_do_site(ler(p))
        bruto = ler(p)
        for rotulo, padrao in LEXICO:
            # os padrões de marcação (form, img) valem no HTML cru; os de prosa,
            # no texto limpo
            onde = bruto if padrao.startswith("<") or "<form" in padrao else alvo
            m = re.search(padrao, onde, re.I)
            if m:
                ruins.append(u"%s: %s — %r" % (rel(p), rotulo, m.group(0)[:60]))
    return ruins


# ============================================================ 2. prova (§2.2)
CAB = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
VERBETE = re.compile(
    r"^:::verbete[ \t]+(?P<id>[\w\-]+)[ \t]*\n(?P<meta>.*?)\n---[ \t]*\n(?P<corpo>.*?)\n:::[ \t]*$",
    re.S | re.M)
TIPOS = (u"ementa", u"enunciado", u"consulta")


def campos(bloco):
    meta = {}
    for linha in bloco.split(u"\n"):
        if u":" in linha:
            k, v = linha.split(u":", 1)
            meta[k.strip()] = v.strip()
    return meta


def checar_prova():
    ruins = []
    for caminho in sorted(glob.glob(os.path.join(ESCRITOS_MD, "*.md"))):
        nome = os.path.basename(caminho)
        bruto = ler(caminho)
        m = CAB.match(bruto)
        meta = campos(m.group(1)) if m else {}
        rascunho = meta.get("rascunho", u"nao").lower() == u"sim"
        blocos = list(VERBETE.finditer(bruto))

        if not blocos:
            ruins.append(u"%s: nenhum bloco de prova — todo escrito carrega "
                         u"prova dentro de si (ESPEC §2.2)" % nome)
            continue

        for b in blocos:
            vm = campos(b.group("meta"))
            vid = b.group("id")
            tipo = vm.get("tipo", u"").strip().lower()
            if tipo not in TIPOS:
                ruins.append(u"%s: verbete %s sem 'tipo' válido (%s)"
                             % (nome, vid, u" | ".join(TIPOS)))
            if tipo == u"consulta":
                for exigido in (u"url", u"acesso"):
                    if not vm.get(exigido):
                        ruins.append(u"%s: verbete %s é consulta e não tem '%s'"
                                     % (nome, vid, exigido))
            if not rascunho and vm.get("inteiro_teor_conferido", u"nao").lower() != u"sim":
                ruins.append(u"%s: cita o verbete %s sem conferência no primeiro uso"
                             % (nome, vid))
            if not b.group("corpo").strip():
                ruins.append(u"%s: verbete %s com corpo vazio" % (nome, vid))
    return ruins


# ======================================================== 3. rascunho vazado
#
# `rascunho: sim` não impedia publicação: o montador gerava a página, punha o
# cartão na capa e no índice, e só imprimia [RASCUNHO] no console. Um merge
# publicaria texto não assumido sob o nome e a OAB do autor. Agora é teste.
def checar_rascunho(paginas):
    ruins = []
    rascunhos = []
    for caminho in sorted(glob.glob(os.path.join(ESCRITOS_MD, "*.md"))):
        m = CAB.match(ler(caminho))
        if m and campos(m.group(1)).get("rascunho", u"nao").lower() == u"sim":
            rascunhos.append(os.path.basename(caminho)[:-3])

    for slug in rascunhos:
        alvo = os.path.join(RAIZ, "escritos", slug + ".html")
        if os.path.exists(alvo):
            ruins.append(u"escritos/%s.html existe e o escrito está como "
                         u"rascunho: sim" % slug)
        for p in paginas:
            if os.path.basename(p) == slug + ".html":
                continue
            if re.search(r'href="[^"]*escritos/%s\.html"' % re.escape(slug), ler(p)):
                ruins.append(u"%s aponta para o rascunho %s" % (rel(p), slug))

    for p in paginas:
        if re.search(r"\bRASCUNHO\b", ler(p)):
            ruins.append(u"%s: marcador RASCUNHO vazou para arquivo gerado" % rel(p))
    return ruins


# =========================================================== 4. estrutura
CABECALHO = re.compile(r"<h([1-6])\b", re.I)


def checar_estrutura(paginas):
    ruins = []
    for p in paginas:
        niveis = [int(n) for n in CABECALHO.findall(ler(p))]
        if niveis.count(1) != 1:
            ruins.append(u"%s: %d elementos h1 (deve haver exatamente um)"
                         % (rel(p), niveis.count(1)))
        anterior = 0
        for n in niveis:
            if anterior and n > anterior + 1:
                ruins.append(u"%s: ordem de títulos quebrada — h%d depois de h%d"
                             % (rel(p), n, anterior))
                break
            anterior = n
    return ruins


# =============================================================== 5. links
HREF = re.compile(r'(?:href|src)="([^"]+)"')


def ancoras(caminho):
    return set(re.findall(r'\bid="([^"]+)"', ler(caminho)))


def checar_links(paginas):
    """Arquivo E fragmento. Só o arquivo não basta: um botão apontando para
    `escritos.html#buscar` passa no teste de arquivo e leva a lugar nenhum."""
    ruins = []
    for p in paginas:
        base = os.path.dirname(p)
        for alvo in HREF.findall(ler(p)):
            if re.match(r"^(https?:|mailto:|tel:|data:)", alvo):
                continue
            arquivo, _, frag = alvo.partition("#")
            destino = p if not arquivo else os.path.normpath(os.path.join(base, arquivo))
            if not os.path.exists(destino):
                ruins.append(u"%s: aponta para %s, que não existe" % (rel(p), alvo))
                continue
            if frag and destino.endswith(".html") and frag not in ancoras(destino):
                ruins.append(u"%s: aponta para %s, e a âncora #%s não existe em %s"
                             % (rel(p), alvo, frag, rel(destino)))
    return ruins


# ================================================= 6, 7, 8. com navegador
#
# Contraste, movimento e estouro só existem depois do CSS aplicado. Grep em
# folha de estilo não vê cascata, não vê herança de fundo e não vê estilo
# em linha — por isso a §2.3 assume o navegador como dependência.
JS_CONTRASTE = u"""() => {
  const lum = (c) => {
    const [r, g, b] = c.map(v => {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const rgb = (s) => {
    const m = s.match(/rgba?\\(([^)]+)\\)/);
    if (!m) return null;
    const p = m[1].split(',').map(x => parseFloat(x));
    return { c: p.slice(0, 3), a: p.length > 3 ? p[3] : 1 };
  };
  const fundoDe = (el) => {
    for (let n = el; n && n !== document.documentElement.parentNode; n = n.parentElement) {
      const f = rgb(getComputedStyle(n).backgroundColor);
      if (f && f.a > 0.99) return f.c;
    }
    const f = rgb(getComputedStyle(document.documentElement).backgroundColor);
    return f ? f.c : [255, 255, 255];
  };
  const ruins = [];
  for (const el of document.querySelectorAll('body *')) {
    const texto = Array.from(el.childNodes)
      .filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join('');
    if (!texto) continue;
    const s = getComputedStyle(el);
    if (s.visibility === 'hidden' || s.display === 'none' || parseFloat(s.opacity) < 0.05) continue;
    const frente = rgb(s.color);
    if (!frente) continue;
    const l1 = lum(frente.c), l2 = lum(fundoDe(el));
    const razao = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    const px = parseFloat(s.fontSize);
    const peso = parseInt(s.fontWeight, 10) || 400;
    const grande = px >= 24 || (px >= 18.66 && peso >= 700);
    const minimo = grande ? 3 : 4.5;
    if (razao < minimo) {
      ruins.push(el.tagName.toLowerCase() + ' "' + texto.slice(0, 40) + '" '
                 + razao.toFixed(2) + ':1 (minimo ' + minimo + ')');
    }
  }
  return ruins;
}"""

# A regra é sobre MOVIMENTO, não sobre mudança. Transição de cor em link não
# desloca nada e não incomoda quem pede redução; travar isso encheria o
# verificador do falso positivo que faz alguém desligá-lo. Vale `animation`,
# e vale transição das propriedades que deslocam ou redimensionam.
JS_MOVIMENTO = u"""() => {
  const MOVE = /transform|translate|scale|rotate|\\btop\\b|\\bleft\\b|\\bright\\b|\\bbottom\\b|margin|width|height/;
  const ruins = [];
  for (const el of document.querySelectorAll('*')) {
    const s = getComputedStyle(el);
    const nome = el.tagName.toLowerCase()
               + (el.className ? '.' + String(el.className).split(' ')[0] : '');
    if (s.animationName && s.animationName !== 'none') {
      ruins.push(nome + ' anima com ' + s.animationName);
    }
    if (parseFloat(s.transitionDuration) > 0.05 && MOVE.test(s.transitionProperty)) {
      ruins.push(nome + ' transiciona ' + s.transitionProperty);
    }
  }
  return ruins.slice(0, 8);
}"""

LARGURAS = (320, 375, 768, 1024, 1440, 1600)


def checar_no_navegador(paginas):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return [u"playwright ausente: pip install -r requirements.txt "
                u"&& playwright install"]

    ruins = []
    with sync_playwright() as pw:
        navegador = pw.chromium.launch()
        for p in paginas:
            url = "file:///" + p.replace("\\", "/")

            # 6. contraste AA, os dois temas testados separadamente
            for tema in ("light", "dark"):
                pag = navegador.new_page(color_scheme=tema, viewport={"width": 1280, "height": 900})
                pag.goto(url)
                for achado in pag.evaluate(JS_CONTRASTE):
                    ruins.append(u"%s [%s]: contraste %s" % (rel(p), tema, achado))
                pag.close()

            # 7. movimento: quem pede redução recebe a página pronta
            pag = navegador.new_page(reduced_motion="reduce")
            pag.goto(url)
            for achado in pag.evaluate(JS_MOVIMENTO):
                ruins.append(u"%s: movimento sob prefers-reduced-motion — %s"
                             % (rel(p), achado))
            pag.close()

            # 8. estouro horizontal
            pag = navegador.new_page()
            pag.goto(url)
            for largura in LARGURAS:
                pag.set_viewport_size({"width": largura, "height": 900})
                estourou = pag.evaluate(
                    "() => document.documentElement.scrollWidth "
                    "- document.documentElement.clientWidth")
                if estourou > 1:
                    ruins.append(u"%s: estouro horizontal de %dpx em %dpx de largura"
                                 % (rel(p), estourou, largura))
            pag.close()
        navegador.close()
    return ruins


# ================================================================== main
CHECAGENS = (
    (u"léxico regulatório", lambda pgs: checar_lexico(pgs)),
    (u"prova", lambda pgs: checar_prova()),
    (u"rascunho", lambda pgs: checar_rascunho(pgs)),
    (u"estrutura", lambda pgs: checar_estrutura(pgs)),
    (u"links", lambda pgs: checar_links(pgs)),
    (u"navegador", lambda pgs: checar_no_navegador(pgs)),
)


def main():
    pgs = paginas_geradas()
    if not pgs:
        sys.exit(u"nao ha pagina gerada: rode `python montar.py` antes")

    total = 0
    for nome, fn in CHECAGENS:
        ruins = fn(pgs)
        total += len(ruins)
        print(u"  %-22s %s" % (nome, u"ok" if not ruins else u"%d problema(s)" % len(ruins)))
        for r in ruins:
            print(u"      - %s" % r)

    if total:
        print(u"\n  A VERIFICACAO RECUSA PUBLICAR: %d problema(s)." % total)
        sys.exit(1)
    print(u"\n  %d pagina(s), tudo verificado." % len(pgs))


if __name__ == "__main__":
    main()
