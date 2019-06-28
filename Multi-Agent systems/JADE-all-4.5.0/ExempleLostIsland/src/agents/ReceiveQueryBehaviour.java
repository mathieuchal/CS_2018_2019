package agents;

import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import preferences.Item;

public class ReceiveQueryBehaviour extends Behaviour {

	public static final int QUERY = 106;
	public static final int INFORM = 107;
	
	@Override
	public void action() {

		/* Listening behaviour to perform query/inform */ 	
		ACLMessage m = myAgent.receive(MessageTemplate.MatchPerformative(QUERY));
		if (m==null) {
			block();
		} else {
			System.out.println("There is still "+ Integer.toString(((Storage)myAgent).getAvailableCost()) +" capacity in the bag ");
			ACLMessage answer = new ACLMessage(INFORM);
			answer.addReceiver(m.getSender());
			answer.setContent(Integer.toString(((Storage)myAgent).getAvailableCost()));
			myAgent.send(answer);
		}
	}
	
	@Override
	public boolean done() {
		// TODO Auto-generated method stub
		return false;
	}

}