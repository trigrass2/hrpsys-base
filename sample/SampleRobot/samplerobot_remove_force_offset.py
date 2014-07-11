#!/usr/bin/env python

try:
    from hrpsys.hrpsys_config import *
    import OpenHRP
except:
    print "import without hrpsys"
    import rtm
    from rtm import *
    from OpenHRP import *
    import waitInput
    from waitInput import *
    import socket
    import time

def getRTCList ():
    return [
            ['seq', "SequencePlayer"],
            ['sh', "StateHolder"],
            ['fk', "ForwardKinematics"],
            ['kf', "KalmanFilter"],
            ['rmfo', "RemoveForceSensorLinkOffset"],
            ]

def init ():
    global hcf
    hcf = HrpsysConfigurator()
    hcf.getRTCList = getRTCList
    hcf.init ("SampleRobot(Robot)0")

def demo():
    import numpy
    init()
    # set initial pose from sample/controller/SampleController/etc/Sample.pos
    initial_pose = [-7.779e-005,  -0.378613,  -0.000209793,  0.832038,  -0.452564,  0.000244781,  0.31129,  -0.159481,  -0.115399,  -0.636277,  0,  0,  0.637045,  -7.77902e-005,  -0.378613,  -0.000209794,  0.832038,  -0.452564,  0.000244781,  0.31129,  0.159481,  0.115399,  -0.636277,  0,  0,  -0.637045,  0,  0,  0]
    hcf.seq_svc.setJointAngles(initial_pose, 0.5)
    hcf.seq_svc.waitInterpolation()
    # 1. force and moment are large because of link offsets
    print numpy.linalg.norm(rtm.readDataPort(hcf.rmfo.port("off_rhsensor")).data) > 1e-2
    print numpy.linalg.norm(rtm.readDataPort(hcf.rmfo.port("off_lhsensor")).data) > 1e-2
    # 2. Set link offsets
    #    link_offset_centroid and link_offset_mass are identified value.
    hcf.rmfo_svc.setForceMomentOffsetParam("rhsensor", OpenHRP.RemoveForceSensorLinkOffsetService.forcemomentOffsetParam(force_offset=[0,0,0], moment_offset=[0,0,0], link_offset_centroid=[0,0.0368,-0.076271], link_offset_mass=0.800011))
    hcf.rmfo_svc.setForceMomentOffsetParam("lhsensor", OpenHRP.RemoveForceSensorLinkOffsetService.forcemomentOffsetParam(force_offset=[0,0,0], moment_offset=[0,0,0], link_offset_centroid=[0,-0.0368,-0.076271], link_offset_mass=0.800011))
    ret = hcf.rmfo_svc.getForceMomentOffsetParam("rhsensor")
    if ret[0] and ret[1].link_offset_mass == 0.800011:
        print "getGaitGeneratorParam() => OK"
    ret = hcf.rmfo_svc.getForceMomentOffsetParam("lhsensor")
    if ret[0] and ret[1].link_offset_mass == 0.800011:
        print "getGaitGeneratorParam() => OK"
    # 3. force and moment are reduced
    print numpy.linalg.norm(rtm.readDataPort(hcf.rmfo.port("off_lhsensor")).data) < 1e-2
    print numpy.linalg.norm(rtm.readDataPort(hcf.rmfo.port("off_lhsensor")).data) < 1e-2
