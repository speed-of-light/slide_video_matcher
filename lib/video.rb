require 'pry'

# @author https://github.com/speed-of-light
module Video
  require_relative 'video/cap'
end

puts 'loading complete'
vf = Video::Cap.new "/home/coder/Desktop/data/pymaging.mp4"

binding.pry
#vf.dump 0, nil
