from pybeamline.algorithms.conformance.MultiperspectiveConformance.multiperspective_conformance import getLogFromFile, runPybeamlineModel
from pybeamline.algorithms.conformance.MultiperspectiveConformance.MP_Declare_Model import MP_declare_model

# trace: a1->a2->a3->a4: i.e. a1->a2 fulfilled, a2->a3 fulfilled, a3->a4 fulfilled
def testFulfillingTrace():
    model = MP_declare_model.from_xml("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/models/model-3-constraints-response.xml")
    log = getLogFromFile("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/logs/response/4-acts-trace-completely-fulfill.xes")
    
    viol, fulfill, violcount, fulfillcount = runPybeamlineModel(log, model)
    assert(violcount == 0)
    assert(fulfillcount == 3)

# trace: asd->a2->a3->a4, i.e. a1->a2 not activated, a2->a3 fulfilled, a3->a4 fulfilled
def testTraceWithoutActivation():
    model = MP_declare_model.from_xml("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/models/model-3-constraints-response.xml")
    log = getLogFromFile("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/logs/response/4-acts-trace-no-activation.xes")
    
    viol, fulfill, violcount, fulfillcount = runPybeamlineModel(log, model)
    assert(violcount == 0)
    assert(fulfillcount == 2)

# trace: a1->asd->a3->a4, i.e. a1->a2 violated + a2->a3 not activated + a3->a4 fulfilled 
def testTraceWithoutCorrelation():
    model = MP_declare_model.from_xml("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/models/model-3-constraints-response.xml")
    log = getLogFromFile("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/logs/response/4-acts-trace-violating-correlation.xes")
    
    viol, fulfill, violcount, fulfillcount = runPybeamlineModel(log, model)
    assert(violcount == 1)
    assert(fulfillcount == 1)

#trace: a1(0)->a2(11)->a3(12)->a4(22): a1(0)->a2(11) violates (should happen within 10s), a2(11)->a3(12) fulfilled, a3(12)->a4(22) fulfilled
def testTraceViolatingTime():
    model = MP_declare_model.from_xml("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/models/model-3-constraints-response.xml")
    log = getLogFromFile("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/logs/response/4-acts-trace-violating-time.xes")
    
    viol, fulfill, violcount, fulfillcount = runPybeamlineModel(log, model)
    assert(violcount == 1)
    assert(fulfillcount == 2)

#trace: a1->a1->a2->a3->a4: a1->a2 (fulfilled), a1->a2 (fulfilled), a2->a3 (fulfilled), a3->a4 (fulfilled)
def testTraceFulfilledButWithRep():
    model = MP_declare_model.from_xml("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/models/model-3-constraints-response.xml")
    log = getLogFromFile("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/logs/response/4-acts-trace-completely-fulfill-but-with-reps.xes")
    
    viol, fulfill, violcount, fulfillcount = runPybeamlineModel(log, model)
    assert(violcount == 0)
    assert(fulfillcount == 4)

#trace: a1->a4->a2->a3->a4: a1->a2 (fulfilled), a2->a3 (fulfilled), a3->a4 (fulfilled)
def testTraceFulfilledButWithEventInBetween():
    model = MP_declare_model.from_xml("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/models/model-3-constraints-response.xml")
    log = getLogFromFile("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/logs/response/4-acts-trace-completely-fulfill-but-with-event-between.xes")
    
    viol, fulfill, violcount, fulfillcount = runPybeamlineModel(log, model)
    assert(violcount == 0)
    assert(fulfillcount == 3)

def runTests():
    testFulfillingTrace()
    testTraceWithoutActivation()
    testTraceWithoutCorrelation()
    testTraceViolatingTime()
    testTraceFulfilledButWithRep()
    testTraceFulfilledButWithEventInBetween()