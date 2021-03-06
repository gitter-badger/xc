# -*- coding: utf-8 -*-
# Geometric entities representation (k-points,lines,surfaces,bodies,...)

import vtk
from xcVtk import cadMesh
from xcVtk import vtk_grafico_base
from miscUtils import LogMessages as lmsg

class RecordDefDisplayCAD(vtk_grafico_base.RecordDefDisplay):
  ''' Defines graphic output.'''
  def defineEscenaMalla(self, field):
    ''' Defines mesh scene on ouput display.'''
    self.gridRecord.uGrid= vtk.vtkUnstructuredGrid()
    self.gridRecord.cellType= "lines"
    setToDraw= self.gridRecord.xcSet
    numKPts= setToDraw.getPoints.size
    if(numKPts>0):
      cadMesh.VtkCargaMalla(self.gridRecord)
      self.renderer= vtk.vtkRenderer()
      self.renderer.SetBackground(self.bgRComp,self.bgGComp,self.bgBComp)
      cadMesh.VtkDefineActorKPoint(self.gridRecord,self.renderer,0.02)
      cadMesh.VtkDefineActorCells(self.gridRecord,self.renderer,"wireframe")
      self.renderer.ResetCamera()
    else:
      lmsg.warning("Error when drawing set: '"+setToDraw.name+"' it has not key points so I can't get set geometry (use fillDownwards?)")

    #Implementar dibujo de etiquetas.
    # if(entToLabel=="cells"):
    #   xcVtk.cadMesh.VtkDibujaIdsCells(self.gridRecord,setToDraw,nmbTipoCeldas,renderer)
    # elif(entToLabel=="points"):
    #   xcVtk.cadMesh.VtkDibujaIdsKPts(self.gridRecord,setToDraw,renderer)


  def grafico_cad(self,xcSet,caption= ''):
    ''' Parameters:
       xcSet:   set to be represented
       caption: text to display in the graphic.
    '''
    self.setupGrid(xcSet)
    self.displayGrid(caption)

  def displayBlocks(self, xcSet, fName= None, caption= ''):
    ''' Parameters:
       xcSet: set to be represented
       field: field to show (optional)
       diagrams: diagrams to show (optional)
       fName: name of the graphic file to create (if None then -> screen window).
       caption: text to display in the graphic.
    '''
    self.setupGrid(xcSet)
    self.defineEscenaMalla(None)
    self.displayScene(caption,fName)
 
  def plotCadModel(self, xcSet, field, fName, caption= ''):
    lmsg.warning('plotCadMOdel DEPRECATED; use displayBlocks.')
    self.displayBlocks(xcSet,fName,caption)


