package agents;

import jade.core.Runtime;

import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.wrapper.AgentContainer;
import jade.wrapper.AgentController;
import jade.wrapper.ControllerException;
import preferences.Value;

public class Launcher {

	public static void main(String [] args) throws ControllerException {
		/** define the possible values */
		Value.initialize();
		Storage.initialize();
		
		/** start the agents */
		
		Runtime rt = Runtime.instance();
		rt.setCloseVM(true);
		Profile pMain = new ProfileImpl("localhost", 8888, null);
		AgentContainer mc = rt.createMainContainer(pMain);
		
		AgentController ac;
		
		ac = mc.createNewAgent("storage", "agents.Storage", new Object[] {});
		ac.start();

		for(int i=1;i<=2;i++) {
			ac = mc.createNewAgent("agent "+i, "agents.Adventurer", new Object[] {});
			ac.start();
		}
	}
}
