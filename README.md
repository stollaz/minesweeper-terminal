# Minesweeper-terminal
Fully playable minesweeper in the terminal!
Why? Why not

### TODO
- Allow quickplay, so once you're familiar with the game, you can enter in a command in a single line instead of using 2 lines
  - e.g. `flag:F5`, `clear:12E`, `C10:flag`, or maybe even `flag d6` or `j14 clear`
- Potentially a new feature to automatically clear all remaining cells around a given cell
  - This is useful if e.g. you have a cell with 1 adjacent mine, and you have already flagged the mine, so you can reveal all surrounding cells without typing it all individually
  - e.g. `clearRadius`, `clearradius:c7` or something    
- More comprehensive playtesting (there *must* be some bugs I missed during development

### Bug Log
- Games on a grid of 2x2 with any number of mines are bugged, as clearing any cell causes an infinite loop
  - This does not seem to happen on larger grid sizes 
- Games on non-square grids don't seem to function properly when clearing
  - On a game of width 10 and height 5, clearing a cell left borders with cells containing no adjacent mines, which is unintended
  - This is likely due to arguments being the wrong way round when expanding the clearing
