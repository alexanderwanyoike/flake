#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor
import logging
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def setup_logging():
    """Configure logging format and level"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def convert_flac_to_mp3(flac_path, output_dir):
    """
    Convert a single FLAC file to MP3 while maintaining quality.
    
    Args:
        flac_path (Path): Path to the FLAC file
        output_dir (Path): Directory to save the MP3 file
    """
    try:
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate output path with .mp3 extension
        output_path = output_dir / f"{flac_path.stem}.mp3"
        
        logging.info(f"Converting: {flac_path.name}")
        
        # Load FLAC file
        audio = AudioSegment.from_file(str(flac_path), format="flac")
        
        # Export as MP3 with high quality settings
        audio.export(
            str(output_path),
            format="mp3",
            parameters=["-q:a", "0"]  # Use highest quality VBR setting
        )
        
        logging.info(f"Converted: {flac_path.name} -> {output_path.name}")
        
    except Exception as e:
        logging.error(f"Error converting {flac_path.name}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert FLAC files to MP3 while maintaining quality"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input directory containing FLAC files"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output directory for converted MP3 files"
    )
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=os.cpu_count(),
        help="Number of conversion threads (default: number of CPU cores)"
    )
    
    args = parser.parse_args()
    
    setup_logging()
    
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    # Verify input directory exists
    if not input_dir.is_dir():
        logging.error(f"Input directory does not exist: {input_dir}")
        return
    
    # Get all FLAC files
    flac_files = list(input_dir.glob("**/*.flac"))
    
    if not flac_files:
        logging.warning("No FLAC files found in input directory")
        return
    
    logging.info(f"Found {len(flac_files)} FLAC files to convert")
    
    # Convert files using thread pool
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for flac_file in flac_files:
            # Preserve directory structure in output
            relative_path = flac_file.relative_to(input_dir)
            output_subdir = output_dir / relative_path.parent
            executor.submit(convert_flac_to_mp3, flac_file, output_subdir)
    
    logging.info("Conversion complete!")

if __name__ == "__main__":
    main()