import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;

public class ReceiveHelloMessage extends Behaviour {

	@Override
	public void action() {
		ACLMessage m = myAgent.receive();
		if (m!=null) {
			System.out.println("Agent "+myAgent.getLocalName()+" received message:");
			System.out.println(m);
			//ACLMessage answer = new ACLMessage(SendingHelloMessageBehaviour.HELLO_PERFORMATIVE);
			//answer.addReceiver(m.getSender());
			//myAgent.send(answer);
		} else
			block();
	}

	@Override
	public boolean done() {
		return false;
	}

}
