# About
This is a personal learning project where I experimented with an idea for tic-tac-toe. 
The game is played against a computer that computes the entire game tree at the beginning of the game and then always makes the most optimal move every time.
To prune search space, the boards are cosidered only up to symmetries of the square.
For example, if the current board is 

| X | O | _ |
| --| -- | -- |
| _ | _ | _  |
| _ | _ | _ |

then, up to symmetry, this the same position as the positions

(90 degree rotation)
| _ | _ | X |
| --| -- | -- |
| _ | _ | **O** |
| _ | _ | _ |

(180 degree rotation)
| _ | _ | _ |
| -- | -- | -- |
| _ | _ | _ |
| _ | **O** | **X** |


(270 degree rotation)
| _ | _ | _ |
| -- | -- | -- |
| **O** | _ | _ |
| **X** | _ | _ |


(mirror along horizontal axis)
| _ | _ | _ |
| --| -- | -- |
| _ | _ | _ |
| **X** | **O** | _ |


(mirror along vertical axis)
| _ | O | X |
| -- | -- | -- |
| _ | _ | _ |
| _ | _ | _ |

(mirror along diagonal axis)
| X | _ | _ |
|-- | -- | -- |
| **O** | _ | _ |
| _ | _ | _ |


(mirror along diagonal axis)
| _ | _ | _ |
| -- | -- | -- |
| _ | _ | **O** |
| _ | _ | **X** |

This reduces the number of positions that need to be considered. 

Below are some numbers that show how much the game tree is pruned and how much faster the computation is. The computations were done with an M1 macbook air.

| Board size, how many to win | Number of nodes in game tree (without symmetry) | Number of nodes in game tree (with symmetry) | Time to compute entire game tree (without symmetry) | Time to compute entire game tree (with symmetry) |
| -- | -- | -- | -- | -- | 
| 3x3, 3 to win| 5478 | 765 | 0.053s | 0.028s |
| 4x4, 3 to win | 6,036,001 | 756,387 | 78.138s | 13.220s |
| 4x4, 4 to win | 9,722,011 | 1,217,977 | 145.947s | 28.086s |

With 5x5 and beyond the game tree starts to get too big to be computed on a laptop, even with symmetry.

# Running
Run the script with your Python3 interpreter e.g.

`python3 tictactoe_symmetry.py`

The game asks the size of the board, how many are needed to win and does the player play with `X` or with `O`.
To place a marker at a square, give the input as `ij` where `i` is the row number and `j` is the column number. For example, `02`.

After each computer move, the game will report if the computer is on a winning path, on a path giving at least a tie, or if the player is on a winning path.

