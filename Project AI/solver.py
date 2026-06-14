def solve(n):
    sols, board = [], [0]*n
    def ok(r): return all(board[i]!=board[r] and abs(board[i]-board[r])!=r-i for i in range(r))
    def bt(r=0):
        if r==n: sols.append(board[:])
        else:
            for c in range(n):
                board[r]=c
                if ok(r): bt(r+1)
    bt(); return sols