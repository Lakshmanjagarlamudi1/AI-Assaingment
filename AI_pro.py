from Missionaries import M, C, LEFT, RIGHT
import svgwrite
DEBUG = False
W=600; H=200
BOAT_LENGTH_FRAC = 0.2 # fraction of overall width W
BOAT_HEIGHT_FRAC = 0.2 # fraction of overall height H

#<INITIAL_STATE>
INITIAL_STATE = {'people':[[3, 0], [3, 0]], 'boat':LEFT }
#</INITIAL_STATE>

#<OPERATORS>
MC_combinations = [(1,0),(2,0),(3,0),(1,1),(2,1)]

OPERATORS = [Operator("Cross the river with "+str(m)+" missionaries and "+str(c)+" cannibals",
    lambda s, m1=m, c1=c: can_move(s,m1,c1),
    lambda s, m1=m, c1=c: move(s,m1,c1) )
    for (m,c) in MC_combinations]
#</OPERATORS>

#<COMMON_CODE>
M=0 # array index to access missionary counts
C=1 # same idea for cannibal
LEFT=0 # same idea for left side of river
RIGHT=1 # etc.

def copy_state(s):
   news = {}
   news['people']=[[0,0],[0,0]]
   for i in range(2): news['people'][i]=s['people'][i][:]
   news['boat'] = s['boat']
   return news

def can_move(s,m,c):
   '''Tests whether it’s legal to move the boat and take
   m missionaries and c cannibals.'''
   side = s['boat'] # Where the boat is.
   p = s['people']
   if m<1: return False # Need an M to steer boat.
   m_available = p[M][side]
   if m_available < m: return False # Can’t take more m’s than available
   c_available = p[C][side]
   if c_available < c: return False # Can’t take more c’s than available
   m_remaining = m_available - m
   c_remaining = c_available - c
   # Missionaries must not be outnumbered on either side:
   if m_remaining > 0 and m_remaining < c_remaining: return False
   m_at_arrival = p[M][1-side]+m
   c_at_arrival = p[C][1-side]+c
   if m_at_arrival > 0 and m_at_arrival < c_at_arrival: return False
   return True

def move(olds,m,c):
   '''Assuming it’s legal to make the move, this computes
   the new state resulting from moving the boat carrying
   m missionaries and c cannibals.'''
   s = copy_state(olds) # start with a deep copy.
   side = s['boat']
   p = s['people']

   p[M][side] = p[M][side]-m # Remove people from the current side.
   p[C][side] = p[C][side]-c
   p[M][1-side] = p[M][1-side]+m # Add them at the other side.
   p[C][1-side] = p[C][1-side]+c
   s['boat'] = 1-side # Move the boat itself.
   return s

def render_state(s):
  global W,H,BOAT_LENGTH_FRAC, DEBUG

  dwg = svgwrite.Drawing(filename = "test-svgwrite.svg",
  id = "state_svg",   # Must match the id in the html template.
  size = (str(W)+"px", str(H)+"px"),
  debug=True)

  # Background rectangle...
  dwg.add(dwg.rect(insert = (0,0),
   size = (str(W)+"px", str(H)+"px"),
   stroke_width = "1",
   stroke = "black",
   fill = "rgb(192, 150, 129)")) # tan

  # River in the middle (another rect.)
  dwg.add(dwg.rect(insert = (W*0.3,0),
    size = (str(W*0.4)+"px", str(H)+"px"),
    stroke_width = "1",
    stroke = "black",
    fill = "rgb(127, 150, 192)")) # turquoise

  # The boat
  boatX = 0.3*W
  boatY = H*(1-BOAT_HEIGHT_FRAC - 0.02)
  if (s['boat']): boatX=(0.7-BOAT_LENGTH_FRAC)*W
  dwg.add(dwg.rect(insert = (boatX,boatY),
     size = (str(W*BOAT_LENGTH_FRAC)+"px", str(H*BOAT_HEIGHT_FRAC)+"px"),
     stroke_width = "1",
     stroke = "black",
     fill = "rgb(192, 63, 63)"))
  # red dish
  dwg.add(dwg.text('B',
      insert = ((boatX+BOAT_LENGTH_FRAC*W/2),
            (boatY+BOAT_HEIGHT_FRAC*H/2)),
      text_anchor="middle",
      font_size="25",
     fill = "white"))

  # Missionaries
  Ms = s['people'][M]
  for i in range(Ms[LEFT]):
     draw_person(dwg, M, LEFT, i)
  for i in range(Ms[RIGHT]):
     draw_person(dwg, M, RIGHT, i)

  # Cannibals
  Cs = s['people'][C]
  for i in range(Cs[LEFT]):
     draw_person(dwg, C, LEFT, i)
  for i in range(Cs[RIGHT]):
     draw_person(dwg, C, RIGHT, i)

  if DEBUG:
     print(dwg.tostring())
     dwg.save()
  return (dwg.tostring())

def draw_person(dwg, M_or_C, left_or_right, i):
   "Represent a person as a colored rectangle."
   global W, H
   box_width = W*0.08
   box_height = H*0.3
   x = 0+W*0.01
   if left_or_right: x+=W*0.70
   x += i*W*0.1
   if M_or_C==M: color='green'; y=H*0.1
   else: color='violet'; y= H*0.6
   dwg.add(dwg.rect(insert = (x,y),
              size = (str(box_width)+"px", str(box_height)+"px"),
              stroke_width = "1",
              stroke = "black",
              fill = color))
   text = "M"
   if M_or_C==C: text = "C"
   dwg.add(dwg.text(text, insert = (x+box_width/2,y+box_height/2),
                    text_anchor="middle",
                    font_size="25",
                    fill = "white"))

 #The following predicate returns True if s is a goal state and False, otherwise.
def goal_test(s):
  '''If all Ms and Cs are on the right, then s is a goal state.'''
  p = s['people']
  return (p[M][RIGHT]==3 and p[C][RIGHT]==3)



copy_state(s)
can_move(s,m,c)
move(olds,m,c)
render_state(s)
draw_person(dwg, M_or_C, left_or_right, i)
goal_test(s)
