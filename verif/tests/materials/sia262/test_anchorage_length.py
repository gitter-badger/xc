# -*- coding: utf-8 -*-

# Home made test.

from __future__ import division
import sys
import materials.sia262.anchorage

phi= 12e-3
fsd= 435e6
fck= 16e6
fbdA= materials.sia262.anchorage.adherenceStress(fck)
lbdA= materials.sia262.anchorage.getBasicAnchorageLength(phi,fck,fsd)
ratioA= (lbdA/phi-60.4166666667)/60.4166666667

fck= 20e6
fbdB= materials.sia262.anchorage.adherenceStress(fck)
lbdB= materials.sia262.anchorage.getBasicAnchorageLength(phi,fck,fsd)
ratioB= (lbdB/phi-51.7857142857)/51.7857142857

fck= 30e6
fbdC= materials.sia262.anchorage.adherenceStress(fck)
lbdC= materials.sia262.anchorage.getBasicAnchorageLength(phi,fck,fsd)
ratioC= (lbdC/phi-40.2777777778)/40.2777777778

# print "lbdA= ",lbdA, " m"
# print "ratioA= ",ratioA
# print "lbdB= ",lbdB, " m"
# print "ratioB= ",ratioB
# print "lbdC= ",lbdC, " m"
# print "ratioC= ",ratioC

import os
fname= os.path.basename(__file__)
if (abs(ratioA)<1e-12) & (abs(ratioB)<1e-12) & (abs(ratioC)<1e-12) :
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
