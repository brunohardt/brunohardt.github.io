# Handoff — site brunohardt

**Atualizado em 30/08/2026, depois da sessão de grill e da implementação.**
Para retomar numa sessão nova, ou para o Bruno tocar sozinho.

Repositório: `C:\Users\Hardt\Dev\site-bruno-hardt`

**Onde o trabalho vive:** branch **`periodico`**, oito commits, de `c172513` a
`72e46d3`. A `main` continua em `52b205a`, servindo o site antigo — e é de lá
que o GitHub Pages publica. **O merge é o ato de estrear**, nunca efeito
colateral de um push.

No ar hoje: <https://brunohardt.github.io/> — ainda a versão antiga.

**A fonte da verdade é a [`ESPEC.md`](ESPEC.md).** Este handoff é o mapa; ela é
a lei. Toda mudança de comportamento começa emendando-a.

---

## 1. Estado

Código: **completo**. `python montar.py` monta e verifica num comando só, e
falha se qualquer das nove checagens reprovar.

O verificador está em **11 reprovações, todas presas à redação**:

| | |
|---|---|
| 9 de rascunho | os três escritos estão `rascunho: sim`, e o verificador recusa página gerada, link na capa e link no índice para texto não assumido |
| 2 de prova | `telas-sistemicas` e `tema-929` não citam nada, e todo escrito precisa carregar prova (§2.2) |

As duas listas fecham com o mesmo trabalho: o Bruno ler, alongar, conferir os
verbetes e assumir a autoria.

---

## 2. As decisões, e por que elas são assim

Saíram das sessões de grill de 30/08. Não reabrir sem motivo novo.

| Decisão | Ficou | Por quê |
|---|---|---|
| Formato | periódico, não cartão de visita | a autoridade de advogado novo vem do que ele demonstra saber |
| Cadência | um escrito por mês, **escrito adiantado** | o teste não é a estreia, é o primeiro mês sem vontade de escrever |
| Extensão | **900 a 1200 palavras** | em 350 não cabe tese, contra-argumento e os dois lados — e os três textos nasceram com ~350 |
| Autoria | o agente rascunha; o Bruno corrige, confere e **assume** | sem a correção dele o texto soa como outra pessoa |
| Home | capa de revista pura | escolha do Bruno, contra a recomendação (ver §6) |
| **Estreia** | **dois escritos**: Súmula 479 em manchete, telas sistêmicas em cartão | capa com um item só parece site quebrado; e sobra estoque |
| **Tema 929** | segurado para **outubro**; um quarto texto escrito agora, para novembro | entrar em outubro com estoque é o que impede o padrão do blog abandonado |
| Prova | **todo escrito carrega prova, ou não monta** | invariante opcional não é invariante |
| Tipos de prova | `ementa`, `enunciado`, `consulta` — e a página **exibe qual é qual** | andamento de tema repetitivo não é ementa, e o site não finge que é |
| **Conferência** | **no primeiro uso**, uma vez por verbete, para sempre | ninguém confere 56 acórdãos em mutirão — o corpus provou isso ficando meses inteiro em `nao` |
| **Fonte da conferência** | a **página de jurisprudência do JusBrasil** | a base é real e validada; a resposta da Jus IA é prosa gerada, e já disse aqui que o Tema 929 fora cancelado |
| Verificação | `verificar.py` com **Playwright**, dentro da montagem | contraste, movimento e estouro só existem depois do CSS aplicado |
| Hospedagem | GitHub Pages, e a estreia é em `github.io` | o `.adv.br` vem depois, com o custo de migração assumido |
| Comissão | não entra no Sobre até a nomeação sair | pedir para entrar não é ser membro |

---

## 3. Como o site se monta

```
python montar.py     # monta E verifica. Falha = nao publica.
python og.py         # as imagens de card (caro: abre navegador)
python guilhoche.py  # regenera os SVG
python citar.py <escrito> <verbete>                       # do corpus
python citar.py <escrito> --consulta <arq> --url <URL>    # de fonte oficial
```

```
_fonte/partes/     cabeca · topo · rodape        a casca, uma vez só
_fonte/paginas/    index · escritos · atuacao · sobre    o miolo de cada uma
_conteudo/escritos/*.md    UM arquivo por escrito
ativos/estilo/     9 módulos numerados de CSS
ativos/og/         as chapas 1200×630, uma por escrito

index.html · escritos.html · atuacao.html · sobre.html
escritos/*.html · ativos/estilo.css        GERADOS — nunca editar
```

**A regra que sustenta tudo:** de um único Markdown saem três coisas — a página
do artigo, a entrada do índice e o cartão da capa. Escrito novo é arquivo novo.

### O que o verificador checa

Léxico do Provimento 205 · prova · rascunho vazado · imagem de card ·
estrutura de títulos · links **e âncoras** · contraste AA nos dois temas ·
movimento sob `prefers-reduced-motion` · estouro de 320 a 1600px.

O léxico mira **frase**, não palavra, e ignora os blocos de prova: a carteira do
Bruno é consumidor bancário, "desconto" e "cobrança" são o objeto dos escritos,
e ementa fala de honorário sucumbencial o tempo todo.

---

## 4. Sistema visual

| | |
|---|---|
| Fundo | marfim `#FBF9F2` · faixa `#F2EFE3` · escuro `#12161A` |
| Acento | pinho `#245C53` (claro) · `#7FCFBD` (escuro) — **um só** |
| Marca | **Prata**, caixa-alta, entreletra 0,095em |
| Título e corpo | **Crimson Pro** |
| Rótulo, dek, data, navegação | **Archivo** |
| Figura | guilhoché gerado — quadrado no cartão, **faixa 16:5 nativa** no artigo |

**A regra tipográfica, medida no site da S&C:** serifada só em título, marca e
corpo. Data em serifada é o que faz um site parecer blog.

A faixa do artigo usa `faixa-1..3.svg` — variantes horizontais da curva de
interferência, em 1600×500 nativo. A roseta não sobrevive ao recorte em 16:5.

---

## 5. O que falta

**Do Bruno, e ninguém faz por ele:**

- [ ] Alongar, revisar e **assumir** `sumula-479` e `telas-sistemicas`
      (`rascunho: nao`)
- [ ] Conferir no JusBrasil os verbetes que esses dois citarem, virando cada um
      para `inteiro_teor_conferido: sim` no corpus **e** no bloco colado
- [ ] Escrever o quarto texto, para novembro
- [ ] Foto nova para o Sobre (a de hoje tem 400px)

**Depois, e só depois:** `python montar.py` verde → merge de `periodico` em
`main` → push. Antes do merge, apagar `_fonte/especime/`.

**Adiado com data:**

- [ ] Busca no índice — quando houver ~10 textos; o botão da barra está
      comentado no `topo.html` esperando por ela
- [ ] Domínio `.adv.br` — trocar `SITE` no `montar.py` e remontar
- [ ] Apagar a branch `claude/brazilian-lawyer-site-nfc709` no repo do ORDIR
      — **depois da estreia**, não antes

---

## 6. As três tensões que sobreviveram ao grill

**A capa pura aposta num leitor que ainda não existe.** O Bruno escolheu a home
sem nenhuma informação sobre quem ele é, e aceitou perder o visitante que chega
sem conhecê-lo. A fonte de tráfego prevista é o Instagram, onde `@hardt.adv` tem
zero seguidores. **Se em três meses o site só receber gente que não o conhece, a
decisão da home é a primeira a revisar.**

**A rajada, agora domada — mas não resolvida.** Estreia com dois, Tema 929 em
outubro, o quarto em novembro. Isso compra três meses. Dezembro depende de o
Bruno escrever em novembro, que é a mesma aposta que todo blog jurídico
abandonado fez.

**A dependência.** O projeto exige `pip install -r requirements.txt` **e**
`playwright install`. Foi escolhido de propósito, contra a recomendação — as
regras do Provimento 205 e o contraste valem mais que clonar-e-montar em
qualquer máquina. É o que vai quebrar numa máquina nova daqui a seis meses.

---

## 7. Contexto que não está no repositório

- **Instagram:** `@hardtbruno` (pessoal, privada, 502 seguidores) →
  `@hardt.adv` (profissional, nova) e `@ordir.com.br` (o software).
- **Comissões:** pedido de entrada na Comissão de Direito Digital e IA da
  Subseção de Blumenau (presidente Alexa Schmitt de Sousa), por e-mail para
  `comissoes@oab-bnu.org.br`. **Quando sair a nomeação, entra no Sobre e na bio
  do Instagram** — é a credencial verificável que hoje falta.
- **A carteira real** é toda consumidor bancário e de telecom, mas o site
  anuncia público, criminal e cível **por decisão dele**: a carteira é nova e
  não define o alcance pretendido.
- **O outro lado da mesma regra** vive no repo da advocacia
  (`C:\Users\Hardt\Dev\HARDT - ADVOCACIA`): o corpus em
  `conhecimento/jurisprudencia/`, o pré-passe `verificar_citacoes.py` — que
  desde 30/08 varre aquele corpus como cânone — e a skill `protocolo`, cujo
  Estágio 5b trava a montagem da pasta se a peça citar verbete não conferido.
  Prazo aberto: **Ação 1 do Johann (Rico/Banco XP), 21/09/2026.**
