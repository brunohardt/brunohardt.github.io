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
| **Autoria** | o agente rascunha; o Bruno lê, corrige, confere as fontes e assume. Sem a correção dele o texto soa como outra pessoa. **O agente escreve o argumento, nunca a citação:** todo julgado vem do corpus ou de fonte que o Bruno forneceu. Precedente que o agente "lembra" é invenção, e é o modo exato de a §2.2 ser furada por dentro. |
| **Data** | a de **publicação**, com hora — nunca a de redação. Enquanto `rascunho: sim` o campo pode faltar; publicado sem data não monta. A hora existe porque a ordenação é por data, e dois escritos no mesmo dia empatam. |
| **Estreia** | dois escritos, no mesmo dia, em horas diferentes. Capa com um item só parece site quebrado. |
| **Estoque** | escreve-se adiantado. Um mês publicado é um mês que já estava escrito. O estoque é regime de cruzeiro, **não pré-requisito de decolagem**: o texto de novembro não segura a estreia. |

Rajada seguida de silêncio é o padrão de todo blog jurídico abandonado, e a
data no cartão carimba o abandono. O teste de um periódico não é a estreia: é
o primeiro mês em que não houve vontade de escrever. O estoque é a forma de
sobreviver a esse mês.

**O que a estreia com dois compra, e o que ela não compra.** Compra setembro e
outubro: o Tema 929 já está escrito, segurado para outubro. Não compra novembro
— dali em diante a cadência não tem estoque nem mecanismo, só disciplina, e nada
no sistema vai avisar. É escolha declarada, não descuido.

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

**Ementa longa entra recortada, e o corte aparece.** Ementa de acórdão passa de
oitocentas palavras sem esforço, e uma página em que a citação pesa o triplo da
prosa não é periódico: é repositório. O recorte é feito pelo `citar.py` sobre os
itens numerados do próprio acórdão — a divisão é do relator, não do autor —,
cada corte vira `[…]` posto pelo script, e o rótulo passa a dizer **Ementa
(trecho)**, porque o leitor precisa saber que está vendo um pedaço antes de
julgar o peso. Nada disso afrouxa a extração programática: o que ficou é byte a
byte o que estava lá, e o que saiu está marcado. Recortar de modo a inverter o
que o acórdão decidiu é a única coisa que a marca não impede, e essa continua
sendo responsabilidade de quem assina.

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

**A fonte varia com o tipo.** Ementa de acórdão se confere no JusBrasil; a
transcrição da base basta, e não se vai ao tribunal. Enunciado de súmula se
confere na página do próprio tribunal — súmula não tem inteiro teor, e o que se
confere ali é o texto e a vigência. O campo segue chamado
`inteiro_teor_conferido` por compatibilidade com o corpus da advocacia, e o nome
mente um pouco no caso do enunciado.

**A conferência é no fim do escrito, não durante.** Escreve-se o texto inteiro,
corta-se o que não presta, e só então se confere o que sobreviveu: conferência
gasta em parágrafo que morreu é conferência jogada fora. O risco assumido é o
inverso — verbete que reprova derruba parágrafo já polido. Quando acontecer,
**cai o parágrafo**. Trocar o precedente para salvar a prosa é exatamente como
se cita mal.

**A linha de crédito é o julgado, e nada mais.** O que sai impresso no
`figcaption` é o campo `credito`, que o `citar.py` monta dos campos do próprio
verbete: tribunal, classe, número, órgão e data de julgamento. É o que um
leitor precisa para achar o acórdão, e é a única coisa naquele arquivo que
credita alguma coisa. O relator fica de fora: nome próprio está gravado sem
acento em parte do corpus, e adivinhar acento de nome é inventar.

**O campo `fonte` do corpus não é publicável, e não entra no escrito.** Lá ele
é nota de trabalho: guarda como a pesquisa começou — a ferramenta que trouxe o
julgado à tela — e às vezes o caminho da pasta do caso, que nomeia cliente e
parte contrária de uma vez só. Rastro de pesquisa não credita julgado nenhum;
o julgado se credita sozinho. E publicar o caminho seria violação da §2.1 que
nenhum despublicar desfaz. O verificador recusa bloco que traga `fonte`, e põe
a mesma rede burra embaixo do `credito`: reconhece a *forma* de um caminho, não
entende o conteúdo.

Peça errada se corrige; publicado erra na frente de todo mundo.

### 2.3 Técnico

- **Zero JavaScript, com uma exceção nomeada.** A regra continua valendo: só
  entra função sem equivalente em CSS, e o site tem de continuar utilizável sem
  ela. A exceção é **o avanço automático do trilho** (§4.1) — carrossel que anda
  sozinho num trilho de `scroll-snap` não tem versão em CSS que não seja
  gambiarra, e gambiarra em CSS é o que estoura em 320px. Sem o script as réguas
  continuam navegando o trilho, e nenhum escrito fica inalcançável.
- **Zero rastreador, zero cookie, zero coleta.**
- **O site é claro, e só claro.** Não há tema escuro: quem estiver com o
  sistema em modo escuro recebe a mesma página marfim. Foi decisão do Bruno em
  30/08/2026, depois de ver a estreia no ar em modo noturno e não reconhecer o
  design que aprovou. O preço está aceito: leitor de tela escura recebe uma
  página clara, e a paleta escura que existia foi apagada, não desligada.
- Contraste **AA**, medido também com `prefers-color-scheme: dark` — ali o teste
  não mede uma segunda paleta, mede que ela não voltou: se o fundo deixar de ser
  marfim sob modo escuro, a montagem para.
- Nenhum estouro horizontal de 320px a 1600px.
- Toda animação dentro de `prefers-reduced-motion: no-preference`, e o
  **estado-base é o final** — quem pede movimento reduzido recebe a página
  pronta, sem piscar. Vale igualmente para movimento **feito em JavaScript**: o
  trilho não avança sob `reduce`, e o verificador prova isso medindo a posição
  do trilho, não lendo o CSS.
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
| Fundo | marfim `--papel` · faixa `--papel-2` — sem tema escuro |
| Tinta | `--tinta` · secundária `--tinta-2` · muda `--mudo` |
| Acento | **um só**: pinho `--acento` |
| Marca | **Prata** (família `Marca`), caixa-alta, entreletra larga |
| Título e corpo | **Crimson Pro** (família `Serifada`), garalda |
| Rótulo, dek, data, navegação | **Archivo** (família `Grotesca`) |
| Figura | **fotografia**, uma por escrito, em dois eixos - a mesma imagem na capa, na faixa do artigo e nas chapas de compartilhamento |

**A regra tipográfica, medida no site da S&C:** serifada só em título, marca e
corpo. Rótulo, data e navegação são grotesca. **Data em serifada é o que faz um
site parecer blog.**

**Desde 30/08/2026 toda figura do site é fotografia gerada por prompt**, e não
desenho gerado por script. O guilhoché saiu - dele, do `guilhoche.py` e dos seis
SVG. Os prompts estão em `PROMPTS.md`, no repositório, pelo mesmo motivo que o
`guilhoche.py` estava: são a origem das imagens, e origem que vive só numa
conversa de gerador não é recuperável.

A referência continua sendo a S&C, e ela é a do *hero*: fotografia escura,
sangrando de borda a borda, com o título em marfim por cima. **Isto revoga a
regra de 30/08 segundo a qual a tipografia nunca fica sobre a arte.** Ela existia
porque a arte de então era clara, de dois tons, e branco sobre ela dava 1,6:1. A
arte agora é escura por composição: metade do quadro é quase-preta *porque é ali
que o título vai*.

**Uma foto por escrito, declarada no `foto:` do frontmatter**, e não uma arte
única reaproveitada. Isso também revoga a regra anterior, e o custo é explícito:
cada escrito passa a dever **duas gerações** - uma deitada e uma em pé -, e sem
elas o site não monta. A dívida nasceu quitada, porque os três prompts cobrem os
três escritos que existem, e **vence no quarto texto**, em novembro, que é
justamente quando o estoque acaba. Se em algum momento a foto virar o que atrasa
a publicação, é esta decisão que se revê primeiro, não a cadência.

| Escrito | Motivo | Por quê |
|---|---|---|
| `telas-sistemicas` | vidro canelado | vê-se a luz, não se vê o que está atrás |
| `sumula-479` | bordas de papel | o autos, de perfil |
| `tema-929` | ardósia | a fonte, e o que nela está gravado |

A afinidade entre motivo e assunto é escolha assumida, e ela contraria o que a
S&C faz - lá a imagem dá peso e não explica. Com foto por escrito essa fronteira
já tinha caído; melhor cair de propósito.

**Cada eixo se corta no próprio eixo longo.** A deitada nasce em 16:9 e serve a
lâmina (3,2:1), a faixa do artigo (16:5), o cartão da grade (16:7) e a prévia de
link (1,9:1) - todos cortes no eixo curto, que a textura macro atravessa sem
sofrer. A em pé nasce em 3:4 e serve o post do feed (4:5). Cortar contra o eixo
esmaga o desenho, e foi por isso que a arte anterior também tinha dois arquivos.

**A foto chega de 2 a 4 MB e não é isso que se serve.** `receber.py` produz três
arquivos por motivo: `-media` (1200px), que é o que o telefone baixa e o que a
faixa e o cartão usam sempre; `-larga` (2400px), o candidato grande do `srcset`
da lâmina e a fonte do `og.py`; e `-alta` (1800px, em pé), que não é servida a
ninguém - só o `og.py` a usa. A maior parte da audiência vem do Instagram, no
telefone: mandar 2400px para pintar uma faixa de 390 CSS px é o desperdício que
espremer qualidade não conserta. A qualidade não é fixa, o teto de peso é que
manda - textura fina é o pior caso do JPEG e custa o dobro de uma foto lisa.

**A metade reservada é composição, não sobra.** Deitada: a metade esquerda, de
topo a base, porque o título recua na medida de 1280 e fica alinhado com a marca.
Em pé: a metade de baixo, de ponta a ponta.

**Prompt não é determinístico, então o que trava a qualidade é a medida.** O
`verificar.py` mede cada foto: luminância média e percentil 90 da metade
reservada, matiz do verde, proporção e tamanho. Só a média deixaria passar a foto
com uma veia clara atravessando exatamente onde o título cai.

`--acento-claro` (#5FA394) existe por causa disso: `--acento` é #245C53 e dá
**2,47:1** sobre o quase-preto - some. Não é acento novo, é o mesmo pinho na
luminância que a superfície escura pede.

Nenhum valor de cor, corpo ou espaço é escrito à mão fora de
`ativos/estilo/10-tokens.css`.

---

## 4. As páginas

| Página | O que tem |
|---|---|
| **Capa** (`index.html`) | capa de revista pura: o trilho em destaque (§4.1) e os demais em cartões |
| **Escritos** | índice completo, datado; a busca nasce aqui quando houver ~10 textos |
| **Escrito** | faixa, título, dek, data, corpo, blocos de prova com o rótulo do tipo |
| **Atuação** | três áreas, dois ou três parágrafos cada — não lista de tópicos |
| **Sobre** | foto, e-mail, cartão `.vcf`, localização, formação e comissões |

Cada uma é página própria: menu que aponta para âncora da mesma página é
incoerente.

### 4.1 O trilho da capa

**O trilho é metade do acervo, com teto de quatro.** Dois escritos: uma lâmina e
um cartão. Quatro: duas e duas. Oito ou mais: quatro lâminas e o resto na grade.
Nenhum campo marca destaque — a regra é a recência, e o frontmatter não tem mais
`destaque`. Escolher a manchete à mão todo mês é passo manual que nada verifica,
e num sistema que já depende inteiro da disciplina do autor, um passo manual a
menos vale mais que a escolha que ele daria.

**A lâmina sangra de borda a borda e traz só o título.** Ela sai do `envelope` -
a grade volta à medida de 1280 num envelope próprio - e ocupa metade da altura da
janela, que é o que foi medido no original: 450px numa de 900. Sem rótulo, sem
dek, sem data: quatro blocos de texto sobre uma fotografia é banner
institucional, e o hero da referência tem só o título. O dek e a data continuam
existindo no cartão e na página do escrito, que é onde o leitor decide se lê.

O título recua na medida de 1280 com o mesmo gutter da barra, o que o alinha com
a marca logo acima - é assim no original. Abaixo de 700px não sobra metade
esquerda: o título ocupa a largura toda e desce para o rodapé da lâmina.

A referência é a S&C, medida: cinco lâminas com indicadores, 450px de altura numa
janela de 900, e dezessete cartões abaixo. Dela não se copia o número, e sim a
proporção — **o carrossel nunca é a página inteira**. A grade não fica vazia nem
no dia da estreia, que é o que a regra da metade garante em qualquer tamanho de
acervo.

**O trilho avança sozinho, e para sob `prefers-reduced-motion: reduce`.** Sem
avanço, lâmina que não é a primeira depende de rolagem horizontal, que quase
ninguém faz: publicar texto que ninguém alcança é pior que não destacá-lo. As
réguas continuam sendo navegação de verdade — clicável, e por teclado.

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
receber.py                     a foto que veio de fora vira os tres arquivos do site
og.py                          as imagens de card, duas por escrito
PROMPTS.md                     a origem das fotos - o que guilhoche.py era
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
| **Crédito** | o `fonte` de um bloco de prova tem forma de caminho interno (`casos/`, barra, nome de arquivo do repositório) |
| Estrutura | falta `h1`, ordem de títulos quebrada, marco ausente |
| Links | href interno aponta para arquivo que não existe |
| Rascunho | escrito com `rascunho: sim` tem pagina gerada, esta linkado na capa ou no indice, ou vazou o marcador |
| **Data** | escrito publicado (`rascunho: nao`) sem `data` |
| **Imagem de card** | falta `ativos/og/<slug>.png`, ou ela e mais velha que o escrito **ou que a foto dele** |
| **Foto do escrito** | falta um dos tres arquivos; passa do teto de peso; a metade reservada nao e escura (media ou p90); o verde esta fora de 148-196 graus; a proporcao contraria o eixo; menos de 2400px na borda longa |
| Contraste AA | qualquer texto abaixo de 4.5:1 (3:1 se grande), nos dois temas |
| Movimento | `animation` fora de `prefers-reduced-motion`, **ou o trilho anda sob `reduce`** — medido pela posição, porque timer de JavaScript não aparece em `getComputedStyle` |
| Estouro | largura de rolagem maior que a janela, de 320 a 1600px |

As oito primeiras são estáticas — leem os arquivos. As quatro últimas rodam no
navegador, com Playwright (§2.3). A foto entra no navegador como `data:` URI:
canvas de origem `file://` fica contaminado e o `getImageData` passa a lançar.

A imagem de card não é gerada pela montagem: abrir navegador para fotografar
oito chapas é caro para pagar a cada build. `python og.py` gera; a montagem
apenas recusa publicar sem elas, ou com elas velhas.

**A foto não é gerada por nada aqui** — vem de fora, do prompt em `PROMPTS.md`.
Por isso ela é o único insumo do site que o repositório não sabe reproduzir, e
por isso a régua sobre ela é de medida e não de existência: aceitar a imagem que
voltou sem medi-la seria confiar num gerador que não é determinístico.

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
- **Duas chapas por escrito, com a foto do próprio escrito**: `og/<slug>.png` em
  1200×630, que é a prévia de link, e `og/<slug>-feed.png` em 1080×1350, que é o
  post do Instagram. São formatos com trabalhos diferentes, e um não substitui o
  outro. A montagem exige só a primeira: link compartilhado sem `og:image`
  renderiza caixa cinza, justamente nas semanas de divulgação. A de feed não
  afeta o site, e por isso não derruba o build.
- **A chapa é a capa, no formato do card.** Foto sangrando, título em marfim por
  cima, rótulo em `--acento-claro`. Quem vê o card no Instagram e clica precisa
  encontrar a mesma imagem do outro lado do clique: card, capa e artigo são uma
  linguagem só. A chapa do site usa a foto do escrito mais recente, que é a mesma
  que abre a capa.
- **O post vem depois do artigo, nunca antes.** O site é a fonte; o Instagram
  (`@hardt.adv`) leva a ele. A conta pessoal não publica escrito — publicidade de
  advogado vive no perfil profissional, que é o alcançado pela §2.1.
- **Antes do merge:** apagar `_fonte/especime/`.

---

## 8. O que está pendente

- [ ] Os **dois** escritos da estreia: alongados a 900–1200, revistos e
      assumidos pelo Bruno
- [ ] Os verbetes que eles citarem, conferidos — do zero: **nenhum verbete do
      corpus guarda URL hoje**, e a busca se faz pelo número do processo. A
      conferência grava a URL que faltava
- [ ] Foto nova para o Sobre (a de hoje tem 400px)
- [ ] O quarto escrito, para novembro — **depois** da estreia, não antes
- [ ] Busca no índice de escritos — só quando houver ~10 textos
- [ ] Domínio `.adv.br`
