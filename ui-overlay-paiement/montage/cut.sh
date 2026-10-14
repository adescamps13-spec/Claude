#!/usr/bin/env bash
# Coupe les faux raccords de la vidéo boulangerie (30 i/s, numéros d'image source).
#  1. 0–8     : une main apparaît au milieu de l'image → on démarre à l'image 9
#  2. 166–182 : la boulangère se tourne vers la gauche puis réapparaît tournée vers la droite → coupé
#  3. 366–385 : le sac se replie instantanément (glitch) → coupé, on enchaîne sur le plan plus large
#  4. 515     : saut de cadre entre deux plans quasi identiques → fondu enchaîné de 0,3 s
# Usage : ./cut.sh video_source.mp4 [sortie.mp4]
set -euo pipefail
SRC="$1"; OUT="${2:-$(dirname "$0")/video_sans_faux_raccords.mp4}"
F=30; XF=0.3
seg() { # $1 label, $2 image début, $3 image fin (exclue ou vide = fin)
  local s e
  s=$(printf "%.6f" "$(echo "$2/$F" | bc -l)")
  if [ -n "$3" ]; then
    e=$(printf "%.6f" "$(echo "$3/$F" | bc -l)")
    echo "[0:v]trim=start_frame=$2:end_frame=$3,setpts=PTS-STARTPTS[v$1];[0:a]atrim=start=$s:end=$e,asetpts=PTS-STARTPTS,afade=t=in:d=0.01,areverse,afade=t=in:d=0.01,areverse[a$1];"
  else
    echo "[0:v]trim=start_frame=$2,setpts=PTS-STARTPTS[v$1];[0:a]atrim=start=$s,asetpts=PTS-STARTPTS,afade=t=in:d=0.01[a$1];"
  fi
}
D123=$(printf "%.6f" "$(echo "(157+183+129)/$F - $XF" | bc -l)")
FC="$(seg 1 9 166)$(seg 2 183 366)$(seg 3 386 515)$(seg 4 515 '')
[v1][a1][v2][a2][v3][a3]concat=n=3:v=1:a=1[v123][a123];
[v123][v4]xfade=transition=fade:duration=$XF:offset=$D123,format=yuv420p[v];
[a123][a4]acrossfade=d=$XF[a]"
ffmpeg -v error -y -i "$SRC" -filter_complex "$FC" -map "[v]" -map "[a]" \
  -c:v libx264 -crf 14 -preset slow -c:a aac -b:a 192k -movflags +faststart "$OUT"
echo "OK → $OUT"
