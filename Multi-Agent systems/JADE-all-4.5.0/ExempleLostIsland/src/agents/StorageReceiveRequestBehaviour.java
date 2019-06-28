package agents;

import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

public class StorageReceiveRequestBehaviour extends Behaviour {

	public static final int TAKE = 100; 
	
	@Override
	public void action() {
		ACLMessage m = myAgent.receive(MessageTemplate.MatchPerformative(TAKE));
		if (m==null) {
			block();
		} else {
			boolean ok = ((Storage)myAgent).take(m.getContent());
			if (!ok) {
				// probably send back a message...
				// should not occur
			}
		}
	}

	@Override
	public boolean done() {
		return false;
	}

}
