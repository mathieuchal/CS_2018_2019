package preferences;
import java.util.ArrayList;
import java.util.Hashtable;

public enum Value {
	
	USELESS, POOR, USEFUL, VERY_USEFUL, NONE, OK, COOL, HOT, AVERAGE, CHEAP, EXPENSIVE;

	public float getValue() {
		switch (this) {
		case USELESS: return 0;
		case POOR: return 2;
		case USEFUL: return 8;
		case VERY_USEFUL: return 10;
		
		case AVERAGE: return 30;
		case CHEAP: return 100;
		case EXPENSIVE: return 2;

		case NONE: return 0;
		case OK: return 100;
		case COOL: return 50;
		case HOT: return 20;
		}
		return 0;
	}
	
	public static final Hashtable<CriterionName,Value[]> possibilities = new Hashtable<CriterionName,Value[]>();
	
	public static void initialize() {
		possibilities.put(CriterionName.COST, new Value[]{AVERAGE, CHEAP, EXPENSIVE});
		possibilities.put(CriterionName.FOOD, new Value[]{USELESS, POOR, USEFUL, VERY_USEFUL});
		possibilities.put(CriterionName.DRINK, new Value[]{USELESS, POOR, USEFUL, VERY_USEFUL});
	}
	
}
