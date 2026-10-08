---
format: 1920x1080
duration: 100s
message: "Les meilleurs experts pour votre projet, coordonnés par un partenaire de confiance : Relax construit l'organisation autour du projet et absorbe la complexité pour le client."
arc: Chaos hérité → le vrai sujet → Comprendre → Révéler → Organiser → Exprimer → Déployer (exponentiel) → la méthode Relax → tourbillon → respiration → logo Relax
audience: Dirigeants et directions marketing/communication, prospects de l'agence Relax (site + réseaux sociaux)
mode: collaborative
---

# Storyboard v2 — Relax × Finaxy

**Ce film dit aux dirigeants et directions marketing que Relax réunit et coordonne, sans couture, les
meilleurs experts autour de leur projet — pour qu'eux n'aient plus à gérer la complexité.**

- **Format :** 1920×1080, ~100 s estimés (somme des beats : 102,5 s) (VO réelle décidera), voix off FR Gemini « Algieba », fond musical
  ambient discret, sound design sur le fil, respiration finale. Déclinaison 4:5 ensuite.
- **DA :** le film parle en Relax (fond blanc et lavis pastel du site, Unbounded + DM Sans, frame.md) ;
  l'identité Finaxy (marine, crème, bordeaux, serif) n'apparaît que sur les livrables montrés.
- **Spine — le fil :** le ruban lavande du site Relax, aplati en une ligne, traverse tout le film sans
  jamais être coupé. Sa tête est le point rose du logo relax•. Chaque contact aligne l'élément suivant
  (effet domino). Le monde glisse vers la gauche, le fil continue vers la droite. À la fin, le fil expire
  et devient le point du logo.
- **Courbe d'énergie :** frénétique au début (dérive rapide, saccades), puis chaque scène plus lente et
  plus posée que la précédente — sauf le déploiement (accélération exponentielle maîtrisée), puis le
  tourbillon, puis le calme total de la respiration.
- **Held frames :** Frame 05 (« L'intelligence collective du risque. » — rien ne bouge) et Frame 12
  (inspiration retenue avant l'expiration).
- **Bans :** pas d'effet catalogue, pas d'anglais à l'écran (sauf « naming », « Team player »), pas de faux
  site ni de fausse interface (captures réelles ou placeholders étiquetés), pas de glow sur le texte.
  Échecs de motion à éviter : le diaporama (chaque beat une nouvelle carte) et l'écran de veille.

## Changes from v1

- « Dans la narration je pense qu'il faut dire que ca va au dela d'un simple pb de logo mais qu'on se parle
  plutot d'un pb de cohérence globale. » → VO Frame 2 réécrite.
- « vu que c'est un case relax, le fond de la DA devrait etre une DA relax plutot que Finaxy. Mais on
  illustre bien dans la video la DA qu'on a mis en place pour finaxy. » → frame.md réécrit (Relax = film,
  Finaxy = artefacts).
- Frame 6 : les 3 verticales réelles de finaxy.com. Frame 12 : vrai logo relax• (relax-agency.com).

## Still open

- Signature finale optionnelle « Maintenant, relax, on s'occupe du reste. » (site Relax) — oui / non.
- Ancien site Finaxy : web.archive.org très instable et peu de captures récentes de finaxy.com — à réessayer
  au build, ou captures à fournir.
- Visuels réels des supports (plaquettes B2B, kakemonos, cartes de visite, masques de présentation,
  cartes de vœux, LinkedIn) et de l'agent IA — placeholders étiquetés en attendant.
- `GEMINI_API_KEY` pour la voix Algieba.
- Respiration finale : enregistrement réel (banque de sons) vs synthèse — à valider à l'écoute.

## Frame 1 — Chaos hérité

- scene: Des dizaines de nœuds épars dérivent vite ; noms de cabinets, expertises, sigles ; ancien logo FINAXY GROUP au milieu ; « 12 000 » s'inscrit
- duration: 9s
- transition_in: cut
- status: built
- src: compositions/01-chaos.html
- voiceover: "Finaxy avait grandi vite. Très vite. Des acquisitions, des cabinets, des expertises, des marques… Plus de douze mille entreprises clientes."
- motion: rules — drift-jitter, stagger-pop, count-up
- poster: 6s

Hero prop : les nœuds (ils reviennent dans chaque scène, de plus en plus ordonnés). Couleur « avant »
#5E7891. L'ancien logo est un nœud parmi d'autres, sans hiérarchie. « Plus de 12 000 entreprises
clientes » arrive en compteur Manrope. Pas de fil encore. Why : poser la puissance ET la complexité.

## Frame 2 — Le vrai sujet

- scene: « Bien au-delà d'un simple problème de logo. » barré ; « Un problème de cohérence globale. » en Unbounded ; le fil entre par le bas-gauche et touche le premier nœud qui cesse de trembler
- duration: 9s
- transition_in: cut
- status: built
- src: compositions/02-coherence.html
- voiceover: "Mais l'enjeu allait bien au-delà d'un simple problème de logo. C'était un problème de cohérence globale. Le défi : simplifier, sans appauvrir."
- motion: rules — strike-through, line-draw, settle
- poster: 7s

« simplifier, sans appauvrir » : les nœuds se rapprochent mais gardent tous leur nom (rien ne disparaît).
Why : recadrer le problème — ce n'est pas un rebranding, c'est un problème de cohérence.

## Frame 3 — Comprendre

- scene: Le fil passe de nœud en nœud ; à chaque contact un mot d'enquête apparaît : dirigeants, collaborateurs, métiers, marché ; étape « 01 Comprendre » en haut à gauche
- duration: 8s
- transition_in: thread-carry
- status: built
- src: compositions/03-comprendre.html
- voiceover: "Alors on a commencé par écouter. Dirigeants, collaborateurs, métiers, marché. Pour comprendre ce que Finaxy était vraiment."
- motion: rules — line-draw, node-ping, label-reveal
- poster: 6s

Chaque contact = un ping bordeaux. Le rail d'étapes (01 → 05) en haut s'installe ici et persistera.
Why : première décision de la chaîne — on ne propose rien avant d'avoir compris.

## Frame 4 — Révéler : la singularité

- scene: Les nœuds se regroupent en réseau maillé ; deux pôles — « La force d'un groupe. » / « L'esprit d'un cabinet. » — reliés par le fil ; étape 02
- duration: 9s
- transition_in: thread-carry
- status: built
- src: compositions/04-reveler.html
- voiceover: "Et une singularité est apparue. La force d'un groupe. L'esprit d'un cabinet. Face à des risques multiples, aucune expertise isolée ne suffit."
- motion: rules — network-form, split-reveal, connect
- poster: 6s

Le réseau reprend le motif du deck plateforme (nœuds connectés). Les nœuds passent du bleu « avant » au
crème. Why : la révélation — ce que Finaxy peut légitimement revendiquer.

## Frame 5 — L'intelligence collective du risque (held)

- scene: Plein cadre, serif 160px : « L'intelligence collective du risque. » ; le réseau, immobile, en arrière-plan ; le fil s'arrête dessous
- duration: 4.5s
- transition_in: crossfade
- status: built
- src: compositions/05-intelligence.html
- voiceover: "Finaxy, c'est l'intelligence collective du risque."
- motion: held frame — seule l'entrée du texte (mask-up 0.8s), puis rien
- poster: 3s

Le principe qui organise tout le reste. Why : la big idea, posée comme une évidence.

## Frame 6 — Organiser : l'architecture

- scene: Le réseau se range sous le logo Finaxy en 3 verticales réelles (finaxy.com) : « Entreprises & institutions », « Affinitaire & partenariats », « Clientèle privée », chacune avec ses offres ; marques autonomes conservées en pointillé ; étape 03
- duration: 10.5s
- transition_in: thread-carry
- status: built
- src: compositions/06-organiser.html
- voiceover: "Cette idée est devenue un principe d'organisation. Architecture, verticales, naming, place de chaque marque : le groupe, lui aussi, est devenu lisible."
- motion: rules — flip-reorder, tree-grow, label-reveal
- poster: 8s

Les mêmes nœuds qu'en Frame 1 (callback) — mais rangés. Certaines marques acquises restent autonomes
(liées en pointillé), d'autres intègrent le système. Verticales et offres reprises de finaxy.com. Why : la plateforme
devient principe d'organisation — « complexe → intelligible ».

## Frame 7 — Exprimer : logo, identité, voix

- scene: L'ancien logo FINAXY GROUP s'efface ; sur un panneau marine Finaxy, le nouveau « Finaxy » crème se dessine et le fil, en passant, signe la virgule bordeaux ; quatre traits en orbite : Ancré · Architecte · Team player · Pédagogue ; étape 04
- duration: 8s
- transition_in: thread-carry
- status: built
- src: compositions/07-exprimer.html
- voiceover: "Puis elle a pris corps. Un logo, une identité, une voix. Plus de stature, sans rien perdre d'humain."
- motion: rules — morph-dissolve, svg-draw, orbit-labels
- poster: 6s

Moment signature : le fil Relax signe la virgule bordeaux du logo Finaxy. Why : la stratégie prend corps
— la marque exprime sa nouvelle stature.

## Frame 8 — Déployer : l'exponentielle

- scene: 1 support → 2 → 4 → 8 → 16 → mur de supports ; libellés : plaquettes B2B, kakemonos, cartes de visite, masques de présentation, cartes de vœux, LinkedIn, nouveau site, agent IA ; compteur ×2 ; étape 05
- duration: 12s
- transition_in: thread-carry
- status: built
- src: compositions/08-deployer.html
- voiceover: "Et le système s'est mis à produire. Plaquettes, kakemonos, cartes de visite, présentations, cartes de vœux, LinkedIn, le nouveau site… Jusqu'à un agent IA, pour que chacun écrive comme Finaxy."
- motion: rules — doubling-grid, push-in, card-flip
- poster: 9s

Chaque doublement est relié au précédent par le fil (le système se reproduit, il ne s'empile pas). Les
supports sont des placeholders étiquetés tant que les visuels réels ne sont pas fournis. L'agent IA ferme
la séquence : une bulle de texte qui s'écrit dans la voix Finaxy. Why : un système qui produit de la
cohérence dans le temps, pas des guidelines rangées dans un tiroir.

## Frame 9 — La méthode Relax : la bonne équipe

- scene: Recul : le fil se dédouble ; au-dessus, une constellation d'experts en mouvement — stratégie, architecture de marque, naming, design, éditorial, production, IA — qui se relient ; au-dessous, une seule ligne calme
- duration: 9s
- transition_in: zoom-out
- status: built
- src: compositions/09-equipe.html
- voiceover: "Stratégie, architecture, naming, design, éditorial, production, IA. Pour chaque enjeu, Relax a réuni la bonne équipe. Et l'a fait jouer comme une seule."
- motion: rules — zoom-out, constellation, converge
- poster: 7s

Les disciplines s'allument dans l'ordre exact de la VO. Why : la singularité Relax n°1 — elle coordonne
elle-même les expertises.

## Frame 10 — Côté Relax / côté client

- scene: Écran partagé horizontal : « Côté Relax » (beaucoup de mouvement) / « Côté client » (un seul fil, immobile) ; « On construit l'équipe autour du projet. » ; « Aucune couture. »
- duration: 10.5s
- transition_in: thread-carry
- status: built
- src: compositions/10-sans-couture.html
- voiceover: "On ne fait pas entrer un projet dans une agence. On construit l'équipe autour du projet. Côté Relax, beaucoup de mouvement. Côté client, un seul fil. Aucune couture."
- motion: rules — split-horizontal, contrast-tempo, settle
- poster: 8s

Visualisation de « construire l'organisation autour du projet » : un carré rigide (l'agence) refuse le
projet, puis les experts se placent autour du projet. Why : la singularité Relax n°2 + le bénéfice client.

## Frame 11 — Tourbillon

- scene: Tous les éléments du film (nœuds, mots, supports, logo Finaxy, disciplines) tourbillonnent et s'agrègent vers le centre ; « Les meilleurs experts pour votre projet. » puis « Coordonnés par un partenaire de confiance. »
- duration: 6s
- transition_in: thread-carry
- status: built
- src: compositions/11-tourbillon.html
- voiceover: "Les meilleurs experts pour votre projet. Coordonnés par un partenaire de confiance."
- motion: rules — vortex, aggregate, text-mask-up
- poster: 4s

Callback de tout le film. Le tourbillon ralentit jusqu'à un point. Why : la promesse, formulée.

## Frame 12 — Respiration → Relax

- scene: Le point rose se dilate sur une grande inspiration (tout se suspend), puis l'expiration relâchée ouvre des ondes douces ; « relax » s'écrit et le point se pose à sa place dans le logo
- duration: 7s
- transition_in: cut
- status: built
- src: compositions/12-relax.html
- voiceover: "(respiration : grande inspiration, expiration relâchée)"
- motion: rules — breathe-scale, iris-open, logo-settle
- poster: 6s

Inspiration ~1.6 s (le point grossit lentement, held), expiration ~2.4 s (le cadre s'ouvre, fond ink →
lavis Relax), le logo relax• s'écrit sur la fin de l'expiration et le point se pose. Silence musical autour du souffle.
Why : le soulagement — la tranquillité d'esprit de confier son projet à Relax.
