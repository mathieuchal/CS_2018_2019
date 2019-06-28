package agents;

import java.util.Random;
import java.util.ArrayList;
import java.util.Collections;

import jade.core.AID;
import jade.core.Agent;
import jade.lang.acl.ACLMessage;
import preferences.CriterionName;
import preferences.CriterionValue;
import preferences.Item;
import preferences.Preferences;
import preferences.Value;

public class Adventurer extends Agent {

	private static Random rand = new Random();
	
	Preferences pref = new Preferences();
	
	/** gives random preferences to the agent */
	public void setupRandom() {
		/* generate a random preference set for each possible item */
		for(Item i: Storage.possible_items) {
			for(CriterionName c : CriterionName.values()) {
				Value[] list_of_possibles = Value.possibilities.get(c);
				int random_rank = rand.nextInt(list_of_possibles.length);
				Value selected_value = list_of_possibles[random_rank];
				pref.add(new CriterionValue(i,c,selected_value));
			}
		}
		/* generate a random order on the criterion for the agent's preference set */
		ArrayList<CriterionName> list_of_criterion = new ArrayList<CriterionName>();
		for(CriterionName c : CriterionName.values())
			list_of_criterion.add(c);
		Collections.shuffle(list_of_criterion);
		pref.setOrderCriteria(list_of_criterion.toArray(new CriterionName[0]));
	}
	
	/** gives specific preferences to the agent */
	public void setupTest1() {
		pref.setOrderCriteria(new CriterionName[] {
				CriterionName.DRINK,
				CriterionName.FOOD,
				CriterionName.COST});

		Item water_bottle = new Item("A super cool bottle of water",10);
		pref.add(new CriterionValue(water_bottle,CriterionName.COST,Value.AVERAGE));
		pref.add(new CriterionValue(water_bottle,CriterionName.FOOD,Value.USELESS));
		pref.add(new CriterionValue(water_bottle,CriterionName.DRINK,Value.VERY_USEFUL));

//		Item shoes = new Item("A pair of shoes");
//		pref.add(new CriterionValue(shoes,CriterionName.COST,Value.AVERAGE));
//		pref.add(new CriterionValue(shoes,CriterionName.FOOD,Value.USELESS));
//		pref.add(new CriterionValue(shoes,CriterionName.DRINK,Value.USELESS));
	}
	public void setupTest2() {
		pref.setOrderCriteria(new CriterionName[] {
				CriterionName.FOOD,
				CriterionName.DRINK,
				CriterionName.COST});

		Item water_bottle = new Item("A super cool bottle of water",10);
		pref.add(new CriterionValue(water_bottle,CriterionName.COST,Value.POOR));
		pref.add(new CriterionValue(water_bottle,CriterionName.FOOD,Value.NONE));
		pref.add(new CriterionValue(water_bottle,CriterionName.DRINK,Value.VERY_USEFUL));

//		Item shoes = new Item("A pair of shoes");
//		pref.add(new CriterionValue(shoes,CriterionName.COST,Value.AVERAGE));
//		pref.add(new CriterionValue(shoes,CriterionName.FOOD,Value.USEFUL));
//		pref.add(new CriterionValue(shoes,CriterionName.DRINK,Value.USELESS));
	}
	
	public void setup() {
		
		setupRandom();
		
//		if (getLocalName().equals("agent 1"))
//			setupTest1();
//		else if (getLocalName().equals("agent 2"))
//			setupTest2();
		
		if (getLocalName().equals("agent 2")) {
			addBehaviour(new NegotiateBehaviour(0)); // start with "listening to PROPOSE"
		}
		
		System.out.println("Adventurer "+getLocalName()+" is ready to negotiate");
		System.out.println(pref);
		
		if (getLocalName().equals("agent 1")) {
			try {
				Thread.sleep(500);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			
			Item most_preferred = pref.mostPreferred(Storage.possible_items.toArray(new Item[0]));
			System.out.println("most preferred = "+most_preferred.getName());
			ACLMessage m = new ACLMessage(NegotiateBehaviour.PROPOSE);
			m.setContent(most_preferred.getName());
			m.addReceiver(new AID("agent 2",false));
			send(m);
			addBehaviour(new NegotiateBehaviour(2)); // start with "listening to any answer"
		}
	}
}
