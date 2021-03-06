//----------------------------------------------------------------------------
//  XC program; finite element analysis code
//  for structural analysis and design.
//
//  Copyright (C)  Luis Claudio Pérez Tato
//
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
//python_interface.tcc

XC::UniaxialMaterial *(XC::Fiber::*getMaterialPtr)(void)= &XC::Fiber::getMaterial;
class_<XC::Fiber,XC::Fiber*, bases<XC::TaggedObject>, boost::noncopyable >("Fiber", no_init)
  .def("getMaterial",make_function(getMaterialPtr,return_internal_reference<>()))
  .def("getArea",&XC::Fiber::getArea)
  .def("setTrialFiberStrain",&XC::Fiber::setTrialFiberStrain)
	
  .def("commitState",&XC::Fiber::commitState)
  .def("revertToLastCommit",&XC::Fiber::revertToLastCommit)
  .def("revertToStart",&XC::Fiber::revertToStart)
    
  .def("getOrder",&XC::Fiber::getOrder)

  .def("isDead",&XC::Fiber::isDead)
  .def("isAlive",&XC::Fiber::isAlive)
  .def("kill",&XC::Fiber::kill)

  .def("alive",&XC::Fiber::alive)

  .def("getFiberLocation",&XC::Fiber::getFiberLocation)
  .def("getLocY",&XC::Fiber::getLocY)
  .def("getLocZ",&XC::Fiber::getLocZ)
  .def("getPos",&XC::Fiber::getPos)

  .def("getArea",&XC::Fiber::getArea,"Returns fiber area.")
  .def("getDeformacion",&XC::Fiber::getStrain,"DEPRECATED (change to getStrain); returns fiber strain.") //Change to getDeformation 
  .def("getFuerza",&XC::Fiber::getFuerza,"DEPRECATED (change to getForce); returns fiber internal force.") //Change to getForce
  .def("getStrain",&XC::Fiber::getStrain,"Returns fiber strain.")
  .def("getForce",&XC::Fiber::getFuerza,"Returns fiber internal force.")
  .def("getMz",&XC::Fiber::getMz)
  .def("getMy",&XC::Fiber::getMy)
  ;

class_<XC::UniaxialFiber, bases<XC::Fiber>, boost::noncopyable >("UniaxialFiber", no_init)
  ;

class_<XC::UniaxialFiber2d, bases<XC::UniaxialFiber>, boost::noncopyable >("UniaxialFiber2d", no_init);

class_<XC::UniaxialFiber3d, bases<XC::UniaxialFiber>, boost::noncopyable >("UniaxialFiber3d", no_init);

typedef XC::DqFibras::dq_ptr_fibras dq_ptr_fibras;
class_<dq_ptr_fibras, boost::noncopyable >("dq_ptr_fibras", no_init)
  .def(vector_indexing_suite<dq_ptr_fibras>())
  ;

XC::Matrix &(XC::DqFibras::*getHomogenizedSectionITensor)(const double &) const= &XC::DqFibras::getIHomogenizedSection;
XC::Matrix &(XC::DqFibras::*getHomogenizedSectionITensorRelToPoint)(const double &,const Pos2d &) const= &XC::DqFibras::getIHomogenizedSection;
double (XC::DqFibras::*getHomogenizedSectionIRelTo)(const double &,const Pos2d &,const XC::Vector &) const= &XC::DqFibras::getIHomogenizedSection;
double (XC::DqFibras::*getHomogenizedSectionIRelToLine)(const double &, const Recta2d &) const= &XC::DqFibras::getIHomogenizedSection;
class_<XC::DqFibras, bases<EntCmd,dq_ptr_fibras>, boost::noncopyable >("DqFibras", no_init)
  .def("__iter__", boost::python::iterator<XC::DqFibras >())
  .def("insert",&XC::DqFibras::push_back,"inserts fiber pointer.")
  .def("empty",&XC::DqFibras::empty)
  .def("getNumFibers",&XC::DqFibras::getNumFibers)
  .def("getCdgY",&XC::DqFibras::getYCdg,return_value_policy<copy_const_reference>())
  .def("getCdgZ",&XC::DqFibras::getZCdg,return_value_policy<copy_const_reference>())
  .def("getCdg",&XC::DqFibras::getCdg)
  .def("getYRelativa",&XC::DqFibras::getYRelativa)
  .def("getZRelativa",&XC::DqFibras::getZRelativa)

//.def("getPosiciones",&XC::DqFibras::getPosiciones)

  .def("hayMomento",&XC::DqFibras::hayMomento)
  .def("getResultant",&XC::DqFibras::Resultante)
  .def("getMz",&XC::DqFibras::getMz)
  .def("getMy",&XC::DqFibras::getMy)
  .def("getExcentricidadMz",&XC::DqFibras::getExcentricidadMz)
  .def("getExcentricidadMy",&XC::DqFibras::getExcentricidadMy)
  .def("getVectorMomento",&XC::DqFibras::getVectorMomento)
  .def("getPosResultante",&XC::DqFibras::getPosResultante)
  .def("getFibraNeutra",&XC::DqFibras::getFibraNeutra)

  .def("ResultanteComp",&XC::DqFibras::ResultanteComp)
  .def("getMzComp",&XC::DqFibras::getMzComp)
  .def("getMyComp",&XC::DqFibras::getMyComp)
  .def("baricentroCompresiones",&XC::DqFibras::baricentroCompresiones,return_value_policy<copy_const_reference>())
  .def("baricentroDefMenores",&XC::DqFibras::baricentroDefMenores,return_value_policy<copy_const_reference>())

  .def("ResultanteTracc",&XC::DqFibras::ResultanteTracc)
  .def("getMzTracc",&XC::DqFibras::getMzTracc)
  .def("getMyTracc",&XC::DqFibras::getMyTracc)
  .def("baricentroTracciones",&XC::DqFibras::baricentroTracciones,return_value_policy<copy_const_reference>())
  .def("baricentroDefMayores",&XC::DqFibras::baricentroDefMayores,return_value_policy<copy_const_reference>())

  .def("commitState",&XC::DqFibras::commitState)

  .def("getStrainMin",&XC::DqFibras::getStrainMin)
  .def("getStrainMax",&XC::DqFibras::getStrainMax)
  .def("getStrainMed",&XC::DqFibras::getStrainMed)
  .def("getStressMin",&XC::DqFibras::getStressMin)
  .def("getStressMax",&XC::DqFibras::getStressMax)
  .def("getStressMed",&XC::DqFibras::getStressMed)
  .def("getPlanoDeformacion",&XC::DqFibras::getDeformationPlane,"DEPRECATED returns deformation plane.")
  .def("getDeformationPlane",&XC::DqFibras::getDeformationPlane,"returns deformation plane.")
  .def("getDeformation",&XC::DqFibras::getDeformation,return_value_policy<copy_const_reference>(),"Returns generalized strain vector.")
  .def("enTraccion",&XC::DqFibras::enTraccion)
  .def("enFlexion",&XC::DqFibras::enFlexion)
  .def("enCompresion",&XC::DqFibras::enCompresion)
  .def("getStrClaseEsfuerzo",&XC::DqFibras::getStrClaseEsfuerzo)
  .def("getNeutralAxixDepth",&XC::DqFibras::getNeutralAxisDepth)
  .def("getVectorBrazoMecanico",&XC::DqFibras::getVectorBrazoMecanico)
  .def("getSegmentoBrazoMecanico",&XC::DqFibras::getSegmentoBrazoMecanico)
  .def("getBrazoMecanico",&XC::DqFibras::getBrazoMecanico)
  .def("getTrazaPlanoFlexion",&XC::DqFibras::getTrazaPlanoFlexion)
  .def("getTrazaPlanoTraccion",&XC::DqFibras::getTrazaPlanoTraccion)
  .def("getTrazaPlanoCompresion",&XC::DqFibras::getTrazaPlanoCompresion)
  .def("calcAcEficazFibras",&XC::DqFibras::calcAcEficazFibras)
   //.def("getContourAcEficazFibra",&XC::DqFibras::getContourAcEficazFibra)
  .def("getAcEficazFibra",&XC::DqFibras::getAcEficazFibra)
  .def("getAcEficazFibras",&XC::DqFibras::getAcEficazFibras)
  .def("calcRecubrimientos",&XC::DqFibras::calcRecubrimientos)
  .def("calcSeparaciones",&XC::DqFibras::calcSeparaciones)
  .def("getRecubrimientoFibra",&XC::DqFibras::getRecubrimientoFibra,return_value_policy<copy_const_reference>())
  .def("getSeparacionFibra",&XC::DqFibras::getSeparacionFibra,return_value_policy<copy_const_reference>())
  .def("getDiamEqFibra",&XC::DqFibras::getDiamEqFibra)
  .def("getSigmaSRFibra",&XC::DqFibras::getSigmaSRFibra)
  .def("getDistMediaFibras",&XC::DqFibras::getDistMediaFibras)
  .def("updateCDG",&XC::DqFibras::updateCDG)

  .def("getYMin",&XC::DqFibras::GetYMin)
  .def("getZMin",&XC::DqFibras::GetZMin)
  .def("getYMax",&XC::DqFibras::GetYMax)
  .def("getZMax",&XC::DqFibras::GetZMax)
  .def("getPMax",&XC::DqFibras::GetPMax)
  .def("getPMin",&XC::DqFibras::GetPMin)
//.def("Bnd",&XC::DqFibras::Bnd)
  .def("getSumaAreas",&XC::DqFibras::getSumaAreas)
  .def("getArea",&XC::DqFibras::getSumaAreas)
  .def("getAreaHomogenizedSection",&XC::DqFibras::getAreaHomogenizedSection)
  .def("getCdgHomogenizedSection",make_function(&XC::DqFibras::getCdgHomogenizedSection,return_internal_reference<>()))
  .def("getIz",&XC::DqFibras::getIz)
  .def("getIy",&XC::DqFibras::getIy)
  .def("getPyz",&XC::DqFibras::getPyz)
  .def("getI1",&XC::DqFibras::getI1)
  .def("getI2",&XC::DqFibras::getI2)
  .def("getTh1",&XC::DqFibras::getTh1)
  .def("getEje1",&XC::DqFibras::getEje1)
  .def("getEje2",&XC::DqFibras::getEje2)
  .def("getIyHomogenizedSection",&XC::DqFibras::getIyHomogenizedSection)
  .def("getIzHomogenizedSection",&XC::DqFibras::getIzHomogenizedSection)
  .def("getPyzHomogenizedSection",&XC::DqFibras::getPyzHomogenizedSection)
  .def("getHomogenizedSectionITensor",make_function(getHomogenizedSectionITensor,return_internal_reference<>()))
  .def("getHomogenizedSectionITensorRelToPoint",make_function(getHomogenizedSectionITensorRelToPoint,return_internal_reference<>()))
  .def("getHomogenizedSectionIRelTo",getHomogenizedSectionIRelTo)
  .def("getHomogenizedSectionIRelToLine",getHomogenizedSectionIRelToLine)
  .def("getSzPos",&XC::DqFibras::getSzPos)
  .def("getSzNeg",&XC::DqFibras::getSzNeg)
  .def("getSyPos",&XC::DqFibras::getSyPos)
  .def("getSyNeg",&XC::DqFibras::getSyNeg)
  .def("getSPosHomogenizedSection",&XC::DqFibras::getSPosHomogenizedSection)
  .def("getSNegHomogenizedSection",&XC::DqFibras::getSNegHomogenizedSection)

  .def("getIpolar",&XC::DqFibras::getIpolar)
  .def("getiz",&XC::DqFibras::getiz)
  .def("getiy",&XC::DqFibras::getiy)
  .def("getTagNearestFiber",&XC::DqFibras::nearest_fiber)
   ;

class_<XC::StoFibras , bases<XC::DqFibras>, boost::noncopyable >("StoFibras", no_init);

typedef std::map<std::string,XC::DqFibras> map_fiber_sets;
class_<map_fiber_sets, boost::noncopyable >("MapFiberSets", no_init)
  .def(boost::python::map_indexing_suite<map_fiber_sets >())
  ;

class_<XC::FiberSets , bases<map_fiber_sets>, boost::noncopyable >("FiberSets", no_init)
  .def("create",make_function(&XC::FiberSets::crea_set_fibras, return_internal_reference<>()),"creates set.")
  ;

