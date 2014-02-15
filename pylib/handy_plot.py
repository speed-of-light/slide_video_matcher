
class HandyPlot:
  """
  Author: speed-of-light
  Purpose: show plot easily
  """

  @staticmethod
  def table( fig, img_list, row=2, col=2):
    """Print tablized image list
    """
    b = row*col
    for i, img in enumerate(img_list, 1):
      ax = fig.add_subplot(row, col, i)
      ax.set_title("img_{}".format(i))
      ax.imshow(img)
      if i >= b: break
    return fig

