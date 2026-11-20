"""Dựng video từ kịch bản, biểu đồ thực nghiệm và giọng đọc tiếng Việt."""
import argparse
import asyncio
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from gtts import gTTS
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent / 'iris-phan-loai'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VOICE = 'gTTS Vietnamese'
WIDTH, HEIGHT = 1280, 720
FONT_DIR = Path('C:/Windows/Fonts')


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_DIR / ('arialbd.ttf' if bold else 'arial.ttf')), size)


def wrapped(draw, text, size, width, bold=False):
    words, lines, current = text.split(), [], ''
    for word in words:
        candidate = (current + ' ' + word).strip()
        if current and draw.textlength(candidate, font=font(size, bold)) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def duration(path):
    result = subprocess.run([FFMPEG, '-i', str(path)], capture_output=True, text=True, encoding='utf-8')
    match = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', result.stderr)
    if not match:
        raise ValueError('Không đọc được thời lượng: ' + str(path))
    h, m, s = map(float, match.groups())
    return h * 3600 + m * 60 + s


def clock(seconds):
    ms = round(seconds * 1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'


def frame(scene, index, count, destination):
    image = Image.new('RGB', (WIDTH, HEIGHT), '#f5f8fb')
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH, 12), fill='#286b9a')
    draw.text((58, 34), scene['section'], font=font(20, True), fill='#286b9a')
    title_lines = wrapped(draw, scene['title'], 40, 1160, True)
    for n, line in enumerate(title_lines):
        draw.text((58, 72 + n * 47), line, font=font(40, True), fill='#172b3a')
    has_figure = 'figure' in scene or scene.get('dashboard')
    text_width = 452 if has_figure else 1110
    y = 178
    for line in scene['bullets']:
        for n, part in enumerate(wrapped(draw, line, 27, text_width)):
            if n == 0:
                draw.ellipse((60, y + 13, 67, y + 20), fill='#286b9a')
            draw.text((82, y), part, font=font(27), fill='#253948')
            y += 35
        y += 16
    if has_figure:
        source = (ROOT.parent / 'minh_chung/20_dashboard_tong_quan.jpg' if scene.get('dashboard')
                  else PROJECT / 'results/figures' / scene['figure'])
        plot = Image.open(source).convert('RGB')
        if scene.get('dashboard'):
            # Lấy phần đầu ảnh chụp thật để thấy bộ lọc, số mẫu và biểu đồ.
            plot = plot.crop((0, 0, plot.width, min(plot.height, 980)))
        plot.thumbnail((652, 405), Image.Resampling.LANCZOS)
        image.paste(plot, (570 + (652 - plot.width)//2, 172 + (405-plot.height)//2))
    draw.line((58, 598, 1222, 598), fill='#cdd9e2', width=2)
    draw.text((58, 575), 'CT999  ·  Iris  ·  Lê Văn Triệu và nhóm', font=font(17), fill='#526978')
    draw.text((1175, 575), f'{index+1}/{count}', font=font(17), fill='#526978')
    # Phụ đề nằm trong khoảng y=620..700, không che nội dung minh họa.
    image.save(destination)


async def synthesize(text, path):
    words, phrases = [], []
    for sentence in re.split(r'(?<=[.!?])\s+', text):
        current = ''
        for word in sentence.split():
            candidate = (current+' '+word).strip()
            if len(candidate)>64 and current:
                phrases.append(current)
                current = word
            else:
                current = candidate
        if current:
            phrases.append(current)
    with tempfile.TemporaryDirectory(prefix='ct999_voice_') as task_tmp:
        work = Path(task_tmp)
        cache = ROOT/'.tts_cache'
        cache.mkdir(exist_ok=True)
        base = 0
        for i, phrase in enumerate(phrases):
            destination = work/f'{i:02}.mp3'
            cache_id = hashlib.sha256((VOICE+phrase).encode('utf-8')).hexdigest()[:24]
            cached_audio = cache/f'{cache_id}.mp3'
            if cached_audio.exists():
                shutil.copy2(cached_audio,destination)
            else:
                gTTS(phrase,lang='vi',lang_check=False,timeout=20).save(str(destination))
                shutil.copy2(destination,cached_audio)
            length = duration(destination)
            # Mốc đầu/cuối của từng đoạn lấy từ âm thanh thật.
            # Thời gian từng từ trong đoạn được nội suy để ghép phụ đề ngắn.
            tokens = phrase.split()
            total = sum(len(word)+1 for word in tokens)
            elapsed = 0
            for word in tokens:
                part = (len(word)+1)/total
                words.append({'text':word,'offset':round((base+.08+elapsed*(length-.16))*1e7),
                              'duration':round(part*(length-.16)*1e7),'voice':VOICE,'phrase':i})
                elapsed += part
            base += length
        (work/'audio.txt').write_text('\n'.join(f"file '{i:02}.mp3'" for i in range(len(phrases))),encoding='utf-8')
        run([FFMPEG,'-y','-f','concat','-safe','0','-i','audio.txt','-c:a','libmp3lame','-b:a','128k',path],cwd=work)
    return words


def run(args, cwd=None):
    subprocess.run([str(x) for x in args], check=True, cwd=cwd, stdout=subprocess.DEVNULL,
                   stderr=subprocess.PIPE)


async def build():
    scenes = json.loads((ROOT/'kich_ban.json').read_text(encoding='utf-8'))
    assets, audio_dir = ROOT/'khung_hinh', ROOT/'am_thanh'
    assets.mkdir(exist_ok=True)
    audio_dir.mkdir(exist_ok=True)
    subtitles, offset, timeline, used_voices = [], 0.0, [], set()
    with tempfile.TemporaryDirectory(prefix='ct999_video_') as task_tmp:
        work = Path(task_tmp)
        # Font chỉ dùng khi dựng ở máy này, không phân phối font Windows.
        (work/'fonts').mkdir()
        shutil.copy2(FONT_DIR/'arial.ttf', work/'fonts/arial.ttf')
        for i, scene in enumerate(scenes):
            stem = f'{i+1:02}'
            still, audio = assets/f'{stem}.png', audio_dir/f'{stem}.mp3'
            boundary_path = audio_dir/f'{stem}_thoi_gian.json'
            source_path = audio_dir/f'{stem}_nguon.json'
            source = {'voice':VOICE,'text_sha256':hashlib.sha256(scene['narration'].encode('utf-8')).hexdigest()}
            frame(scene, i, len(scenes), still)
            if audio.exists() and boundary_path.exists() and source_path.exists() and json.loads(source_path.read_text(encoding='utf-8'))==source:
                boundaries = json.loads(boundary_path.read_text(encoding='utf-8'))
            else:
                boundaries = await synthesize(scene['narration'], audio)
                boundary_path.write_text(json.dumps(boundaries, ensure_ascii=False, indent=2), encoding='utf-8')
                source_path.write_text(json.dumps(source),encoding='utf-8')
            spoken = duration(audio)
            used_voices.update(b.get('voice',VOICE) for b in boundaries)
            speed = max(1.0,spoken/(scene['seconds']-.6))
            if speed>1.30:
                raise ValueError(f'Cần rút ngắn lời cảnh {i+1}: tốc độ yêu cầu {speed:.2f}.')
            length = scene['seconds']
            if offset + length > 180:
                raise ValueError('Video vượt ba phút. Cần rút kịch bản hoặc điều chỉnh tốc độ đọc.')
            # Gom theo từng đoạn âm thanh; tối đa 64 ký tự, 2 dòng.
            group = []
            for item in boundaries:
                if group and (item['phrase']!=group[-1]['phrase'] or len(' '.join(x['text'] for x in group+[item]))>64):
                    subtitles.append((offset+group[0]['offset']/1e7/speed,
                                      offset+(group[-1]['offset']+group[-1]['duration'])/1e7/speed+.04,
                                      ' '.join(x['text'] for x in group)))
                    group = []
                group.append(item)
            if group:
                subtitles.append((offset+group[0]['offset']/1e7/speed,
                                  offset+(group[-1]['offset']+group[-1]['duration'])/1e7/speed+.10,
                                  ' '.join(x['text'] for x in group)))
            part = work/f'{stem}.mp4'
            # Zoom nhẹ trên khung hình 16:9, giữ vùng phụ đề trống.
            vf = "scale=1344:756,crop=1280:720:x='32+12*sin(t/8)':y=18,format=yuv420p"
            run([FFMPEG,'-y','-loop','1','-framerate','25','-i',still,'-i',audio,
                 '-vf',vf,'-af',f'atempo={speed:.6f},apad','-t',f'{length:.3f}','-c:v','libx264','-preset','fast',
                 '-crf','21','-threads','4','-c:a','aac','-b:a','128k',part])
            timeline.append({'scene':i+1,'title':scene['title'],'start':round(offset,3),
                             'end':round(offset+length,3),'spoken_seconds':spoken,'tempo':round(speed,6)})
            offset += length
            print(f'Khung {i+1}/{len(scenes)}: giọng {spoken:.2f}s; video {length:.2f}s', flush=True)
        srt = []
        for n, (start, end, text) in enumerate(subtitles,1):
            lines = wrapped(ImageDraw.Draw(Image.new('RGB',(1,1))), text, 27, 1110)
            srt.append(f'{n}\n{clock(start)} --> {clock(end)}\n'+ '\n'.join(lines)+'\n')
        (ROOT/'Phu_de_Iris.srt').write_text('\n'.join(srt), encoding='utf-8')
        shutil.copy2(ROOT/'Phu_de_Iris.srt', work/'subtitles.srt')
        (work/'parts.txt').write_text('\n'.join(f"file '{i+1:02}.mp4'" for i in range(len(scenes))), encoding='utf-8')
        run([FFMPEG,'-y','-f','concat','-safe','0','-i','parts.txt','-c','copy','joined.mp4'], cwd=work)
        vf = "subtitles=subtitles.srt:fontsdir=fonts:force_style='FontName=Arial,FontSize=14,PrimaryColour=&H00FFFFFF,OutlineColour=&H00202020,BorderStyle=3,Outline=1,Shadow=0,MarginV=14,Alignment=2'"
        run([FFMPEG,'-y','-i','joined.mp4','-vf',vf,'-c:v','libx264','-preset','fast','-crf','21',
             '-threads','4','-c:a','copy','-movflags','+faststart',ROOT/'Video_dung_tu_khung_hinh.mp4'], cwd=work)
        run([FFMPEG,'-y','-i',ROOT/'Video_dung_tu_khung_hinh.mp4','-vn','-c:a','libmp3lame',
             '-b:a','128k',ROOT/'Thuyet_minh_Iris.mp3'])
    final = ROOT/'Video_dung_tu_khung_hinh.mp4'
    actual = duration(final)
    assert actual <= 180
    (ROOT/'thong_tin_ban_dung.json').write_text(json.dumps({
        'voices':sorted(used_voices),'rate':'+0%','duration_seconds':actual,'resolution':[WIDTH,HEIGHT],
        'fps':25,'subtitles':'Phu_de_Iris.srt','subtitles_burned_in':True,'timeline':timeline,
        'data_sha256':hashlib.sha256((PROJECT/'data/iris.csv').read_bytes()).hexdigest(),
        'video_sha256':hashlib.sha256(final.read_bytes()).hexdigest()
    },ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Đã tạo {final.name}: {actual:.2f} giây',flush=True)


if __name__ == '__main__':
    asyncio.run(build())
