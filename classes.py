class PlayerClass():
    def __init__(self, x, y, radius, image, score=0)-> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.image = image
        self.score = score
    
    def jump(self):
        self.y -=6


class PipeClass():
    def __init__(self, x, y, length, width, image) -> None:
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.image = image
