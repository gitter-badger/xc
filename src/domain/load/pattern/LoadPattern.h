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
                                                                        
// $Revision: 1.12 $
// $Date: 2005/11/22 19:44:22 $
// $Source: /usr/local/cvs/OpenSees/SRC/domain/load/pattern/LoadPattern.h,v $
                                                                        
                                                                        
#ifndef LoadPattern_h
#define LoadPattern_h

// Written: fmk 
// Created: 07/99
// Revision: A
//
// Purpose: This file contains the class definition for LoadPattern.
// LoadPattern is a concrete class
//
// What: "@(#) LoadPattern.h, revA"

#include "NodeLocker.h"


namespace XC {
class NodalLoad;
class TimeSeries;
class ElementalLoad;
class NodalLoadIter;
class ElementalLoadIter;
class GroundMotion;
class Vector;

//! @ingroup BoundCond
//!
//!
//! @defgroup LPatterns Load patterns.
//
//! @ingroup LPatterns
//
//! @brief A LoadPattern object is used to 
//! to store reference loads and single point constraints
//! and a TimeSeries function which is used to determine
//! the load factor given the pseudo-time to the model. 
class LoadPattern: public NodeLocker
  {
  private:
    std::string description; //!< Load description (self weight, wind,...)
    double loadFactor; //!< Load factor obtained from TimeSeries (see applyLoad).
    double gamma_f; //!< Load factor imposed from current load combination.

    TimeSeries *theSeries; //!< load variation in time.

    // storage objects for the loads.
    TaggedObjectStorage  *theNodalLoads; //!< Nodal load container.
    TaggedObjectStorage  *theElementalLoads; //!< Elemental load container.

    // iterator objects for the objects added to the storage objects
    NodalLoadIter       *theNodIter; //!< Iterator over nodal loads.
    ElementalLoadIter   *theEleIter; //!< Iterator over elemental loads.

    // AddingSensitivity:BEGIN //////////////////////////////////////
    Vector *randomLoads;
    bool RVisRandomProcessDiscretizer;
    // AddingSensitivity:END ////////////////////////////////////////

    void libera_contenedores(void);
    void libera_iteradores(void);
    void alloc_contenedores(void);
    void alloc_iteradores(void);
    void libera(void);
  protected:
    int isConstant;     // to indicate whether setConstant has been called
    DbTagData &getDbTagData(void) const;
    int sendData(CommParameters &cp);
    int recvData(const CommParameters &cp);
  public:
    LoadPattern(int tag);
    LoadPattern(void);                  // for FEM_ObjectBroker
    LoadPattern(int tag, int classTag); // for subclasses
    virtual ~LoadPattern(void);

    // method to set the associated TimeSeries and Domain
    virtual void setTimeSeries(TimeSeries *theSeries);
    virtual void setDomain(Domain *theDomain);
    bool addToDomain(void);
    void removeFromDomain(void);

    // methods to add loads
    virtual bool addNodalLoad(NodalLoad *);
    NodalLoad *newNodalLoad(const int &,const Vector &);
    virtual bool addElementalLoad(ElementalLoad *);
    bool newElementalLoad(ElementalLoad *);
    ElementalLoad *newElementalLoad(const std::string &);
    virtual bool addSFreedom_Constraint(SFreedom_Constraint *theSp);

    virtual NodalLoadIter &getNodalLoads(void);
    virtual ElementalLoadIter &getElementalLoads(void);
    int getNumNodalLoads(void) const;
    int getNumElementalLoads(void) const;
    int getNumLoads(void) const;

    // methods to remove things (loads, time_series,...)
    virtual void clearAll(void);
    virtual void clearLoads(void);
    virtual bool removeNodalLoad(int tag);
    virtual bool removeElementalLoad(int tag);

    // methods to apply loads
    virtual void applyLoad(double pseudoTime = 0.0);
    virtual void setLoadConstant(void);


    inline const std::string &getDescription(void) const
      { return description; }
    inline void setDescription(const std::string &d)
      { description= d; }
    virtual const double &getLoadFactor(void) const;
    const double &GammaF(void) const;
    double &GammaF(void);
    void setGammaF(const double &);
       

    // methods for o/p
    virtual int sendSelf(CommParameters &);
    virtual int recvSelf(const CommParameters &);

    virtual void Print(std::ostream &s, int flag =0);

    virtual LoadPattern *getCopy(void);

    virtual int addMotion(GroundMotion &theMotion, int tag);
    virtual GroundMotion *getMotion(int tag);

    // AddingSensitivity:BEGIN //////////////////////////////////////////
    virtual void applyLoadSensitivity(double pseudoTime = 0.0);
    virtual int  setParameter(const std::vector<std::string> &argv, Parameter &param);
    virtual int  updateParameter(int parameterID, Information &info);
    virtual int  activateParameter(int parameterID);
    virtual const Vector &getExternalForceSensitivity(int gradNumber);
    // AddingSensitivity:END ///////////////////////////////////////////
  };

} // end of XC namespace

#endif







