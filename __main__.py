import sys


"""Charts are lists of lists, ordered by ascending list length.
Within each list, the first element must be the smallest positive element.
"""
CHART = [[1, -1], [2, 3, -2, -3]]
# Hard case with 1 orbit.
# CHART = [[1, 5, -2, -1, 7, 3, 2, 6, -3, -4, -5, -6, -7, 4]]

TIKZ_PICTURE_BEGIN = """\\begin{tikzpicture}[use Hobby shortcut]"""
TIKZ_PICTURE_END = "\\end{tikzpicture}"

KNOT_BEGIN = """\\begin{knot}[
  consider self intersections=true,
  end tolerance=3pt,
%  draft mode=crossings,
  only when rendering/.style={
%    show curve endpoints
  }
]"""
KNOT_END = "\\end{knot}"

class Chart:
  def __init__(self, chart):
    self._chart = chart
    self._num_orbits = len(chart)

  # Returns the index of the dict in arc_dicts containing val.
  def _get_cycle_index(self, arc_dicts, val):
    for (idx, arc_dict) in enumerate(arc_dicts):
      if val in arc_dict.keys():
        return idx

  # Computes the string specifying the curve.
  # Crossings are positioned 3 units apart on the x-axis.
  def _compute_curve(self):
    arc_dicts = []
    total_multiplicity = 0
    for cycle in self._chart:
      multiplicity = int(len(cycle) / 2)
      total_multiplicity += multiplicity

      # Given a value, find its position in the cycle
      arc_dict = {}
      for idx, val in enumerate(cycle):
        arc_dict[val] = idx
      arc_dicts.append(arc_dict)
          
    output = "([closed]0, 0) .. (1, 0) .. "
    for val in range(2, total_multiplicity + 1):
      # Which cycle?
      idx = self._get_cycle_index(arc_dicts, val)
      arc_dict = arc_dicts[idx]
      orbit_size = len(arc_dict)
    
      # Incoming arc
      x = idx * 3
      angle = (360.0/orbit_size) * arc_dict[-val]
      output +=  "($(" + str(x) + ", 0) "
      output += "+ (" + str(angle) + ":1)$) .. "
      output += "(" + str(x) + ", 0) .. "
      
      # Outgoing arc
      angle = (360.0/orbit_size) * arc_dict[val]
      output += "+(" + str(angle) + ":1) .. "
    # Final incoming arc
    idx = self._get_cycle_index(arc_dicts, -1)
    arc_dict = arc_dicts[idx]
    orbit_size = len(arc_dict)
    x = idx * 3
    angle = (360.0/orbit_size) * arc_dict[-1]
    output +=  "($(" + str(x) + ", 0) "
    output += "+ (" + str(angle) + ":1)$) .. "
    output += "(" + str(x) + ", 0);"
    return output

  # Returns string that draws the curve.
  def draw_strand(self):
    return "\\strand " + self._compute_curve()
 
  # Returns string to draws orientation arrows on the curve.
  # Uses the method from here:
  #   https://tex.stackexchange.com/questions/534491/unexpected-behavior-of-arrow-decorations-on-knots-multiple-arrows-and-gaps-appe
  def draw_arrows(self):
    output = "\\draw[opacity=0, postaction={decorate}, decoration={"
    output += "\n  markings,"
    
    total_multiplicity = 0
    for cycle in self._chart:
      total_multiplicity += int(len(cycle) / 2)
    for i in range(total_multiplicity):
      output += '\n' + "  mark=at position "
      output += str((2 * i + 1)/(total_multiplicity * 2))
      output += " with {\\arrow[line width=2pt, red, opacity=1]{>}},"
      
    output += "}]"
    output += self._compute_curve()
    return output

  # Returns string to draw crossing points.
  # They are spaced 3 units apart on the x-axis.
  def draw_crossings(self):
    output = ""
    for i in range(self._num_orbits):
      output += '\n' + ("\\draw[fill=red, draw=none] ("
                        + str(i * 3) + ",0) circle (0.15);")
    return output

  # Returns string to draw tikzpicture of the curve.
  def draw_chart(self):
    output = TIKZ_PICTURE_BEGIN
    output += '\n' + KNOT_BEGIN
    output += '\n' + self.draw_strand()
    output += '\n' + KNOT_END
    output += '\n' + self.draw_arrows()
    output += '\n' + self.draw_crossings()
    output += '\n' + TIKZ_PICTURE_END
    return output


def main():
  my_chart = Chart(CHART)
  print(my_chart.draw_chart())


if __name__ == "__main__":
    sys.exit(main())
