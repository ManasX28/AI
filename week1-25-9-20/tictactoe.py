import copy

class XO:
    def opp_sign(self, sign):
        return 'O' if sign == 'X' else 'X' 

class Board:
    def __init__(self, size):
        self.s = size
        self.q = size*size
        self.empty = [i for i in range(self.q)]
        self.grid = ['.'] * self.q
    def ins(self, move, sign):
        self.grid[move] = sign
        self.empty = [i for i in self.empty if i != move]
    def is_full(self):
        return not len(self.empty)
    def get_col(self, col):
        return [self.grid[i] for i in range(col-1, self.q, self.s)] 
    def get_row(self, row):
        return self.grid[(row-1)*self.s:row*self.s] 
    def get_diag1(self):
        return [self.grid[i] for i in range(0, self.q, self.s+1)] 
    def get_diag2(self):
        return [self.grid[i] for i in range(self.s-1, self.q, self.s-1)][:-1] 
    def __str__(self):
        return '\n'.join([' '.join(map(str,self.grid[i:i+self.s])) 
                for i in range(0, self.q, self.s)]) + '\n'
    
class Tree:
    def find_best_move(self,board,depth,sign):

        if (board.empty==[]): return None
    
        best_move=-(2**(board.s**2))
        m=board.empty[0]
        for move in board.empty:
            b=copy.deepcopy(board)
            b.ins(move,sign)
            if (self.is_win(b,sign) or self.is_win(b,xo.opp_sign(sign))):
                return move
            curr_move=self.minimax(b,depth,False,xo.opp_sign(sign))
            if (curr_move > best_move):
                best_move = curr_move
                m=move
        return m 
    
    def minimax(self,board,depth,myTurn,sign):
        if (self.is_win(board,xo.opp_sign(sign))):
            if myTurn: 
                return -(board.s**2+1) + depth
            else:
                return (board.s**2+1) - depth
                
        elif (board.is_full()):
            return 0
    
        if (myTurn):
            bestVal=-(2**700)
            for move in board.empty: 
                b = copy.deepcopy(board)
                b.ins(move, sign)
                value=self.minimax(b,depth+1,not myTurn, xo.opp_sign(sign))
                bestVal = max([bestVal,value])
    
        else:
            bestVal = (2**700)
            for move in board.empty:
                b = copy.deepcopy(board)
                b.ins(move, sign)
                value = self.minimax(b, depth + 1, not myTurn, xo.opp_sign(sign))
                bestVal = min([bestVal, value])

        return bestVal

    def is_win(self,board, sign):
        temp=board.s
        wins = []  
        for i in range(1, temp + 1):
            wins.append(board.get_col(i))
            wins.append(board.get_row(i))
        wins.append(board.get_diag1())
        wins.append(board.get_diag2())
    
        for i in wins:
            if (self.is_same(i, sign)):
                return True
        return False
    
    def is_same(self, l, sign):
        for i in l:
            if (i != sign):
                return False
        return True

 
xo = XO()
board = Board(3)
tree = Tree()
sign = 'O'
human = False
while not board.is_full() and not tree.is_win(board, sign):
    sign = xo.opp_sign(sign)
    human = not human
    if human:
        move = input('your move as {} (0-8):'.format(sign))
    else:
        print('calculating...')
        move = tree.find_best_move(board, 0, sign)
    board.ins(int(move), sign)
    print (board)

