#######################################################################################
## Ning An, March 2021
## http://www.anning003.com/standard-linear-viscoelastic-model
## Modeling standard linear viscoelastic material using prony series.
#######################################################################################
# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from abaqusConstants import *
import os

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

Mdb()

mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=2.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(1.0, 1.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=1.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']


mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(moduli=INSTANTANEOUS, 
    table=((2.0, 0.49), ))
mdb.models['Model-1'].materials['Material-1'].Viscoelastic(domain=TIME, table=(
    (0.5, 0.5, 1.0), ), time=PRONY)


mdb.models['Model-1'].HomogeneousSolidSection(material='Material-1', name=
    'Section-1', thickness=None)
mdb.models['Model-1'].parts['Part-1'].Set(cells=
    mdb.models['Model-1'].parts['Part-1'].cells, name='Set-1')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName=
    'Section-1', thicknessAssignment=FROM_SECTION)

mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])

mdb.models['Model-1'].ViscoStep(cetol=0.0, initialInc=0.001, name='Step-1', 
    previous='Initial', timeIncrementationMethod=FIXED, timePeriod=0.001)
mdb.models['Model-1'].ViscoStep(cetol=0.0001, initialInc=0.01, maxInc=0.05, 
    maxNumInc=1000, minInc=0.0001, name='Step-2', previous='Step-1', 
    timePeriod=10.0)


mdb.models['Model-1'].rootAssembly.Set(
    name='Node-1', 
    vertices=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((0.0, 0.0, 0.0), )))
mdb.models['Model-1'].rootAssembly.Set(
    name='Node-2', 
    vertices=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((0.0, 1.0, 0.0), )))
mdb.models['Model-1'].rootAssembly.Set(
    name='Node-3', 
    vertices=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((1.0, 1.0, 0.0), )))
mdb.models['Model-1'].rootAssembly.Set(
    name='Node-4', 
    vertices=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((1.0, 0.0, 0.0), )))
mdb.models['Model-1'].rootAssembly.Set(
    name='Node-5', 
    vertices=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((0.0, 0.0, 1.0), )))
mdb.models['Model-1'].rootAssembly.Set(
    name='Node-6', 
    vertices=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((0.0, 1.0, 1.0), )))
mdb.models['Model-1'].rootAssembly.Set(
    name='Node-7', 
    vertices=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((1.0, 1.0, 1.0), )))
mdb.models['Model-1'].rootAssembly.Set(
    name='Node-8', 
    vertices=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((1.0, 0.0, 1.0), )))


mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Node-1'], u1=SET, u2=SET, 
    u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-2', 
    region=mdb.models['Model-1'].rootAssembly.sets['Node-2'], u1=SET, u2=UNSET, 
    u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-3', 
    region=mdb.models['Model-1'].rootAssembly.sets['Node-3'], u1=UNSET, u2=UNSET, 
    u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-4', 
    region=mdb.models['Model-1'].rootAssembly.sets['Node-4'], u1=UNSET, u2=SET, 
    u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-5', 
    region=mdb.models['Model-1'].rootAssembly.sets['Node-5'], u1=UNSET, u2=UNSET, 
    u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-6', 
    region=mdb.models['Model-1'].rootAssembly.sets['Node-6'], u1=UNSET, u2=UNSET, 
    u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-7', 
    region=mdb.models['Model-1'].rootAssembly.sets['Node-7'], u1=UNSET, u2=UNSET, 
    u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-8', 
    region=mdb.models['Model-1'].rootAssembly.sets['Node-8'], u1=UNSET, u2=UNSET, 
    u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)

mdb.models['Model-1'].boundaryConditions['BC-5'].setValuesInStep(stepName=
    'Step-1', u3=1.0)
mdb.models['Model-1'].boundaryConditions['BC-6'].setValuesInStep(stepName=
    'Step-1', u3=1.0)
mdb.models['Model-1'].boundaryConditions['BC-7'].setValuesInStep(stepName=
    'Step-1', u3=1.0)
mdb.models['Model-1'].boundaryConditions['BC-8'].setValuesInStep(stepName=
    'Step-1', u3=1.0)

mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=1.0)
mdb.models['Model-1'].parts['Part-1'].generateMesh()
mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD), 
    ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-1'].parts['Part-1'].cells, ))

jobName = 'StandardLinearModel_Single3DElement'
mdb.Job(model='Model-1', name=jobName)
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()