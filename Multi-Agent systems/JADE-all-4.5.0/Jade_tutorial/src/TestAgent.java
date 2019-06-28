import jade.core.Agent;
import jade.core.AgentDescriptor;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAAgentManagement.DFAgentDescription;

public class TestAgent extends Agent {

	public void setup() {
		
		ServiceDescription sd = new ServiceDesciption();
		sd.setName("Hello");
		DFAgentDescription ad = new DFAgentDescription();
		ad.setName(getAID());
		ad.addServices(sd);
		
		if (getlocalName().contains("0"))
			addBehaviour(new SendingHelloMessageBehaviour());
			addBehaviour(new TellMeBehaviour());
		addBehaviour(new ReceiveHelloMessgae());
		addBehaviour(new ReceiveTellMe());
		getAID();
	}
}
