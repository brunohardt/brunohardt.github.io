# Especificação do site — brunohardt

> Este arquivo é a **fonte da verdade**. O código implementa o que está aqui.
> Quando os dois divergem, ou o código está errado, ou a especificação foi
> emendada de propósito — e a emenda entra aqui **antes** do código mudar.

---

## 1. O que este site é

O periódico de um advogado. A referência declarada é a **Sullivan & Cromwell**:
fundo marfim, uma só família serifada, a home como publicação datada, e nenhuma
chamada para ação em lugar nenhum.

A autoridade de um advogado que ninguém conhece ainda não vem de dizer que é
bom. Vem do que ele demonstra saber. Por isso a escrita é a primeira coisa da
página, e não um blog escondido no menu.

**Não é** um cartão de visita, um Linktree, nem uma vitrine de serviços.

---

## 2. Invariantes — o que nunca muda sem decisão explícita

### 2.1 Regulatório (Provimento 205/2021 do CFOAB)

A página é **passiva e meramente informativa**. É proibido, e o verificador
falha se aparecer:

| Proibido | Por quê |
|---|---|
| Menção a caso, cliente, depoimento ou resultado | captação e mercantilização |
| Honorário, forma de pagamento, desconto, "primeira consulta grátis" | art. 40 do CED |
| Superlativo, "o melhor", "especialista" sem título comprovável | alegação não verificável |
| Comparação com colega | vedada |
| Formulário, chat, pixel, botão de WhatsApp como chamada | captação ativa |
| Símbolo da OAB | vedado em publicidade |

É **permitido** e desejável: área de atuação, título acadêmico, cadeira em
comissão, artigo informativo e educativo, participação em evento ou imprensa —
desde que verdadeiro e verificável.

> Os escritos são **tese, nunca caso**. É essa distinção que os põe dentro do
> art. 4º.

### 2.2 Citação

Herdado do repositório da advocacia: **jurisprudência nunca de memória, nunca
de resumo de terceiro**. Um acórdão só entra num escrito publicado depois de
`inteiro_teor_conferido: sim` no verbete de origem. Peça errada se corrige;
publicado erra na frente de todo mundo.

### 2.3 Técnico

- **Zero JavaScript** no que já existe. Se algum dia entrar, é para uma função
  que não tem equivalente em CSS — e o site precisa continuar utilizável sem.
- **Zero rastreador, zero cookie, zero coleta.**
- Contraste **AA** em claro e escuro, os dois testados separadamente.
- Nenhum estouro horizontal de 320px a 1600px.
- Toda animação dentro de `prefers-reduced-motion: no-preference`, e o
  **estado-base é o final** — quem pede movimento reduzido recebe a página
  pronta, sem piscar.
- Identidade **única**: o Ordir aparece descrito, nunca com a marca dele.

---

## 3. Sistema visual

| | |
|---|---|
| Fundo | marfim quente `--papel` · faixa `--papel-2` |
| Tinta | `--tinta` · secundária `--tinta-2` · muda `--mudo` |
| Acento | **um só**: pinho `--acento` |
| Marca | Cormorant, caixa-alta, entreletra larga |
| Título | Source Serif 4, corte óptico de display |
| Texto e rótulo | Source Serif 4, corte óptico de texto |
| Figura | guilhoché — epitrocoides, uma marca por escrito |

Nenhum valor de cor, corpo ou espaço é escrito à mão fora de
`ativos/estilo/10-tokens.css`.

---

## 4. As páginas

| Página | Existe? | O que tem |
|---|---|---|
| **Home** | sim | vitrine (carrossel de escritos) · lista de escritos · atuação · contato |
| **Escritos** | não | índice completo, datado; a busca nasce aqui quando houver ~10 textos |
| **Escrito** (artigo) | não | título, dek, data, corpo, citações literais com fonte |
| **Atuação** | não | três áreas, dois ou três parágrafos cada — não lista de tópicos |
| **Sobre** | não | foto, e-mail, cartão `.vcf`, localização, formação e comissões |

**Sobre só nasce quando houver o que dizer.** Uma página de biografia com nome e
OAB e nada mais é pior que não ter página.

---

## 5. Arquitetura — como não virar monolito

```
_fonte/                        FONTE — é isto que se edita
  partes/    cabeca · topo · rodape      a casca, uma vez só
  paginas/   *.html                      só o miolo de cada página
  especime/                              provas de tipografia (não publica)
_conteudo/                     CONTEÚDO — previsto, ainda não implementado
  escritos/  *.md                        um arquivo por texto
ativos/estilo/                 ESTILO — um módulo por assunto
  00-fontes 10-tokens 20-base 30-topo 40-vitrine 50-colunas 60-rodape 90-movimento
montar.py                      MONTAGEM
verificar.py                   VERIFICAÇÃO (previsto)

index.html · ativos/estilo.css        GERADOS — nunca editar à mão
```

**As cinco regras que sustentam a separação:**

1. **Um assunto por arquivo.** Módulo de CSS se divide por *componente*, nunca
   por página. Se um seletor serve duas páginas, ele não pertence a nenhuma das
   duas — pertence ao componente.
2. **Gerado não se edita.** `index.html` e `ativos/estilo.css` trazem aviso no
   topo. A próxima montagem sobrescreve, e é para sobrescrever mesmo.
3. **Página nova não toca no montador.** Basta um arquivo em `_fonte/paginas/`
   com o bloco de metadados. O montador descobre sozinho.
4. **Escrito novo não toca em HTML.** É um arquivo de conteúdo; a montagem gera
   a página, a entrada no índice e o card do carrossel a partir dele. *(É o
   passo que falta implementar — hoje o escrito ainda é HTML na mão.)*
5. **A montagem falha alto.** Marcador não substituído derruba o build. Nada
   sobe quebrado em silêncio.

---

## 6. Desenvolvimento dirigido por especificação

O ciclo, em quatro tempos:

**1. Emendar a especificação.** Toda mudança de comportamento começa aqui — na
seção que ela afeta. Se a mudança não cabe em nenhuma seção, provavelmente é
uma seção nova, e vale perguntar se ela pertence ao site.

**2. Escrever a verificação antes da implementação.** A regra vira um teste em
`verificar.py`. "Sem menção a honorário" não é uma boa intenção: é uma lista de
termos que derruba a montagem.

**3. Implementar** no módulo certo — e só nele.

**4. Provar.** `python montar.py && python verificar.py`. Verde, commita.

### O que `verificar.py` precisa checar

| Verificação | Falha quando |
|---|---|
| **Léxico regulatório** | aparece termo da lista da §2.1 |
| Contraste AA | qualquer texto abaixo de 4.5:1 (3:1 se grande), nos dois temas |
| Estrutura | falta `h1`, ordem de títulos quebrada, marco ausente |
| Links | href interno aponta para arquivo que não existe |
| Rascunho | sobrou marcador `RASCUNHO` num arquivo gerado |
| Citação | escrito cita acórdão com `inteiro_teor_conferido: nao` |
| Movimento | `animation` fora de `prefers-reduced-motion` |
| Estouro | largura de rolagem maior que a janela, de 320 a 1600px |

As quatro primeiras são estáticas — leem os arquivos. As demais precisam de
navegador, e rodam com o Chrome DevTools.

> O léxico regulatório é o mesmo padrão que `scripts/verificar_lexico.py` já faz
> no repositório da advocacia. Vale portar a ideia, não o código.

---

## 7. O que está pendente

- [ ] Páginas: Escritos, Escrito, Atuação, Sobre
- [ ] `_conteudo/escritos/*.md` e a montagem a partir deles (regra 4 da §5)
- [ ] `verificar.py`
- [ ] Os três escritos de rascunho: revisão e assunção de autoria pelo Bruno,
      e `inteiro_teor_conferido` fechado nos acórdãos citados
- [ ] Busca no índice de escritos — só quando houver ~10 textos
- [ ] Foto para o Sobre; `og.png` 1200×630
- [ ] Domínio `.adv.br` (trocar canonical, og:url e os dois `@id` do JSON-LD)
