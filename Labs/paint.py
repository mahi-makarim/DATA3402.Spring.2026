
class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


class Shape:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
    def get_x(self): return self.__x
    def get_y(self): return self.__y
    
    def paint(self, canvas, char='*'):
        for r in range(canvas.height):
            for c in range(canvas.width):
                if self.is_inside(c, r):
                    canvas.set_pixel(r, c, char)
                                     
    def overlaps(self, other):
        for px, py in self.get_points():
            if other.is_inside(px, py): return True
        for px, py in other.get_points():
            if self.is_inside(px, py): return True
        return False

    def is_inside(self, px, py):
        raise NotImplementedError()
        
    def get_points(self):
        raise NotImplementedError()


class Rectangle(Shape):
    def __init__(self, length, width, x, y):
        super().__init__(x, y) 
        self.__length = length
        self.__width = width
        
    def is_inside(self, px, py):
        x, y = self.get_x(), self.get_y()
        return x <= px <= x + self.__length and y <= py <= y + self.__width
        
    def get_points(self):
        pts = []
        x, y, l, w = self.get_x(), self.get_y(), self.__length, self.__width
        for i in range(4): pts.append((x + (i/4)*l, y))
        for i in range(4): pts.append((x + l, y + (i/4)*w))
        for i in range(4): pts.append((x + l - (i/4)*l, y + w))
        for i in range(4): pts.append((x, y + w - (i/4)*w))
        return pts


class Circle(Shape):
    def __init__(self, radius, x, y):
        super().__init__(x, y) 
        self.__radius = radius
        
    def is_inside(self, px, py):
        return (px - self.get_x())**2 + (py - self.get_y())**2 <= self.__radius**2
        
    def get_points(self):
        r, x, y = self.__radius, self.get_x(), self.get_y()
        s2 = 0.707 * r
        return [(x+r, y), (x-r, y), (x, y+r), (x, y-r), (x+s2, y+s2), (x-s2, y+s2)]


class Triangle(Shape):
    def __init__(self, base, height, x, y):
        super().__init__(x, y)
        self._base, self._height = base, height
        
                                     
    def is_inside(self, px, py):
        rel_x, rel_y = px - self.get_x(), py - self.get_y()
        if rel_x < 0 or rel_x > self._base or rel_y < 0 or rel_y > self._height: return False
        return (rel_y / self._height) + (rel_x / self._base) <= 1
        
    def get_points(self):
        pts = []
        x, y, b, h = self.get_x(), self.get_y(), self._base, self._height
        v = [(x, y), (x + b, y), (x, y + h), (x, y)]
        for i in range(3):
            p1, p2 = v[i], v[i+1]
            for j in range(5):
                t = j / 5
                pts.append((p1[0] + (p2[0]-p1[0])*t, p1[1] + (p2[1]-p1[1])*t))
        return pts


class CompoundShape(Shape):
    def __init__(self):
        super().__init__(0, 0)
        self.__shapes = []
        
    def add_shape(self, shape):
        self.__shapes.append(shape)
        
    def is_inside(self, px, py):
        for s in self.__shapes:
            if s.is_inside(px, py): return True
        return False
        
    def get_points(self):
        all_pts = []
        for s in self.__shapes: all_pts.extend(s.get_points())
        return all_pts
    
    
# Needed help from Gemini to understand the question, it recommended me to start the cote with a %%write.file.paint.py
