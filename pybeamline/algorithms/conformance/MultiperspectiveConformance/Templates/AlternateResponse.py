from pybeamline.algorithms.conformance.MultiperspectiveConformance.Templates.TemplateProtocol import Template

# NB - work in progress
class Alternate():
    
    def __init__(self) -> None:
        self.possibleTargets = set()

    def opening(self):
        self.possibleTargets = set()

    def closing(self, pending, fulfillments : set, violations : set, phi_c, phi_tau): # added phi_c, phi_tau
        if (len(pending) == 1):
            targetFound = False
            act = list(pending)[0]
            for p in self.possibleTargets:
                if (Template.verify2(phi_c, act, p) and Template.verify3(phi_tau, act, p)):
                    targetFound = True
                    fulfillments.add(act)
            if (not targetFound):
                violations.add(act)
        return pending, violations

    def fullfillment(self, e, trace, pending : set, fulfillments : set, T, phi_a, phi_c, phi_tau, A):
        if Template.phi_activity(e) in A['concept:name']:
            if (Template.verify1(phi_a, e)):
                if (len(self.possibleTargets) >= 1 and len(pending) >= 1):
                    act = list(pending)[0] # only 1 element
                    for p in self.possibleTargets:
                        if (Template.verify2(phi_c, act, p) and Template.verify3(phi_tau,act, p)):
                            fulfillments.add(act)
                            pending.remove(act)
        if e.event_attributes['concept:name'] in T['concept:name']:
            self.possibleTargets.add(e)

        return pending, fulfillments

    def violation(self, e, trace, pending : set, violations : set, T, phi_c, phi_tau, phi_a, A): # added phi_a
        if Template.phi_activity(e) in A['concept:name']:
            if (Template.verify1(phi_a, e) and len(pending) == 1):
                act = list(pending)[0]
                pending.remove(act)
                violations.add(act)
        return pending, violations

    def activation(self, e, A, pending, phi_a):
        if Template.phi_activity(e) in A['concept:name']:
            if (Template.verify1(phi_a, e)):
                self.possibleTargets = set()
                pending.add(e)

        return pending  