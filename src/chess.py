import random

class Board:
	def __init__(self):
		self.squares = [(Side.WHITE, Piece.EMPTY)]*64
		self[0, 0] = (Side.BLACK, Piece.ROOK)
		self[1, 0] = (Side.BLACK, Piece.KNIGHT)
		self[2, 0] = (Side.BLACK, Piece.BISHOP)
		self[3, 0] = (Side.BLACK, Piece.KING)
		self[4, 0] = (Side.BLACK, Piece.QUEEN)
		self[5, 0] = (Side.BLACK, Piece.BISHOP)
		self[6, 0] = (Side.BLACK, Piece.KNIGHT)
		self[7, 0] = (Side.BLACK, Piece.ROOK)

		for i in range(8):
			self[i, 1] = (Side.BLACK, Piece.PAWN)

		self[0, 7] = (Side.WHITE, Piece.ROOK)
		self[1, 7] = (Side.WHITE, Piece.KNIGHT)
		self[2, 7] = (Side.WHITE, Piece.BISHOP)
		self[3, 7] = (Side.WHITE, Piece.KING)
		self[4, 7] = (Side.WHITE, Piece.QUEEN)
		self[5, 7] = (Side.WHITE, Piece.BISHOP)
		self[6, 7] = (Side.WHITE, Piece.KNIGHT)
		self[7, 7] = (Side.WHITE, Piece.ROOK)

		for i in range(8):
			self[i, 6] = (Side.WHITE, Piece.PAWN)


	def __getitem__(self, index):
		return self.squares[index[0] + index[1]*8]

	def __setitem__(self, index, value):
		self.squares[index[0] + index[1]*8] = value

	def path_clear(self, *path):
		for p in path:
			if p[0] < 0 or p[1] < 0 or p[0] > 7 or p[1] > 7:
				return False
		return all(self[pos][1] == Piece.EMPTY for pos in path)

	def to_num_pos(self, pos):
		return ('abcdefgh'.index(pos[0]), int(pos[1]) - 1)	

	def to_str_pos(self, pos):
		return 'abcdefgh'[pos[0]] + str(pos[1] + 1)

	def moves_for(self, pos):
		side, piece = self[pos]
		moves = []
		def move(*path):
			if self.path_clear(*path):
				moves.append([0, path])

		def take(*path):
			if not (path[-1][0] < 0 or path[-1][1] < 0 or path[-1][0] > 7 or path[-1][1] > 7) and self.path_clear(*path[:-1]):
				if self[path[-1]][0] != side and self[path[-1]][1] != Piece.EMPTY:
					moves.append([Piece.value(self[path[-1]][1]), path])

		def movetake(*path):
			move(*path)
			take(*path)

		def increment(inc):
			p = (pos[0] + inc[0], pos[1] + inc[1])
			if p[0] < 0 or p[1] < 0 or p[0] > 7 or p[1] > 7:
				return
			move = []
			try:
				while self[p][1] == Piece.EMPTY:
					if p[0] < 0 or p[1] < 0 or p[0] > 7 or p[1] > 7:
						break
					move.append(p)
					moves.append([0, move])
					p = (p[0] + inc[0], p[1] + inc[1])
				else:
					if not (p[0] < 0 or p[1] < 0 or p[0] > 7 or p[1] > 7) and self[p][0] != side:
						move.append(p)
						moves.append([Piece.value(self[p][1]), move])
			except:
				pass

		if piece == Piece.PAWN and side == Side.BLACK:
			move((pos[0], pos[1] + 1))
			if pos[1] == 1:
				move((pos[0], pos[1] + 1), (pos[0], pos[1] + 2))
			take((pos[0] + 1, pos[1] + 1))
			take((pos[0] - 1, pos[1] + 1))
		elif piece == Piece.PAWN and side == Side.WHITE:
			move((pos[0], pos[1] - 1))
			if pos[1] == 6:
				move((pos[0], pos[1] - 1), (pos[0], pos[1] - 2))
			take((pos[0] + 1, pos[1] - 1))
			take((pos[0] - 1, pos[1] - 1))
		elif piece == Piece.BISHOP:
			increment((1, 1))
			increment((1, -1))
			increment((-1, 1))
			increment((-1, -1))
		elif piece == Piece.ROOK:
			increment((0, 1))
			increment((1, 0))
			increment((-1, 0))
			increment((0, -1))
		elif piece == Piece.QUEEN:
			increment((0, 1))
			increment((1, 0))
			increment((-1, 0))
			increment((0, -1))
			increment((1, 1))
			increment((1, -1))
			increment((-1, 1))
			increment((-1, -1))
		elif piece == Piece.KING:
			movetake((pos[0] + 1, pos[1] + 1))
			movetake((pos[0] + 1, pos[1]))
			movetake((pos[0] + 1, pos[1] - 1))
			movetake((pos[0], pos[1] + 1))
			movetake((pos[0], pos[1] - 1))
			movetake((pos[0] - 1, pos[1] + 1))
			movetake((pos[0] - 1, pos[1]))
			movetake((pos[0] - 1, pos[1] - 1))
		elif piece == Piece.KNIGHT:
			movetake((pos[0] + 1, pos[1] + 2))
			movetake((pos[0] - 1, pos[1] + 2))
			movetake((pos[0] - 1, pos[1] - 2))
			movetake((pos[0] + 1, pos[1] - 2))
			movetake((pos[0] + 2, pos[1] + 1))
			movetake((pos[0] - 2, pos[1] + 1))
			movetake((pos[0] - 2, pos[1] - 1))
			movetake((pos[0] + 2, pos[1] - 1))
		return moves

	def is_valid_for(self, pos, move):
		for m in self.moves_for(pos):
			if m[1][-1] == move:
				return True
		return False

	def in_check(self, side):
		for x in range(8):
			for y in range(8):
				s, piece = self[x, y]
				if s != side:
					for move in self.moves_for((x, y)):
						if move[0] == None:
							return True

	def in_danger(self, pos):
		side = self[pos][0]
		if side == Side.WHITE:
			side = Side.BLACK
		elif side == Side.BLACK:
			side = Side.WHITE

		for pos, peice in self.peices_for_side(side):
			for move in self.moves_for(pos):
				if move[1][-1] == pos:
					return True
		else:
			return False

	def print(self):
		print('  abcdefgh')
		for i in range(8):
			row = [str(i + 1),' ']
			for j in range(8):
				row.append(Piece.repr(self[j, i]))
			print(''.join(row))
		print()

	def indicate(self, *points):
		print('  abcdefgh')
		for i in range(8):
			row = [str(i + 1),' ']
			for j in range(8):
				if (j, i) in points:
					row.append('X')
				else:
					row.append(Piece.repr(self[j, i]))
			print(''.join(row))
		print()

	def set(self, pos, value):
		pos = self.to_num_pos(pos)
		self[pos] = value

	def get(self, pos):
		pos = self.to_num_pos(pos)
		return self[pos]

	def move(self, a, b):
		side, piece = self[a]
		if self.is_valid_for(a, b):
			old, self[b] = self[b], self[a]
			if self.in_check(side):
				self[b] = old
				return False
			else:
				self[a] = (side, Piece.EMPTY)
				return True
		else:
			return False

	def peices_for_side(self, side):
		for y in range(8):
			for x in range(8):
				s, piece = self[x, y]
				if s == side:
					yield (x, y), piece 

class Piece:
	EMPTY = 0
	PAWN = 1
	ROOK = 2
	KNIGHT = 3
	BISHOP = 4
	QUEEN = 5
	KING = 6

	def value(piece):
		if piece == Piece.PAWN:
			return 1
		elif piece in (Piece.BISHOP, Piece.KNIGHT):
			return 3
		elif piece == Piece.ROOK:
			return 5
		elif piece == Piece.QUEEN:
			return 9
		elif piece == Piece.EMPTY:
			return 0

	def repr(piece):
		side, piece = piece
		if piece == Piece.PAWN:
			x = 'P'
		elif piece == Piece.KNIGHT:
			x = 'N'
		elif piece == Piece.ROOK:
			x = 'R'
		elif piece == Piece.BISHOP:
			x = 'B'
		elif piece == Piece.QUEEN:
		 	x = 'Q'
		elif piece == Piece.KING:
			x = 'K'
		else:
			x = ' '
		if side == Side.BLACK:
			return x.lower()
		elif side == Side.WHITE:
			return x.upper()

class Side:
	BLACK = 0
	WHITE = 1

class ChessBot:
	def __init__(self, side):
		self.board = Board()
		self.side = side

	def move(self):
		valid_moves = []
		for pos, piece in self.board.peices_for_side(self.side):
			for move in self.board.moves_for(pos):
				valid_moves.append((pos, move))

		valid_moves.sort(key=lambda x: self.board.in_danger(x[1][1][-1]))
		a, (cp, p) = sorted(valid_moves, key=lambda x: x[1][0], reverse=True)[0]
		x = self.board.move(a, p[-1])
		return a, p[-1], cp

