class Video::Cap
  require 'opencv'
  include OpenCV
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

  def dump from, to
    cc = @cap
    top = cc.frame_count / cc.fps if to.nil?
    i = from
    while i <= top
      cc.millisecond = i * 1000
      break unless cc.grab
      img = cc.retrieve
      puts "val: #{img[12][0]}, ms: #{cc.millisecond}"
      i += 1
    end
  end
end

vf = Video::Cap.new "/home/coder/Desktop/data/pymaging.mp4"
vf.dump 0, nil
