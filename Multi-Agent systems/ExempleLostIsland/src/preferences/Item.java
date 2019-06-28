package preferences;
import java.util.ArrayList;

public class Item {
	
	private String name;
	private int real_cost;

	public Item(String name,int cost) {
		this.name = name;
		this.real_cost = cost;
	}
	
	@Override
	public String toString() {
		return name;
	}

	public String getName() {
		return name;
	}
	
	public int getCost() {
		return real_cost;
	}
	
	public Value getValue(Preferences p, CriterionName c) {
		return p.getValue(this,c);
	}

	public float getScore(Preferences p) {
		float weight = 100;
		float sum = 0;
		for(CriterionName c: p.getCriteriaInOrder()) {
			sum = sum + weight * getValue(p,c).getValue();
			weight = weight / 2;
		}
		return sum;
	}
}

