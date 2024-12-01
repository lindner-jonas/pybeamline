from pybeamline.algorithms.conformance.MultiperspectiveConformance.Templates.TemplateProtocol import Template

class Chain():
    
    def __init__(self) -> None:
        pass

    def opening(self):
        pass

    def closing(self, pending, fulfillments, violations):
        for act in pending:
            pending = pending.remove(act)
            violations = violations + [act]
        return pending, violations

    def fullfillment(self, e, trace, pending, fulfillments, T, phi_a, phi_c, phi_tau):
        if len(pending) == 1:
            act = pending[0]
            if Template.phi_activity(e) in T and temp.verify(phi_c, act, e) and Template.verify3(phi_tau, act, e):
                pending = pending[1:]
                fulfillments = fulfillments + [act]
                
        return pending, fulfillments

    def violation(self, e, trace, pending, violations, T, phi_c, phi_tau):
        if len(pending) == 1:
            act = pending[0]
            if Template.phi_activity(e) not in T or not Template.verify2(phi_c, act, e) or not Template.verify3(phi_tau, act, e):
                pending = pending[1:]
                violations = violations + [act]

        return pending, violations

    def activation(self, e, A, pending, phi_a):
        if Template.phi_activity(e) in A and Template.verify1(phi_a, e):
            pending = pending + [e]
        return pending