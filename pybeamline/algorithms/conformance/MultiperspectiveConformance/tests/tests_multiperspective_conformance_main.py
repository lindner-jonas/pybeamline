import pybeamline.algorithms.conformance.MultiperspectiveConformance.tests.tests_multiperspective_conformance_response as response
import pybeamline.algorithms.conformance.MultiperspectiveConformance.tests.tests_multiperspective_conformance_alternate as alternate
import pybeamline.algorithms.conformance.MultiperspectiveConformance.tests.tests_multiperspective_conformance_chain as chain


if __name__ == "__main__":
    response.runTests()
    alternate.runTests()
    chain.runTests()