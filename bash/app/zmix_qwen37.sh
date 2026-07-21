#!/bin/bash

printf "Argument count: %s.\n" "${#@}"
# ==========================================
# WAV Segmenter & Rubberband Effect Script
# ==========================================
# Check if input file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <input.wav> [number_of_segments] [pitch_factor]"
    echo "Example: $0 audio.wav 5 1.3"
    echo "  - number_of_segments: How many equal parts to split the audio into (Default: 5)"
    echo "  - pitch_factor: Rubberband pitch shift. 1.0 = normal, >1.0 = higher, <1.0 = lower (Default: 1.2)"
    exit 1
fi

INPUT_FILE="$1"
NUM_SEGMENTS="${2:-5}"
PITCH_FACTOR="${3:-1.2}" 
OUTPUT_DIR="rubberband_segments"

rm rubberband_segments/*


echo $INPUT_FILE

yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

# 1. Validate Input File
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: File '$INPUT_FILE' not found!"
    exit 1
fi

# 2. Check Dependencies
if ! command -v ffmpeg &> /dev/null || ! command -v ffprobe &> /dev/null; then
    echo "❌ Error: ffmpeg and ffprobe are required but not installed."
    exit 1
fi

# 3. Check for Rubberband Filter Availability
if ffmpeg -filters 2>/dev/null | grep -q "rubberband"; then
    # Native rubberband filter (changes pitch without changing speed)
    AUDIO_FILTER="rubberband=pitch=$(shuf -i0-8 -n1)"
    echo "✅ Using native 'rubberband' filter."
else
    # Fallback: asetrate changes pitch but also changes playback speed
    echo "⚠️  Warning: Native 'rubberband' filter not found in your FFmpeg build."
    echo "   Falling back to 'asetrate' (this will change both pitch and speed)."
    AUDIO_FILTER="asetrate=44100*${PITCH_FACTOR},aresample=44100"
fi

# 4. Get Audio Duration
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT_FILE")

if [ -z "$DURATION" ] || [ "$DURATION" == "N/A" ]; then
    echo "❌ Error: Could not determine the duration of the audio file."
    exit 1
fi

# 5. Calculate Segment Duration (using awk for float math)
SEGMENT_DURATION=$(awk "BEGIN {print $DURATION / $NUM_SEGMENTS}")

# 6. Create Output Directory
mkdir -p "$OUTPUT_DIR"

echo "🎵 Processing '$INPUT_FILE' into $NUM_SEGMENTS segments..."
echo "⏱️  Total Duration: ${DURATION}s | Segment Duration: ${SEGMENT_DURATION}s"
echo "🎛️  Pitch Factor: $PITCH_FACTOR"
echo "---------------------------------------------------"

# 7. Loop, Split, and Apply Effect
for((i=0;i<$NUM_SEGMENTS;i++))
do 

    # Calculate start time for current segment
    START_TIME=$(awk "BEGIN {print $i * $SEGMENT_DURATION}")
    #START_TIME=(($i+1))
    #echo $START_TIME
    
    # Format output filename with leading zeros (e.g., segment_00.wav)
    OUTPUT_FILE=$(printf "%s/segment_%03d.wav" "$OUTPUT_DIR" "$i")
    
    echo "🔪 Creating segment $((i+1))/$NUM_SEGMENTS (Start: ${START_TIME}s)..."


    # https://manpages.debian.org/unstable/rubberband-cli/rubberband.1.en.html
    #-t, --time X
    #Stretch to X times original duration, or
    #-T, --tempo X
    #Change tempo by multiple X (equivalent to --time 1/X), or
    #-T, --tempo X:Y
    #Change tempo from X to Y (same as --time X/Y), or
    #-D, --duration X
    #Stretch or squash to make output file X seconds long
    #-p, --pitch X
    #Raise pitch by X semitones, or
    #-f, --frequency X
    #Change frequency by multiple X
    #-c, --crisp N
    #Crispness (N = 0,1,2,3,4,5); default 4 (see below)



    
    # Run FFmpeg
    # -ss: start time, -t: duration, -af: audio filter, -c:a: force wav encoding
    #ffmpeg -y -i "$INPUT_FILE" -ss "$START_TIME" -t "$SEGMENT_DURATION" \
    #       -af "$AUDIO_FILTER" -c:a pcm_s16le \
    #       "$OUTPUT_FILE" -hide_banner -loglevel error

    OUTPUT_FILE='rubberband_segments/segment_%03d.wav' 
    AUDIO_FILTER=rubberband=pitch=$(shuf -i0-8 -n1), rubberband=tempo=$(shuf -i0-2 -n1), \
     rubberband=time=$(shuf -i0-2 -n1), rubberband=crisp=$(shuf -i0-3 -n1)

    ffmpeg -y -i "$INPUT_FILE"  -f segment -segment_time "$i" \
    -codec pcm_s16le -segment_format wav \
    -af  ${AUDIO_FILTER} \
       ${OUTPUT_FILE}  -hide_banner -loglevel error

           
    if [ $? -eq 0 ]; then
        echo "✅ Saved: $OUTPUT_FILE"
    else
        echo "❌ Error processing segment $((i+1))"
    fi
done

echo "---------------------------------------------------"
echo "🎉 Done! Check the '$OUTPUT_DIR' directory for your files."



# create a bash script that reads a wav file , makes equal segments with ffmpeg and applies rubberband effect 

# chmod +x zmix_qwen37.sh
#./zmix_qwen37.sh my_audio.wav
#./zmix_qwen37.sh my_audio.wav 10
#./zmix_qwen37.sh my_audio.wav 5 0.8

exit 1