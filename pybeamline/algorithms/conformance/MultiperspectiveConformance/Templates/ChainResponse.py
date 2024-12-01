from pybeamline.algorithms.conformance.MultiperspectiveConformance.Templates.TemplateProtocol import Template

class Chain():
    
    def __init__(self) -> None:
        pass

    def opening(self):
        pass

    def closing(self, pending: set, fulfillments: set, violations: set, phi_c, phi_tau):
        for act in pending:
            pending.remove(act)
            violations.add(act)
        return pending, violations

    def fullfillment(self, e, trace, pending : set, fulfillments : set, T, phi_a, phi_c, phi_tau, A):
        if len(pending) == 1:
            act = next(iter(pending))
            if Template.phi_activity(e) in T['concept:name'] and Template.verify2(phi_c, act, e) and Template.verify3(phi_tau, act, e):
                pending.remove(act)
                fulfillments.add(act)
                
        return pending, fulfillments

    def violation(self, e, trace, pending: set, violations: set, T, phi_c, phi_tau, phi_a, A):
        if len(pending) == 1:
            act = next(iter(pending))
            if Template.phi_activity(e) not in T['concept:name'] or not Template.verify2(phi_c, act, e) or not Template.verify3(phi_tau, act, e):
                pending.remove(act)
                violations.add(act)

        return pending, violations

    def activation(self, e, A, pending: set, phi_a):
        if Template.phi_activity(e) in A['concept:name'] and Template.verify1(phi_a, e):
            pending.add(e)
        return pending