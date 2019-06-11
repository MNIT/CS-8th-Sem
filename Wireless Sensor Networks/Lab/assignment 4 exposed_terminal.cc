#include "ns3/core-module.h"
#include "ns3/propagation-module.h"
#include "ns3/applications-module.h"
#include "ns3/mobility-module.h"
#include "ns3/internet-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/wifi-module.h"
#include "ns3/netanim-module.h"

using namespace ns3;

/// Run single 10 seconds experiment with enabled or disabled RTS/CTS mechanism
void experiment (bool enableCtsRts)
{
  //Enable or disable CTS/RTS
  UintegerValue ctsThr = (enableCtsRts ? UintegerValue (2200) : UintegerValue (100));
  Config::SetDefault ("ns3::WifiRemoteStationManager::RtsCtsThreshold", ctsThr);

  NodeContainer nodes;
  nodes.Create (4);

  //Place nodes
  for (size_t i = 0; i < 4; ++i)
  {
      nodes.Get (i)->AggregateObject (CreateObject<ConstantPositionMobilityModel> ());
  }

  //Propagation loss matrix
  Ptr<MatrixPropagationLossModel> lossModel = CreateObject<MatrixPropagationLossModel> ();
  lossModel->SetDefaultLoss (200); // set default loss to 200 dB (no link)
  lossModel->SetLoss (nodes.Get (1)->GetObject<MobilityModel> (), nodes.Get (0)->GetObject<MobilityModel> (), 50); 
  lossModel->SetLoss (nodes.Get (2)->GetObject<MobilityModel> (), nodes.Get (3)->GetObject<MobilityModel> (), 50); 

  //Create & setup wifi channel
  Ptr<YansWifiChannel> wifiChannel = CreateObject <YansWifiChannel> ();
  wifiChannel->SetPropagationLossModel (lossModel);
  wifiChannel->SetPropagationDelayModel (CreateObject <ConstantSpeedPropagationDelayModel> ());

  // 5. Install wireless devices
  WifiHelper wifi;
  wifi.SetStandard(WIFI_PHY_STANDARD_80211b);
  wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager",
                                "DataMode",StringValue ("DsssRate2Mbps"),
                                "ControlMode",StringValue ("DsssRate1Mbps"));
  
  YansWifiPhyHelper wifiPhy =  YansWifiPhyHelper::Default ();
  wifiPhy.SetChannel (wifiChannel);
  WifiMacHelper wifiMac;
  wifiMac.SetType ("ns3::AdhocWifiMac");
  NetDeviceContainer devices = wifi.Install(wifiPhy, wifiMac, nodes);


  //Install TCP/IP stack & assign IP addresses
  InternetStackHelper internet;
  internet.Install (nodes);
  Ipv4AddressHelper ipv4;
  ipv4.SetBase ("10.0.0.0", "255.0.0.0");
  ipv4.Assign (devices);

  // 7. Install applications: two CBR streams each saturating the channel
  
  // flow 1:  node 1 -> node 0
  ApplicationContainer cbrApps;
  uint16_t cbrPort = 12345;
  OnOffHelper onOffHelper ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address ("10.0.0.1"), cbrPort));
  onOffHelper.SetAttribute ("PacketSize", UintegerValue (1400));
  onOffHelper.SetAttribute ("OnTime",  StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
  onOffHelper.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));

  onOffHelper.SetAttribute ("DataRate", StringValue ("3000000bps"));
  onOffHelper.SetAttribute ("StartTime", TimeValue (Seconds (1.000000)));
  cbrApps.Add (onOffHelper.Install (nodes.Get (1)));
  
  
  // flow 3:  node 2 -> node 3
  ApplicationContainer cbrApps1;
  uint16_t cbrPort1 = 12346;
  OnOffHelper onOffHelper1 ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address ("10.0.0.4"), cbrPort1));
  onOffHelper1.SetAttribute ("PacketSize", UintegerValue (1400));
  onOffHelper1.SetAttribute ("OnTime",  StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
  onOffHelper1.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));

  onOffHelper1.SetAttribute ("DataRate", StringValue ("3001100bps"));
  onOffHelper1.SetAttribute ("StartTime", TimeValue (Seconds (1.001)));
  cbrApps1.Add (onOffHelper1.Install (nodes.Get (2)));


  uint16_t  echoPort = 9;
  UdpEchoClientHelper echoClientHelper (Ipv4Address ("10.0.0.1"), echoPort);
  echoClientHelper.SetAttribute ("MaxPackets", UintegerValue (1));
  echoClientHelper.SetAttribute ("Interval", TimeValue (Seconds (0.1)));
  echoClientHelper.SetAttribute ("PacketSize", UintegerValue (10));
  ApplicationContainer pingApps;

  echoClientHelper.SetAttribute ("StartTime", TimeValue (Seconds (0.001)));
  pingApps.Add (echoClientHelper.Install (nodes.Get (1)));
  
  
  uint16_t  echoPort1 = 10;
  UdpEchoClientHelper echoClientHelper1 (Ipv4Address ("10.0.0.4"), echoPort1);
  echoClientHelper1.SetAttribute ("MaxPackets", UintegerValue (1));
  echoClientHelper1.SetAttribute ("Interval", TimeValue (Seconds (0.1)));
  echoClientHelper1.SetAttribute ("PacketSize", UintegerValue (10));
  ApplicationContainer pingApps1;

  echoClientHelper1.SetAttribute ("StartTime", TimeValue (Seconds (0.006)));
  pingApps1.Add (echoClientHelper1.Install (nodes.Get (2)));
 


  //Install FlowMonitor on all nodes
  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();

  //Run simulation for 10 seconds
  Simulator::Stop (Seconds (10));
  
  if(!enableCtsRts)
  	AnimationInterface anim ("animation_hidden_terminal.xml");
  
  Simulator::Run ();

  monitor->CheckForLostPackets ();
  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ());
  FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats ();
  for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin (); i != stats.end (); ++i)
  {
      if (i->first > 2)
      {
          Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (i->first);
          std::cout << "Flow " << i->first - 2 << " (" << t.sourceAddress << " -> " << t.destinationAddress << ")\n";
          std::cout << "  Tx Packets: " << i->second.txPackets << "\n";
          std::cout << "  Tx Bytes:   " << i->second.txBytes << "\n";
          std::cout << "  TxOffered:  " << i->second.txBytes * 8.0 / 9.0 / 1000 / 1000  << " Mbps\n";
          std::cout << "  Rx Packets: " << i->second.rxPackets << "\n";
          std::cout << "  Rx Bytes:   " << i->second.rxBytes << "\n";
          std::cout << "  Throughput: " << i->second.rxBytes * 8.0 / 9.0 / 1000 / 1000  << " Mbps\n";
      }
  }

  Simulator::Destroy ();
}

int main (int argc, char **argv)
{
  CommandLine cmd;
  cmd.Parse (argc, argv);

  std::cout << "RTS/CTS disabled:\n" << std::flush;
  experiment (false);
  std::cout << "---------------\n";
  std::cout << "RTS/CTS enabled:\n";
  experiment (true);

  return 0;
}
