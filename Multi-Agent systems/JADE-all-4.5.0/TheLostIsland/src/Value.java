
public enum Value {
	USELESS, POOR, NEUTRAL, USEFUL, VERY_USEFUL, OK, COOL, NONE, HOT, AVERAGE;
	
	public  float getValue() {
		switch (this) {
		case USELESS: return 0;
		case POOR: return 0;
		case USEFUL: return 0;
		case VERY_USEFUL: return 0;
		
		case NONE: return 0;
		case OK: return 0;
		case COOL: return 0;
		case HOT: return 0;
		
		case AVERAGE: return 0;
		
		}
	}
}
