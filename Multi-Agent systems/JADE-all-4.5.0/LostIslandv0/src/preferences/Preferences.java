package preferences;
import java.util.ArrayList;

public class Preferences {
	
	private CriterionName[] order_on_criteria; // a total order to begin with...
	private ArrayList<CriterionValue> values = new ArrayList<CriterionValue>();	

	
	public String toString() {
		String s = "";
		for(CriterionValue cv: values) {
			s = s+cv.getTheItem().getName()+": "
				+cv.getNameOfCriterion()+"="
				+cv.getValueForThisCriterion()+"\n";
		}
		return s;
	}
	
	
	
	
	public Preferences() {
		// nothing to do for now
		// in the constructor, you could compute random values of preferences (so
		// that all agents can have random preferences just by invoking new Preferences();
	}
	
	// we are missing a few methods to "see" the values of preferences of an agent
	
	public void add(CriterionValue cv) {
		values.add(cv);
	}
	
	public CriterionName[] getCriteriaInOrder() {
		return order_on_criteria;
	}
	
	public void setOrderCriteria(CriterionName[] list) {
		order_on_criteria = list;
	}
	
	public Value getValue(Item i, CriterionName c) {
		for(CriterionValue v: values)
			if (v.getTheItem()==i && v.getNameOfCriterion()==c) // && = AND
				return v.getValueForThisCriterion();
		return null;
	}

	/** This methods allows to know the preferences in terms of Criteria.
	 * @param c1 A criterion name
	 * @param c2 Another criterion name
	 * @return <code>true</code> if and only if c1 is preferred to c2, which means that the
	 * criterion c1 appears earlier in the list order_on_criteria of the agent. 
	 */
	public boolean isPreferred(CriterionName c1, CriterionName c2) {
		for(CriterionName n: order_on_criteria) {
			if (n==c1)
				return true;
			if (n==c2)
				return false;
		}
		throw new RuntimeException("There is an error in the preference list of the agent: c1 and c2 were not found...");
	}
	
	/** This methods allows to know the preferences in terms of Items.
	 * @param i1 An Item
	 * @param i2 Another Item
	 * @return <code>true</code> if and only if i1 is preferred to i2. 
	 */
	public boolean isPreferred(Item i1, Item i2) {
		return i1.getScore(this)>i2.getScore(this);
	}

	public Item mostPreferred(Item [] list) {
		float best_score = -1;
		Item best_item = null;
		for(Item i: list) {
			if (best_score<i.getScore(this)) {
				best_score = i.getScore(this);
				best_item = i;
			}
		}
		return best_item;
	}
	
	public Item [] sort(Item [] list) {
		// TODO
		return null;
	}
	
	public static void main(String [] args) {
		Preferences preferences_of_Agent1 = new Preferences();
		preferences_of_Agent1.setOrderCriteria(new CriterionName[] {
				CriterionName.DRINK,
				CriterionName.FOOD,
				CriterionName.COST});

		Item water_bottle = new Item("A super cool bottle of water");
		preferences_of_Agent1.add(new CriterionValue(water_bottle,CriterionName.COST,Value.AVERAGE));
		preferences_of_Agent1.add(new CriterionValue(water_bottle,CriterionName.FOOD,Value.USELESS));
		preferences_of_Agent1.add(new CriterionValue(water_bottle,CriterionName.DRINK,Value.VERY_USEFUL));

		Item shoes = new Item("A pair of shoes");
		preferences_of_Agent1.add(new CriterionValue(shoes,CriterionName.COST,Value.AVERAGE));
		preferences_of_Agent1.add(new CriterionValue(shoes,CriterionName.FOOD,Value.USELESS));
		preferences_of_Agent1.add(new CriterionValue(shoes,CriterionName.DRINK,Value.USELESS));

		// test list of preferences
		System.out.println(water_bottle.getValue(preferences_of_Agent1, CriterionName.COST));
		System.out.println(preferences_of_Agent1.isPreferred(CriterionName.FOOD,CriterionName.DRINK));
		System.out.println("water > shoes : " + preferences_of_Agent1.isPreferred(water_bottle,shoes));
		System.out.println("shoes > water : " + preferences_of_Agent1.isPreferred(shoes,water_bottle));
		System.out.println("shoes (for agent 1) = " + shoes.getScore(preferences_of_Agent1));
		System.out.println("water (for agent 1) = " + water_bottle.getScore(preferences_of_Agent1));
		System.out.println("Most preferred item is : " +
				preferences_of_Agent1.mostPreferred(new Item[] {water_bottle, shoes}).getName() );
	}
}
