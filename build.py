#!/usr/bin/env python3
import PyInstaller.__main__
import platform
import os
import shutil

def find_system_binary(binary_name):
    """Find the path of a system binary using 'which' command"""
    path = shutil.which(binary_name)
    if not path:
        raise FileNotFoundError(f"Could not find {binary_name} in system PATH")
    return path

def build_executable():
    # Determine the system
    system = platform.system().lower()
    
    # Base name for the executable
    exe_name = "flake"
    if system == "windows":
        exe_name += ".exe"

    # Common PyInstaller arguments
    args = [
        "flake.py",  # your main script
        "--onefile",  # create a single executable
        "--name", exe_name,
        "--clean",  # clean PyInstaller cache
        "--log-level", "INFO",
        # Add hidden imports required by pydub
        "--hidden-import", "pydub",
        "--hidden-import", "pydub.utils",
    ]

    # Add FFmpeg binary paths based on the operating system
    if system == "windows":
        args.extend([
            "--add-binary", "ffmpeg.exe;.",
            "--add-binary", "ffprobe.exe;."
        ])
    else:  # Linux/MacOS
        # Find system FFmpeg and FFprobe
        ffmpeg_path = find_system_binary("ffmpeg")
        ffprobe_path = find_system_binary("ffprobe")
        
        args.extend([
            f"--add-binary={ffmpeg_path}:.",
            f"--add-binary={ffprobe_path}:."
        ])

    # Run PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    build_executable()