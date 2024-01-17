import math
import random
class node:
    def __init__(self,row,col):
        self.row=row
        self.col=col
        self.gval=0
        self.hval=0
        self.obs=False
        self.parent=None
        self.goal=False

    def __repr__(self):
        return f"node(row={self.row}, col={self.col}, gval={self.gval}, hval={self.hval}"
goal_point=node(9,9)
goal_point.goal=True
open_list=[]
closed=[]
start_point=node(0,0)
start_point.hval=127.27
solved=False
open_list.append(start_point)
def generate_random_binary_matrix(rows, cols, probability_of_one):
    return [[1 if random.random() < probability_of_one else 0 for _ in range(cols)] for _ in range(rows)]

obstacle_matrix= generate_random_binary_matrix(10, 10, 0.2)
obstacle_matrix[0][0]=0
obstacle_matrix[9][9]=0
for row in obstacle_matrix:
    print(row)

def pickcurrent():
    w=None
    c=math.inf
    for a in open_list:
        b=a.gval+a.hval
        if b<c:
            c=b
            w=a
    return w
def findneighbours(h):
    x=h.row
    y=h.col
    nearby=[]
    if x!=0 and y!=0 and x!=9 and y!=9:
        nearby.append(node(y+1,x+1))
        nearby.append(node(y,x+1))
        nearby.append(node(y+1,x))
        nearby.append(node(y-1,x+1))
        nearby.append(node(y+1,x-1))
        nearby.append(node(y-1,x-1))
        nearby.append(node(y,x-1))
        nearby.append(node(y-1,x))
    elif x==0 and 0<y<9:
        nearby.append(node(y,x+1))
        nearby.append(node(y+1,x))
        nearby.append(node(y-1,x))
        nearby.append(node(y + 1, x + 1))
        nearby.append(node(y - 1, x + 1))
    elif y==0 and 0<x<9:
        nearby.append(node(y + 1, x + 1))
        nearby.append(node(y, x + 1))
        nearby.append(node(y + 1, x))
        nearby.append(node(y + 1, x - 1))
        nearby.append(node(y, x - 1))
    elif x==9 and 0<y<9:
        nearby.append(node(y + 1, x))
        nearby.append(node(y + 1, x - 1))
        nearby.append(node(y - 1, x - 1))
        nearby.append(node(y, x - 1))
        nearby.append(node(y - 1, x))
    elif y==9 and 0<x<9:
        nearby.append(node(y, x + 1))
        nearby.append(node(y - 1, x + 1))
        nearby.append(node(y - 1, x - 1))
        nearby.append(node(y, x - 1))
        nearby.append(node(y - 1, x))
    elif x==0 and y==0:
        nearby.append(node(y + 1, x))
        nearby.append(node(y, x + 1))
        nearby.append(node(y + 1, x + 1))
    elif x==0 and y==9:
        nearby.append(node(y, x + 1))
        nearby.append(node(y - 1, x + 1))
        nearby.append(node(y - 1, x))
    elif x==9 and y==0:
        nearby.append(node(y + 1, x))
        nearby.append(node(y + 1, x - 1))
        nearby.append(node(y, x - 1))
    else:
        nearby.append(node(y, x - 1))
        nearby.append(node(y - 1, x))
        nearby.append(node(y - 1, x - 1))
    return nearby
def findgval(o,p):
    if o.row==p.row:
        j=p.gval+10
    elif o.col==p.col:
        j= p.gval + 10
    else:
        j=p.gval+math.sqrt(2)*10
    return j

def findhval(o):
    a=o.row
    b=o.col
    h=math.sqrt((9-a)*(9-a)+(9-b)*(9-b))*10
    return h
c=0
def check_obstacle(d):
    a=d.col
    b=d.row
    if obstacle_matrix[b][a]==1:
        return True
    else:
        return False
while solved==False:
    current=pickcurrent()
    for i in range(len(open_list)):
        if open_list[i] == current:
            open_list.pop(i)
            break;

    print(c,current)
    c+=1
    closed.append(current)
    neighbours=findneighbours(current)
    for d in neighbours:
        if check_obstacle(d)==True or any(cell.row == d.row and cell.col == d.col for cell in closed):
            continue
        if findgval(d,current)<d.gval or not any(cell.row == d.row and cell.col == d.col for cell in open_list):
            d.gval=findgval(d,current)
            d.hval=findhval(d)
            d.parent=current
            print(d.gval,d.hval,d.row,d.col,check_obstacle(d))
            if d.hval==0:
                goal_point.parent=d
                solved=True
                break
            if d not in open_list:
                open_list.append(d)
path = []
current = goal_point

while current != start_point:
    path.append(current)
    current = current.parent

path.append(start_point)
path.reverse()
print(path)