#!/usr/bin/env bash
set -euo pipefail
mkdir -p clips final audio
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
REF="assets/reference/luna-rio-character-reference.jpg"

ffmpeg -y -loop 1 -i "$REF" -t 10 \
-vf "scale=-1:2160,crop=1215:2160:(iw-1215)/2:(ih-2160)/2,zoompan=z='min(zoom+0.0015,1.08)':d=300:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,eq=contrast=1.08:brightness=-0.03:saturation=1.12,drawbox=x=0:y=0:w=iw:h=ih:color=black@0.22:t=fill,drawtext=fontfile=${FONT}:text='我没有模特':x=(w-text_w)/2:y=1220:fontsize=76:fontcolor=white:borderw=4:bordercolor=black@0.7,drawtext=fontfile=${FONT}:text='没有摄影师':x=(w-text_w)/2:y=1320:fontsize=76:fontcolor=white:borderw=4:bordercolor=black@0.7,drawtext=fontfile=${FONT}:text='没有团队':x=(w-text_w)/2:y=1420:fontsize=76:fontcolor=white:borderw=4:bordercolor=black@0.7" \
-an -c:v libx264 -pix_fmt yuv420p -r 30 clips/clip01.mp4

ffmpeg -y -loop 1 -i "$REF" -t 10 \
-vf "scale=-1:2300,crop=1294:2300:(iw-1294)/2:(ih-2300)/2,zoompan=z='1.08-0.0002*on':d=300:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,eq=contrast=1.12:brightness=-0.02:saturation=1.18,drawbox=x=0:y=0:w=iw:h=ih:color=black@0.18:t=fill,drawtext=fontfile=${FONT}:text='我创造了一个':x=(w-text_w)/2:y=1220:fontsize=72:fontcolor=white:borderw=4:bordercolor=black@0.7,drawtext=fontfile=${FONT}:text='AI 虚拟网红':x=(w-text_w)/2:y=1320:fontsize=86:fontcolor=0xE9D5FF:borderw=4:bordercolor=black@0.8,drawtext=fontfile=${FONT}:text='她叫 Luna Rio':x=(w-text_w)/2:y=1440:fontsize=78:fontcolor=white:borderw=4:bordercolor=black@0.7" \
-an -c:v libx264 -pix_fmt yuv420p -r 30 clips/clip02.mp4

ffmpeg -y -loop 1 -i "$REF" -t 10 \
-vf "scale=-1:2160,crop=1215:2160:(iw-1215)/2:(ih-2160)/2,zoompan=z='1.02+0.0009*on':d=300:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,eq=contrast=1.15:brightness=-0.04:saturation=1.1,drawbox=x=0:y=0:w=iw:h=ih:color=black@0.28:t=fill,drawtext=fontfile=${FONT}:text='90 天挑战':x=(w-text_w)/2:y=1200:fontsize=92:fontcolor=0xFDE68A:borderw=5:bordercolor=black@0.8,drawtext=fontfile=${FONT}:text='从 0 到 \$1000':x=(w-text_w)/2:y=1330:fontsize=86:fontcolor=white:borderw=5:bordercolor=black@0.8,drawtext=fontfile=${FONT}:text='公开记录全过程':x=(w-text_w)/2:y=1450:fontsize=62:fontcolor=white:borderw=4:bordercolor=black@0.7" \
-an -c:v libx264 -pix_fmt yuv420p -r 30 clips/clip03.mp4

printf "file '%s'\nfile '%s'\nfile '%s'\n" "$PWD/clips/clip01.mp4" "$PWD/clips/clip02.mp4" "$PWD/clips/clip03.mp4" > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy final/luna-rio-001-video-only.mp4

# Stretch voice to 30s and mix with final video.
VOICE="audio/luna-rio-001-voice.mp3"
ffmpeg -y -i "$VOICE" -filter:a "atempo=0.774" audio/luna-rio-001-voice-30s.mp3
ffmpeg -y -i final/luna-rio-001-video-only.mp4 -i audio/luna-rio-001-voice-30s.mp3 -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest final/luna-rio-001-short.mp4

for f in clips/clip01.mp4 clips/clip02.mp4 clips/clip03.mp4 final/luna-rio-001-short.mp4; do
  echo "--- $f"
  ffprobe -v error -show_entries stream=width,height,codec_name,r_frame_rate -show_entries format=duration -of default=nw=1 "$f"
done
