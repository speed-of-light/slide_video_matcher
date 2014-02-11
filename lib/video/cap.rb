# Class use for capture video
# @!attribute [r] :stream_path
#   @return [String] A stream path for capture operations
# @version 0.1.0
class Video::Cap
  require "opencv"
  include OpenCV

  # get stream path value
  attr_reader :stream_path
  @stream_path = ""
  @cap = nil

  # set stream_path
  # @param value [String] a consumable string for OpenCV module.
  def stream_path=(value)
    set_stream_path(value)
  end

  # override to string method
  def to_s
    cc = @cap
    "Capture Info:" +
    "\nFps: #{cc.fps}\nFrame count: #{cc.frame_count}\nSize: #{cc.size.to_a}" +
    "\nLength: #{cc.frame_count/cc.fps} seconds"
  end

  # Constructor for cap video
  # @param sp [String] initialize internal stream path, optional.
  def initialize(sp="")
    set_stream_path(sp) if not sp.empty?
  end

  # Method for dump and manipulate all single frame from a given stream.
  # @param from [Fixnum] grab the frame from this index.
  # @param to [Fixnum] grab the frame to this index, use nil to get all.
  # @return [Array] with given block.
  def dump from, to
    cc = @cap
    top = (to == nil) ? cc.frame_count / cc.fps : to
    i = from
    prev = nil
    a = []
    while i <= top
      cc.millisecond = i * 1000
      break unless cc.grab
      img = cc.retrieve
      a << yield(img) if block_given?
      puts "val: #{img[12][0]}, ms: #{cc.millisecond}"
      i += 1
    end
    a
  end

  # sum and diff with previous image
  # @param img [OpenCV::lplimage] image variable from #dump
  # @return [Object] the returned object will fill into array
  def sum_diff img
    img.sum
  end

private

  def set_stream_path(value)
    @stream_path = value
    @cap = CvCapture.open(@stream_path)
    puts "Stream path setted\n#{to_s}"
  end
end

