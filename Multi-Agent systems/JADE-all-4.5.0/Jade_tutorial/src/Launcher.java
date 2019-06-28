import jade.core.Runtime;
import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.wrapper.AgentContainer;
import jade.wrapper.AgentController;
import jade.wrapper.StaleProxyException;

public class Launcher {

	public static void main(String [] args) throws StaleProxyException {
	  Runtime rt = Runtime.instance();
	  rt.setCloseVM(true);
	  Profile pMain = new ProfileImpl("localhost", 8888, null);
	  AgentContainer mc = rt.createMainContainer(pMain);
	  
	  //mc.createNewAgent("MyAgentName", "TestAgent.class.getName()", arg2)
	  for(int i=0;i<2;i++) {
	  	AgentController ac = mc.createNewAgent("agent"+i , "TestAgent", new Object[] {"IamAgent"+i} );
	  	ac.start();
	  }
	}
}