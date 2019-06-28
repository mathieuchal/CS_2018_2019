import jade.core.Agent;
import jade.core.behaviours.TickerBehaviour;

public class SecondTestBehaviour extends TickerBehaviour {
	
	public SecondTestBehaviour(Agent a, long period) {
		super(a, period);
	}
	
	protected void onTick() {
		System.out.println("it is time now");
	}

}
