请在当前目录 /sources/luna-rio 下，基于 assets/reference/luna-rio-character-reference.jpg 和 script-001.md，制作 3 个各 10 秒、竖屏 9:16 的 mp4 视频片段：

输出路径必须是：
- clips/clip01.mp4
- clips/clip02.mp4
- clips/clip03.mp4

要求：
1. 每段 10 秒，1080x1920，H.264，30fps，无音频或静音均可。
2. 使用参考图保持 Luna Rio 视觉一致性；如果不能生成新视频素材，就用参考图通过 ffmpeg 做 Ken Burns 动效、叠加文字、光效/暗色科技感背景。
3. 每段叠加大号中文字幕：
   - clip01：我没有模特 / 没有摄影师 / 没有团队
   - clip02：我创造了一个 AI 虚拟网红 / 她叫 Luna Rio
   - clip03：90 天挑战 / 从 0 到 $1000
4. 视觉风格：dark premium tech aesthetic, cinematic lighting, documentary influencer teaser, YouTube Shorts.
5. 完成后用 ffprobe 验证三个文件时长约 10 秒，并输出结果。

请直接执行，不要只写方案。