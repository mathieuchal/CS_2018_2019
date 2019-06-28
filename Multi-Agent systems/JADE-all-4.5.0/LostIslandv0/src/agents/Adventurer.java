package agents;

import java.util.Collections;
import java.util.Random;

import java.util.ArrayList;

import jade.core.Agent;
import preferences.CriterionName;
import preferences.CriterionValue;
import preferences.Item;
import preferences.Preferences;
import preferences.Value;


public class Adventurer extends Agent {

	Preferences pref = new Preferences();
	
	private static Random rand = new Random();
	
	/**give random preferences to the agent */ 
	public void setupRandom() {
		
		for(Item i: Storage.possible_items) {
			for(CriterionName c: CriterionName.values()) {
				Value[] list_of_possibles = Value.possibilities.get(c);
				int random_rank = rand.nextInt(list_of_possibles.length);
				Value selected_value = list_of_possibles[random_rank];
				pref.add(new CriterionValue(water_bottle,c,selected_value));
			}
		}
		
		
		/* generate a random order on the criterions for the agent's preference */
		ArrayList<CriterionName> list_of_criterion = new ArrayList<CriterionName>();
		for(CriterionName c: CriterionName.values())
			list_of_criterion.add(c);
		Collections.shuffle(list_of_criterion);
		pref.setOrderCriteria(list_of_criterion.toArray(new CriterionName[0]));
		
	}
	
	/**give random preferences to the agent */ 
	public void setupTest1() {
		
		pref.setOrderCriteria(new CriterionName[] {
				CriterionName.DRINK,
				CriterionName.FOOD,
				CriterionName.COST});

		Item water_bottle = new Item("A super cool bottle of water");
		pref.add(new CriterionValue(water_bottle,CriterionName.COST,Value.AVERAGE));
		pref.add(new CriterionValue(water_bottle,CriterionName.FOOD,Value.USELESS));
		pref.add(new CriterionValue(water_bottle,CriterionName.DRINK,Value.VERY_USEFUL));

		Item shoes = new Item("A pair of shoes");
		pref.add(new CriterionValue(shoes,CriterionName.COST,Value.AVERAGE));
		pref.add(new CriterionValue(shoes,CriterionName.FOOD,Value.USELESS));
		pref.add(new CriterionValue(shoes,CriterionName.DRINK,Value.USELESS));

		
		System.out.println("An adventurer is ready to negotiate");
	}
	
	public void setupTest2() {
		
		pref.setOrderCriteria(new CriterionName[] {
				CriterionName.DRINK,
				CriterionName.FOOD,
				CriterionName.COST});

		Item water_bottle = new Item("A super cool bottle of water");
		pref.add(new CriterionValue(water_bottle,CriterionName.COST,Value.POOR));
		pref.add(new CriterionValue(water_bottle,CriterionName.FOOD,Value.NONE));
		pref.add(new CriterionValue(water_bottle,CriterionName.DRINK,Value.VERY_USEFUL));

		Item shoes = new Item("A pair of shoes");
		pref.add(new CriterionValue(shoes,CriterionName.COST,Value.AVERAGE));
		pref.add(new CriterionValue(shoes,CriterionName.FOOD,Value.USEFUL));
		pref.add(new CriterionValue(shoes,CriterionName.DRINK,Value.USELESS));

		}
		
		
	
	public void setup() {
		
		setupRandom();
	
//		if (getLocalName(.equals("agent1"))
//			setupTest1();
//		else if if (getLocalName(.equals("agent2"))
//			setupTest1();
		
		addBehaviour(new IntitialListeningBehaviour());
		
		System.out.println("Adventurer "+ getLocalName() + " is ready to negotiate");
		System.out.println(pref);
	}
		

}
