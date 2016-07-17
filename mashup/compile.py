from moviepy.editor import VideoFileClip, concatenate_videoclips

STEP_SIZE = 2
MAX_VIDEO_LENGTH = 20


def compile_clips(homevideo_path, musicvideo_path, out_path="output/clip.mp4"):
    """Compile a homevideo and a music video by interlacing every 
    STEP_SIZE seconds, up to a maximum of MAX_VIDEO_LENGTH.

    input:
        homevideo_path: filename to the home video
        musicvideo_path: filename of the music video. This soundtrack will be used
            during the whole clip
        out_path: the file path where the output file will be placed

    output:
        none
    """
    homevideo = VideoFileClip(homevideo_path)
    musicvideo = VideoFileClip(musicvideo_path)

    audio = musicvideo.subclip(0, MAX_VIDEO_LENGTH).audio

    clips = []
    flipping = True
    step = 0
    while True:
        video = musicvideo
        if flipping and step % 2 == 0:
            video = homevideo

        try:
            clips.append(
                video.subclip(step * STEP_SIZE, (step + 1) * STEP_SIZE).resize(width=400))
            step += 1
        except:
            flipping = False

        if step > MAX_VIDEO_LENGTH / STEP_SIZE:
            break

    final_clip = concatenate_videoclips(clips, method='compose').without_audio()
    final_clip.audio = audio
    final_clip.write_videofile(out_path, fps=24, codec='libvpx', audio_codec='libvorbis')

if __name__ == "__main__":
    print "Compiling two clips..."
    compile_clips("testmovie.mov", "pitbull.mp4")
    print "Done!"
