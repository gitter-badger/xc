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
//Element1D.cc

#include "Element1D.h"
#include "preprocessor/cad/matrices/TritrizPtrNod.h"
#include "preprocessor/cad/matrices/TritrizPtrElem.h"
#include "preprocessor/Preprocessor.h"
#include "preprocessor/loaders/LoadLoader.h"
#include "preprocessor/set_mgmt/SetEstruct.h"
#include "domain/mesh/node/Node.h"
#include "domain/load/beam_loads/Beam3dUniformLoad.h"
#include "domain/load/beam_loads/Beam3dPointLoad.h"
#include "domain/load/beam_loads/Beam2dUniformLoad.h"
#include "domain/load/beam_loads/Beam2dPointLoad.h"
#include "domain/load/beam_loads/BeamStrainLoad.h"

#include "utility/matrix/Matrix.h"
#include "xc_basic/src/matrices/m_int.h"
#include "domain/mesh/element/utils/coordTransformation/CrdTransf2d.h"
#include "domain/mesh/element/utils/coordTransformation/CrdTransf3d.h"
#include "xc_utils/src/geom/pos_vec/MatrizPos3d.h"
#include "xc_utils/src/geom/pos_vec/Vector3d.h"
#include "xc_utils/src/geom/pos_vec/Pos2d.h"
#include "xc_utils/src/geom/d1/Segmento3d.h"
#include "utility/actor/objectBroker/FEM_ObjectBroker.h"
#include "med.h"
#include "vtkCellType.h"

//! @brief Constructor.
XC::Element1D::Element1D(int tag, int classTag)
  : ElementBase<2>(tag,classTag), longsTributarias(2,0.0) {}

//! @brief Constructor.
XC::Element1D::Element1D(int tag, int classTag,int Nd1,int Nd2)
  : ElementBase<2>(tag,classTag), longsTributarias(2,0.0)
  { theNodes.set_id_nodos(Nd1,Nd2); }


void XC::Element1D::vector2dUniformLoadGlobal(const Vector &v)
  {
    const CrdTransf *crd_trf= getCoordTransf();
    const Vector vTrf= crd_trf->getVectorLocalCoordFromGlobal(v);
    vector2dUniformLoadLocal(vTrf);
  }

void XC::Element1D::vector2dUniformLoadLocal(const Vector &v)
  {
    Preprocessor *preprocessor= GetPreprocessor();
    MapLoadPatterns &casos= preprocessor->getLoadLoader().getLoadPatterns();
    static ID eTags(1);
    eTags[0]= getTag(); //Load for this element.
    const int &loadTag= casos.getCurrentElementLoadTag(); //Load identifier.

    const size_t sz= v.Size();
    if(sz>1)
      {
        if(sz>2)
	  std::cerr << __FUNCTION__ << ": WARNING a vector of dimension 2 was expected instead of: " << v << std::endl;
        Beam2dUniformLoad *tmp= new Beam2dUniformLoad(loadTag,v[1],v[0],eTags);
        LoadPattern *lp= casos.getCurrentLoadPatternPtr();
        if(lp)
          {
            lp->addElementalLoad(tmp);
            casos.setCurrentElementLoadTag(loadTag+1);
          }
        else
	  std::cerr << "There is no current load pattern. Load ignored."
                    << std::endl; 
      }
    else
      std::cerr << __FUNCTION__ << ": ERROR a vector of dimension 2 was expected instead of: " << v << std::endl;
  }

void XC::Element1D::vector2dPointByRelDistLoadGlobal(const double &x,const Vector &v)
  {
    const size_t sz= v.Size();
    if(sz>1)
      {
        const CrdTransf *crd_trf= getCoordTransf();
        const Vector vTrf= crd_trf->getVectorLocalCoordFromGlobal(v);
        vector2dPointByRelDistLoadLocal(x,vTrf);
      }
    else
      std::cerr << __FUNCTION__ << "; ERROR a vector of dimension 2 was expected instead of: " << v << std::endl;
  }

void XC::Element1D::vector2dPointByRelDistLoadLocal(const double &x,const Vector &v)
  {
    const size_t sz= v.Size();
    if(sz>1)
      {
        Preprocessor *preprocessor= GetPreprocessor();
        MapLoadPatterns &casos= preprocessor->getLoadLoader().getLoadPatterns();
        static ID eTags(1);
        eTags[0]= getTag(); //Load for this element.
        const int &loadTag= casos.getCurrentElementLoadTag(); //Load identifier.

	if(sz>2)
	  std::cerr << __FUNCTION__ << ": WARNING a vector of dimension 2 was expected instead of: " << v << std::endl;
        Beam2dPointLoad *tmp= new Beam2dPointLoad(loadTag,v[1],x,eTags,v[0]);
        LoadPattern *lp= casos.getCurrentLoadPatternPtr();
        if(lp)
          {
            lp->addElementalLoad(tmp);
            casos.setCurrentElementLoadTag(loadTag+1);
          }
        else
	  std::cerr << "There is no current load pattern. Load ignored."
                    << std::endl; 
      }
    else
      std::cerr << __FUNCTION__ << ": ERROR a vector of dimension 2 was expected instead of: " << v << std::endl;
  }

void XC::Element1D::vector2dPointLoadGlobal(const Vector &p,const Vector &v)
  {
    const CrdTransf *crd_trf= getCoordTransf();
    const double x= crd_trf->getPointBasicCoordFromGlobal(p);
    if(x<0.0 || x>1.0)
      std::cerr << "Error vector2dPointLoadGlobal; la distancia relativa x= "
                << x << " obtenida del punto: " << p
                << " debe estar comprendida entre 0 y 1." << std::endl;
    vector2dPointByRelDistLoadGlobal(x,v);
  }

void XC::Element1D::vector2dPointLoadLocal(const Vector &p,const Vector &v)
  {
    const CrdTransf *crd_trf= getCoordTransf();
    const double x= crd_trf->getPointBasicCoordFromGlobal(p);
    if(x<0.0 || x>1.0)
      std::cerr << "Error vector2dPointLoadGlobal; la distancia relativa x= "
                << x << " obtenida del punto: " << p
                << " debe estar comprendida entre 0 y 1." << std::endl;
    vector2dPointByRelDistLoadLocal(x,v);
  }

void XC::Element1D::vector3dUniformLoadGlobal(const Vector &v)
  {
    const size_t sz= v.Size();
    if(sz>2)
      {
        const CrdTransf *crd_trf= getCoordTransf();
        const Vector vTrf= crd_trf->getVectorLocalCoordFromGlobal(v);
        vector3dUniformLoadLocal(vTrf);
      }
    else
      std::cerr << __FUNCTION__ << ": ERROR a vector of dimension 3 was expected instead of: " << v << std::endl;
  }

void XC::Element1D::vector3dUniformLoadLocal(const Vector &v)
  {
    const size_t sz= v.Size();
    if(sz>2)
      {
        Preprocessor *preprocessor= GetPreprocessor();
        MapLoadPatterns &casos= preprocessor->getLoadLoader().getLoadPatterns();
        static ID eTags(1);
        eTags[0]= getTag(); //Load for this element.
        const int &loadTag= casos.getCurrentElementLoadTag(); //Load identifier.

        LoadPattern *lp= casos.getCurrentLoadPatternPtr();
        if(lp)
          {
            Beam3dUniformLoad *tmp= new Beam3dUniformLoad(loadTag,v,0.0,eTags);
            lp->addElementalLoad(tmp);
            casos.setCurrentElementLoadTag(loadTag+1);
          }
        else
	  std::cerr << "There is no current load pattern. Load ignored."
                    << std::endl; 
      }
    else
      std::cerr << __FUNCTION__ << ": ERROR a vector of dimension 3 was expected instead of: " << v << std::endl;
  }

void XC::Element1D::vector3dPointByRelDistLoadGlobal(const double &x,const Vector &v)
  {
    const size_t sz= v.Size();
    if(sz>2)
      {
        const CrdTransf *crd_trf= getCoordTransf();
        const Vector vTrf= crd_trf->getVectorLocalCoordFromGlobal(v);
        vector3dPointByRelDistLoadLocal(x,vTrf);
      }
    else
      std::cerr << __FUNCTION__ << ": ERROR a vector of dimension 3 was expected instead of: " << v << std::endl;
  }

void XC::Element1D::vector3dPointByRelDistLoadLocal(const double &x,const Vector &v)
  {
    const size_t sz= v.Size();
    if(sz>2)
      {
        Preprocessor *preprocessor= GetPreprocessor();
        MapLoadPatterns &casos= preprocessor->getLoadLoader().getLoadPatterns();
        static ID eTags(1);
        eTags[0]= getTag(); //Load for this element.
        const int &loadTag= casos.getCurrentElementLoadTag(); //Load identifier.

        Beam3dPointLoad *tmp= new Beam3dPointLoad(loadTag,v[1],v[2],x,eTags,v[0]);
        LoadPattern *lp= casos.getCurrentLoadPatternPtr();
        if(lp)
          {
            lp->addElementalLoad(tmp);
            casos.setCurrentElementLoadTag(loadTag+1);
          }
        else
	  std::cerr << "There is no current load pattern. Load ignored."
                    << std::endl; 

      }
    else
      std::cerr << __FUNCTION__ << ": ERROR a vector of dimension 3 was expected instead of: " << v << std::endl;
  }

void XC::Element1D::vector3dPointLoadGlobal(const Vector &p,const Vector &v)
  {
    const CrdTransf *crd_trf= getCoordTransf();
    const double x= crd_trf->getPointBasicCoordFromGlobal(p);
    if(x<0.0 || x>1.0)
      std::cerr << "Error vector3dPointLoadGlobal; la distancia relativa x= "
                << x << " obtenida del punto: " << p
                << " debe estar comprendida entre 0 y 1." << std::endl;
    vector3dPointByRelDistLoadGlobal(x,v);
  }

void XC::Element1D::vector3dPointLoadLocal(const Vector &p,const Vector &v)
  {
    const CrdTransf *crd_trf= getCoordTransf();
    const double x= crd_trf->getPointBasicCoordFromGlobal(p);
    if(x<0.0 || x>1.0)
      std::cerr << "Error vector3dPointLoadGlobal; la distancia relativa x= "
                << x << " obtenida del punto: " << p
                << " debe estar comprendida entre 0 y 1." << std::endl;
    vector3dPointByRelDistLoadLocal(x,v);
  }

void XC::Element1D::strainLoad(const DeformationPlane &p1,const DeformationPlane &p2)
  {
    Preprocessor *preprocessor= GetPreprocessor();
    MapLoadPatterns &casos= preprocessor->getLoadLoader().getLoadPatterns();
    static ID eTags(1);
    eTags[0]= getTag(); //Load for this element.
    const int &loadTag= casos.getCurrentElementLoadTag(); //Load identifier.

    BeamStrainLoad *tmp= new BeamStrainLoad(loadTag,eTags);
    tmp->setDeformationPlane1(p1);
    tmp->setDeformationPlane2(p2);
    LoadPattern *lp= casos.getCurrentLoadPatternPtr();
    if(lp)
      {
        lp->addElementalLoad(tmp);
        casos.setCurrentElementLoadTag(loadTag+1);
      }
    else
      std::cerr << "There is no current load pattern. Load ignored."
                << std::endl; 
  }

//! @brief Return the dimensión del elemento.
size_t XC::Element1D::getDimension(void) const
  { return 1; }

void meshing_on_i(const XC::Element1D &e,const XC::TritrizPtrNod::const_ref_fila_i &nodos,XC::TritrizPtrElem::var_ref_fila_i &elementos)
  {
    const size_t ncapas= nodos.GetCapas();
    for(size_t i=1;i<ncapas;i++)
      {
	XC::Element *tmp= e.getCopy();
        const int Nd1= nodos(i)->getTag();
        const int Nd2= nodos(i+1)->getTag();
        tmp->getNodePtrs().set_id_nodos(Nd1,Nd2);
        elementos(i)= tmp;
      }
  }

void meshing_on_j(const XC::Element1D &e,const XC::TritrizPtrNod::const_ref_fila_j &nodos,XC::TritrizPtrElem::var_ref_fila_j &elementos)
  {
    const size_t nfilas= nodos.getNumFilas();
    for(size_t j=1;j<nfilas;j++)
      {
	XC::Element *tmp= e.getCopy();
        const int Nd1= nodos(j)->getTag();
        const int Nd2= nodos(j+1)->getTag();
        tmp->getNodePtrs().set_id_nodos(Nd1,Nd2);
        elementos(j)= tmp;
      }
  }

void meshing_on_k(const XC::Element1D &e,const XC::TritrizPtrNod::const_ref_fila_k &nodos,XC::TritrizPtrElem::var_ref_fila_k &elementos)
  {
    const size_t ncols= nodos.getNumCols();
    for(size_t k=1;k<ncols;k++)
      {
	XC::Element *tmp= e.getCopy();
        const int Nd1= nodos(k)->getTag();
        const int Nd2= nodos(k+1)->getTag();
        tmp->getNodePtrs().set_id_nodos(Nd1,Nd2);
        elementos(k)= tmp;
      }
  }

void XC::Element1D::unidimensional_meshing(const XC::TritrizPtrNod &nodos,XC::TritrizPtrElem &elementos) const
  {
    const size_t ncapas= nodos.GetCapas();
    const size_t nfilas= nodos.getNumFilas();
    const size_t ncols= nodos.getNumCols();
    if(nodos.EsFilaI())
      {
        elementos= TritrizPtrElem(ncapas-1,MatrizPtrElem(1,1));
        TritrizPtrElem::var_ref_fila_i fila_elem= elementos.GetVarRefFilaI(1,1);
        meshing_on_i(*this,nodos.GetConstRefFilaI(1,1),fila_elem);
      }
    else if(nodos.EsFilaJ())
      {
        elementos= TritrizPtrElem(ncapas,MatrizPtrElem(nfilas-1,ncols));
        TritrizPtrElem::var_ref_fila_j fila_elem= elementos.GetVarRefFilaJ(1,1);
        meshing_on_j(*this,nodos.GetConstRefFilaJ(1,1),fila_elem);
      }
    else if(nodos.EsFilaK())
      {
        elementos= TritrizPtrElem(ncapas,MatrizPtrElem(nfilas,ncols-1));
        TritrizPtrElem::var_ref_fila_k fila_elem= elementos.GetVarRefFilaK(1,1);
        meshing_on_k(*this,nodos.GetConstRefFilaK(1,1),fila_elem);
      }
  }

XC::TritrizPtrElem XC::Element1D::put_on_mesh(const TritrizPtrNod &nodos,meshing_dir dm) const
  {
    const size_t ncapas= nodos.GetCapas();
    const size_t nfilas= nodos.getNumFilas();
    const size_t ncols= nodos.getNumCols();
    const size_t mesh_dim= nodos.GetDim();
    TritrizPtrElem retval;
    if(mesh_dim<1)
      std::cerr << "Existe un sólo nodo, no se pudieron crear elementos." << std::endl;
    else
      {
       if(mesh_dim<2) //Bidimensional mesh
          unidimensional_meshing(nodos,retval);
        else
          {
            switch(dm)
              {
              case dirm_i:
                if(ncapas<2)
		  std::cerr << "Element1D::put_on_mesh; número insuficiente de nodos en dirección i. No se crean elementos." << std::endl;
                else
                  {
                    retval= TritrizPtrElem(ncapas-1,MatrizPtrElem(nfilas,ncols));
                    for(size_t j=1;j<=nfilas;j++)
                      for(size_t k=1;k<=ncols;k++)
                        {
                          TritrizPtrElem::var_ref_fila_i fila_elem= retval.GetVarRefFilaI(j,k);
                          meshing_on_i(*this,nodos.GetConstRefFilaI(j,k),fila_elem);
                        }
                  }
                break;
              case dirm_j:
                if(nfilas<2)
		  std::cerr << "Element1D::put_on_mesh; número insuficiente de nodos en dirección j. No se crean elementos." << std::endl;
                else
                  {
                    retval= TritrizPtrElem(ncapas,MatrizPtrElem(nfilas-1,ncols));
                    for(size_t i=1;i<=ncapas;i++)
                      for(size_t k=1;k<=ncols;k++)
                        {
                          XC::TritrizPtrElem::var_ref_fila_j fila_elem= retval.GetVarRefFilaJ(i,k);
                          meshing_on_j(*this,nodos.GetConstRefFilaJ(i,k),fila_elem);
                        }
                  }
                break;
              case dirm_k:
                if(ncols<2)
		  std::cerr << "Element1D::put_on_mesh; número insuficiente de nodos en dirección k. No se crean elementos." << std::endl;
                else
                  {
                    retval= TritrizPtrElem(ncapas,MatrizPtrElem(nfilas,ncols-1));
                    for(size_t i=1;i<=ncapas;i++)
	              for(size_t j=1;j<=nfilas;j++)
                        {
                          XC::TritrizPtrElem::var_ref_fila_k fila_elem= retval.GetVarRefFilaK(i,j);
                          meshing_on_k(*this,nodos.GetConstRefFilaK(i,j),fila_elem);
                        }
                  }
                break;
              default:
                break;
              }
          }  
      }
    return retval;
  }

XC::TritrizPtrElem XC::Element1D::cose(const SetEstruct &f1,const SetEstruct &f2) const
  {
    const size_t nelem= f1.NumNodos();
    TritrizPtrElem retval(nelem,1,1);
    const size_t ncapas= std::min(f1.GetNumCapasNodos(),f2.GetNumCapasNodos());
    const size_t nfilas= std::min(f1.GetNumFilasNodos(),f2.GetNumFilasNodos());
    const size_t ncols= std::min(f1.GetNumColsNodos(),f2.GetNumColsNodos());
    for(size_t i=1;i<=ncapas;i++)
      for(size_t j=1;j<=nfilas;j++)
        for(size_t k=1;k<=ncols;k++)
          {
            Element *tmp= getCopy();
            const int Nd1= f1.GetNodo(i,j,k)->getTag();
            const int Nd2= f2.GetNodo(i,j,k)->getTag();
            tmp->getNodePtrs().set_id_nodos(Nd1,Nd2);
            retval(i,1,1)= tmp;
          }
    return retval;
  }

void XC::Element1D::setDomain(Domain *theDomain)
  {
    ElementBase<2>::setDomain(theDomain);
  }

//! @brief Returns (if possible) a pointer to the coordinate transformation.
XC::CrdTransf *XC::Element1D::getCoordTransf(void)
  { return nullptr; }

//! @brief Returns (if possible) a const pointer to the coordinate transformation.
const XC::CrdTransf *XC::Element1D::getCoordTransf(void) const
  { return nullptr; }

//! @brief Returns (and checks that it exists) a const pointer to the coordinate transformation.
XC::CrdTransf *XC::Element1D::checkCoordTransf(void)
  {
    CrdTransf *ct= getCoordTransf();
    if(!ct)
      std::cerr << nombre_clase() << __FUNCTION__
                << "; coordinate transformation not defined."
                << std::endl;
    return ct;
  }

//! @brief Returns (and checks that it exists) a const pointer to the coordinate transformation.
const XC::CrdTransf *XC::Element1D::checkCoordTransf(void) const
  {
    const CrdTransf *ct= getCoordTransf();
    if(!ct)
      std::cerr << nombre_clase() << __FUNCTION__
                << "; coordinate transformation not defined."
                << std::endl;
    return ct;
  }


//! @brief Returs a matrix with the axes of the element as matrix rows
//! [[x1,y1,z1],[x2,y2,z2],...·]
XC::Matrix XC::Element1D::getLocalAxes(bool initialGeometry) const
  {
    return getCoordTransf()->getLocalAxes(initialGeometry);
  }

//! @brief Returns puntos distribuidos entre los nodos extremos.
const XC::Matrix &XC::Element1D::getCooPuntos(const size_t &ndiv) const
  {
    static Matrix retval;
    const CrdTransf *tmp= getCoordTransf();
    if(tmp)
      retval= tmp->getCooPuntos(ndiv);
    else
      {
        const Pos3d p0= theNodes[0]->getPosInicial3d();
        const Pos3d p1= theNodes[1]->getPosInicial3d();
        MatrizPos3d linea(p0,p1,ndiv);
        retval= Matrix(ndiv+1,3);
        Pos3d tmp;
        for(size_t i= 0;i<ndiv+1;i++)
          {
            tmp= linea(i+1,1);
            retval(i,0)= tmp.x();
            retval(i,1)= tmp.y();
            retval(i,2)= tmp.z();
          }
      }
    return retval;
  }

//! @brief Returns the punto correspondiente a la coordenada 0<=xrel<=1.
const XC::Vector &XC::Element1D::getCooPunto(const double &xrel) const
  {
    static Vector retval;
    const CrdTransf *tmp= getCoordTransf();
    if(tmp)
      retval= tmp->getCooPunto(xrel);
    else
      {
        const Pos3d p0= theNodes[0]->getPosInicial3d();
        const Pos3d p1= theNodes[1]->getPosInicial3d();
        const Vector3d v= p1-p0;
        retval= Vector(3);
        const Pos3d tmp= p0+xrel*v;
        retval(0)= tmp.x();
        retval(1)= tmp.y();
        retval(2)= tmp.z();
      }
    return retval;
  }

//! @brief Returns the segmento definido por el elemento.
Segmento3d XC::Element1D::getSegmento(bool initialGeometry) const
  {
    if(initialGeometry)
      return Segmento3d(theNodes[0]->getPosInicial3d(),theNodes[1]->getPosInicial3d());
    else
      return Segmento3d(theNodes[0]->getPosFinal3d(),theNodes[1]->getPosFinal3d());
  }

//! @brief Returns the cuadrado de la distancia desde el elemento al punto que
//! is being passed as parameter.
double XC::Element1D::getDist2(const Pos2d &p,bool initialGeometry) const
  { return getDist2(To3dXY2d(p),initialGeometry); }

//! @brief Return the distancia desde el elemento al punto que
//! is being passed as parameter.
double XC::Element1D::getDist(const Pos2d &p,bool initialGeometry) const
  { return getDist(To3dXY2d(p),initialGeometry); }

//! @brief Returns the cuadrado de la distancia desde el elemento al punto que
//! is being passed as parameter.
double XC::Element1D::getDist2(const Pos3d &p,bool initialGeometry) const
  {
    const Segmento3d sg(getSegmento(initialGeometry));
    return sg.dist2(p);
  }

//! @brief Return the distancia desde el elemento al punto que
//! is being passed as parameter.
double XC::Element1D::getDist(const Pos3d &p,bool initialGeometry) const
  {
    const Segmento3d sg(getSegmento(initialGeometry));
    return sg.dist(p);
  }

//! @brief Envía la coordinate transformation through the channel being passed as parameter.
int XC::Element1D::sendCoordTransf(int posFlag,const int &posClassTag,const int &posDbTag,CommParameters &cp)
  {
    int retval= 0;
    CrdTransf *ptr= getCoordTransf();
    DbTagData &dt= getDbTagData();    
    if(!ptr)
      setDbTagDataPos(posFlag,1);
    else
      {
        setDbTagDataPos(posFlag,0);
        setDbTagDataPos(posClassTag,ptr->getClassTag());
        cp.sendMovable(*ptr,dt,CommMetaData(posDbTag));
      }
    return retval;
  }

//! @brief Recibe la coordinate transformation through the channel being passed as parameter.
XC::CrdTransf *XC::Element1D::recvCoordTransf(int posFlag,const int &posClassTag,const int &posDbTag,const CommParameters &cp)
  {
    CrdTransf *ptr= getCoordTransf();
    DbTagData &dt= getDbTagData();
    if(getDbTagDataPos(posFlag) == 0)
      {
        // make some room and read in the vector
        if(!ptr)
          {
            ptr= cp.getNewCrdTransf(getDbTagDataPos(posClassTag));
            if(!ptr)
              std::cerr << "receiveCoordTransf -- ran out of memory\n";
          }
        if(ptr)
          {
            int res= cp.receiveMovable(*ptr,dt,CommMetaData(posDbTag));
            ptr->revertToLastCommit();// Revert the crdtrasf to its last committed state
            if(res<0)
              std::cerr << "receiveCoordTransf - failed to receive vector data\n";
          }
      }
    return ptr;
  }

//! @brief Recibe una coordinate transformation 2d through the channel being passed as parameter.
XC::CrdTransf2d *XC::Element1D::recvCoordTransf2d(int posFlag,const int &posClassTag,const int &posDbTag,const CommParameters &cp)
  {
    CrdTransf2d *retval= nullptr;
    CrdTransf *tmp= recvCoordTransf(posFlag,posClassTag,posDbTag,cp);
    if(tmp)
      {
        retval= dynamic_cast<CrdTransf2d *>(tmp);
        if(!retval)
          {
	    std::cerr << "El tipo de la transformación no es adecuado"
                      << std::endl;
            delete tmp;
          }
      }
    return retval;
  }

//! @brief Recibe una coordinate transformation 3d through the channel being passed as parameter.
XC::CrdTransf3d *XC::Element1D::recvCoordTransf3d(int posFlag,const int &posClassTag,const int &posDbTag,const CommParameters &cp)
  {
    CrdTransf3d *retval= nullptr;
    CrdTransf *tmp= recvCoordTransf(posFlag,posClassTag,posDbTag,cp);
    if(tmp)
      {
        retval= dynamic_cast<CrdTransf3d *>(tmp);
        if(!retval)
          {
	    std::cerr << "El tipo de la transformación no es adecuado"
                      << std::endl;
            delete tmp;
          }
      }
    return retval;
  }


//! @brief Interfaz con VTK.
int XC::Element1D::getVtkCellType(void) const
  { return VTK_LINE; }

//! @brief Interfaz con el formato MED de Salome.
int XC::Element1D::getMEDCellType(void) const
  { return MED_SEG2; }


//! @brief Calcula las longitudes tributarias correspondientes a cada
//! nodo del elemento
void XC::Element1D::calculaLongsTributarias(bool initialGeometry) const
  {
    const double lt= getSegmento(initialGeometry).Longitud()/2.0;
    longsTributarias[0]= lt;
    longsTributarias[1]= lt;
    vuelcaTributarias(longsTributarias);
  }

//! @brief Return the longitud tributaria correspondiente to the node being passed
//! as parameter.
double XC::Element1D::getLongTributaria(const Node *nod) const
  {
    double retval= 0;
    const int i= theNodes.find(nod);
    if(i>=0) //El nodo es de este elemento.
      retval= longsTributarias[i];
    return retval;
  }
