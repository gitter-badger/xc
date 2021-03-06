# -*- coding: utf-8 -*-
''' Lateral torsional buckling of steel beams. '''
from __future__ import division

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2016 LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import math
from miscUtils import LogMessages as lmsg
import scipy.interpolate
import numpy

def getLateralTorsionalBucklingCurve(profile):
  ''' Returns the lateral torsional bukling curve name (a,b,c or d) depending of the type of section (rolled, welded,...). EC3 Table 6.4, 6.3.2.2(2).
  :param profile: cross section profile.
  :param rypo: 'rolled' or 'welded' profile
  '''
  if(profile.typo=='rolled'):
    if((profile.h()/profile.b())<=2):
      return 'a'
    else:
      return 'b'
  elif(profile.typo=='welded'):
    if((profile.h()/profile.b())<=2):
      return 'c'
    else:
      return 'd'
  else:
    return 'd'

def shearBucklingVerificationNeeded(profile):
  '''Returns true if shear buckling verification is needed EC3-1-5
  :param profile: cross section profile.'''
  epsilon= math.sqrt(235e6/profile.steelType.fy)
  eta= 1.0 #Conservative
  f1= profile.hw()/profile.tw()
  f2= 72*epsilon/eta
  return (f1>f2)

def getBendingResistanceReductionCoefficient(profile,Vd):
  '''Returns bending resistance reduction coefficient as in
     clause 6.2.8 of EC31-1
  :param profile: cross section profile.
  '''
  VplRd= profile.getVplRdy()
  ratio= Vd/VplRd
  if(ratio<=0.5):
    return 0.0 #No reduction
  else:
    return (2*ratio-1)**2

def getMvRdz(profile,sectionClass,Vd):
  '''Returns the major bending resistance of the cross-section under a
     shear force of Vd.
    :param profile: cross section profile.
  '''
  McRdz= profile.getMcRdz(sectionClass)
  reductionCoeff= profile.getBendingResistanceReductionCoefficient(Vd)
  if(reductionCoeff<=0.0):
    return McRdz
  else:
    Aw= profile.hw()*profile.tw()
    sustr= reductionCoeff*Aw**2/4.0/profile.tw()
    return min((profile.getWz(sectionClass)-sustr)*profile.steelType.fy/profile.steelType.gammaM0(),McRdz)

def getLateralBucklingImperfectionFactor(profile):
  ''' Returns lateral torsional imperfection factor depending of the type of section (rolled, welded,...).
    :param profile: cross section profile.
  '''
  curve= getLateralTorsionalBucklingCurve(profile)
  if(curve=='A' or curve=='a'):
    return 0.21
  elif(curve=='B' or curve=='b'):
    return 0.34
  elif(curve=='C' or curve=='c'):
    return 0.49
  elif(curve=='D' or curve=='d'):
    return 0.76
  else:
    return 0.76

class SupportCoefficients(object):

  def __init__(self,ky= 1.0, kw= 1.0, k1= 1.0, k2= 1.0):
    ''' Constructor

     :param ky: lateral bending coefficient ky= 1.0 => free lateral bending
                                            ky= 0.5 => prevented lateral bending
     :param kw: warping coefficient kw= 1.0 => free warping
                                    ky= 0.5 => prevented warping
     :param k1: warping AND lateral bending coefficient at left end
                                    k1= 1.0 => free warping AND lateral bending
                                    k1= 0.5 => prevented warp. AND lateral bending
     :param k2: warping AND lateral bending coefficient at right end
                                    k2= 1.0 => free warping AND lateral bending
                                    k2= 0.5 => prevented warp. AND lateral bending.
    '''

    self.ky= ky
    self.kw= kw
    self.k1= k1
    self.k2= k2
    
  def getAlphaI(self):
    ''' returns the five alpha values that are needed for C1 calculation.'''
    return [(1.0-self.k2),5*self.k1**3/self.k2**2,5*(1.0/self.k1+1.0/self.k2),5*self.k2**3/self.k1**2,(1.0-self.k1)]

def getLateralBucklingIntermediateFactor(profile,sectionClass,xi,Mi,supportCoefs= SupportCoefficients()):
  ''' Returns lateral torsional buckling intermediate factor value.

     :param profile: cross section profile.
     :param xi: abcissae for the moment diagram
     :param Mi: ordinate for the moment diagram
     :param supportCoefs: coefficients that represent support conditions.
  '''
  alphaLT= profile.getLateralBucklingImperfectionFactor()
  overlineLambdaLT= profile.getLateralBucklingNonDimensionalBeamSlenderness(sectionClass,xi,Mi,supportCoefs)
  return 0.5*(1+alphaLT*(overlineLambdaLT-0.2)+overlineLambdaLT**2)

def getLateralBucklingReductionFactor(profile,sectionClass,xi,Mi,supportCoefs= SupportCoefficients()):
  ''' Returns lateral torsional buckling reduction factor value.

     :param profile: cross section profile.
     :param sectionClass: section classification (1,2,3 or 4)
     :param xi: abcissae for the moment diagram
     :param Mi: ordinate for the moment diagram
     :param supportCoefs: coefficients that represent support conditions.
  '''  
  phiLT= profile.getLateralBucklingIntermediateFactor(sectionClass,xi,Mi,supportCoefs)
  overlineLambdaLT= profile.getLateralBucklingNonDimensionalBeamSlenderness(sectionClass,xi,Mi,supportCoefs)
  return 1.0/(phiLT+math.sqrt(phiLT**2-overlineLambdaLT**2))

def getLateralTorsionalBucklingResistance(profile,sectionClass,xi,Mi,supportCoefs= SupportCoefficients()):
  '''Returns lateral torsional buckling resistance of this cross-section.
     Calculation is made following the paper:

     A. López, D. J. Yong, M. A. Serna,
     Lateral-torsional buckling of steel beams: a general expression for
     the moment gradient factor.
     (Lisbon, Portugal: Stability and ductility of steel structures, 2006).

     :param profile: cross section profile.
     :param sectionClass: section classification (1,2,3 or 4)
     :param xi: abcissae for the moment diagram
     :param Mi: ordinate for the moment diagram
     :param supportCoefs: coefficients that represent support conditions.
  '''  
  chiLT= profile.getLateralBucklingReductionFactor(sectionClass,xi,Mi,supportCoefs)
  return chiLT*profile.getMcRdz(sectionClass)

def getMcr(profile,xi,Mi,supportCoefs= SupportCoefficients()):
  '''Returns elastic critical moment about minor axis: y
     Calculation is made following the paper:

     A. López, D. J. Yong, M. A. Serna,
     Lateral-torsional buckling of steel beams: a general expression for
     the moment gradient factor.
     (Lisbon, Portugal: Stability and ductility of steel structures, 2006).

     :param profile: cross section profile.
     :param xi: abcissae for the moment diagram
     :param Mi: ordinate for the moment diagram
     :param supportCoefs: coefficients that represent support conditions.
  '''
  mgf= MomentGradientFactorC1(xi,Mi)
  L= mgf.getL()
  C1= mgf.getC1(supportCoefs)
  pi2EIy= math.pi**2*profile.EIy()
  GIt= profile.GJ()
  kyL2= (supportCoefs.ky*L)**2
  Mcr0= pi2EIy/kyL2
  sum1= (supportCoefs.ky/supportCoefs.kw)**2*profile.Iw()/profile.Iy()
  sum2= GIt/Mcr0
  f2= math.sqrt(sum1+sum2)
  # print '  L= ', L
  # print '  kyL2= ', kyL2
  # print '  GJ= ', GIt/1e3
  # print '  Iw= ', profile.Iw()*100**6, ' cm^6'
  # print '  C1= ', C1
  # print '  Mcr0=', Mcr0/1e3  
  # print '  sum1= ', sum1
  # print '  sum2= ', sum2
  # print '  f2= ', f2
  return C1*Mcr0*f2

def getLateralBucklingNonDimensionalBeamSlenderness(profile,sectionClass,xi,Mi,supportCoefs= SupportCoefficients()):
  '''Returns non dimensional beam slenderness
     for lateral torsional buckling
     see parameter definition on method getMcr.

     :param profile: cross section profile.
     :param sectionClass: section classification (1,2,3 or 4)
     :param xi: abcissae for the moment diagram
     :param Mi: ordinate for the moment diagram
     :param supportCoefs: coefficients that represent support conditions.
  '''
  Mcr= profile.getMcr(xi,Mi,supportCoefs)
  return math.sqrt(profile.getWz(sectionClass)*profile.steelType.fy/Mcr)

class MomentGradientFactorC1(object):
  ''' Calculation of the C1 moment gradient factor as defined
      in: A. López, D. J. Yong, M. A. Serna,
      Lateral-torsional buckling of steel beams: a general expression for
      the moment gradient factor.
      (Lisbon, Portugal: Stability and ductility of steel structures, 2006). '''
  def __init__(self,xi,Mi):
    self.xi= xi
    self.Mi= Mi
    self.momentDiagram= scipy.interpolate.interp1d(xi, Mi)
  
  def getL(self):
    ''' Returns the length of the moment diagram. '''
    return self.xi[-1]-self.xi[0]
  
  def getExtremeMoment(self):
    ''' Return the extreme of the bending moments (maximum or minimum). '''
    mMax= max(self.Mi)
    mMin= min(self.Mi)
    retval= mMax
    if(abs(retval)<abs(mMin)):
      retval= mMin
    return retval

  def getMi(self):
    ''' returns the five moment values that are needed for C1 calculation. '''
    nDiv= 4
    step= self.getL()/nDiv
    retval=list()
    xi= 0.0
    Mi= 0.0
    for i in range(0,nDiv+1):
      Mi= self.momentDiagram(xi)
      retval.append(float(Mi))
      xi+= step
    return retval

  def getA2(self):
    ''' return the value for the A2 coefficient. '''
    Mi= self.getMi()
    return (Mi[0]+2*Mi[1]+3*Mi[2]+2*Mi[3]+Mi[4])/(9*self.getExtremeMoment())

  def getA1(self,supportCoefs):
    ''' return the value for the A1 coefficient. 
       k1: warping AND lateral bending coefficient at left end
                               k1= 1.0 => free warping AND lateral bending
                               k1= 0.5 => prevented warp. AND lateral bending
       k2: warping AND lateral bending coefficient at right end
                               k2= 1.0 => free warping AND lateral bending
                               k2= 0.5 => prevented warp. AND lateral bending'''
    Mi= self.getMi()
    ai= supportCoefs.getAlphaI()
    Mmax2= self.getExtremeMoment()**2
    return (Mmax2+ai[0]*Mi[0]**2+ai[1]*Mi[1]**2+ai[2]*Mi[2]**2+ai[3]*Mi[3]**2+ai[4]*Mi[4]**2)/((1+ai[0]+ai[1]+ai[2]+ai[3]+ai[4])*Mmax2)

  def getC1(self,supportCoefs):
    ''' return the value for the C1 coefficient. 
       k1: warping AND lateral bending coefficient at left end
                               k1= 1.0 => free warping AND lateral bending
                               k1= 0.5 => prevented warp. AND lateral bending
       k2: warping AND lateral bending coefficient at right end
                               k2= 1.0 => free warping AND lateral bending
                               k2= 0.5 => prevented warp. AND lateral bending'''
    k= math.sqrt(supportCoefs.k1*supportCoefs.k2)
    rootK= math.sqrt(k)
    A1= self.getA1(supportCoefs)
    A2= self.getA2()
    B1= rootK*A1+((1-rootK)/2.0*A2)**2
    return (math.sqrt(B1)+(1-rootK)/2.0*A2)/A1

  
