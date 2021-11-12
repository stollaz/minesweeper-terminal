# Minesweeper-terminal
Fully playable minesweeper in the terminal!
Why? Why not

### TODO
- Potentially a new feature to automatically clear all remaining cells around a given cell
  - This is useful if e.g. you have a cell with 1 adjacent mine, and you have already flagged the mine, so you can reveal all surrounding cells without typing it all individually
  - e.g. `clearRadius`, `clearradius:c7` or something    
- More comprehensive playtesting (there *must* be some bugs I missed during development
- Allow game to be marked as won when only unmarked bombs remain on the map, no safe cells are left

### Bug Log
- Games on a grid of 2x2 with any number of mines are bugged, as clearing any cell causes an infinite loop
  - This does not seem to happen on larger grid sizes 
  - **STATUS**: Forbidden Behaviour
    - As of current commit (12/11/2021 02:30), the player is unnable to create boards with sizes below 3 in any direction (3x3 is the smallest possible)  
- Games on non-square grids don't seem to function properly when clearing
  - On a game of width 10 and height 5, clearing a cell left borders with cells containing no adjacent mines, which is unintended
  - This is likely due to arguments being the wrong way round when expanding the clearing, and the subroutine incorrectly thinking it has reached the edge of the board (height and width mixed up)
  - **STATUS**: Known, not addressed

### Done
- (This is now default) Allow quickplay, so once you're familiar with the game, you can enter in a command in a single line instead of using 2 lines
  - e.g. `flag:F5`, `clear:12E`, `C10:flag`, or maybe even `flag d6` or `j14 clear`
- Added time elapsed when game is won
