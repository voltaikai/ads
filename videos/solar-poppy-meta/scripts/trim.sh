#!/bin/bash
# Keep segments (frame-aligned, 30fps). Each removed span leaves ~0.22s of natural pause.
set -e
cd "$(dirname "$0")/.."
SRC=source/aroll-original.mp4
S="0:26.033333 26.366667:41.333333 41.633333:45.5 45.866667:49.166667"
F=""; i=0; V=""; A=""
for seg in $S; do a=${seg%:*}; b=${seg#*:}
  F+="[0:v]trim=start=$a:end=$b,setpts=PTS-STARTPTS[v$i];"
  F+="[0:a]atrim=start=$a:end=$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.008,areverse,afade=t=in:d=0.008,areverse[a$i];"
  V+="[v$i]"; A+="[a$i]"; i=$((i+1)); done
F+="${V}concat=n=$i:v=1:a=0[vout];${A}concat=n=$i:v=0:a=1,aresample=48000[aout]"
ffmpeg -hide_banner -loglevel error -y -i $SRC -filter_complex "$F" -map "[vout]" -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -r 30 -an assets/aroll-trimmed.mp4 -map "[aout]" -c:a pcm_s24le work/voice-raw.wav
