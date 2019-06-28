package agents;

import jade.core.Runtime;

import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.wrapper.AgentContainer;
import jade.wrapper.AgentController;
import jade.wrapper.ControllerException;

public class Launcher {

	public static void main(String [] args) throws ControllerException {
		/** define the possible values */
		
		Value.initialize();
		Storage.initialize();
		
		
		
		
		Runtime rt = Runtime.instance();
		rt.setCloseVM(true);
		Profile pMain = new ProfileImpl("localhost", 8888, null);
		AgentContainer mc = rt.createMainContainer(pMain);
		
		for(int i=1;i<=2;i++) {
			AgentController ac = mc.createNewAgent("agent "+i, "agents.Adventurer", new Object[] {});
			ac.start();
		}
	}
}
