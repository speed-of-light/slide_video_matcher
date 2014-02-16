
module Video::FeatHelper
  include OpenCV

  # match two images
  # @example Setup
  #   # loading images for input
  #   ima = CvMat.load('lenna.jpg', CV_LOAD_IMAGE_GRAYSCALE)
  #   imb = CvMat.load('lenna-rotated.jpg', CV_LOAD_IMAGE_GRAYSCALE)
  #   matching ima, imb
  def matching ima, imb
    use_extended_descriptor = true
    threshold = 1500
    descriptor_size = use_extended_descriptor ? 128 : 64
    puts "this is feat test"
    @cap = nil
  end
end
