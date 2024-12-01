from pybeamline.algorithms.conformance.MultiperspectiveConformance.MP_Declare_Model import Constraint, MP_declare_model
from pybeamline.algorithms.conformance.MultiperspectiveConformance.Templates.Response import Response
from pybeamline.algorithms.conformance.MultiperspectiveConformance.Templates.AlternateResponse import Alternate
from pybeamline.algorithms.conformance.MultiperspectiveConformance.Templates.ChainResponse import Chain

from pybeamline.sources import xes_log_source_from_file
from reactivex import operators as ops
from pybeamline.bevent import BEvent
import json
# Given a log and a model (a set of constraints), return the violations and fulfillments of the model on the log
def check_log_conformance(log, model: MP_declare_model):
    viol = dict()
    fulfill = dict()
    violcount = 0
    fulfillcount = 0
    for caseid, trace in log.items():
        if caseid not in viol:
            viol[caseid] = dict()

        if caseid not in fulfill:
            fulfill[caseid] = dict()

        for constraint in model.get_constraints():
            viol_res, fulfill_res = check_trace_conformance(trace, constraint)

            if (len(viol_res) > 0):
                violcount += len(viol_res)
            if (len(fulfill_res) > 0):
                fulfillcount += len(fulfill_res)
            
            viol[caseid][constraint.id] = list(str(event) for event in viol_res)

            fulfill[caseid][constraint.id] = list(str(event) for event in fulfill_res)
        
    return viol, fulfill, violcount, fulfillcount

# Given a trace and a constraint, return the violations and fulfillments of the constraint on the trace
def check_trace_conformance(trace, constraint:Constraint):
    pending = set()
    fulfillments = set()
    violations = set()
    #temp = Response() #Use correct template later

    if (constraint.name[0] == 'response'):
        temp = Response()
    elif (constraint.name[0] == 'alternate'):
        temp = Alternate()
    elif (constraint.name[0] == 'chain'):
        temp = Chain()
    else: # not implemented
        raise NotImplementedError

    temp.opening()
    for e in trace:
        pending, fulfillments = temp.fullfillment(e, trace, pending, fulfillments, constraint.condition[0].T, constraint.condition[0].phi_a, constraint.condition[0].phi_c, constraint.condition[0].phi_tau, constraint.condition[0].A)
        pending, violations = temp.violation(e, trace, pending, violations, constraint.condition[0].T, constraint.condition[0].phi_c, constraint.condition[0].phi_tau, constraint.condition[0].phi_a, constraint.condition[0].A)
        pending = temp.activation(e, constraint.condition[0].A, pending, constraint.condition[0].phi_a)
    pending, violations = temp.closing(pending, fulfillments, violations, constraint.condition[0].phi_c, constraint.condition[0].phi_tau)

    return violations, fulfillments

def group_events_by_caseid(eventList : list[BEvent]):
    groupedEvents : dict[str, BEvent] = {}
    for event in eventList:
        caseId = event.trace_attributes['concept:name']
        if (caseId not in groupedEvents):
            groupedEvents[caseId] = [event]
        else:
            groupedEvents[caseId].append(event)

    return groupedEvents

def getLogFromFile(file):
    log = xes_log_source_from_file(file).pipe(
        ops.to_list()
    ).run()
    log = group_events_by_caseid(log)
    return log


def runPybeamlineModel(log, model):    
    viol = dict()
    fulfill = dict()
    
    viol, fulfill, violcount, fulfillcount = check_log_conformance(log, model)

    print("violating = " + str(violcount)) # no. constraints failed
    print("fulfilling = " + str(fulfillcount)) # no. constraints fulfilled

    with open('fulfill.json', 'w') as file:
        # Write text to the file
        json.dump(fulfill, file, indent=4)
    
    with open('viol.json', 'w') as file:
        # Write text to the file
        json.dump(viol, file, indent=4)

    return viol, fulfill, violcount, fulfillcount


if __name__ == "__main__":
    model = MP_declare_model.from_xml("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/models/model-from-bridge.xml")
    log = getLogFromFile("pybeamline/algorithms/conformance/MultiperspectiveConformance/tests/logs/log_from_bridge/extension-log-noisy-4.xes")
    
    viol, fulfill, violcount, fulfillcount = runPybeamlineModel(log, model)