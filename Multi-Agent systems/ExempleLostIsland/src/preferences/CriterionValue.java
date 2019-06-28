package preferences;

public class CriterionValue {

	private Item theItem;
	private CriterionName nameOfCriterion;
	private Value valueForThisCriterion;
	
	public CriterionValue(Item i, CriterionName nameOfCriterion, Value valueForThisCriterion) {
		this.theItem = i;
		this.nameOfCriterion = nameOfCriterion;
		this.valueForThisCriterion = valueForThisCriterion;
	}

	public Item getTheItem() {
		return theItem;
	}

	public CriterionName getNameOfCriterion() {
		return nameOfCriterion;
	}

	public Value getValueForThisCriterion() {
		return valueForThisCriterion;
	}	
}
