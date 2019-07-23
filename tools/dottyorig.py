# Dot a Glyph

from fontTools.ttLib import TTFont
from beziers.path import BezierPath
from beziers.path.representations.fontparts import FontParts
from fontParts.world import *
from beziers.point import Point
from beziers.path.geometricshapes import Circle
import sys

dotradius   = 5
dotspacing  = 8
drawarrows  = True
arrowvector = Point(15,15)

fontpath    = "StrokeTest-Regular.ufo"
newfontpath  = "StrokeTest-Dotted.ufo"

glyphs_to_annotate = ["A","B","C","D","h","i","j"]

numbersfont = "Source Sans Pro-Regular.ufo"
numbers = ["one", "two","three","four","five","six","seven","eight","nine"]

font = OpenFont(fontpath)
numbersfont = OpenFont(numbersfont)

def annotate_glyph(glyphname):
  paths = FontParts.fromFontpartsGlyph(font[glyphname])
  paths2 = []
  if drawarrows:
    for i in range(0,len(paths)):
      arrowP = paths[i].clone()
      arrowP.translate(arrowvector)
      arrowSeg, _ = (arrowP.asSegments())[0].splitAtTime(0.25)
      s = arrowSeg.start
      arrowPath = BezierPath.fromSegments([arrowSeg])
      # arrowPath.closed = False
      paths2.append(arrowPath)
      number = FontParts.fromFontpartsGlyph(numbersfont[numbers[i]])
      # print(number[0].asNodelist())
      number[0].scale(0.05)
      number[0].translate(Point(s.x+5,s.y+5))
      number[0].closed=True
      paths2.append(number[0])
      # print('<text x="%s" y="%s">%i</text>' % (s.x+5.0,height-(s.y+5.0),1+i))
      # print('<path d="%s" stroke="black" stroke-width="2" fill="transparent" marker-end="url(#arrowhead)"/>\n' % path2svg([arrowSeg]))

  splitlist = []
  for i in range(0,len(paths)):
    for j in range(i+1,len(paths)):
      one = paths[i]
      two = paths[j]
      for s1 in one.asSegments():
        for s2 in two.asSegments():
          for inter in s1.intersections(s2):
            splitlist.append((inter.seg1,inter.t1))
            splitlist.append((inter.seg2,inter.t2))

  for path in paths:
    path.splitAtPoints(splitlist)

  segs = []
  for i in range(0,len(paths)):
    segs = paths[i].asSegments()
    for s in segs:
      paths2.append(Circle(dotradius, origin=s.start))
      if s.length > dotspacing*dotradius:
        closeEnough = int(s.length/(dotspacing*dotradius))
        samples = s.regularSample(closeEnough)
        for p in samples[1:]:
          paths2.append(Circle(dotradius, origin=p))

  if len(segs)>0:
    paths2.append(Circle(dotradius, origin=segs[-1].end))
  for p in paths2:
    FontParts.drawToFontpartsGlyph(font[glyphname],p)

for i in glyphs_to_annotate:
  print("Annotating %s" % i)
  annotate_glyph(i)

font.save(newfontpath)