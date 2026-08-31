# Prompts das figuras

Desde 30/08/2026 toda figura do site é fotografia gerada, não desenho de script.
Estes prompts são a origem dessas imagens, do mesmo jeito que `guilhoche.py` era
a origem das anteriores - e por isso moram no repositório. Prompt que vive só
numa conversa de gerador não é recuperável: quando a arte precisar de retoque,
não há a que voltar.

## Regras que valem para os seis

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
| `telas-sistemicas` | vidro canelado | `ativos/img/vidro-larga.jpg` · `vidro-alta.jpg` |
| `sumula-479` | bordas de papel | `ativos/img/papel-larga.jpg` · `papel-alta.jpg` |
| `tema-929` | ardósia | `ativos/img/ardosia-larga.jpg` · `ardosia-alta.jpg` |

---

## 1. Vidro canelado - deitada

```
Create a photorealistic macro photograph of a thick panel of fluted reeded
glass, the kind used in a door, filling the entire frame. Its vertical ribs run
slightly diagonally across the image, and a single distant light source behind
the glass, placed to the right, is refracted by each rib into a soft vertical
band of pale light. No object is visible behind the glass, only light. Studio,
black background, no props.

Composition: extreme close-up, no recognisable scale, the ribs bleeding off all
four edges. Aspect ratio 16:9. The left half of the frame falls into near-black
and runs the full height of the picture, top edge to bottom edge, where a title
will be set later in warm off-white. Nothing of interest sits in the top quarter
or the bottom quarter: the picture will be cropped to a wide 3.2:1 band and must
still read after that crop. Shot with a macro lens at f/11, deep depth of field
- everything in the frame is in sharp focus, front to back, with no blur
anywhere.

Style: sober low-key editorial photography, dark overall. The shadows carry one
colour and one only: a deep, desaturated pine green that leans blue, hue around
170 degrees, close to hex #245C53. Not cyan, not emerald, not olive, not steel
blue. Low saturation throughout, no glow, no lens flare, no bokeh, no added
vignette. At least 3000 pixels on the long edge.

Do not include: any text, letters, numbers, objects, hands, people, faces, logos
or brand marks. No blurred areas, no shallow depth of field. No colour other
than that pine green and neutral greys.
```

## 2. Vidro canelado - em pé

```
Create a photorealistic macro photograph of a thick panel of fluted reeded
glass, the kind used in a door, filling the entire frame. Its ribs run
horizontally, slightly diagonally across the image, and a single distant light
source behind the glass, placed above, is refracted by each rib into a soft band
of pale light. No object is visible behind the glass, only light. Studio, black
background, no props.

Composition: extreme close-up, no recognisable scale, the ribs bleeding off all
four edges. Aspect ratio 3:4, portrait. The bottom half of the frame falls into
near-black and runs the full width of the picture, left edge to right edge,
where a title will be set later in warm off-white. Nothing of interest sits in
the left eighth or the right eighth: the picture will be cropped to 4:5 and must
still read after that crop. Shot with a macro lens at f/11, deep depth of field
- everything in the frame is in sharp focus, front to back, with no blur
anywhere.

Style: sober low-key editorial photography, dark overall. The shadows carry one
colour and one only: a deep, desaturated pine green that leans blue, hue around
170 degrees, close to hex #245C53. Not cyan, not emerald, not olive, not steel
blue. Low saturation throughout, no glow, no lens flare, no bokeh, no added
vignette. At least 3000 pixels on the long edge.

Do not include: any text, letters, numbers, objects, hands, people, faces, logos
or brand marks. No blurred areas, no shallow depth of field. No colour other
than that pine green and neutral greys.
```

## 3. Bordas de papel - deitada

```
Create a photorealistic macro photograph of the cut edges of a thick stack of
uncoated paper, seen almost edge-on, so that each individual sheet reads as a
fine parallel line and the stack fills the entire frame. A hard raking light
from the right grazes across the edges, catching the fibre of the paper. Studio,
black background, no props, no printing on the paper.

Composition: extreme close-up, no recognisable scale, the lines running
diagonally and bleeding off all four edges. Aspect ratio 16:9. The left half of
the frame falls into near-black and runs the full height of the picture, top
edge to bottom edge, where a title will be set later in warm off-white. Nothing
of interest sits in the top quarter or the bottom quarter: the picture will be
cropped to a wide 3.2:1 band and must still read after that crop. Shot with a
macro lens at f/11, deep depth of field - everything in the frame is in sharp
focus, front to back, with no blur anywhere.

Style: sober low-key editorial photography, dark overall. The shadows carry one
colour and one only: a deep, desaturated pine green that leans blue, hue around
170 degrees, close to hex #245C53. Not cyan, not emerald, not olive, not steel
blue. Low saturation throughout, no glow, no lens flare, no bokeh, no added
vignette. At least 3000 pixels on the long edge.

Do not include: any text, letters, numbers, printing, objects, hands, people,
faces, logos or brand marks. No blurred areas, no shallow depth of field. No
colour other than that pine green and neutral greys.
```

## 4. Bordas de papel - em pé

```
Create a photorealistic macro photograph of the cut edges of a thick stack of
uncoated paper, seen almost edge-on, so that each individual sheet reads as a
fine parallel line and the stack fills the entire frame. A hard raking light
from above grazes across the edges, catching the fibre of the paper. Studio,
black background, no props, no printing on the paper.

Composition: extreme close-up, no recognisable scale, the lines running
diagonally and bleeding off all four edges. Aspect ratio 3:4, portrait. The
bottom half of the frame falls into near-black and runs the full width of the
picture, left edge to right edge, where a title will be set later in warm
off-white. Nothing of interest sits in the left eighth or the right eighth: the
picture will be cropped to 4:5 and must still read after that crop. Shot with a
macro lens at f/11, deep depth of field - everything in the frame is in sharp
focus, front to back, with no blur anywhere.

Style: sober low-key editorial photography, dark overall. The shadows carry one
colour and one only: a deep, desaturated pine green that leans blue, hue around
170 degrees, close to hex #245C53. Not cyan, not emerald, not olive, not steel
blue. Low saturation throughout, no glow, no lens flare, no bokeh, no added
vignette. At least 3000 pixels on the long edge.

Do not include: any text, letters, numbers, printing, objects, hands, people,
faces, logos or brand marks. No blurred areas, no shallow depth of field. No
colour other than that pine green and neutral greys.
```

## 5. Ardósia - deitada

> O original mandava a luz da esquerda e reservava a metade direita. Como o
> título mora sempre à esquerda, os dois foram invertidos aqui.

```
Create a photorealistic macro photograph of the surface of a slab of dark slate,
filling the entire frame: fine mineral grain, the shallow steps where the stone
was split, and one thin pale vein running diagonally across it. A hard raking
light from the right grazes the surface, so every texture casts its own small
shadow. Studio, no props.

Composition: extreme close-up, flat-on view, no recognisable scale, the surface
bleeding off all four edges. Aspect ratio 16:9. The left half of the frame falls
into near-black and runs the full height of the picture, top edge to bottom
edge, where a title will be set later in warm off-white. Nothing of interest
sits in the top quarter or the bottom quarter, and the pale vein stays out of
the left half: the picture will be cropped to a wide 3.2:1 band and must still
read after that crop. Shot with a macro lens at f/11, deep depth of field -
everything in the frame is in sharp focus, front to back, with no blur anywhere.

Style: sober low-key editorial photography, dark overall. The shadows carry one
colour and one only: a deep, desaturated pine green that leans blue, hue around
170 degrees, close to hex #245C53. Not cyan, not emerald, not olive, not steel
blue. Low saturation throughout, no glow, no lens flare, no bokeh, no added
vignette. At least 3000 pixels on the long edge.

Do not include: any text, letters, numbers, objects, hands, people, faces, logos
or brand marks. No blurred areas, no shallow depth of field. No colour other
than that pine green and neutral greys.
```

## 6. Ardósia - em pé

```
Create a photorealistic macro photograph of the surface of a slab of dark slate,
filling the entire frame: fine mineral grain, the shallow steps where the stone
was split, and one thin pale vein running diagonally across it. A hard raking
light from above grazes the surface, so every texture casts its own small
shadow. Studio, no props.

Composition: extreme close-up, flat-on view, no recognisable scale, the surface
bleeding off all four edges. Aspect ratio 3:4, portrait. The bottom half of the
frame falls into near-black and runs the full width of the picture, left edge to
right edge, where a title will be set later in warm off-white. Nothing of
interest sits in the left eighth or the right eighth, and the pale vein stays
out of the bottom half: the picture will be cropped to 4:5 and must still read
after that crop. Shot with a macro lens at f/11, deep depth of field -
everything in the frame is in sharp focus, front to back, with no blur anywhere.

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
