# Handoff — site brunohardt

**Gerado em 30/08/2026.** Para retomar o trabalho numa sessão nova, ou para o
Bruno tocar sozinho.

Repositório: `C:\Users\Hardt\Dev\site-bruno-hardt`
**Atenção: nada disto está commitado.** O último commit é `52b205a`, a versão
anterior do site. Todo o trabalho descrito aqui está na árvore de trabalho, sem
commit — vale fazer um antes de qualquer outra coisa.

No ar hoje: <https://brunohardt.github.io/> — **ainda a versão antiga**.
Nada do que está descrito aqui foi publicado.

---

## 1. Onde parou

O site foi refeito do zero como **periódico**, no registro da Sullivan &
Cromwell. Existem, funcionando localmente:

- **capa** (`index.html`) — um escrito em destaque e os demais em cartões
- **escritos.html** — o índice
- **três páginas de artigo**, geradas de Markdown
- **atuacao.html** e **sobre.html**
- barra fixa sem fio, rodapé com marca e botões de contato, cartão `.vcf`

O que **falta** para publicar está na §6.

---

## 2. As decisões, e por que elas são assim

Saíram de uma sessão de grill em 30/08. Não reabrir sem motivo novo.

| Decisão | Ficou | Por quê |
|---|---|---|
| Formato do site | periódico, não cartão de visita | a autoridade de advogado novo vem do que ele demonstra saber |
| Cadência | **um escrito por mês** | 12/ano é o mínimo para a seção não parecer morta, e cabe numa banca em formação |
| Autoria | o agente rascunha; **o Bruno lê, corrige e confere as fontes** | ele é o autor; sem a correção dele o texto soa como outra pessoa |
| Home | **capa de revista pura** — só manchete e cartões | escolha do Bruno, contra a recomendação (ver §7) |
| Páginas | Escritos, Atuação e Sobre, todas próprias | menu que aponta para âncora da mesma página é incoerente |
| Fonte do escrito | `_conteudo/escritos/*.md`, no repo do site | o site publica sozinho, sem depender de outro repositório |
| Formato | Markdown com `python-markdown` | primeira e única dependência do projeto |
| Prova da citação | o escrito **carrega o verbete dentro de si** | referência entre repositórios quebra em silêncio |
| Hospedagem | **GitHub Pages**, onde já está | não havia problema a resolver; Firebase seria downgrade |
| Foto | retrato pequeno com os 400px de hoje | é miniatura de LinkedIn; troca prevista |
| Comissão | **não entra no Sobre até a nomeação sair** | pedir para entrar não é ser membro |
| Estreia | quando os escritos estiverem revistos pelo Bruno | periódico não estreia sem texto assumido |

---

## 3. Como o site se monta

```
python montar.py       # gera tudo
python citar.py <escrito> <verbete>   # cola a prova dentro de um escrito
```

```
_fonte/partes/     cabeca · topo · rodape        a casca, uma vez só
_fonte/paginas/    index · escritos · atuacao · sobre    o miolo de cada uma
_conteudo/escritos/*.md    UM arquivo por escrito
ativos/estilo/     9 módulos numerados de CSS

index.html · escritos.html · atuacao.html · sobre.html
escritos/*.html · ativos/estilo.css        GERADOS — nunca editar
```

**A regra que sustenta tudo:** de um único Markdown saem três coisas — a página
do artigo, a entrada do índice e o cartão da capa. Escrito novo é arquivo novo,
e nada mais.

### O bloco de prova

`citar.py` lê o corpus em `Dev\HARDT - ADVOCACIA\conhecimento\jurisprudencia`,
extrai a ementa entre `<!--EMENTA_BEGIN-->` e `<!--EMENTA_END-->` — extração
programática, nunca redigitada — e cola no fim do escrito:

```
:::verbete 10-sumula-479-fortuito-interno
fonte: ...
inteiro_teor_conferido: nao
---
<ementa literal>
:::
```

**A montagem recusa publicar** escrito não-rascunho que cite verbete com
`inteiro_teor_conferido: nao`. Sai com código 1 e nomeia o culpado. Testado.

---

## 4. Sistema visual

| | |
|---|---|
| Fundo | marfim `#FBF9F2` · faixa `#F2EFE3` · escuro `#12161A` |
| Acento | pinho `#245C53` (claro) · `#7FCFBD` (escuro) — **um só** |
| Marca | **Prata**, caixa-alta, 2,3rem, entreletra 0,095em |
| Título e corpo | **Crimson Pro** (garalda, peso 500 nos títulos) |
| Rótulo, dek, data, navegação | **Archivo** (grotesca) |
| Figura | guilhoché — epitrocoides geradas, uma por escrito |

**A regra tipográfica, que veio de medir o site da S&C:** serifada só em título,
marca e corpo. Rótulo, data e navegação são grotesca. Data em serifada é o que
faz um site parecer blog.

O gerador dos guilhochés é o `guilhoche.py`, na raiz do repositório. Ele recria
os três SVG do zero — são epitrocoides, não desenho à mão, então variante nova é
parâmetro novo, não arquivo novo.

---

## 5. Regulatório — Provimento 205/2021

Página passiva e meramente informativa. Proibido: caso, cliente, depoimento,
resultado, honorário, forma de pagamento, superlativo, "especialista" sem
título, comparação com colega, formulário, chat, pixel, símbolo da OAB.

Os escritos são **tese, nunca caso** — é o que os põe dentro do art. 4º.

---

## 6. O que falta para publicar

- [ ] **Bruno revisa e assume os três escritos** (estão como `rascunho: sim`)
- [ ] Fechar `inteiro_teor_conferido` nos acórdãos citados, no site do tribunal
- [ ] **Escrever `verificar.py`** — e a peça que falta para o método existir de
      verdade. Hoje as regras do Provimento 205 são disciplina escrita em
      `ESPEC.md`; o verificador as transforma em teste que derruba a montagem.
      Precisa checar: léxico proibido (honorário, garantia, superlativo,
      depoimento, "melhor", menção a caso ou cliente), contraste AA nos dois
      temas, ordem de títulos, `h1` presente, link interno existente, marcador
      de rascunho vazado para arquivo gerado, e `animation` fora de
      `prefers-reduced-motion`. As quatro primeiras são estáticas; as demais
      pedem navegador
- [ ] Buscar no índice de escritos — só quando houver ~10 textos
- [ ] `og.png` 1200×630 e as linhas `og:image` de volta
- [ ] Domínio `.adv.br`: trocar `SITE` em `montar.py` e remontar
- [ ] Foto nova (a de hoje tem 400px); trocar = trocar `ativos/img/bruno-hardt.jpg`
- [ ] **A faixa de guilhoche no topo do artigo** esta em 16:5 com recorte, e a
      roseta vira uma forma espelhada que parece acidental. Ou ela cabe inteira
      (com sobra nas laterais), ou se desenha uma curva propria para faixa larga
      — a de interferencia (`guilhoche-2`) ja funciona bem nesse formato, entao
      o caminho mais barato e gerar variantes horizontais dela
- [ ] Apagar `_fonte/especime/` antes de publicar
- [ ] Apagar a branch `claude/brazilian-lawyer-site-nfc709` do repo do ORDIR

---

## 7. As três tensões que sobreviveram ao grill

**A capa pura aposta num leitor que ainda não existe.** O Bruno escolheu a home
sem nenhuma informação sobre quem ele é, e aceitou explicitamente perder o
visitante que chega sem conhecê-lo. A fonte de tráfego prevista é o Instagram,
onde `@hardt.adv` tem zero seguidores. Se em três meses o site só receber gente
que não o conhece, **a decisão da home é a primeira a revisar.**

**A rajada.** Três ou quatro textos de uma vez, com prazo em 21/09 no meio, e
depois um por mês. Rajada seguida de silêncio é o padrão de todo blog jurídico
abandonado, e a data no cartão carimba o abandono. **O teste real não é a
estreia: é o texto de outubro.**

**A dependência.** O projeto deixou de clonar-e-montar em qualquer máquina —
agora exige `pip install -r requirements.txt`. Registrado, mas é o tipo de coisa
que quebra numa máquina nova daqui a seis meses.

---

## 8. Contexto que não está no repositório

- **Instagram:** `@hardtbruno` (pessoal, privada, 502 seguidores) →
  `@hardt.adv` (profissional, nova) e `@ordir.com.br` (o software).
  A bio da pessoal é `Advogado @hardt.adv / Fundador @ordir.com.br`.
- **Comissões:** o Bruno vai pedir para entrar na Comissão de Direito Digital e
  IA da Subseção de Blumenau (presidente Alexa Schmitt de Sousa) e talvez em
  criminal ou constitucional. Inscrição por e-mail para
  `comissoes@oab-bnu.org.br` com nome, número da OAB, telefone e a comissão.
  **Quando sair a nomeação, ela entra no Sobre e na bio do Instagram** — é a
  credencial verificável que hoje falta.
- **A carteira real** é toda consumidor bancário e de telecom (cinco ações
  Johann, uma Só Calcário × TIM), mas o site anuncia público, criminal e cível
  **por decisão dele**: a carteira é nova e não define o alcance pretendido.

---

## 9. Especificação

`ESPEC.md`, na raiz do repositório, é a fonte da verdade. Toda mudança de
comportamento começa por emendá-la — depois a verificação, depois o código.
