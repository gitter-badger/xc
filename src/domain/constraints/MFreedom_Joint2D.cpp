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
                                                                        
// $Revision: 1.6 $
// $Date: 2004/09/01 04:01:27 $
// $Source: /usr/local/cvs/OpenSees/SRC/element/special/joint/MFreedom_Joint2D.cpp,v $

// Written: Arash Altoontash, Gregory Deierlein
// Created: 08/01
// Revision: Arash

// Purpose: This file contains the implementation of class MFreedom_Joint2D.


#include "MFreedom_Joint2D.h"
#include <domain/domain/Domain.h>
#include <domain/mesh/node/Node.h>

#include <cstdlib>
#include <cmath>

#include <utility/matrix/Matrix.h>
#include <utility/matrix/ID.h>
#include <utility/actor/objectBroker/FEM_ObjectBroker.h>
 
                                // main degree of freedom for rotation

// constructor for FEM_ObjectBroker
XC::MFreedom_Joint2D::MFreedom_Joint2D(void)
 : MFreedom_Constraint(0, CNSTRNT_TAG_MFreedom_Joint2D ),
   MainDOF(0), AuxDOF(0), FixedEnd(0),
   RetainedNode(nullptr), ConstrainedNode(nullptr),
   LargeDisplacement(0), Length0(0.0)
  {}


// general constructor for XC::ModelBuilder
XC::MFreedom_Joint2D::MFreedom_Joint2D(Domain *domain, int tag, int nodeRetain, int nodeConstr,int Maindof, int fixedend, int LrgDsp )
  : MFreedom_Constraint(tag,nodeRetain,nodeConstr,CNSTRNT_TAG_MFreedom_Joint2D ),
    MainDOF(Maindof), AuxDOF(0), FixedEnd(fixedend),
    RetainedNode(nullptr), ConstrainedNode(nullptr),
    LargeDisplacement( LrgDsp ), Length0(0.0)
  {
    setDomain(domain);
    if(getDomain() == nullptr)
      {
        std::cerr << "WARNING MFreedom_Joint2D(): Specified domain does not exist";
        std::cerr << "Domain = 0\n";
        return;
      }

    this->setTag(tag);

    // get node pointers of constrainted and retained nodes
    ConstrainedNode = getDomain()->getNode(getNodeConstrained());
    if(ConstrainedNode == nullptr)
      {
        std::cerr << "MFreedom_Joint2D::MFreedom_Joint2D: constrained node: ";
        std::cerr << getNodeConstrained() << "does not exist in model\n";
        exit(0);
      }

    RetainedNode = getDomain()->getNode(getNodeRetained());
    if(RetainedNode == nullptr)
      {
        std::cerr << "XC::MFreedom_Joint2D::MFreedom_Joint2D: retained node: ";
        std::cerr << getNodeRetained() << "does not exist in model\n";
        exit(0);
      }

    // check for proper degrees of freedom
    int RnumDOF = RetainedNode->getNumberDOF();
    int CnumDOF = ConstrainedNode->getNumberDOF();
    if(RnumDOF != 4 || CnumDOF != 3 )
      {
        std::cerr << "MFreedom_Joint2D::MFreedom_Joint2D - mismatch in numDOF\n DOF not supported by this type of constraint";
        return;
      }

    // check the XC::main degree of freedom. Assign auxilary DOF 
    if( MainDOF!= 2 && MainDOF!=3 )
      {
        std::cerr << "MFreedom_Joint2D::MFreedom_Joint2D - Wrong main degree of freedom" ;
        return;
      }
    if(MainDOF == 2 ) AuxDOF = 3;
    if(MainDOF == 3 ) AuxDOF = 2;
        
    // check the fixed end flag
    if( FixedEnd!= 0 && FixedEnd!=1 )
      {
        std::cerr << "XC::MFreedom_Joint2D::MFreedom_Joint2D - Wrong fixed end flag";
        return;
      }
        
    // check for proper dimensions of coordinate space
    const Vector &crdR = RetainedNode->getCrds();
    int dimR = crdR.Size();
    const Vector &crdC = ConstrainedNode->getCrds();
    int dimC = crdC.Size();
    
    if(dimR != 2 || dimC != 2 )
      {
        std::cerr << "MFreedom_Joint2D::MFreedom_Joint2D - mismatch in dimnesion\n dimension not supported by this type of constraint";
        return;
      }

    // calculate the initial length of the rigid link
    double deltaX = crdC(0) - crdR(0);
    double deltaY = crdC(1) - crdR(1);

    Length0 = sqrt( deltaX*deltaX + deltaY*deltaY );
    if( Length0 <= 1.0e-12 )
      {
        std::cerr << "XC::MFreedom_Joint2D::MFreedom_Joint2D - The constraint length is zero\n";
      }
   
    // allocate and set up the constranted and retained id's
    // allocate and set up the constraint matrix
    if( FixedEnd == 0 )
      {
        // the end is released
        set_constrained_dofs(ID(CnumDOF-1));
        set_retained_dofs(ID(RnumDOF-1));
               
        constrDOF(0) = 0;
        constrDOF(1) = 1;

        retainDOF(0) = 0;
        retainDOF(1) = 1;
        retainDOF(2) = MainDOF;
                
        set_constraint(Matrix( CnumDOF-1 , RnumDOF-1 ));
               
        constraintMatrix(0,0) = 1.0 ;
        constraintMatrix(0,2) = -deltaY ;
        constraintMatrix(1,1) = 1.0 ;
        constraintMatrix(1,2) = deltaX ;
      }
    else
      {
        // the end is fixed
        constrDOF = ID(CnumDOF);
        retainDOF = ID(RnumDOF);
                
        constrDOF(0) = 0;
        constrDOF(1) = 1;
        constrDOF(2) = 2;
                
        retainDOF(0) = 0;
        retainDOF(1) = 1;
        retainDOF(2) = 2;
        retainDOF(3) = 3;
                
        constraintMatrix= Matrix(CnumDOF,RnumDOF);
               
        constraintMatrix(0,0) = 1.0 ;
        constraintMatrix(0,MainDOF) = -deltaY ;
        constraintMatrix(1,1) = 1.0 ;
        constraintMatrix(1,MainDOF) = deltaX ;
        constraintMatrix(2,AuxDOF) = 1.0 ;
      }
 
    if(constraintMatrix.Nula())
       {
         std::cerr << "XC::MFreedom_Joint2D::MFreedom_Joint2D - ran out of memory \ncan not generate the constraint matrix";
         exit(-1);
       }
  }

XC::MFreedom_Joint2D::~MFreedom_Joint2D(void)
  {
    if(RetainedNode)
      RetainedNode->disconnect(this);
    if(ConstrainedNode)
      ConstrainedNode->disconnect(this);
  }


int XC::MFreedom_Joint2D::applyConstraint(double timeStamp)
  {
    if(LargeDisplacement != 0 )
      {
        // calculate the constraint at this moment

        // get the coordinates of the two nodes - check dimensions are the same FOR THE MOMENT
        const Vector &crdR = RetainedNode->getCrds();
        const Vector &crdC = ConstrainedNode->getCrds();

        // get commited displacements of nodes to get updated coordinates
        const Vector &dispR = RetainedNode->getDisp();
        const Vector &dispC = ConstrainedNode->getDisp();

        double deltaX = dispC(0) + crdC(0) - dispR(0) - crdR(0);
        double deltaY = dispC(1) + crdC(1) - dispR(1) - crdR(1);

        constraintMatrix.Zero();
                
        if(FixedEnd == 0 )
          {
            // the end is released
            constraintMatrix(0,0) = 1.0 ;
            constraintMatrix(0,2) = -deltaY ;
            constraintMatrix(1,1) = 1.0 ;
            constraintMatrix(1,2) = deltaX ;
          }
        else
          {
            // the end is fixed
            constraintMatrix(0,0) = 1.0 ;
            constraintMatrix(0,MainDOF) = -deltaY ;
            constraintMatrix(1,1) = 1.0 ;
            constraintMatrix(1,MainDOF) = deltaX ;
            constraintMatrix(2,AuxDOF) = 1.0 ;
          }
      }
    return 0;
   }


bool XC::MFreedom_Joint2D::isTimeVarying(void) const
  {
     if(LargeDisplacement != 0 )
       return true;
     else
       return false;
  }


int XC::MFreedom_Joint2D::sendSelf(CommParameters &cp)
  {
    static ID data(18);
    int result= sendData(cp);
    data(13) = MainDOF;
    data(14) = AuxDOF;
    data(15) = FixedEnd;
    data(16) = LargeDisplacement;
    data(17) = Length0;

    const int dataTag= getDbTag();
    result = cp.sendIdData(getDbTagData(),dataTag);
    if(result<0)
      std::cerr << "WARNING MFreedom_Joint2D::sendSelf - error sending XC::ID data\n";
    return result;  
  }


int XC::MFreedom_Joint2D::recvSelf(const CommParameters &cp)
  {
    static ID data(18);
    const int dataTag= getDbTag();
    int result = cp.receiveIdData(getDbTagData(),dataTag);
    if(result < 0)
      std::cerr << "WARNING XC::MFreedom_Joint2D::recvSelf - error receiving XC::ID data\n";
    else
      {
        result+= recvData(cp);
        MainDOF= data(13);
        AuxDOF= data(14);
        FixedEnd= data(15);
        LargeDisplacement= data(16);
        Length0= data(17);
      }
    return result;  
  }


const XC::Matrix &XC::MFreedom_Joint2D::getConstraint(void) const
  {
    if(constraintMatrix.Nula())
      {
        std::cerr << "MFreedom_Joint2D::getConstraint - no XC::Matrix was set\n";
        exit(-1);
      }    

    // Length correction
    // to correct the trial displacement
    if(LargeDisplacement == 2 )
      {
        // get the coordinates of the two nodes - check dimensions are the same FOR THE MOMENT
        const XC::Vector &crdR = RetainedNode->getCrds();
        const XC::Vector &crdC = ConstrainedNode->getCrds();

        // get commited displacements of nodes to get updated coordinates
        const XC::Vector &dispR = RetainedNode->getTrialDisp();
        const XC::Vector &dispC = ConstrainedNode->getTrialDisp();

        double deltaX = dispC(0) + crdC(0) - dispR(0) - crdR(0);
        double deltaY = dispC(1) + crdC(1) - dispR(1) - crdR(1);


        Vector Direction(2);
        Direction(0) = deltaX;
        Direction(1) = deltaY;
        double NewLength = Direction.Norm();
        if(NewLength < 1e-12)
          std::cerr << "XC::MFreedom_Joint2D::applyConstraint : length of rigid link is too small or zero"; 
        Direction = Direction * (Length0/NewLength);  // correct the length
                // find new displacements of the constrainted node
        
        Vector NewLocation(3);
        NewLocation(0) = Direction(0) + dispR(0) + crdR(0) - crdC(0);
        NewLocation(1) = Direction(1) + dispR(1) + crdR(1) - crdC(1);
        NewLocation(2) = dispC(2);
        ConstrainedNode->setTrialDisp(NewLocation);
      } // end of length correction procedure
    // return the constraint matrix Ccr
    return constraintMatrix;
  }
    
void XC::MFreedom_Joint2D::Print(std::ostream &s, int flag )
  {
    s << "MFreedom_Joint2D: " << this->getTag() << "\n";
    s << "\tConstrained XC::Node: " << getNodeConstrained();
    s << " Retained XC::Node: " << getNodeRetained() ;
    s << " Fixed end: " << FixedEnd << " Large Disp: " << LargeDisplacement;
    s << " constrained dof: " << constrDOF;    
    s << " retained dof: " << retainDOF;        
    s << " constraint matrix: " << constraintMatrix << "\n";
  }


void XC::MFreedom_Joint2D::setDomain(Domain *domain)
  {
    MFreedom_Constraint::setDomain(domain);
    RetainedNode= getDomain()->getNode(getNodeRetained());
    if(RetainedNode)
      RetainedNode->connect(this);
    ConstrainedNode= getDomain()->getNode(getNodeConstrained());
    if(ConstrainedNode)
      ConstrainedNode->connect(this);
  }


