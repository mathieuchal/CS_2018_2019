import java.util.ArrayList;
import java.util.List;

public class Preference {
	
	private Criteria[] order_on_criteria;
	
	public ArrayList<CriterionValue> values = new ArrayList<CriterionValue>();
	
	public Preference() {
		//nothing to do for no
	}
	
	public void setOrderCriteria(CriterionName[] list) {
		order_on_criteria = list;
	}
	
	public Value getValue(Item i, CriterionName c) {
		for(CriterionValue v: values) {
			if (v.getTheItem()==i && v.getNameOfCriterion()==c)
				return v.getValueForThisCriterion();
			return null;
		}
	
	public boolean isPreferred(CriterionName c1, CriterionName c2) {
		for(CriterionName n: order_on_criteria) {
			if (n==c1)
				return true;
			if (n==c2)
				return false;
			}
		throw new RuntimeException("There is an error in the preference list of the agent")
		}
	
	public boolean isPreferred(Item i1, Item i2 {
		return i1.getScore(this)>i2.getScore(this);
	}
	
	public Item mostPreferred(Item [] list) {
		float best_score = -1;
		Item best_item = null;
		for(Item i: list) {
			if (best_score<i.getScore(this))
		
	}
	
	public Item [] sort(Item [] list) {
		//TODO
		return null;
	}
			
					
			//TODO
		return false;
	}
			)
		
		public static void main(String [] args) {
			Preferences preferences_of_Agent1 = new Preferences();
			preferences_of_Agent1.setOrderCriteria(new  CriterionName[] {
					CriterionName.DRINK,
					CriterionName.FOOD,
					CriterionName.COST});
			
			Item water_bottle = new Item("bottle");
			water_bottle.values.add(new CriterionValue(CriterionValue(CriterionName.COST,Value.AVERAGE)));
			water_bottle.values.add(new CriterionValue(CriterionValue(CriterionName.FOOD,Value.USELESS)));
			water_bottle.values.add(new CriterionValue(CriterionValue(CriterionName.DRINK,Value.VERY_USEFUL)));
			
			
					
					
					
			}
					)
			order_on_criteria = list;
		}
}
}
