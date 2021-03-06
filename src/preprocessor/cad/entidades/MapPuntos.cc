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
//MapPuntos.cc

#include "MapPuntos.h"
#include "preprocessor/Preprocessor.h"
#include "xc_utils/src/geom/pos_vec/Vector3d.h"
#include "xc_utils/src/geom/d2/Plano3d.h"
#include "xc_utils/src/geom/d1/Recta3d.h"
#include "domain/mesh/node/Node.h"
#include "domain/mesh/element/Element.h"

#include "preprocessor/cad/entidades/Pnt.h"
#include "preprocessor/set_mgmt/Set.h"



//! @brief Constructor.
XC::MapPuntos::MapPuntos(Cad *cad)
  : MapEnt<Pnt>(cad) {}


//! @brief Inserta el nuevo punto en the set total y the opened sets.
void XC::MapPuntos::UpdateSets(Pnt *nuevo_punto) const
  {
    Cad *cad= const_cast<Cad *>(dynamic_cast<const Cad *>(Owner()));
    Preprocessor *preprocessor= cad->getPreprocessor();
    preprocessor->get_sets().get_set_total()->GetPuntos().push_back(nuevo_punto);
    preprocessor->get_sets().inserta_ent_mdlr(nuevo_punto);
    MapSet::map_sets &abiertos= preprocessor->get_sets().get_sets_abiertos();
    for(MapSet::map_sets::iterator i= abiertos.begin();i!= abiertos.end();i++)
      {
        Set *ptr_set= dynamic_cast<Set *>((*i).second);
        assert(ptr_set);
        ptr_set->GetPuntos().push_back(nuevo_punto);
      }
  }

//! @brief Returns the vector defined by the points which indices are being passed as parameters.
Vector3d XC::MapPuntos::getVector(const Indice &i,const Indice &j) const
  {
    Vector3d retval;
    const Pnt *pA= busca(i);
    const Pnt *pB= busca(j);
    if(!pA)
      std::cerr << nombre_clase() << __FUNCTION__ << "; point: " << i
		<< " not found." << std::endl;
    else if(!pB)
      std::cerr << nombre_clase() << __FUNCTION__ << "; point: " << j 
		<< " not found." << std::endl;
    else
      retval= Vector3d(pA->GetPos(),pB->GetPos());
    return retval;
  }

//! @brief Return the line defined by the points which indices are being passed as parameters.
Recta3d XC::MapPuntos::getRecta(const Indice &i,const Indice &j) const
  {
    Recta3d retval;
    const Pnt *pA= busca(i);
    const Pnt *pB= busca(j);
    if(!pA)
      std::cerr << nombre_clase() << __FUNCTION__ << "; point: " << i
		<< " not found." << std::endl;
    else if(!pB)
      std::cerr << nombre_clase() << __FUNCTION__ << "; point: " << j 
		<< " not found." << std::endl;
    else
      retval= Recta3d(pA->GetPos(),pB->GetPos());
    return retval;
  }

//! @brief Returns the plane defined by the points which indices are being passed as parameters.
Plano3d XC::MapPuntos::getPlano(const Indice &i,const Indice &j,const Indice &k) const
  {
    Plano3d retval;
    const Pnt *pA= busca(i);
    const Pnt *pB= busca(j);
    const Pnt *pC= busca(k);
    if(!pA)
      std::cerr << nombre_clase() << __FUNCTION__ << "; point: " << i
		<< " not found." << std::endl;
    else if(!pB)
      std::cerr << nombre_clase() << __FUNCTION__ << "; point: " << j 
		<< " not found." << std::endl;
    else if(!pC)
      std::cerr << nombre_clase() << __FUNCTION__ << "; point: " << k 
		<< " not found." << std::endl;
    else
      retval= Plano3d(pA->GetPos(),pB->GetPos(),pC->GetPos());
    return retval;
  }


//! @brief Creates a nuevo punto.
XC::Pnt *XC::MapPuntos::Crea(void)
  {
    Preprocessor *preprocessor= getPreprocessor();
    assert(preprocessor);
    Pnt *retval= new Pnt("p"+boost::lexical_cast<std::string>(getTag()),preprocessor);
    (*this)[getTag()]= retval;
    UpdateSets(retval);
    tag++;
    return retval;
  }

//! @brief Creates a nuevo punto.
XC::Pnt *XC::MapPuntos::Nuevo(void)
  {
    Pnt *retval= busca(getTag());
    if(!retval) //El punto es nuevo.
      retval= Crea();
    return retval;
  }


//! @brief Creates a new point at the position being passed as parameter.
XC::Pnt *XC::MapPuntos::Nuevo(const Pos3d &pos)
  {
    Pnt *retval= busca(getTag());
    if(retval)
      std::cerr << "MapPuntos::Nuevo; point with tag: " 
                << getTag() << " already exists, doing nothing." << std::endl;
    else //El punto es nuevo.
      {
        retval= Crea();
        retval->Pos()= pos;
      }
    return retval;
  }

//! @brief Lee un nuevo punto desde archivo.
XC::Pnt *XC::MapPuntos::Nuevo(const size_t &tag,const Pos3d &pos)
  {
    bool nuevo= true;
    size_t old_tag= getTag();
    Pnt *retval= nullptr;
    setTag(tag); //Identificador del punto.
    retval= busca(getTag());
    if(retval)
      nuevo= false;
    else
      retval= Crea();
    if(!nuevo)
      setTag(old_tag);
    retval->setPos(pos); //Asigna la posición
    return retval;
  }

//! @brief Creates a nuevo punto, copia del being passed as parameter con
//! el nombre que le toca según el valor del tag. Las coordenadas del
//! nuevo punto serán las que resulten de sumar a las del primitivo el
//! vector being passed as parameter.
XC::Pnt *XC::MapPuntos::Copia(const Pnt *p,const Vector3d &v= Vector3d())
  {
    Pnt *retval= busca(getTag());
    if(!p)
      {
        std::cerr << "MapPuntos::CopiaPunto; the pointer al punto original es nulo." << std::endl;
        return retval;
      }
    if(retval)
      std::cerr << "MapPuntos::CopiaPunto; el punto con identificador: " 
                << getTag() << " ya existe, no se hacen cambios." << std::endl;
    else //El punto es nuevo.
      {
        retval= new Pnt(*p);
        if(retval)
          {
            if(!v.Nulo())
              retval->Pos()+= v;
            retval->Nombre()= "p"+boost::lexical_cast<std::string>(getTag());
            (*this)[getTag()]= retval;
            UpdateSets(retval);
            tag++;
	  }
        else
	  std::cerr << "MapPuntos::CopiaPunto; memoria agotada." << std::endl; 
      }
    return retval;
  }

//! @brief Crea copias de los puntos cuyos identificadores being passed as parameters.
void XC::MapPuntos::Copia(const std::vector<Indice> &indices)
  {
    for(std::vector<Indice>::const_iterator i= indices.begin();i!=indices.end();i++)
      {
        Pnt *original= busca(*i);
        if(original)
          Copia(original);
        else
	  std::cerr << nombre_clase() << __FUNCTION__
	            << "; point: " << *i << " not found.\n";
      }
  }

//! @brief Aplica la transformación a los puntos cuyos identificadores being passed as parameters.
void XC::MapPuntos::Transforma(const TrfGeom &trf,const std::vector<Indice> &indices)
  {
    for(std::vector<Indice>::const_iterator i= indices.begin();i!=indices.end();i++)
      {
        Pnt *p= busca(*i);
        if(p)
          p->Transforma(trf);
        else
	  std::cerr << nombre_clase() << __FUNCTION__
	            << "; point: " << *i << " not found.\n";
      }
  }

//! @brief Return the distancia entre los puntos cuyos identificadores being passed as parameters.
double XC::MapPuntos::Dist(const Indice &i,const Indice &j) const
  {
    double retval(-1.0);
    const Pnt *pA= busca(i);
    const Pnt *pB= busca(j);
    if(!pA)
      std::cerr << "MapPuntos::DistPuntos; no se encontró el punto: " 
                << i << std::endl;
    else if(!pB)
      std::cerr << "MapPuntos::DistPuntos; no se encontró el punto: " 
                << j << std::endl;
    else
      retval= pA->DistanciaA(pB->GetPos());
    return retval;
  }
