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
//NDAdaptorMaterial.h

#ifndef NDAdaptorMaterial_h
#define NDAdaptorMaterial_h

#include <utility/matrix/Vector.h>
#include <material/nD/NDMaterial.h>

namespace XC {
//! @ingroup NDMat
//
//! @brief ??.
class NDAdaptorMaterial: public NDMaterial
  {
  protected:
    double Tstrain22;
    double Cstrain22;

    NDMaterial *theMaterial;
    Vector strain;
  protected:
    int sendData(CommParameters &);
    int recvData(const CommParameters &);
  public:
    NDAdaptorMaterial(int classTag,int tag, NDMaterial &theMat, int strain_size);
    NDAdaptorMaterial(int classTag,int tag, int strain_size);
    NDAdaptorMaterial(int classTag, int strain_size);
    virtual ~NDAdaptorMaterial(void);

    const Vector& getStrain(void);
    double getRho(void) const;

    int commitState(void);
    int revertToLastCommit(void);
    int revertToStart(void);

    void Print(std::ostream &s, int flag);

  };
} // end of XC namespace

#endif



