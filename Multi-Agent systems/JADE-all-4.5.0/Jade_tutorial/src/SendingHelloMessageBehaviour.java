import jade.core.AID;
import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;

public class SendingHelloMessageBehaviour extends Behaviour {

	public static final int HELLO_PERFORMATIVE = 100;
	
	@Override
	public void action() {
		ACLMessage m = new ACLMessage(HELLO_PERFORMATIVE);
		m.setContent("my content");
		AID id = new AID("agent 1", false);
		m.addReceiver(id);
		myAgent.send(m);	
	}

	@Override
	public boolean done() {
		return true;
	}

}
