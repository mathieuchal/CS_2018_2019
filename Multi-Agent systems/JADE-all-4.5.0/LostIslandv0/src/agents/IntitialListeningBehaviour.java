package agents;
import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;

public class IntitialListeningBehaviour extends Behaviour {
	
	@Override
	public void action() {
		ACLMessage m = myAgent.receive();
		if (m==null) {
			block():
		} else {
			System.out.println("Agent "+myAgent.getLocalName()+" received message:");
			System.out.println(m);
			//ACLMessage answer = new ACLMessage(SendingHelloMessageBehaviour.HELLO_PERFORMATIVE);
			//answer.addReceiver(m.getSender());
			//myAgent.send(answer);
		}
	}

	@Override
	public boolean done() {
		return false;
	}

}

