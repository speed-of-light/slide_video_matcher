require 'opencv'
include OpenCV

module Video
  class Frame
    attr_reader :stream_path
    @stream_path = ""
    @cap = nil
    # @cap methods:
    # avi_ratio  contrast    format fps=        frames= height  millisecond  query         saturation width
    # avi_ratio= convert_rgb fourcc frame_count gain    height= millisecond= rectification size       width=
    # brightness exposure    fps    frames      grab    hue     mode         retrieve      size=

    def set_stream_path(value)
      @stream_path = value
      @cap = CvCapture.open(@stream_path)
      puts "Stream path setted\n#{to_s}"
    end

    def stream_path=(value)
      set_stream_path(value)
    end

    def to_s
      cc = @cap
      "Capture Info:" +
      "\nFps: #{cc.fps}\nFrame count: #{cc.frame_count}\nSize: #{cc.size.to_a}" +
      "\nLength: #{cc.frame_count/cc.fps} seconds"
    end

    def initialize(sp="")
      set_stream_path(sp) if not sp.empty?
    end

    def dump
      cap = CvCapture.open(vid)
      i = 0
      while i < 200
        cap.millisecond = i* 1000
        break unless cap.grab
        img = cap.retrieve
        puts "val: #{img[12][0]}, ms: #{cap.millisecond}"
        i += 1
      end
    end
  end
end

vf = Video::Frame.new "/home/coder/Desktop/data/pymaging.mp4"
#vf.stream_path = "/home"

#vf.test
