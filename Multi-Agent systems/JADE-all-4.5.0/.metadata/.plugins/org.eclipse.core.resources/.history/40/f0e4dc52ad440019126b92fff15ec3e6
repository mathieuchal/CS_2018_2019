package agents;

import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import preferences.Item;

public class NegotiateBehaviour extends Behaviour {

	public static final int PROPOSE = 101;
	public static final int ACCEPT = 102;
	public static final int COMMIT = 103;
	public static final int ASK_WHY = 104;
	public static final int ARGUE = 105;

	private int current_step = 0;

	public NegotiateBehaviour(int initial_step) {
		current_step = initial_step;
	}
	
	@Override
	public void action() {


		/* Step 0 : wait for =a PROPOSE message */ 
		if (current_step==0) {			
			ACLMessage m = myAgent.receive(MessageTemplate.MatchPerformative(PROPOSE));
			if (m==null) {
				block();
			} else {
				boolean ok = ((Adventurer)myAgent).pref
						.acceptable(m.getContent(), Storage.possible_items.toArray(new Item[0]));
				if (ok) {
					System.out.println("Item "+m.getContent()+" is acceptable");
					ACLMessage answer = new ACLMessage(ACCEPT);
					answer.addReceiver(m.getSender());
					answer.setContent(m.getContent());
					myAgent.send(answer);
					// remain in step 0
				} else {
					System.out.println("Item "+m.getContent()+" is NOT acceptable");
					ACLMessage answer = new ACLMessage(ASK_WHY);
					answer.addReceiver(m.getSender());
					answer.setContent(m.getContent());
					myAgent.send(answer);
					// switch to step 1
					current_step = 1;
				}
			}
		}
		/* Step 1 : wait for some explaination (after an ASK_WHY) */ 
		if (current_step==1) {
			ACLMessage m = myAgent.receive();
			if (m==null) {
				block();
			} else {
				System.out.println("received : "+m);
			}
		}
		/* Step 2 : wait for some ASK_WHY or an ACCEPT or an ARGUE */
		if (current_step==2) {
			ACLMessage m = myAgent.receive();
			if (m==null) {
				block();
			} else {
				System.out.println("received : "+m);
				/* reaction is based on the message performative */
				
				/* 1. In the case of an ASK_WHY -> answer with an ARGUE */
				if (m.getPerformative()==ASK_WHY) {
					ACLMessage answer = new ACLMessage(ARGUE);
					answer.addReceiver(m.getSender());
					
					/* see section 6.3 for "how to find the argument values" */
//					Argument myArgument = new Argument(...);
//					myArgument.addPremissComparison(...);
//					myArgument.addPremissCoupleValue(...);
//					
//					answer.setContentObject(myArgument);
					
					myAgent.send(answer);
				}
			}
		}
	}

	@Override
	public boolean done() {
		// TODO Auto-generated method stub
		return false;
	}

}
