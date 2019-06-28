package agents;

import java.util.ArrayList;

import jade.core.Agent;
import preferences.Item;

public class Storage extends Agent {

	public static final ArrayList<Item> possible_items = new ArrayList<Item>();
	public static final int MAXIMUM = 10;
	
	public static void initialize() {
		possible_items.add(new Item("A super cool bottle of water",10));
		possible_items.add(new Item("A pair of shoes",5));
		possible_items.add(new Item("A dangerous knife",1));
	}

	/* attributes */
	
	private ArrayList<Item> selected_items;
	private ArrayList<Item> to_discuss_items;
	private int remaining_capacity = MAXIMUM;
	
	/* agent */
	public void setup() {
		selected_items = new ArrayList<Item>();
		to_discuss_items = new ArrayList<Item>(possible_items);
		
		addBehaviour(new StorageReceiveRequestBehaviour());
		addBehaviour(new StorageReceiveTakeBehaviour());
		
		System.out.println("Storage agent is ready");
//		selected_items.add(possible_items.get(0));
//		System.out.println("there remains : "+getAvailableCost());
	}
	
	/* how much cost is left in the storage */
	public int getAvailableCost() {
//		int v = MAXIMUM;
//		for(Item i : selected_items)
//			v = v-i.getCost();
		return remaining_capacity;
	}
	
	public boolean take(String name) {
		for(Item p : possible_items)
			if (p.getName().equals(name)) {
				selected_items.add(p);
				to_discuss_items.remove(p);
				remaining_capacity -= p.getCost();
				return true;
			}
		return false;
	}
}
