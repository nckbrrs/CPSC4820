import kivy

from kivy.app             import App
from kivy.properties      import *
from kivy.uix.label       import Label
from math                 import acos,cos,sin
from math                 import sqrt
from math                 import pi
from math                 import atan2,degrees, radians

class PatternId():
  DEBUG = False
  pc = None
  pb = None
  pa = None
  paUid = None
  pbUid = None
  pcUid = None
  minLength = 0
  minSide = (None, None)
  midPoint = (None, None)
  topPoint = None
  topPointUid = None
  distMidTop = None
  token_angle = None


  def build(self):
    pass 
    #self.buildPoints()
    #self.findTokenId(self.pa, self.pb, self.pc)

  def findTokenId(self, dic_points, points):
    # This function finds the smaller side of a triangle
    # Rotates the triangle so that smaller side is the base
    # Finds the mid-point of the smaller side
    # Finds the distance and angle between the mid-point and 
    # the third (top-point) of the triangle
    # Compares distance and angle to determine the ID of the token
    # print  points
    pa = dic_points[0]
    pb = dic_points[1]
    pc = dic_points[2]

    self.paUid = points[0].uid
    self.pbUid = points[1].uid
    self.pcUid = points[2].uid

    self.findMinLength(pa, pb, pc)
    #Adjust angle, rotate points
    '''
    angle = self.findAngle(self.minSide[1], self.minSide[0])
    self.token_angle = angle
    if angle < 0:
        angle = angle + 360

    #Rotate to determine id
    nmin = self.rotate(self.minSide[1], self.minSide[0], radians(360-angle))
    self.minSide = (nmin, self.minSide[1])
    self.topPoint = self.rotate(self.minSide[1], self.topPoint, radians(360-angle))

    if self.topPoint[1] < nmin[1]:
      nmin = self.rotate(self.minSide[1], self.minSide[0], radians(180))
      self.minSide = (nmin, self.minSide[1])
      self.topPoint = self.rotate(self.minSide[1], self.topPoint, radians(180))

    self.midPoint = self.findMidPoint(self.minSide[0], self.minSide[1])

    self.distMidTop = self.findLength(self.midPoint, self.topPoint)

    # Find angle between midpoint and top point
    idAngle = self.findAngle(self.midPoint, self.topPoint)

    tokenId = self.findId(idAngle, self.distMidTop)

    return tokenId
    '''
    if self.DEBUG: print  "Original minSide: " + str(self.minSide)
    angle = self.findAngle(self.minSide[1], self.minSide[0])
    if self.DEBUG: print  "original angle: " + str(angle)
    self.token_angle = angle
    if angle < 0:
        angle = angle + 360
    if self.DEBUG: print  "angle: " + str(angle)
    if self.DEBUG: print  "rotation pivot: " + str(self.minSide[1])
    #Rotate to determine id
    nmin = self.rotate(self.minSide[1], self.minSide[0], radians(360-angle))
    self.minSide = (nmin, self.minSide[1])
    if self.DEBUG: print  "normalized minSide: " + str(self.minSide)
    self.topPoint = self.rotate(self.minSide[1], self.topPoint, radians(360-angle))
    if self.DEBUG: print  "topPoint: " + str(self.topPoint)
    
    if self.topPoint[1] < nmin[1]:
      nmin = self.rotate(self.minSide[1], self.minSide[0], radians(180))
      self.minSide = (nmin, self.minSide[1])
      if self.DEBUG: print  "180 rotate normalized minSide: " + str(self.minSide)
      self.topPoint = self.rotate(self.minSide[1], self.topPoint, radians(180))
      if self.DEBUG: print  "180 rotate topPoint: " + str(self.topPoint)

    self.midPoint = self.findMidPoint(self.minSide[0], self.minSide[1])
    if self.DEBUG: print  "midPoint: " + str(self.midPoint)
    self.distMidTop = self.findLength(self.midPoint, self.topPoint)
    if self.DEBUG: print  "distMidTop: " + str(self.distMidTop)
    # Find angle between midpoint and top point
    idAngle = self.findAngle(self.midPoint, self.topPoint)
    if self.DEBUG: print  "idAngle: " + str(idAngle)
    
    tokenId = self.findId(idAngle, self.distMidTop)
    if self.DEBUG: print  "tokenId: " + str(tokenId)
    return tokenId

  def buildPoints(self):
    #Creates three points
    #Used for testing purposes only
    self.pc = [-525.928, 7.876]
    self.pb = [-553.876, 17.318]
    self.pa = [-529.491, -11.842]

  def findMinLength(self, pa, pb, pc):
    # Finds the side of minimum length given three points (triangle)

    l1 = self.findLength(pa, pb)
    l2 = self.findLength(pb, pc)
    l3 = self.findLength(pc, pa)

    if l1 < l2 and l1 < l3:
      self.minSide = (pa,pb)
      self.topPoint = pc
      self.topPointUid = self.pcUid
      self.minLength = l1
    elif l2 < l1 and l2 < l3:
      self.minSide = (pb, pc)
      self.topPoint = pa
      self.topPointUid = self.paUid
      self.minLength = l2
    else:
      self.minSide = (pc,pa)
      self.topPoint = pb
      self.topPointUid = self.pbUid
      self.minLength = l3

  def findLength(self, pi, pj):
    # Find length between two points
    x = abs(pi[0]-pj[0])
    y = abs(pi[1]-pj[1])
    length = sqrt((x*x)+(y*y))
    return length

  def findAngle(self, p1, p2):
    # Find the angle between two points
    xDiff = p2[0] - p1[0]
    yDiff = p2[1] - p1[1]
    return degrees(atan2(yDiff, xDiff))

  def rotate(self, origin, point, angle):
    #Rotates a point counterclockwise by a given angle around a given origin.
    #The angle should be given in radians.

    ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return [qx, qy]

  def findMidPoint(self, pa, pb):
    # Finds the mid-point between two points
    return (pa[0]+pb[0])/2, (pa[1]+pb[1])/2

  def findId(self, idAngle, distMidTop):
    # Compares angles and distances to determine the id of a token
    # if an id cannot be determined it returns zero

    tokenId = 0
    if idAngle <= 140.99 and idAngle >= 123.90:
      if distMidTop >= 29.9:
        tokenId = 1
    if idAngle <= 118.02 and idAngle >= 104.58:
      if distMidTop >= 36.8:
        tokenId = 2
    if idAngle <= 95.74 and idAngle >= 81.00:
      if distMidTop >= 151:
        tokenId = 3
    if idAngle <= 76.71 and idAngle >= 62.92:

      if distMidTop >= 37.2:
        tokenId = 4
    if idAngle <= 57.79 and idAngle >= 41.51:
      if distMidTop >= 30.1:
        tokenId = 5
    if idAngle <= 124.82 and idAngle >= 107.14:
      if distMidTop >= 27.4 and distMidTop <= 37.0:
        tokenId = 6
    if idAngle <= 95.74 and idAngle >= 81.00:
      if distMidTop <= 39.18:
        tokenId = 7
    if idAngle <= 73.6 and idAngle >= 55.02:
      
      if distMidTop >= 27.12 and distMidTop <= 37.9:
        tokenId = 8
    return tokenId

  def getTokenAngle(self):
    # Returns the angle of the identified token
    return self.token_angle
  
  def getTopPointUid(self):
    return self.topPointUid

  def clearTopPointUid(self):
    self.topPointUid = None