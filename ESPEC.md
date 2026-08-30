# Especificação do site — brunohardt

> Este arquivo é a **fonte da verdade**. O código implementa o que está aqui.
> Quando os dois divergem, ou o código está errado, ou a especificação foi
> emendada de propósito — e a emenda entra aqui **antes** do código mudar.

---

## 1. O que este site é

O periódico de um advogado. A referência declarada é a **Sullivan & Cromwell**:
fundo marfim, a home como publicação datada, e nenhuma chamada para ação em
lugar nenhum.

A autoridade de um advogado que ninguém conhece ainda não vem de dizer que é
bom. Vem do que ele demonstra saber. Por isso a escrita é a primeira coisa da
página, e não um blog escondido no menu.

**Não é** um cartão de visita, um Linktree, nem uma vitrine de serviços.

### 1.1 Regime editorial

| | |
|---|---|
| **Cadência** | um escrito por mês. Doze por ano é o mínimo para a seção não parecer morta, e cabe numa banca em formação. |
| **Extensão** | 900 a 1200 palavras. Abaixo disso não cabe tese, contra-argumento e os julgados dos dois lados — e escrito que não cumpre o próprio dek trabalha contra a autoridade que o site existe para construir. |
| **Autoria** | o agente rascunha; o Bruno lê, corrige, confere as fontes e assume. Sem a correção dele o texto soa como outra pessoa. |
| **Estoque** | escreve-se adiantado. Um mês publicado é um mês que já estava escrito. |

Rajada seguida de silêncio é o padrão de todo blog jurídico abandonado, e a
data no cartão carimba o abandono. O teste de um periódico não é a estreia: é
o primeiro mês em que não houve vontade de escrever. O estoque é a forma de
sobreviver a esse mês.

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
de resumo de terceiro.**

**Todo escrito carrega prova dentro de si.** Escrito sem ao menos um bloco de
prova não monta. A regra é dura de propósito: a promessa "eu cito o que
conferi" não pode ser opcional, porque invariante opcional não é invariante.
Referência a outro repositório também não serve — ela quebra em silêncio.

São três tipos de bloco, e a página **exibe qual é qual**:

| Tipo | O que guarda |
|---|---|
| `ementa` | ementa de acórdão, extraída entre `EMENTA_BEGIN`/`EMENTA_END` do corpus |
| `enunciado` | súmula ou enunciado de turma recursal — o texto é o próprio verbete |
| `consulta` | consulta a fonte oficial: URL, data de acesso e o trecho literal da página |

O leitor vê o rótulo e julga o peso. O andamento de um tema repetitivo não é
uma ementa, e o site não finge que é. **Extração programática nos três** — nada
é redigitado, nunca.

**Conferência no primeiro uso.** Um verbete nasce `inteiro_teor_conferido: nao`.
Na primeira vez que ele entra num escrito ou numa petição, o Bruno abre a fonte
e confere — uma vez, para sempre. A montagem recusa escrito não-rascunho que
cite verbete com `nao`, e nomeia o culpado. O gate não é burocracia: é o que faz
a conferência acontecer na hora em que o julgado já está aberto na tela, em vez
de virar mutirão de cinquenta acórdãos que nunca acontece.

**A fonte de conferência é a página de jurisprudência do JusBrasil** — a base,
que é real e validada. **Não** a resposta da Jus IA, que é prosa gerada e que
neste projeto já afirmou que o Tema 929 havia sido cancelado. São camadas
diferentes do mesmo produto, e essa distinção é a razão de o campo existir.

Peça errada se corrige; publicado erra na frente de todo mundo.

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
- **A montagem exige navegador.** `verificar.py` roda com Playwright, e sem ele
  não há build. É a segunda dependência do projeto e a mais pesada, assumida de
  propósito: as regras da §2.1 e o contraste valem mais que a propriedade de
  clonar e montar em qualquer máquina. Quem clonar precisa de
  `pip install -r requirements.txt` e `playwright install`.

---

## 3. Sistema visual

| | |
|---|---|
| Fundo | marfim `--papel` · faixa `--papel-2` · escuro |
| Tinta | `--tinta` · secundária `--tinta-2` · muda `--mudo` |
| Acento | **um só**: pinho `--acento` |
| Marca | **Prata** (família `Marca`), caixa-alta, entreletra larga |
| Título e corpo | **Crimson Pro** (família `Serifada`), garalda |
| Rótulo, dek, data, navegação | **Archivo** (família `Grotesca`) |
| Figura | guilhoché — epitrocoides geradas, uma por escrito |

**A regra tipográfica, medida no site da S&C:** serifada só em título, marca e
corpo. Rótulo, data e navegação são grotesca. **Data em serifada é o que faz um
site parecer blog.**

As figuras são **geradas** por `guilhoche.py`, nunca desenhadas: variante nova é
parâmetro novo, não arquivo novo. A faixa larga do topo do artigo usa
**variantes horizontais da curva de interferência** — a roseta não sobrevive ao
recorte em 16:5, e uma forma espelhada por acidente é pior que figura nenhuma.

Nenhum valor de cor, corpo ou espaço é escrito à mão fora de
`ativos/estilo/10-tokens.css`.

---

## 4. As páginas

| Página | O que tem |
|---|---|
| **Capa** (`index.html`) | capa de revista pura: um escrito em manchete e os demais em cartões |
| **Escritos** | índice completo, datado; a busca nasce aqui quando houver ~10 textos |
| **Escrito** | faixa, título, dek, data, corpo, blocos de prova com o rótulo do tipo |
| **Atuação** | três áreas, dois ou três parágrafos cada — não lista de tópicos |
| **Sobre** | foto, e-mail, cartão `.vcf`, localização, formação e comissões |

Cada uma é página própria: menu que aponta para âncora da mesma página é
incoerente.

**A capa pura é uma aposta declarada.** Ela não diz nada sobre quem é o autor, e
por isso perde o visitante que chega sem conhecê-lo. A fonte de tráfego prevista
é o Instagram. Se em três meses o site só receber gente que não o conhece, esta
é a primeira decisão a revisar.

**Comissão só entra no Sobre depois da nomeação.** Pedir para entrar não é ser
membro.

---

## 5. Arquitetura — como não virar monolito

```
_fonte/                        FONTE — é isto que se edita
  partes/    cabeca · topo · rodape      a casca, uma vez só
  paginas/   index · escritos · atuacao · sobre    só o miolo de cada uma
  especime/                              provas de tipografia (não publica)
_conteudo/
  escritos/  *.md                        UM arquivo por escrito
ativos/estilo/                 ESTILO — um módulo por assunto
  00-fontes 10-tokens 20-base 30-topo 40-vitrine
  50-cartoes 60-rodape 70-leitura 90-movimento
montar.py                      MONTAGEM (monta e verifica)
citar.py                       cola o bloco de prova dentro de um escrito
guilhoche.py                   gera as epitrocoides
og.py                          as imagens de card, uma por escrito
verificar.py                   VERIFICAÇÃO

index.html · escritos.html · atuacao.html · sobre.html
escritos/*.html · ativos/estilo.css      GERADOS — nunca editar
```

**As cinco regras que sustentam a separação:**

1. **Um assunto por arquivo.** Módulo de CSS se divide por *componente*, nunca
   por página. Se um seletor serve duas páginas, ele não pertence a nenhuma das
   duas — pertence ao componente.
2. **Gerado não se edita.** Os arquivos gerados trazem aviso no topo. A próxima
   montagem sobrescreve, e é para sobrescrever mesmo.
3. **Página nova não toca no montador.** Basta um arquivo em `_fonte/paginas/`
   com o bloco de metadados. O montador descobre sozinho — e descobre também os
   módulos de CSS, por varredura do diretório.
4. **Escrito novo é arquivo novo, e nada mais.** De um único Markdown saem três
   coisas: a página do artigo, a entrada do índice e o cartão da capa.
5. **A montagem falha alto.** Marcador não substituído, metadados ausentes ou
   verbete não conferido derrubam o build. Nada sobe quebrado em silêncio.

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

**4. Provar.** `python montar.py` — que monta e, em seguida, verifica. Um
comando só: montar sem verificar não é montagem, é rascunho de HTML, e a §2.3
não deixa isso ser uma escolha de quem digita. Verde, commita.

### O que `verificar.py` precisa checar

| Verificação | Falha quando |
|---|---|
| **Léxico regulatório** | aparece termo da lista da §2.1 |
| **Prova** | escrito sem nenhum bloco de prova, ou citando verbete com `inteiro_teor_conferido: nao` |
| Estrutura | falta `h1`, ordem de títulos quebrada, marco ausente |
| Links | href interno aponta para arquivo que não existe |
| Rascunho | escrito com `rascunho: sim` tem pagina gerada, esta linkado na capa ou no indice, ou vazou o marcador |
| **Imagem de card** | falta `ativos/og/<slug>.png`, ou ela e mais velha que o escrito |
| Contraste AA | qualquer texto abaixo de 4.5:1 (3:1 se grande), nos dois temas |
| Movimento | `animation` fora de `prefers-reduced-motion` |
| Estouro | largura de rolagem maior que a janela, de 320 a 1600px |

As seis primeiras são estáticas — leem os arquivos. As três últimas rodam no
navegador, com Playwright (§2.3).

A imagem de card não é gerada pela montagem: abrir navegador para fotografar
quatro chapas é caro para pagar a cada build. `python og.py` gera; a montagem
apenas recusa publicar sem elas, ou com elas velhas.

> O léxico regulatório é o mesmo padrão que `scripts/verificar_lexico.py` já faz
> no repositório da advocacia. Vale portar a ideia, não o código.

---

## 7. Publicação

- **`main` é de onde o GitHub Pages publica.** O site novo vive na branch
  `periodico` até a estreia. O merge é ato deliberado, nunca efeito colateral de
  um push distraído — o que está na branch tem escritos em `rascunho: sim`, e
  publicar rascunho sob o nome e a OAB do autor é caro sob o Provimento 205.
- **A estreia é em `brunohardt.github.io`.** O domínio `.adv.br` vem depois,
  aceitando o custo da migração: `SITE` no `montar.py`, canonical, `og:url` e os
  dois `@id` do JSON-LD, mais todo link já compartilhado apontando para o
  endereço velho.
- **`og.png` 1200×630 por escrito**, gerada do guilhoché. Todo o tráfego previsto
  vem do Instagram, e link compartilhado sem `og:image` renderiza caixa cinza —
  justamente nas semanas de divulgação do lançamento.
- **Antes do merge:** apagar `_fonte/especime/`.

---

## 8. O que está pendente

- [ ] Os escritos da estreia: alongados a 900–1200, revistos e assumidos pelo
      Bruno, com os verbetes conferidos no JusBrasil
- [ ] Foto nova para o Sobre (a de hoje tem 400px)
- [ ] Busca no índice de escritos — só quando houver ~10 textos
- [ ] Domínio `.adv.br`
