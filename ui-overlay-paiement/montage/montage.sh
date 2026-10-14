#!/usr/bin/env bash
# Incruste la carte (avec flou verre dépoli) sur une vidéo 1280x720.
# Usage : ./montage.sh video_source.mp4 [début_s] [sortie.mp4]
set -euo pipefail
cd "$(dirname "$0")/.."
SRC="$1"; T="${2:-19.7}"; OUT="${3:-montage/video_finale.mp4}"
S=382      # taille du canevas de la carte (carte ≈ 300 px de large)
X=889; Y=85  # position : en haut à droite
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC")
ffmpeg -v error -y -i "$SRC" -i exports/carte_paiement_masque_flou.mov -i exports/carte_paiement_alpha_sans_perte.mov -filter_complex "\
[0:v]split[bg][bg2];\
[bg2]gblur=sigma=16,eq=brightness=0.035[blur];\
color=black:s=1280x720:r=30:d=$DUR[blk];\
[1:v]scale=$S:$S,format=rgba,setpts=PTS+$T/TB[mt];\
[blk][mt]overlay=$X:$Y:eof_action=pass:format=auto,format=gray[mask];\
[bg][blur][mask]maskedmerge[glass];\
[2:v]scale=$S:$S:flags=lanczos,format=rgba,setpts=PTS+$T/TB[card];\
[glass][card]overlay=$X:$Y:eof_action=pass:format=auto,format=yuv420p[out]" \
  -map "[out]" -map 0:a? -c:v libx264 -crf 18 -preset slow -c:a copy -t "$DUR" -movflags +faststart "$OUT"
echo "OK → $OUT"
