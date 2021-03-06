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
                                                                        
// $Revision: 1.7 $
// $Date: 2005/11/07 21:36:34 $
// $Source: /usr/local/cvs/OpenSees/SRC/domain/load/pattern/UniformExcitation.cpp,v $
                                                                        
                                                                        
// File: ~/domain/load/UniformExcitation.h
//
// Written: fmk 11/98
// Revised:
//
// Purpose: This file contains the class definition for XC::UniformExcitation.
// UniformExcitation is an abstract class.

#include <domain/load/pattern/load_patterns/UniformExcitation.h>
#include <domain/load/groundMotion/GroundMotion.h>
#include <domain/load/groundMotion/GroundMotionRecord.h>
#include <domain/domain/Domain.h>
#include <domain/mesh/node/Node.h>
#include <domain/mesh/element/Element.h>
#include "domain/mesh/node/NodeIter.h"
#include "domain/mesh/element/ElementIter.h"
#include <utility/actor/objectBroker/FEM_ObjectBroker.h>


XC::UniformExcitation::UniformExcitation(int tag)
  :EarthquakePattern(tag, PATTERN_TAG_UniformExcitation),
    theMotion(nullptr), theDof(0), vel0(0.0) {}

XC::UniformExcitation::UniformExcitation(GroundMotion &_theMotion, int dof, int tag, double velZero)
  :EarthquakePattern(tag, PATTERN_TAG_UniformExcitation), theMotion(&_theMotion), theDof(dof), vel0(velZero)
  {
    // add the motion to the list of ground motions
    addMotion(*theMotion);
  }

XC::GroundMotion &XC::UniformExcitation::getGroundMotionRecord(void)
  {
    if(!theMotion)
      {
        theMotion= new GroundMotionRecord();
        assert(theMotion);
        addMotion(*theMotion);
      }
    return *theMotion;
  }

void XC::UniformExcitation::setDomain(Domain *theDomain) 
  {
    XC::EarthquakePattern::setDomain(theDomain);

    // now we go through and set all the node velocities to be vel0
    if(vel0 != 0.0)
      {
        NodeIter &theNodes = theDomain->getNodes();
        Node *theNode;
        Vector newVel(1);
        int currentSize = 1;
        while ((theNode = theNodes()) != 0)
          {
            int numDOF = theNode->getNumberDOF();
            if(numDOF != currentSize) 
	      newVel.resize(numDOF);
      
            newVel = theNode->getVel();
            newVel(theDof) = vel0;
            theNode->setTrialVel(newVel);
            theNode->commitState();
          }
      }
  }

void XC::UniformExcitation::applyLoad(double time)
  {
    Domain *theDomain = getDomain();
    if(theDomain)
      {
        //if (numNodes != theDomain->getNumNodes()) {
        NodeIter &theNodes = theDomain->getNodes();
        Node *theNode;
        while((theNode = theNodes()) != 0)
          {
            theNode->setNumColR(1);
            theNode->setR(theDof, 0, 1.0);
          }
        //  }
        EarthquakePattern::applyLoad(time);
      }
    return;
  }

void XC::UniformExcitation::applyLoadSensitivity(double time)
  {
    Domain *theDomain = this->getDomain();
    if(theDomain)
      {

        //if (numNodes != theDomain->getNumNodes()) {
        NodeIter &theNodes = theDomain->getNodes();
        Node *theNode;
        while((theNode = theNodes()) != 0)
          {
            theNode->setNumColR(1);
            theNode->setR(theDof, 0, 1.0);
          }
        //  }
        EarthquakePattern::applyLoadSensitivity(time);
      }
  }

//! @brief Send members del objeto through the channel being passed as parameter.
int XC::UniformExcitation::sendData(CommParameters &cp)
  {
    int res= EarthquakePattern::sendData(cp);
    res+= cp.sendInt(theDof,getDbTagData(),CommMetaData(23));
    res+= cp.sendDouble(vel0,getDbTagData(),CommMetaData(24));
    res+= sendGroundMotionPtr(theMotion,getDbTagData(),cp,BrokedPtrCommMetaData(25,26,27));
    return res;
  }

//! @brief Receives members del objeto through the channel being passed as parameter.
int XC::UniformExcitation::recvData(const CommParameters &cp)
  {
    int res= EarthquakePattern::recvData(cp);
    res+= cp.receiveInt(theDof,getDbTagData(),CommMetaData(23));
    res+= cp.receiveDouble(vel0,getDbTagData(),CommMetaData(24));
    theMotion= receiveGroundMotionPtr(theMotion,getDbTagData(),cp,BrokedPtrCommMetaData(25,26,27));
    return res;
  }

//! @brief Sends object through the channel being passed as parameter.
int XC::UniformExcitation::sendSelf(CommParameters &cp)
  {
    setDbTag(cp);
    const int dataTag= getDbTag();
    inicComm(3);
    int res= sendData(cp);

    res+= cp.sendIdData(getDbTagData(),dataTag);
    if(res < 0)
      std::cerr << nombre_clase() << "sendSelf() - failed to send data\n";
    return res;
  }


//! @brief Receives object through the channel being passed as parameter.
int XC::UniformExcitation::recvSelf(const CommParameters &cp)
  {
    inicComm(3);
    const int dataTag= getDbTag();
    int res= cp.receiveIdData(getDbTagData(),dataTag);

    if(res<0)
      std::cerr << nombre_clase() << "::recvSelf - failed to receive ids.\n";
    else
      {
        setTag(getDbTagDataPos(0));
        res+= recvData(cp);
        if(res<0)
          std::cerr << nombre_clase() << "::recvSelf - failed to receive data.\n";
      }
    return res;
  }

void XC::UniformExcitation::Print(std::ostream &s, int flag)
  {
    s << "UniformExcitation  " << this->getTag() 
      << " - Not Printing the XC::GroundMotion\n";
  }
