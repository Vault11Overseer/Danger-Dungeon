from items import Item
from character import Character
import constants

class World():
  def __init__(self):
    self.mapTiles = []
    self.obstacleTiles = []
    self.exitTile = None
    self.itemList  = []
    self.player = None
    self.characterList = []

  def processData(self, data, tileList, itemImages, mob_animations):
    self.levelLength = len(data)
    for y, row in enumerate(data):
      for x, tile in enumerate(row):
        image = tileList[tile]
        imageRect = image.get_rect()
        imageX = x * constants.TILE_SIZE
        imageY = y * constants.TILE_SIZE
        imageRect.center = (imageX, imageY)
        tileData = [image, imageRect, imageX, imageY]

        if tile == 7:
          self.obstacleTiles.append(tileData)
        elif tile == 8:
          self.exitTile = tileData
        elif tile ==9:
          coin = Item(imageX, imageY, 0, itemImages[0])
          self.itemList.append(coin)
          tileData[0] = tileList[0]
        elif tile == 10:
          potion = Item(imageX, imageY, 1, [itemImages[1]])
          self.itemList.append(potion)
          tileData[0] = tileList[0]
        elif tile == 11:
          player = Character(imageX, imageY,100, mob_animations, 0, False)
          self.player = player
          tileData[0] = tileList[0]
        elif tile >= 12 and tile <= 16:
          enemy = Character(imageX, imageY,100, mob_animations, tile - 11, False)
          self.characterList.append(enemy)
          tileData[0] = tileList[0]
        elif tile == 17:
          enemy = Character(imageX, imageY,100, mob_animations, 6, True)
          self.characterList.append(enemy)
          tileData[0] = tileList[0]

        # ADD IMAGE DATA TO MAIN TILE LIST
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
  