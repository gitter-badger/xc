//----------------------------------------------------------------------------
//  XC program; finite element analysis code
//  for structural analysis and design.
//
//  Copyright (C)  Luis Claudio Pérez Tato
//
//  This program derives from OpenSees <http://opensees.berkeley.edu>
//  developed by the  «Pacific earthquake engineering research center».
//
//  Except for the restrictions that may arise from the copyright
//  of the original program (see copyright_opensees.txt)
//  XC is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or 
//  (at your option) any later version.
//
//  This software is distributed in the hope that it will be useful, but 
//  WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details. 
//
//
// You should have received a copy of the GNU General Public License 
// along with this program.
// If not, see <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------------
/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
**                                                                    **
** (C) Copyright 1999, The Regents of the University of California    **
** All Rights Reserved.                                               **
**                                                                    **
** Commercial use of this program without express permission of the   **
** University of California, Berkeley, is strictly prohibited.  See   **
** file 'COPYRIGHT'  in main directory for information on usage and   **
** redistribution,  and for a DISCLAIMER OF ALL WARRANTIES.           **
**                                                                    **
** Developed by:                                                      **
**   Frank McKenna (fmckenna@ce.berkeley.edu)                         **
**   Gregory L. Fenves (fenves@ce.berkeley.edu)                       **
**   Filip C. Filippou (filippou@ce.berkeley.edu)                     **
**                                                                    **
** ****************************************************************** */

// $Revision: 1.1 $
// $Date: 2006/01/18 22:11:05 $
// $Source: /usr/local/cvs/OpenSees/SRC/element/forceBeamColumn/DistHingeIntegration.cpp,v $

#include <domain/mesh/element/truss_beam_column/forceBeamColumn/beam_integration/DistHingeIntegration.h>

#include <utility/matrix/Matrix.h>
#include <utility/matrix/Vector.h>
#include <utility/actor/objectBroker/FEM_ObjectBroker.h>
#include <domain/mesh/element/utils/Information.h>
#include "domain/component/Parameter.h"

void XC::DistHingeIntegration::libera(void)
  {
    if(beamInt)
      delete beamInt;
    beamInt= nullptr;
  }

void XC::DistHingeIntegration::copia(const BeamIntegration *bi)
  {
    libera();
    if(bi)
      beamInt = bi->getCopy();
//     if(!beamInt)
//       std::cerr << "XC::DistHingeIntegration::DistHingeIntegration -- failed to get copy of XC::BeamIntegration" << std::endl;
  }


XC::DistHingeIntegration::DistHingeIntegration(double lpi,double lpj,const BeamIntegration &bi)
  : PlasticLengthsBeamIntegration(BEAM_INTEGRATION_TAG_HingeMidpoint,lpi,lpj), beamInt(nullptr), parameterID(0)
  { copia(&bi); }

XC::DistHingeIntegration::DistHingeIntegration(void)
  : PlasticLengthsBeamIntegration(BEAM_INTEGRATION_TAG_HingeMidpoint), beamInt(nullptr), parameterID(0)
  {}

XC::DistHingeIntegration::DistHingeIntegration(const DistHingeIntegration &otro)
  : PlasticLengthsBeamIntegration(otro), beamInt(nullptr), parameterID(otro.parameterID)
  { copia(otro.beamInt); }

XC::DistHingeIntegration &XC::DistHingeIntegration::operator=(const DistHingeIntegration &otro)
  {
    PlasticLengthsBeamIntegration::operator=(otro);
    parameterID= otro.parameterID;
    copia(otro.beamInt);
    return *this;
  }

XC::DistHingeIntegration::~DistHingeIntegration(void)
  { libera(); }

void XC::DistHingeIntegration::getSectionLocations(int numSections, double L,double *xi) const
  {
    int numPerHinge = numSections/2;

    beamInt->getSectionLocations(numPerHinge, L, xi);

    double betaI = lpI/L;
    double betaJ = lpJ/L;
  
    // Map from [0,L] to [L-lpJ,L]
    for(int i = 0; i < numPerHinge; i++)
      {
        xi[numSections-1-i] = 1.0-betaJ*xi[i];
        xi[i] *= betaI;
      }
    std::cerr << "XC::DistHingeIntegration::getSectionLocations -- implementation for interior not yet finished" << std::endl;
  }

void XC::DistHingeIntegration::getSectionWeights(int numSections, double L,double *wt) const
  {
    int numPerHinge = numSections/2;

    beamInt->getSectionWeights(numPerHinge, L, wt);

    double betaI = lpI/L;
    double betaJ = lpJ/L;
  
    // Map from [0,lpI] to [L-lpJ,L]
    for(int i = 0; i < numPerHinge; i++)
      {
        wt[numSections-1-i] = betaJ*wt[i];
        wt[i] *= betaI;
      }
    std::cerr << "XC::DistHingeIntegration::getSectionWeights -- implementation for interior not yet finished" << std::endl;
  }

XC::BeamIntegration *XC::DistHingeIntegration::getCopy(void) const
  { return new DistHingeIntegration(*this); }

int XC::DistHingeIntegration::setParameter(const std::vector<std::string> &argv, Parameter &param)
  {
    if(argv[0] == "lpI")
      return param.addObject(1, this);
    else if(argv[0] == "lpJ")
      return param.addObject(2, this);
    else 
      return -1;
  }

int XC::DistHingeIntegration::updateParameter(int parameterID, Information &info)
  {
    switch (parameterID)
      {
      case 1:
        lpI = info.theDouble;
        return 0;
      case 2:
        lpJ = info.theDouble;
        return 0;
      default:
        return -1;
      }
  }

int XC::DistHingeIntegration::activateParameter(int paramID)
  {
    parameterID = paramID;
    // For Terje to do
    return 0;
  }

void XC::DistHingeIntegration::Print(std::ostream &s, int flag)
  {
    s << "DistHinge" << std::endl;
    s << " lpI = " << lpI;
    s << " lpJ = " << lpJ << std::endl;
    beamInt->Print(s, flag);
    return;
  }

void XC::DistHingeIntegration::getLocationsDeriv(int numSections, double L, double dLdh, double *dptsdh)
  {
    int numPerHinge = numSections/2;

    double oneOverL = 1/L;
    double betaI = lpI*oneOverL;
    double betaJ = lpJ*oneOverL;

    beamInt->getSectionLocations(numPerHinge, L, dptsdh);

    if(parameterID == 1)
      { // lpI
        for(int i = 0; i < numPerHinge; i++)
          {
            dptsdh[i] = oneOverL*dptsdh[i];
            dptsdh[numSections-1-i] = 0.0;
          }
      }
    else if(parameterID == 2)
      { // lpJ
        for(int i = 0; i < numPerHinge; i++)
          {
            dptsdh[numSections-1-i] = -oneOverL*dptsdh[i];
            dptsdh[i] = 0.0;
          }
      }
    else if(dLdh != 0.0)
      {
        for(int i = 0; i < numPerHinge; i++)
          {
            dptsdh[numSections-1-i] = betaJ*oneOverL*dLdh*dptsdh[i];
            dptsdh[i] = -betaI*oneOverL*dLdh*dptsdh[i];
          }
      }
    else
      {
        for(int i = 0; i < numSections; i++)
          dptsdh[i] = 0.0;
      }
    return;
  }

void XC::DistHingeIntegration::getWeightsDeriv(int numSections, double L,double dLdh, double *dwtsdh)
  {
    int numPerHinge = numSections/2;

    double oneOverL = 1/L;
    double betaI = lpI*oneOverL;
    double betaJ = lpJ*oneOverL;

    beamInt->getSectionWeights(numPerHinge, L, dwtsdh);

    if(parameterID == 1)
      { // lpI
        for(int i = 0; i < numPerHinge; i++)
          {
            dwtsdh[i] = oneOverL*dwtsdh[i];
            dwtsdh[numSections-1-i] = 0.0;
          }
      }
    else if(parameterID == 2)
      { // lpJ
        for(int i = 0; i < numPerHinge; i++)
          {
            dwtsdh[numSections-1-i] = oneOverL*dwtsdh[i];
            dwtsdh[i] = 0.0;
          }
      }
    else if(dLdh != 0.0)
      {
        for(int i = 0; i < numPerHinge; i++)
          {
            dwtsdh[numSections-1-i] = -betaJ*oneOverL*dLdh*dwtsdh[i];
            dwtsdh[i] = -betaI*oneOverL*dLdh*dwtsdh[i];
          }
      }
    else
      {
        for(int i = 0; i < numSections; i++)
          dwtsdh[i] = 0.0;
      }
    return;
  }
