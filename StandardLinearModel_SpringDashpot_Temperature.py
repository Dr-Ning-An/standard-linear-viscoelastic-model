#######################################################################################
## Ning An, March 2021
## http://www.anning003.com/modeling-viscoelasticity-in-abaqus
## Modeling standard linear viscoelastic material using spring and dashpot elements.
## Temperature effects are predicted by the WLF function.
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

# Parameters for the WLF function
C1 = 1.0
C2 = 10.0
T0 = 20.0 # degree Celsius; reference temperature

T = 18.0 # Temperature of Interest
tau = 1.0
alpha_T = 10.0**(-C1*(T-T0)/(C2+(T-T0)))
tau_prime = tau*alpha_T

#############################################################################################################################
# Created by Ning An
# 2019/12
# http://www.anning003.com/create-virtual-nodes
# Created in Abaqus Version 2017

# Function for creating virtual nodes
# mdb: model database
# NameModel: A string with the name of your model
# NameRef1 & NameRef2: A string with the name of your two virtual nodes.
#############################################################################################################################
def VirtualNodes(mdb, NameModel, NameRef1, x, y, z):
    from part import THREE_D, DEFORMABLE_BODY
    #Create reference parts and assemble
    mdb.models[NameModel].Part(dimensionality=THREE_D, name=NameRef1, type=
        DEFORMABLE_BODY)
    mdb.models[NameModel].parts[NameRef1].ReferencePoint(point=(x,y,z))
    mdb.models[NameModel].rootAssembly.Instance(dependent=ON, name=NameRef1, 
        part=mdb.models[NameModel].parts[NameRef1])


    #Create set of reference points
    mdb.models[NameModel].rootAssembly.Set(name=NameRef1, referencePoints=(
        mdb.models[NameModel].rootAssembly.instances[NameRef1].referencePoints[1],))
    mdb.models[NameModel].rootAssembly.engineeringFeatures.PointMassInertia(alpha=
    0.0, composite=0.0, mass=1.0, name='Inertia-'+NameRef1, region=
    mdb.models[NameModel].rootAssembly.sets[NameRef1])


Mdb()

VirtualNodes(mdb, 'Model-1', 'Node-1', 0.0, 0.0, 0.0)
VirtualNodes(mdb, 'Model-1', 'Node-2', 0.0, 1.0, 0.0)
VirtualNodes(mdb, 'Model-1', 'Node-3', 0.0, 2.0, 0.0)


mdb.models['Model-1'].rootAssembly.engineeringFeatures.TwoPointSpringDashpot(
    axis=NODAL_LINE, 
    dashpotBehavior=ON, 
    dashpotCoefficient=tau_prime, 
    name='Dashpots-1', 
    regionPairs=((mdb.models['Model-1'].rootAssembly.sets['Node-1'], 
    mdb.models['Model-1'].rootAssembly.sets['Node-2']), ), 
    springBehavior=OFF, 
    springStiffness=0.0)

mdb.models['Model-1'].rootAssembly.engineeringFeatures.TwoPointSpringDashpot(
    axis=NODAL_LINE, 
    dashpotBehavior=OFF, 
    dashpotCoefficient=0.0, 
    name='Springs-1', 
    regionPairs=((mdb.models['Model-1'].rootAssembly.sets['Node-2'], 
    mdb.models['Model-1'].rootAssembly.sets['Node-3']), ), 
    springBehavior=ON, 
    springStiffness=1.0)

mdb.models['Model-1'].rootAssembly.engineeringFeatures.TwoPointSpringDashpot(
    axis=NODAL_LINE, 
    dashpotBehavior=OFF, 
    dashpotCoefficient=0.0, 
    name='Springs-2', 
    regionPairs=((mdb.models['Model-1'].rootAssembly.sets['Node-1'], 
    mdb.models['Model-1'].rootAssembly.sets['Node-3']), ), 
    springBehavior=ON, 
    springStiffness=1.0)

mdb.models['Model-1'].ViscoStep(cetol=0.0, initialInc=0.001, name='Step-1', 
    previous='Initial', timeIncrementationMethod=FIXED, timePeriod=0.001)
mdb.models['Model-1'].ViscoStep(cetol=0.0001, initialInc=0.01, maxInc=0.05, 
    maxNumInc=1000, minInc=0.0001, name='Step-2', previous='Step-1', 
    timePeriod=10.0)

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Node-1'], u1=SET, u2=SET, 
    u3=SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-2', 
    region=mdb.models['Model-1'].rootAssembly.sets['Node-3'], u1=SET, u2=SET, 
    u3=SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models['Model-1'].boundaryConditions['BC-2'].setValuesInStep(stepName=
    'Step-1', u2=1.0)

jobName = 'StandardLinearModel_SpringDashpot'
mdb.Job(model='Model-1', name=jobName)
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()