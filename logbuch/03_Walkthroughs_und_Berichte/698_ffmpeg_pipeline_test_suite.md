# 🧪 **FFmpeg Test-Suite** – Vollständige Pipeline-Tests

**FFmpeg** Tests: **Input → Output → Quality** – **Automatisierte Pipeline-Validierung** für **Remux/Transcode/Stream**!

## **FFmpeg Test-Phasen**

```
1. INPUT  → ffprobe (Codecs, HDR, Subs)
2. PROCESS → FFmpeg Remux/Transcode
3. OUTPUT → ffprobe + FFplay (Integrität)
4. QUALITY → Bitrate, PSNR, Chapters
```

## **Test-Suite Tabelle**

| **Phase**   | **Test**             | **Tool**   | **Prüft**                     |
|-------------|----------------------|------------|-------------------------------|
| **Input**   | Codecs/Tracks        | ffprobe    | H.264/HEVC/TrueHD            |
| **Input**   | HDR Metadata         | ffprobe    | BT2020, HDR10                 |
| **Process** | Remux MKV→MP4        | FFmpeg     | Lossless Container            |
| **Process** | HLS Generation       | FFmpeg     | Segmente, Index               |
| **Output**  | Bitrate Match        | ffprobe    | Kein Qualitätsverlust         |
| **Output**  | Chapters behalten    | ffprobe    | Navigation                    |
| **Quality** | PSNR/SSIM            | FFmpeg     | Transcode Qualität            |

## **Backend: FFmpeg Pipeline Suite**

```python
class FFmpegTestSuite:
    def __init__(self, input_path):
        self.input = input_path
        self.input_analysis = ffprobe_suite(input_path)
        self.tests = []
    
    def test_remux_mkv_mp4(self):
        """MKV → MP4 Lossless"""
        input_base = self.input.rsplit('.', 1)[0]
        output_mp4 = f"{input_base}_test.mp4"
        
        cmd = ['ffmpeg', '-i', self.input, '-c', 'copy', 
               '-movflags', '+faststart', output_mp4]
        subprocess.run(cmd, check=True)
        
        # ffprobe Output
        output_analysis = ffprobe_suite(output_mp4)
        
        # Vergleich
        video_match = (self.input_analysis['video'][0]['codec'] == 
                      output_analysis['video'][0]['codec'])
        duration_match = abs(self.input_analysis['container']['duration_min'] - 
                           output_analysis['container']['duration_min']) < 0.1
        
        return {
            'test': 'MKV→MP4 Remux',
            'success': video_match and duration_match,
            'input_video': self.input_analysis['video'][0]['codec'],
            'output_video': output_analysis['video'][0]['codec'],
            'output_file': output_mp4
        }
    
    def test_hls_generation(self, hls_dir='/tmp/hls_test'):
        """Input → HLS Stream"""
        os.makedirs(hls_dir, exist_ok=True)
        
        cmd = [
            'ffmpeg', '-i', self.input,
            '-c:v', 'libx264', '-preset', 'ultrafast',
            '-f', 'hls', '-hls_time', '6', '-hls_list_size', '0',
            f"{hls_dir}/playlist.m3u8"
        ]
        subprocess.run(cmd, check=True)
        
        # HLS Validierung
        playlist = f"{hls_dir}/playlist.m3u8"
        segments = glob.glob(f"{hls_dir}/*.ts")
        
        return {
            'test': 'HLS Generation',
            'success': len(segments) > 5,
            'segments': len(segments),
            'playlist': playlist
        }
    
    def test_chapter_preservation(self):
        """Chapters nach Remux"""
        input_chapters = self.input_analysis['chapters']
        test_mkv = f"{self.input.rsplit('.',1)[0]}_chapters.mkv"
        
        cmd = ['ffmpeg', '-i', self.input, '-c', 'copy', '-map_chapters', '1', test_mkv]
        subprocess.run(cmd, check=True)
        
        output_chapters = ffprobe_suite(test_mkv)['chapters']
        return {
            'test': 'Chapter Preservation',
            'success': output_chapters == input_chapters,
            'chapters': input_chapters
        }
    
    def run_full_suite(self):
        """Alle Tests"""
        return {
            'input_analysis': self.input_analysis,
            'remux_test': self.test_remux_mkv_mp4(),
            'hls_test': self.test_hls_generation(),
            'chapter_test': self.test_chapter_preservation(),
            'quality_score': ffprobe_quality_score(self.input_analysis)
        }
```

## **App-Integration**

```html
<button id="runFfmpegSuite">🚀 Full FFmpeg Suite</button>
<div id="ffmpegResults"></div>
```

```js
document.getElementById('runFfmpegSuite').onclick = async () => {
    const suite = await eel.ffmpeg_test_suite(currentPath)();
    displayFfmpegResults(suite);
};

function displayFfmpegResults(suite) {
    document.getElementById('ffmpegResults').innerHTML = `
        <h3>FFmpeg Pipeline Tests</h3>
        <div>${suite.remux_test.success ? '✅' : '❌'} Remux: ${suite.remux_test.output_file}</div>
        <div>${suite.hls_test.success ? '✅' : '❌'} HLS: ${suite.hls_test.segments} Segmente</div>
        <div>${suite.chapter_test.success ? '✅' : '❌'} Chapters: ${suite.chapter_test.chapters}</div>
        <div>🎯 Quality: ${suite.quality_score}/100</div>
    `;
}
```

## **Eel Exposed**

```python
ffmpeg_suite = FFmpegTestSuite('dummy')
eel.expose(lambda path: FFmpegTestSuite(path).run_full_suite())
```

## **Erweiterte Tests**

```python
def test_psnr_quality(input_path, output_path):
    """PSNR zwischen Original + Transcode"""
    cmd = ['ffmpeg', '-i', input_path, '-i', output_path, 
           '-lavfi', 'psnr', '-f', 'null', '-']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return parse_psnr(result.stderr)

def test_bitrate_stability(hls_playlist):
    """HLS Bitrate Variation"""
    segments = glob.glob(f"{hls_playlist.rsplit('/',1)[0]}/*.ts")
    bitrates = [get_segment_bitrate(s) for s in segments[:20]]
    stability = 1 - (max(bitrates) - min(bitrates)) / sum(bitrates)
    return stability > 0.8  # 80% stable
```

## **Demo Output**

```
🚀 FFmpeg Suite Results
✅ Remux: movie_test.mp4 (H.265→H.265)
✅ HLS: 42 Segmente (playlist.m3u8)
✅ Chapters: 28 behalten
🎯 Quality Score: 95/100
⏱️ 12s Total
```

**FFmpeg Test-Suite** = **Input → Process → Output → Quality**! 🧪✅

**Automatisierte Pipeline-Validierung** – **vor Production**! 🚀

**Integriere**: `ffmpeg_test_suite(path)` → **Stream Ready**! 🎬
