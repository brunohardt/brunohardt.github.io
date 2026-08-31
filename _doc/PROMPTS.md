# Prompts das figuras

Desde 30/08/2026 toda figura do site é fotografia gerada, não desenho de script.
Estes prompts são a origem dessas imagens, do mesmo jeito que `guilhoche.py` era
a origem das anteriores - e por isso moram no repositório. Prompt que vive só
numa conversa de gerador não é recuperável: quando a arte precisar de retoque,
não há a que voltar.

> **O arquivo passou a guardar só o que está pendente.** Os prompts das três
> fotos que já estão no ar - vidro canelado, bordas de papel e ardósia - saíram
> daqui em 31/08/2026, por decisão de quem assina. Eles não deixaram de existir:
> estão no histórico do git, no commit anterior a este. Se alguma das três
> precisar de retoque, é de lá que se recupera o prompt - `git log -p _doc/PROMPTS.md`.

## Regras que valem para os dois

- **Duas gerações por escrito**: uma deitada e uma em pé. Cada formato usa a arte
  cortada no próprio eixo longo; cortar contra o eixo esmaga o desenho.
- **A metade escura é composição, não sobra.** É onde o título vai. Na deitada
  ela é a metade esquerda, de topo a base. Na em pé é a metade de baixo, de
  ponta a ponta. Um prompt que a ponha do outro lado gera arte inútil.
- **Nada de interesse nas bordas que o recorte come.** A deitada nasce em 16:9 e
  é servida em 3,2:1 (lâmina da capa, faixa do artigo) e em 1,9:1 (chapa de
  link): o quarto de cima e o de baixo somem. A em pé nasce em 3:4 e é servida em
  4:5: os oitavos laterais somem.
- **Um verde só, e é o do site.** `--acento` é `#245C53`, matiz ~170°: verde de
  pinho puxando para o azul. O prompt fixa esse valor porque "teal" sozinho tanto
  dá o pinho quanto dá ciano, e ciano na maior imagem do site briga com o único
  acento dele. Depois de gerada, a foto é medida contra o token pelo
  `verificar.py`.
- **Sem desfoque.** Textura macro com profundidade rasa vira mancha quando
  ampliada até sangrar borda a borda.

| Escrito | Motivo | Arquivos |
|---|---|---|
| quarto escrito, de novembro - sem slug ainda | malha de aço | `ativos/img/malha-larga.jpg` · `malha-alta.jpg` |

---

## Malha de aço

> **A arte foi gerada, medida e aceita em 31/08/2026**, e o que se previu aqui
> não se confirmou - fica registrado porque a previsão errada é o que ensina.
>
> A previsão era que a malha fosse o motivo mais arriscado dos quatro para o
> orçamento de peso: trama regular e fina é detalhe de alta frequência em cada
> pixel, que é a "textura de ponta a ponta, sem área lisa" do passo 4 do *Ao
> receber a arte*. As duas defesas escritas nos prompts - trama grossa o
> bastante para o fio individual se ler, e uma queda da luz para a sombra numa
> das bordas - resolveram com folga: os três arquivos couberam em **q86, o
> degrau mais alto da escada**, sem descer um passo. `malha-alta` 623 KB de 900,
> `malha-larga` 510 KB de 640, `malha-media` 174 KB de 190.
>
> As medidas do `verificar.py` também passaram folgadas: metade reservada com
> média 0,008 na deitada e 0,028 na em pé (teto 0,09), e matiz 175° e 164°
> (faixa 148-196). A metade reservada da deitada é a **mais calma das quatro**
> do site - o título assenta bem nela. A da em pé é a mais agitada, no mesmo
> patamar da do papel, que já estava publicada.
>
> **Duas coisas para quem regerar.** Primeira: as duas voltaram com desfoque -
> a em pé amolece no topo, a deitada no canto superior esquerdo e na borda
> direita -, contra o "sem desfoque" que os prompts pedem com todas as letras.
> Aceitou-se porque ali o desfoque faz o trabalho da margem lisa, e não a mancha
> que a regra teme; não é licença para o quadro inteiro amolecer. Segunda: os
> dois eixos vieram com 11° de diferença de matiz entre si, e eles aparecem lado
> a lado - lâmina no site, chapa no feed. Se der para casar melhor, melhor.
>
> Se algum dia o `receber.py` recusar uma regeração, é aqui que se mexe:
> engrossar mais a trama, nunca retocar a imagem.

### 1. Malha de aço - deitada

```
Create a photorealistic macro photograph of a taut sheet of woven steel wire
mesh, the kind used as an industrial sieve, filling the entire frame. The weave
runs slightly diagonally across the image, coarse enough that each individual
wire reads clearly and the square openings between the wires are plainly
visible. A hard raking light from the right grazes the mesh, so every crossing
of one wire over another casts its own small shadow. Nothing is visible through
the openings, only darkness. Studio, black background, no props, no frame, rim
or selvage around the mesh.

Composition: extreme close-up, no recognisable scale, the weave bleeding off all
four edges. Aspect ratio 16:9. The left half of the frame falls into near-black
and runs the full height of the picture, top edge to bottom edge, where a title
will be set later in warm off-white. The light falls off smoothly into shadow at
the far right edge as well, leaving a calm unbusy margin there. Nothing of
interest sits in the top quarter or the bottom quarter: the picture will be
cropped to a wide 3.2:1 band and must still read after that crop. Shot with a
macro lens at f/11, deep depth of field - everything in the frame is in sharp
focus, front to back, with no blur anywhere.

Style: sober low-key editorial photography, dark overall. The shadows carry one
colour and one only: a deep, desaturated pine green that leans blue, hue around
170 degrees, close to hex #245C53. Not cyan, not emerald, not olive, not steel
blue. Low saturation throughout, no glow, no lens flare, no bokeh, no added
vignette. At least 3000 pixels on the long edge.

Do not include: any text, letters, numbers, objects, hands, people, faces, logos
or brand marks. No blurred areas, no shallow depth of field. No colour other
than that pine green and neutral greys.
```

### 2. Malha de aço - em pé

```
Create a photorealistic macro photograph of a taut sheet of woven steel wire
mesh, the kind used as an industrial sieve, filling the entire frame. The weave
runs slightly diagonally across the image, coarse enough that each individual
wire reads clearly and the square openings between the wires are plainly
visible. A hard raking light from above grazes the mesh, so every crossing of
one wire over another casts its own small shadow. Nothing is visible through the
openings, only darkness. Studio, black background, no props, no frame, rim or
selvage around the mesh.

Composition: extreme close-up, no recognisable scale, the weave bleeding off all
four edges. Aspect ratio 3:4, portrait. The bottom half of the frame falls into
near-black and runs the full width of the picture, left edge to right edge,
where a title will be set later in warm off-white. The light falls off smoothly
into shadow at the top edge as well, leaving a calm unbusy margin there. Nothing
of interest sits in the left eighth or the right eighth: the picture will be
cropped to 4:5 and must still read after that crop. Shot with a macro lens at
f/11, deep depth of field - everything in the frame is in sharp focus, front to
back, with no blur anywhere.

Style: sober low-key editorial photography, dark overall. The shadows carry one
colour and one only: a deep, desaturated pine green that leans blue, hue around
170 degrees, close to hex #245C53. Not cyan, not emerald, not olive, not steel
blue. Low saturation throughout, no glow, no lens flare, no bokeh, no added
vignette. At least 3000 pixels on the long edge.

Do not include: any text, letters, numbers, objects, hands, people, faces, logos
or brand marks. No blurred areas, no shallow depth of field. No colour other
than that pine green and neutral greys.
```

---

## Ao receber a arte

1. `python _ferramentas/receber.py <motivo> <deitada.jpg> <em-pe.jpg>` - direto do Downloads,
   sem passo intermediario. Ele produz os tres arquivos que o site usa
   (`-media`, `-larga`, `-alta`), redimensiona, comprime ate caber no
   orcamento de peso e apaga o metadado. Nao recorta e nao clareia: enquadramento
   e luz sao decisao do prompt.
2. `python _ferramentas/og.py` refaz as chapas, e `python _ferramentas/montar.py` mede a foto: matiz do verde contra `--acento`,
   luminância da metade reservada, e recusa foto que não exista para um escrito
   publicado.
3. Se o verde vier ciano, ou a metade reservada vier clara, é o prompt que se
   corrige aqui - não a imagem num editor. Imagem retocada à mão não se
   reproduz na próxima geração.
4. Se o `receber.py` disser que não coube no teto nem na qualidade mais baixa, a
   foto é densa demais para o lugar: textura de ponta a ponta, sem área lisa.
   Isso também é conversa de prompt.
