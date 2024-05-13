import constants

class World():
  def __init__(self):
    self.mapTiles = []

  def processData(self, data, tileList):
    self.levelLength = len(data)
    for y, row in enumerate(data):
      for x, tile in enumerate(row):
        image = tileList[tile]
        imageRect = image.get_rect()
        imageX = x * constants.TILE_SIZE
        imageY = y * constants.TILE_SIZE
        imageRect.center = (imageX, imageY)
        tileData = [image, imageRect, imageX, imageY]

        if tile >= 0:
          self.mapTiles.append(tileData)
  def update(self, screenScroll):
    for tile in self.mapTiles:
      tile[2] += screenScroll[0]
      tile[3] += screenScroll[1]
      tile[1].center = (tile[2], tile[3])
  
  def draw(self, surface):
    for tile in self.mapTiles:
      surface.blit(tile[0], tile[1])
  