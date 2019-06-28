package agents;

import preferences.CriterionName;
import preferences.Value;
import java.util.ArrayList;

import jade.util.leap.Serializable;

public class Argument implements Serializable {

	private static final long serialVersionUID = 1L;
	private boolean pro;
	private String conclusion;
	private ArrayList<Comparison> comparisons = new ArrayList<Comparison>();
	private ArrayList<CoupleValue> values = new ArrayList<CoupleValue>();
	
	public Argument(boolean p, String name) {
		this.pro = p;
		this.conclusion = name;
	}
	
	public void addPremissComparison(CriterionName n1, CriterionName n2) {
		comparisons.add(new Comparison(n1,n2));
	}

	public void addPremissCoupleValue(CriterionName n, Value v) {
		values.add(new CoupleValue(n,v));
	}
}

class Comparison {
	CriterionName best;
	CriterionName worst;
	public Comparison(CriterionName best, CriterionName worst) {
		this.best = best;
		this.worst = worst;
	}	
}

class CoupleValue {
	CriterionName name;
	Value value;
	public CoupleValue(CriterionName name, Value value) {
		this.name = name;
		this.value = value;
	}	
}