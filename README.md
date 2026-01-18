# Optimal Transcoding Preset Selection for Live Video Streaming

A comprehensive Python framework for extracting video features, transcoding videos with different presets and bitrates, and optimizing preset selection using Integer Linear Programming (ILP) to maximize PSNR while respecting time and bitrate constraints.

## Overview

This project provides tools for:
- Video segmentation and format conversion
- Feature extraction from H.264 encoded videos (frame-level, macroblock-level, motion vectors)
- Transcoding videos with multiple presets and bitrates
- Optimizing preset selection per video chunk using ILP to maximize quality (PSNR) under constraints

## Project Structure

```
.
├── main.py                          # Main orchestration script
├── segment_videos.py                # Video segmentation utility
├── convert_mp4_h264.py             # MP4 to H.264 converter
├── extract_h264_features.py        # H.264 feature extraction and transcoding
├── extract_features_twitch.py      # Twitch decoder feature extraction
├── twitch_features_parse.py        # Parse Twitch decoder output
├── Process_Motionvector.py         # Motion vector extraction
├── merge_all_extracted_features.py # Merge all extracted features
├── split_train_test_data.py        # Split data by preset
└── ILP_loop.py                     # ILP optimization for preset selection
```

## Features

### 1. Video Processing Pipeline

- **Video Segmentation** (`segment_videos.py`): Segments input videos into fixed-length chunks (default: 2 seconds)
- **Format Conversion** (`convert_mp4_h264.py`): Converts MP4 videos to raw H.264 format
- **Transcoding** (`extract_h264_features.py`): Transcodes videos with multiple presets and bitrates

### 2. Feature Extraction

The framework extracts multiple types of features:

- **Frame-level features**: Key frames, packet size, aspect ratio, color space, frame types (I/P/B frames)
- **Macroblock features**: Block sizes (16x16, 16x8, 8x16, 8x8, 4x4), frame types distribution
- **Motion vector features**: Motion vector counts and histograms
- **Video metadata**: Duration, resolution, bitrate, frame count

### 3. Optimization

- **ILP-based Preset Selection** (`ILP_loop.py`): Uses Integer Linear Programming to select optimal presets for video chunks that maximize PSNR while respecting:
  - Total transcoding time constraints
  - Total bitrate constraints
  - One preset per chunk constraint

## Requirements

### Python Dependencies

```python
pandas
numpy
ffmpeg-python
pulp  # For ILP optimization
mvextractor  # For motion vector extraction
matplotlib
scipy
cv2 (opencv-python)
```

### External Tools

- **FFmpeg**: Required for video processing and transcoding
- **ldecod_static**: Twitch H.264 decoder (for macroblock feature extraction)
- **mvextractor**: For motion vector extraction

## Usage

### Main Pipeline

Run the complete feature extraction pipeline:

```python
python main.py
```

The main function (`main_preset_time_prediction`) orchestrates:
1. Video segmentation
2. MP4 to H.264 conversion
3. Feature extraction (H.264, Twitch, motion vectors)

### Individual Components

#### 1. Segment Videos

```python
from segment_videos import segment_videos

segment_videos(
    video_path='./videos',
    segment_path='./videos_segment',
    video_length=2,  # seconds
    format_type='mkv'
)
```

#### 2. Convert MP4 to H.264

```python
from convert_mp4_h264 import convert_mp4_to_h264

convert_mp4_to_h264(
    mp4_path='./videos_segment',
    h264_path='./videos_segment_h264'
)
```

#### 3. Extract H.264 Features

```python
from extract_h264_features import extract_h264_features

preset = ["veryslow", "slow", "fast", "veryfast", "ultrafast"]
bit_rate = ['6000k', '5000k', '4000k', '3000k', '2000k', '1000k', '800k', '600k', '400k', '200k']
bit_rate_in = [8000]
bit_rate_out = [6000, 5000, 4000, 3000, 2000, 1000, 800, 600, 400, 200]

h264_measures = extract_h264_features(
    mp4_path='./videos_segment',
    h264_path='./videos_segment_h264',
    preset=preset,
    bit_rate=bit_rate,
    bit_rate_in=bit_rate_in,
    bit_rate_out=bit_rate_out,
    linux=1  # 1 for Linux/WSL, 0 for Windows
)
```

#### 4. Extract Motion Vectors

```python
from Process_Motionvector import mv_extractor

mv_extractor(
    path='./videos_segment_h264',
    path_mp4='./videos_segment'
)
```

#### 5. Parse Twitch Features

```python
from twitch_features_parse import parse_twitch_files

twitch_measures = parse_twitch_files(
    path='./videos_segment',
    txt_path='./videos_segment_h264'
)
```

#### 6. Merge All Features

```python
python merge_all_extracted_features.py
```

#### 7. Split Data for Training

```python
python split_train_test_data.py
```

#### 8. Optimize Preset Selection with ILP

```python
python ILP_loop.py
```

The ILP optimization:
- Randomly selects 6 video chunks
- For each chunk, considers 50 preset-bitrate combinations (5 presets × 10 bitrates)
- Maximizes total PSNR subject to:
  - Time constraint: `T_max = 5` seconds
  - Bitrate constraint: `B_max = 6 × bitrate[k]`
  - One preset per chunk constraint

## Configuration

### Presets

The default presets used are:
- `veryslow`
- `slow`
- `fast`
- `veryfast`
- `ultrafast`

### Bitrates

Default bitrate range: `[6000k, 5000k, 4000k, 3000k, 2000k, 1000k, 800k, 600k, 400k, 200k]`

### Video Constraints

- Minimum input bitrate: 7200 kbps
- Segment duration: 2 seconds
- Video format: MP4/MKV

## Output Files

- `measures_features_maedeh_{bitrate}_h264.pkl`: H.264 features per bitrate
- `twitch_features_h264.pkl`: Macroblock features
- `mv_no.npy`: Motion vector counts
- `mv_hist_all.npy`: Motion vector histograms
- `all_features_PSNR_Time_Windows.pkl`: Merged feature dataset
- `preset{0-4}features.csv`: Features split by preset
- `output_sel_{bitrate}_2.csv`: ILP optimization results
- `chunk_sel_{bitrate}_2.csv`: Selected chunk indices

## Notes

- The code includes hardcoded paths that may need adjustment for your system
- Some functions require Linux/WSL environment (especially motion vector extraction)
- FFmpeg must be installed and accessible from command line
- The `ldecod_static` decoder must be available in the working directory
- Video files should meet minimum quality thresholds (bitrate > 7200 kbps)

## Author

Created by NBZ (Nabizadeh)

## License

**Academic Use Only**

Copyright (c) 2023 NBZ (Nabizadeh)

This software and associated documentation files (the "Software") are provided for academic research and educational purposes only. 

**Terms and Conditions:**

1. **Academic Use Only**: The Software may only be used for academic research, educational purposes, and non-commercial scholarly activities.

2. **No Commercial Use**: You may not use the Software for any commercial purposes, including but not limited to:
   - Commercial product development
   - Commercial services
   - Any form of commercial exploitation

3. **Attribution**: If you use this Software in your research, you must cite the original work appropriately.

4. **No Redistribution**: You may not redistribute, sublicense, or sell copies of the Software without explicit written permission from the copyright holder.

5. **No Warranty**: THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

6. **Limitation of Liability**: IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For commercial licensing inquiries, please contact.

