require 'pry'

# @author https://github.com/speed-of-light
module Video
  require "opencv"

  #require_relative 'video/*'
  _root = File.dirname(File.absolute_path(__FILE__))
  Dir.glob(_root + '/video/*') {|file| require file}

  def self.included base
    base.send :include, FeatHelper
    #base.extend ClassMethods
  end
end

puts 'loading complete'
vf = Video::Cap.new "/home/coder/Desktop/data/pymaging.mp4"

binding.pry
#vf.dump 0, nil
