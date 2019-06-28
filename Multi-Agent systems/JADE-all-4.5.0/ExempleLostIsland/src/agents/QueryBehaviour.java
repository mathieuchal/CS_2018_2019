package agents;

import jade.core.AID;
import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import preferences.Item;

public class QueryBehaviour extends Behaviour {

	public static final int QUERY = 106;
	public static final int INFORM = 107;
	
	private int current_step = 0;
	
	public QueryBehaviour(int initial_step) {
		current_step = initial_step;
	}
	
	public void action() {
		
		if (current_step==0) {			
			ACLMessage query = new ACLMessage(QUERY);
			query.addReceiver(new AID("storage",false));  //get storage Agent
			query.setContent("Query_capacity"); // get query content 
			myAgent.send(query);
			//System.out.println("A query is being sent by "+ ((Adventurer)myAgent).getName());
			current_step = 1;
		} else {
			((Adventurer)myAgent).capacity_ok  = Boolean.valueOf(myAgent.receive(MessageTemplate.MatchPerformative(INFORM)).getContent());
		}
	}
	
	
	@Override
	public boolean done() {
		// TODO Auto-generated method stub
		return true;
	}

}