from pybeamline.algorithms.conformance.MultiperspectiveConformance.Templates.TemplateProtocol import Template

class Response(): 
    def __init__(self) -> None:
        pass

    def opening(self):
        pass

    def closing(self, pending, fulfillments, violations, phi_c, phi_tau):

        for act in pending.copy():
            pending.remove(act)
            violations.add(act)
        
        return pending, violations

    def fullfillment(self, e, trace, pending, fulfillments, T, phi_a, phi_c, phi_tau, A):
        
        x = Template.phi_activity(e)
        if (x in T['concept:name']):
            y = pending.copy()
            for act in y:
                if (Template.verify2(phi_c,act,e) and Template.verify3(phi_tau, act,e)):
                    pending.remove(act)
                    fulfillments.add(act)

        return pending, fulfillments

    def violation(self, e, trace, pending, violations, T, phi_c, phi_tau, phi_a, A):
        
        return pending, violations

    def activation(self, e, A, pending, phi_a):

        x = Template.phi_activity(e)
        y = Template.verify1(phi_a,e)
        if (x in A['concept:name'] and y):
            pending.add(e)
        
        return pending