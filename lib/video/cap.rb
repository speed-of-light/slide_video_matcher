# Class use for capture video
# @author speed-of-light@github
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

  # Light version of cached_dump, only accept given ranges
  # @option (see #cached_dump)
  # @return (see #cached_dump)
  # @see #cached_dump
  # @example Get raw image sum
  #   cap.dump(from: 0, to: 10){|c| cap.check_dump(c) }
  def dump opts={}
    fr = opts[:from] || 0
    to = opts[:to] || -1
    cached_dump(from: fr, to: to, cache_size: 1, interval: 1000) do |cache|
      yield(cache)
    end
  end

  # Dump stream frame with given range, and manipulate with cached image array.
  # @option opts [Integer] :from (0) time from the start frame.
  # @option opts [Integer] :to (-1) time to the end frame.
  # @option opts [Integer] :cache_size (1) the size of cache.
  # @option opts [Integer] :interval (1000) the captured frame interval.
  # @return [Array] a collection of handled data
  # @see #dump
  # @example Get raw image sum
  #   cap.cached_dump(from: 0, to: 10, cache_size: 3){|c| cap.check_dump(c) }
  def cached_dump opts={}
    return nil if @cap.nil?
    cc = @cap
    fs = cc.frame_count / cc.fps
    fr = opts[:from] || 0
    to = (opts[:to] == -1 || opts[:to].nil?) ? fs : opts[:to]
    cs = opts[:cache_size] || 1
    iv = opts[:interval] || 1000
    ca = []
    ra = []
    i = fr
    while i <= to
      cc.millisecond = i * iv
      break unless cc.grab
      ca << cc.retrieve
      ra << yield( ca ) if block_given?
      puts "Operation on #{cc.millisecond} ms"
      ca.shift 1 if ca.size % cs == 0
      i += 1
    end
    ra
  end

  # sum and diff with previous image
  # @return [Object] the returned object will fill into array
  # @see #cached_dump
  def diff_img
    cached_dump(from: 0, to: 10, cache_size: 2) do |c|
      next if c[1].nil?
      #sum
      (c[1].sum - c[0].sum).to_a.inject(0){|mem, obj| mem+obj}.abs
    end
  end

  # @!visibility private
  def check_dump cache, img
    puts "cache size: #{cache.size}, img raw: #{img[20][0]}"
  end

  def outliers ary=[], type=:mild
    iqq = { mild: 1.5, extreme: 3 }
    iq  = type.class == Fixnum ? type : iqq[type]
    sa  = ary.sort
    q1  = percentile sa, 0.25
    mid = percentile sa, 0.5
    q3  = percentile sa, 0.75
    iqr = (q3 - q1)*iq
    #fence = (q1 - iqr)..(q3 + iqr)
    fence = q3+iqr
    o = ary.reject{|v| v < fence}
  end

private

  def set_stream_path(value)
    @stream_path = value
    @cap = CvCapture.open(@stream_path)
    puts "Stream path setted\n#{to_s}"
  end

  def percentile(ary=[], percent=0.0)
    # multiply items in the array by the required percentile
    # (e.g. 0.75 for 75th percentile)
    # round the result up to the next whole number
    # then subtract one to get the array item we need to return
    ary ? ary[((ary.length * percent).ceil)-1] : nil
  end
end

