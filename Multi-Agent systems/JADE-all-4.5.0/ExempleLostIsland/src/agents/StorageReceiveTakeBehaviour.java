package agents;

import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

public class StorageReceiveTakeBehaviour extends Behaviour {

	@Override
	public void action() {
		ACLMessage m = myAgent.receive(MessageTemplate.MatchPerformative(ACLMessage.QUERY_REF));
		if (m==null) {
			block();
		} else {
			ACLMessage answer = new ACLMessage(ACLMessage.INFORM_REF);
			answer.addReceiver(m.getSender());
			answer.setContent(String.valueOf( ((Storage)myAgent).getAvailableCost() ));
			myAgent.send(answer);
		}
	}

	@Override
	public boolean done() {
		return false;
	}

}
