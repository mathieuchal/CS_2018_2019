import jade.core.behaviours.Behaviour;

public class SayingHelloBehaviour extends Behaviour {

	private int counter = 0;
	public static final int MA =10;
	
	public void action() {
		if (counter==0)
			System.out.println("Agent" + ((TestAgent)myAgent).getMyID() + " is starting");
		counter++;
		
		System.out.println("Agent" + ((TestAgent)myAgent).getMyID() + " is at step " + counter);
		//Random rand = new Random()
		block(500);
		if (counter==MA)
			System.out.println("Agent" + ((TestAgent)myAgent).getMyID() + " has finished");	
	}

	public boolean done() {
		// TODO Auto-generated method stub
		return counter>=MA;
	}
	
}
