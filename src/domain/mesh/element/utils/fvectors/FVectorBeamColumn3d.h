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
//FVectorBeamColumn3d.h

#ifndef FVectorBeamColumn3d_h
#define FVectorBeamColumn3d_h

#include "FVectorData.h"

namespace XC {
class Vector;

//! \ingroup ElemFV
//
//! @brief Esfuerzos en un elemento de tipo barra 3D.
class FVectorBeamColumn3d: public FVectorData<5>
  {
  public:
    FVectorBeamColumn3d(void);
    FVectorBeamColumn3d(const FVectorBeamColumn3d &otro);
    explicit FVectorBeamColumn3d(const Vector &);
    FVectorBeamColumn3d &operator=(const FVectorBeamColumn3d &otro);
    void zero(void);

    FVectorBeamColumn3d &operator*=(const double &d);
    FVectorBeamColumn3d &operator+=(const FVectorBeamColumn3d &otro);
    FVectorBeamColumn3d &operator-=(const FVectorBeamColumn3d &otro);

    void Print(std::ostream &os) const;
  };

} // end of XC namespace

#endif


