# Overlay UI : carte « Paiement titre restaurant / carte wallet »

Carte en verre dépoli animée, fond transparent, à poser sur une vidéo pendant le montage.
Elle reprend le style de la référence : une petite goutte se transforme en carte, les lignes arrivent une par une (spinner puis coche), et à la fin la carte se floute et se rétracte.

Durée 7 s · 30 i/s · 1260 × 1260 px (carte ≈ 990 px de large, nette jusqu'en 4K).

## Fichiers (`exports/`)

| Fichier | Usage |
|---|---|
| `carte_paiement_alpha_prores4444.mov` | **À utiliser en priorité.** ProRes 4444 avec transparence (Premiere, After Effects, Final Cut, DaVinci, CapCut desktop). |
| `carte_paiement_alpha_sans_perte.mov` | Même animation, codec PNG sans perte, avec transparence (si le ProRes pose problème). |
| `carte_paiement_alpha.webm` | VP9 avec transparence, léger (web, CapCut, Canva). |
| `carte_paiement_masque_flou.mov` | Masque blanc de la forme de la carte, synchronisé, pour l'effet « verre dépoli » (voir ci-dessous). |
| `carte_paiement_capcut.mov` | Version allégée (840 px) du ProRes 4444 avec transparence, pour CapCut. |
| `carte_paiement_capcut_fond_noir.mp4` | Solution de secours pour CapCut : carte sur fond noir, à mettre en mode de fusion « Écran ». |
| `carte_paiement_finale.png` | Image fixe de la carte complète, fond transparent. |

## Obtenir le flou « verre dépoli »

Le flou d'arrière-plan dépend de ce qu'il y a derrière la carte, donc il ne peut pas être intégré dans un fichier transparent. Il se fait au montage en 30 secondes :

1. Piste 1 : ta vidéo.
2. Piste 2 : une copie de ta vidéo avec un **flou gaussien** (≈ 30–40) et une luminosité légèrement augmentée.
3. Piste 3 : `carte_paiement_masque_flou.mov`, utilisé comme **cache alpha / track matte** de la piste 2.
4. Piste 4 : `carte_paiement_alpha_prores4444.mov` par-dessus.

Les pistes 3 et 4 doivent avoir la même position et la même échelle. Sans cette étape, la carte reste lisible : elle sera simplement translucide, sans flou.

## Modifier le texte ou le timing

Tout est dans `src/card.html` (tableau `ITEMS` : texte + instant d'apparition).
Aperçu dans un navigateur : `src/card.html?preview&play`.
Pour régénérer les exports : `node src/render.js exports 30 3` (Playwright + ffmpeg).
