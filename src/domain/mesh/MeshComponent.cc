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
//MeshComponent.cc

#include "MeshComponent.h"
#include "utility/matrix/Matrix.h"


#include "utility/actor/actor/MovableID.h"

void XC::MeshComponent::check_matrices(const std::deque<Matrix> &matrices,const int &ndof) const
  {
    const size_t numMatrices= matrices.size();
    for(size_t i=0; i<numMatrices; i++)
      if(matrices[i].noRows() == ndof)
        {
          index = i;
          i = numMatrices;
        }
  }

void XC::MeshComponent::nueva_matriz(std::deque<Matrix> &matrices,const int &ndof) const
  {
    const size_t numMatrices= matrices.size();
    matrices.push_back(Matrix(ndof,ndof));
    index = numMatrices;
  }

void XC::MeshComponent::setup_matrices(std::deque<Matrix> &matrices,const int &ndof) const
  {
    check_matrices(matrices,ndof);
    if(index == -1)
      nueva_matriz(matrices,ndof);
  }

XC::MeshComponent::MeshComponent(int classTag)
  : ContinuaReprComponent(0,classTag), index(-1){}

XC::MeshComponent::MeshComponent(int tag, int classTag)
  : ContinuaReprComponent(tag,classTag), index(-1){}

//! @brief Send labelsthrough the channel being passed as parameter.
int XC::MeshComponent::sendIdsEtiquetas(int posDbTag,CommParameters &cp)
  {
    int res= 0;
    static ID etiqIds;
    const std::set<int> ids= labels.getIdsEtiquetas();
    const size_t sz= ids.size();
    if(sz>0)
      {
        etiqIds.resize(sz);
        int conta= 0;
        for(std::set<int>::const_iterator i= ids.begin();i!=ids.end();i++,conta++)
          etiqIds[conta]= *i;
        res+= cp.sendID(etiqIds,getDbTagData(),CommMetaData(posDbTag));
      }
    else
      setDbTagDataPos(posDbTag,0);
    return res;
  }

//! @brief Receive labels through the channel being passed as parameter.
int XC::MeshComponent::recvIdsEtiquetas(int posDbTag,const CommParameters &cp)
  {
    int res= 0;
    static ID etiqIds;
    if(getDbTagDataPos(posDbTag)!= 0)
      {
        const DiccionarioEtiquetas &dic= labels.getDiccionario();
        res= cp.receiveID(etiqIds,getDbTagData(),CommMetaData(posDbTag));
    
        const size_t sz= etiqIds.Size();
        for(size_t i=0;i<sz;i++)
          labels.addEtiqueta(dic(etiqIds[i]));
      }
    return res;
  }

//! @brief Send members through the channel being passed as parameter.
int XC::MeshComponent::sendData(CommParameters &cp)
  {
    int res= ContinuaReprComponent::sendData(cp);
    cp.sendInt(index,getDbTagData(),CommMetaData(2));
    res+= sendIdsEtiquetas(3,cp);
    return res;
  }

//! @brief Receives members through the channel being passed as parameter.
int XC::MeshComponent::recvData(const CommParameters &cp)
  {
    int res= ContinuaReprComponent::recvData(cp);
    cp.receiveInt(index,getDbTagData(),CommMetaData(2));
    res+= recvIdsEtiquetas(3,cp);
    return res;
  }

