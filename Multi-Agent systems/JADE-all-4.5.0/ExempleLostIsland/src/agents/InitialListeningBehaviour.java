package agents;

import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;

public class InitialListeningBehaviour extends Behaviour {

	@Override
	public void action() {
		ACLMessage m = myAgent.receive();
		if (m==null) {
			block();
		} else {
			System.out.println(myAgent.getLocalName() + " received:");
			System.out.println(m);
		}
	}

	@Override
	public boolean done() {
		return false;
	}

}
