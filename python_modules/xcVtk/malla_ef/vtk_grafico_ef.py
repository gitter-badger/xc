# -*- coding: utf-8 -*-
# Graphing of a finite element model.

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2014 LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import sys
import vtk
from miscUtils import LogMessages as lmsg
import xc_base
from vtkUtils import utilsVtk
from xcVtk import vtk_grafico_base
from xcVtk.malla_ef import vtk_define_malla_nodos
from xcVtk.malla_ef import vtk_define_malla_elementos
from xcVtk.malla_ef import vtk_define_malla_cells_ef




class RecordDefDisplayEF(vtk_grafico_base.RecordDefDisplay):
  ''' Define las variables que se emplean para definir
     el dispositivo de salida. '''

  def __init__(self):
    super(RecordDefDisplayEF,self).__init__()
    self.nodos= None
    self.gridMapper= None
  def VtkDefineActorElementos(self, tipoRepr,field):
    # Actor for the surfaces.
    if(field):
      field.setupOnGrid(self.gridRecord.uGrid)
    self.gridMapper= vtk.vtkDataSetMapper()
    self.gridMapper.SetInput(self.gridRecord.uGrid)
    if(field):
      field.setupOnMapper(self.gridMapper)
    elemActor= vtk.vtkActor()
    elemActor.SetMapper(self.gridMapper)
    elemActor.GetProperty().SetColor(1,1,0)

    if(tipoRepr=="points"):
      elemActor.GetProperty().SetRepresentationToPoints()
    elif(tipoRepr=="wireframe"):
      elemActor.GetProperty().SetRepresentationToWireFrame()
    elif(tipoRepr=="surface"):
      elemActor.GetProperty().SetRepresentationToSurface()
    else:
      print "Representation type: '", tipoRepr, "' unknown."
    self.renderer.AddActor(elemActor)
    if(field):
      field.creaColorScaleBar()
      self.renderer.AddActor2D(field.scalarBar)

  # Define el actor a emplear para dibujar nodos.
  def defineActorNode(self, radius):
    sphereSource= vtk.vtkSphereSource()
    sphereSource.SetRadius(radius)
    sphereSource.SetThetaResolution(5)
    sphereSource.SetPhiResolution(5)
    
    markNodos= vtk.vtkGlyph3D()
    markNodos.SetInput(self.gridRecord.uGrid)
    markNodos.SetSource(sphereSource.GetOutput())
    markNodos.ScalingOff()
    markNodos.OrientOff()
    
    mappNodos= vtk.vtkPolyDataMapper()
    mappNodos.SetInput(markNodos.GetOutput())
    visNodos= vtk.vtkActor()
    visNodos.SetMapper(mappNodos)
    visNodos.GetProperty().SetColor(.7, .5, .5)
    self.renderer.AddActor(visNodos)

  def VtkCargaMallaElem(self,field):
    # Definimos grid
    self.nodos= vtk.vtkPoints()
    self.gridRecord.uGrid= vtk.vtkUnstructuredGrid()
    self.gridRecord.uGrid.SetPoints(self.nodos)
    eSet= self.gridRecord.xcSet
    eSet.numerate()
    # Scalar values.
    nodeSet= eSet.getNodes
    if(field):
      arr= field.fillArray(nodeSet)
      field.creaLookUpTable()      
    # Cargamos los nodos en vtk
    setNodos= eSet.getNodes
    if(self.gridRecord.dispScale==0.0):
      for n in setNodos:
        pos= n.getInitialPos3d
        self.nodos.InsertPoint(n.getIdx,pos.x,pos.y,pos.z)
    else:
      posNodo= xc.Vector([0,0,0])
      for n in setNodos:
        posNodo= n.get3dCoo+self.gridRecord.dispScale*n.getDispXYZ
        self.nodos.insertPoint(n.getIdx,posNodo[0],posNodo[1],posNodo[2])
    # Cargamos los elementos en vtk
    setElems= eSet.getElements
    for e in setElems:
      vertices= xc_base.vector_int_to_py_list(e.getIdxNodes)
      vtx= vtk.vtkIdList()
      for vIndex in vertices:
        vtx.InsertNextId(vIndex)
      if(e.getVtkCellType!= vtk.VTK_VERTEX):
        self.gridRecord.uGrid.InsertNextCell(e.getVtkCellType,vtx)
 
    #Cargamos constraint on XXX FALLA
    setConstraints= eSet.getConstraints
    for c in setConstraints:
      vtx= vtk.vtkIdList()
      vtx.InsertNextId(c.getNodeIdx)
      if(c.getVtkCellType!= vtk.VTK_LINE):
        self.gridRecord.uGrid.InsertNextCell(c.getVtkCellType,vtx)

  def defineEscenaMalla(self, field):
    # Define la escena de la malla en el dispositivo de salida.
    self.VtkCargaMallaElem(field)
    self.renderer= vtk.vtkRenderer()
    self.renderer.SetBackground(self.bgRComp,self.bgGComp,self.bgBComp)
    #self.defineActorNode(0.02)
    self.VtkDefineActorElementos("surface",field)
    self.renderer.ResetCamera()

    #Implementar dibujo de etiquetas.
    # if(self.gridRecord.entToLabel=="elementos"):
    #   VtkDibujaIdsElementos(self.renderer)
    # elif(self.gridRecord.entToLabel=="nodos"):
    #   vtk_define_malla_nodos.VtkDibujaIdsNodos(self.renderer)
    # else:
    #   print "Entity: ", self.gridRecord.entToLabel, " unknown."

  def grafico_mef(self,xcSet,caption= '',viewNm='XYZPos'):
    ''' :returs: a graphic of the FE mesh

    :param xcSet:   XC set of elements to be displayed
    :param caption: text to write in the graphic
    :param viewNm:  name of the view to use for the representation
                    predefined view names: 'XYZPos','XNeg','XPos','YNeg','YPos',
                    'ZNeg','ZPos'  (defaults to 'XYZPos')
    '''
    self.viewName=viewNm
    self.setupGrid(xcSet)
    self.displayGrid(caption)

  def displayMesh(self, xcSet, field= None, diagrams= None, fName= None, caption= ''):
    ''' Parameters:
       xcSet: set to be represented
       field: field to show (optional)
       diagrams: diagrams to show (optional)
       fName: name of the graphic file to create (if None then -> screen window).
       caption: text to display in the graphic.
    '''
    self.setupGrid(xcSet)
    self.defineEscenaMalla(field)
    if(diagrams):
      for d in diagrams:
        self.appendDiagram(d)
    self.displayScene(caption,fName)

  def displayScalarField(self, preprocessor, xcSet, field, fName= None):
    lmsg.warning('displayScalarField DEPRECATED; use displayMesh.')
    self.displayMesh(xcSet, field, None, fName)

  def displayNodalLoad(self, nod, color, carga, momento, fEscala):
    #actorName= baseName+"%04d".format(nod.tag) # Tag nodo.

    pos= nod.getCurrentPos3d
    absCarga= carga.Norm()
    if(absCarga>1e-6):
      utilsVtk.dibujaFlecha(self.renderer,color,pos,carga,fEscala*absCarga)

    absMomento= momento.Norm()
    if(absMomento>1e-6):
      utilsVtk.dibujaFlechaDoble(self.renderer,color,pos,momento,fEscala*absMomento)

  def displayNodalLoads(self, preprocessor, loadPattern, color, fEscala):
    loadPattern.addToDomain()
    loadPatternName= loadPattern.getProp("dispName")
    lIter= loadPattern.getNodalLoadIter
    load= lIter.next()
    while not(load is None):
      actorName= "flecha"+loadPatternName+"%04d".format(load.tag) # Tag carga.
      nodeTag= load.getNodeTag
      node= preprocessor.getNodeLoader.getNode(nodeTag)
      carga= load.getForce
      momento= load.getMoment
      self.displayNodalLoad(node, color,carga,momento,fEscala)    
      load= lIter.next()
    loadPattern.removeFromDomain()


  def displayElementPunctualLoad(self, preprocessor, pLoad,loadPattern, renderer, color, carga, fEscala):
    xCarga= pLoad.getElems()
    eleTags= pLoad.elementTags
    loadPatternName= loadPattern.getProp("dispName")
    actorName= "flechaP"+loadPatternName+"%04d".format(tag) # Tag carga.
    for tag in eleTags:
      ele= preprocessor.getElementLoader.getElement(tag)
      actorName+= "%04d".format(tag) # Tag elemento.
      pos= ele.punto(xCarga)
      utilsVtk.dibujaFlecha(self.renderer,color,pos,carga,fEscala)()

  def displayElementUniformLoad(self, preprocessor, unifLoad,loadPattern, color, carga, fEscala):
    loadPatternName= loadPattern.getProp("dispName")
    actorName= "flechaU"+loadPatternName+"%04d".format(unifLoad.tag) # Tag carga.
    eleTags= unifLoad.elementTags
    for tag in eleTags:
      ele= preprocessor.getElementLoader.getElement(tag)
      actorName+= "%04d".format(tag) # Tag elemento.
      print "displayElementUniformLoad not implemented."
      # puntos= ele.getPoints(3,1,1,True)
      # i= 0
      # for capa in puntos:
      #   for pos in capa: 
      #     print pos
      #     utilsVtk.dibujaFlecha(self.renderer,color,pos,carga,fEscala*carga.Norm())
      #     i+= 1

  def displayElementalLoads(self, preprocessor,loadPattern, color, fEscala):
    loadPattern.addToDomain()
    eleLoadIter= loadPattern.getElementalLoadIter
    eleLoad= eleLoadIter.next()
    print "displayElementalLoads not implemented."
    # while not(eleLoad is None):
    #   carga= eleLoad.getGlobalForces()
    #   categoria= eleLoad.category
    #   if(categoria=="uniforme"):
    #     self.displayElementUniformLoad(preprocessor, eleLoad,loadPattern,color,carga,fEscala)
    #   else:
    #     self.displayElementPunctualLoad(preprocessor, eleLoad,loadPattern,color,carga,fEscala)
    # loadPattern.removeFromDomain()

  def displayLoads(self, preprocessor, loadPattern):
    clrVectores= loadPattern.getProp("color")
    fEscalaVectores= loadPattern.getProp("scale")
    self.displayElementalLoads(preprocessor, loadPattern,clrVectores,fEscalaVectores)
    self.displayNodalLoads(preprocessor, loadPattern,clrVectores,fEscalaVectores)

  def appendDiagram(self,diagram):
    diagram.agregaDiagramaAEscena(self)
