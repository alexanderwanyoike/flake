# FLAC to MP3 Converter

A command-line tool that efficiently converts FLAC audio files to MP3 format while maintaining audio quality. The converter processes files in parallel using multiple threads and preserves your directory structure in the output.

## Features

- High-quality conversion from FLAC to MP3
- Multi-threaded processing for faster conversion
- Preserves directory structure
- Detailed logging of conversion progress
- Simple command-line interface
- Maintains original audio quality using VBR encoding

## Installation

### Prerequisites

1. Make sure you have Python 3.8+ installed:
```bash
python --version
```

2. Install FFmpeg (required for audio conversion):

For Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

For Fedora:
```bash
sudo dnf install ffmpeg
```

For Arch Linux:
```bash
sudo pacman -S ffmpeg
```

For macOS:
```bash
brew install ffmpeg
```

### Building from Source

1. Clone the repository or download the source files

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install pyinstaller pydub
```

4. Build the executable:
```bash
python build.py
```

### Global Installation

To make the converter accessible from anywhere, install it to `/usr/local/bin`:
```bash
sudo cp dist/flac_converter /usr/local/bin/
sudo chmod +x /usr/local/bin/flac_converter
```

Alternatively, for a user-specific installation:
```bash
mkdir -p ~/.local/bin
cp dist/flac_converter ~/.local/bin/
chmod +x ~/.local/bin/flac_converter
```

If using `~/.local/bin`, add this to your `~/.bashrc` or `~/.zshrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Usage

Basic usage:
```bash
flac_converter -i <input_directory> -o <output_directory>
```

Example:
```bash
flac_converter -i ~/Music/flac -o ~/Music/mp3
```

### Command Line Options

- `-i, --input`: Input directory containing FLAC files (required)
- `-o, --output`: Output directory for converted MP3 files (required)
- `-t, --threads`: Number of conversion threads (optional, defaults to CPU core count)

Example with custom thread count:
```bash
flac_converter -i ~/Music/flac -o ~/Music/mp3 -t 4
```

## Output Structure

The converter maintains your directory structure. For example:

Input:
```
~/Music/flac/
├── Album1/
│   ├── track1.flac
│   └── track2.flac
└── Album2/
    └── track1.flac
```

Output:
```
~/Music/mp3/
├── Album1/
│   ├── track1.mp3
│   └── track2.mp3
└── Album2/
    └── track1.mp3
```

## Error Handling

- The program logs all operations and any errors that occur during conversion
- If a conversion fails, the program will continue with the remaining files
- Error messages will indicate which files failed to convert and why

## Support

If you encounter any issues or need help, please open an issue in the repository's issue tracker.