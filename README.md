Python code to assist in generation of curves for the Appendix.

This is based on Andrew Stacey's tutorial for his knots and hobby packages:
https://loopspace.mathforge.org/HowDidIDoThat/TeX/Knots/

The following Stack Exchange threads were useful for debugging:
  * On adding orientation arrows to a knot:
    https://tex.stackexchange.com/questions/534491/unexpected-behavior-of-arrow-decorations-on-knots-multiple-arrows-and-gaps-appe
  * If an intersection is not recognized, the fix is to adjust the `end
    tolerance` parameter to be more sensitive:
    https://tex.stackexchange.com/questions/621135/tikz-s-knots-library-does-not-find-all-intersections
