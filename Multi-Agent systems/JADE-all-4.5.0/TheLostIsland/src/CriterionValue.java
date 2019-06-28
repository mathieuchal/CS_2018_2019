
public class CriterionValue {
	
	private Item theItem;
	private CriterionName nameOfCriterion;
	private Value ValueForThisCriterion;

	public CriterionValue(String nameOfCriterion, String valueForThisCriterion) {
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
		return ValueForThisCriterion;
	}




}
