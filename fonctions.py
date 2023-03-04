import random


class Serpent:
    def __init__(self):
        self.dir = 0
        self.long = 5
        self.tete = [25, 25]
        self.corps = []

    def avance(self):
        if self.dir == 0:
            self.tete[1] -= 1
        elif self.dir == 2:
            self.tete[1] += 1
        elif self.dir == 1:
            self.tete[0] -= 1
        elif self.dir == 3:
            self.tete[0] += 1

    def queue(self):
        if len(self.corps) >= self.long:
            del self.corps[0]
        self.corps.append([self.tete[0], self.tete[1]])

    def collision(self):
        coll = 0
        if self.tete[0] > 49 or self.tete[0] < 0 or self.tete[1] > 49 or self.tete[1] < 0:
            coll = 1
        elif self.tete in self.corps:
            coll = 1
        return coll

    def testcolli(self, dir):
        if dir == 0:
            if [self.tete[0], self.tete[1]-1] in self.corps or self.tete[1]-1 == -1:
                return True
        if dir == 1:
            if [self.tete[0]-1, self.tete[1]] in self.corps or self.tete[0]-1 == -1:
                return True
        if dir == 2:
            if [self.tete[0], self.tete[1]+1] in self.corps or self.tete[1]+1 == 50:
                return True
        if dir == 3:
            if [self.tete[0]+1, self.tete[1]] in self.corps or self.tete[0]+1 == 50:
                return True
        return False

    def track2(self, pomme):
        tab = []
        for i in range(50):
            tab.append([])
            for j in range(50):
                tab[i].append(100)

        for c in self.corps:
            tab[c[1]][c[0]] = -1

        path = path_finder(tab, self.tete[0], self.tete[1], pomme[0], pomme[1])
        if path:
            dir_list = []
            if self.tete[0] == path[0][0] + 1:
                dir_list.append(1)
            if self.tete[0] == path[0][0] - 1:
                dir_list.append(3)
            if self.tete[1] == path[0][1] + 1:
                dir_list.append(0)
            if self.tete[1] == path[0][1] - 1:
                dir_list.append(2)

            for coord in range(len(path)-1):
                if path[coord][0] == path[coord+1][0] + 1:
                    dir_list.append(1)
                if path[coord][0] == path[coord+1][0] - 1:
                    dir_list.append(3)
                if path[coord][1] == path[coord+1][1] + 1:
                    dir_list.append(0)
                if path[coord][1] == path[coord+1][1] - 1:
                    dir_list.append(2)

            return dir_list



class Pomme:
    def __init__(self):
        self.pos = []

    def spawn(self, serpent):
        x = random.randrange(0, 50)
        y = random.randrange(0, 50)
        self.pos = [x, y]
        if self.pos in serpent.corps:
            self.spawn(serpent)


def path_finder(tab, x, y, x_end, y_end):
    tab = manhattan(tab, x, y, 0, True, True, True, True)
    i = tab[y_end][x_end]
    if i == 100:
        return []
    path_temp, path = [], []
    while i != 0:
        path_temp.append((x_end, y_end))
        br = 1
        if y_end > 0:
            if tab[y_end-1][x_end] == i-1:
                y_end -= 1
                br = 0
        if x_end > 0 and br == 1:
            if tab[y_end][x_end-1] == i-1:
                x_end -= 1
                br = 0
        if y_end < len(tab)-1 and br == 1:
            if tab[y_end+1][x_end] == i-1:
                y_end += 1
                br = 0
        if x_end < len(tab[0])-1 and br == 1:
            if tab[y_end][x_end+1] == i-1:
                x_end += 1
        i -= 1
    for co in reversed(path_temp):
        path.append(co)
    return path


def manhattan(tab, x, y, i, n, s, e, w):
    """
    makes the manhattan mapping of a 2D array
    :param tab: the array to map
    :param x: the column starting point
    :param y: the line starting point
    :param i: value of the cell, must be 0 when the function is called
    :return: a new 2D array with the manhattan mapping
    """
    tab[y][x] = i
    if x > 0 and w:
        if tab[y][x-1] > i+1:
            n_temp, s_temp = n, s
            if y < len(tab)-1:
                if tab[y+1][x] == -1:
                    s = True
            if y > 0:
                if tab[y-1][x] == -1:
                    n = True
            tab = manhattan(tab, x-1, y, i+1, n, s, False, w)
            n, s = n_temp, s_temp

    if x < len(tab[0])-1 and e:
        if tab[y][x+1] > i+1:
            n_temp, s_temp = n, s
            if y < len(tab)-1:
                if tab[y+1][x] == -1:
                    s = True
            if y > 0:
                if tab[y-1][x] == -1:
                    n = True
            tab = manhattan(tab, x+1, y, i+1, n, s, e, False)
            n, s = n_temp, s_temp

    if y > 0 and n:
        if tab[y-1][x] > i+1:
            w_temp, e_temp = w, e
            if x > 0:
                if tab[y][x-1] == -1:
                    w = True
            if x < len(tab[0])-1:
                if tab[y][x+1] == -1:
                    e = True
            tab = manhattan(tab, x, y-1, i+1, n, False, e, w)
            w, e = w_temp, e_temp

    if y < len(tab)-1 and s:
        if tab[y+1][x] > i+1:
            w_temp, e_temp = w, e
            if x > 0:
                if tab[y][x-1] == -1:
                    w = True
            if x < len(tab[0])-1:
                if tab[y][x+1] == -1:
                    e = True
            tab = manhattan(tab, x, y+1, i+1, False, s, e, w)
            w, e = w_temp, e_temp
    return tab

