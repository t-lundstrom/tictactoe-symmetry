# tictactoe-symmetry
A tic-tac-toe game that computes the entire game tree of an nxn board, but only up to symmetry.

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

| Board size , how many to win | Number of nodes in game tree (without symmetry) | Number of nodes (with symmetry) | Time (without symmetry) | Time (with symmetry) |
| -- | -- | -- | -- | -- | 
| 3x3, 3 to win| 5478 | _ | 0.053s | _ |
| 4x4, 3 to win | 6,036,001 | _ | 78.138s | _ |
| 4x4, 4 to win | _ | _ | _ | _ |

