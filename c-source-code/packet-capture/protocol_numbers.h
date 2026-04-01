#ifndef PROTO_NUMS_H
#define PROTO_NUMS_H

#include <windows.h>
#include <stdbool.h>

static const char* intToProto[256] = {
    "HOPOPT", "ICMP", "IGMP", "GGP", "IPv4", "ST", "TCP", "CBT", "EGP", "IGP",
    "BBN-RCC-MON", "NVP-II", "PUP", "ARGUS", "EMCON", "XNET", "CHAOS", "UDP",
    "MUX", "DCN-MEAS", "HMP", "PRM", "XNS-IDP", "TRUNK-1", "TRUNK-2", "LEAF-1",
    "LEAF-2", "RDP", "IRTP", "ISO-TP4", "NETBLT", "MFE-NSP", "MERIT-INP",
    "DCCP", "3PC", "IDPR", "XTP", "DDP", "IDPR-CMTP", "TP++", "IL", "IPv6",
    "SDRP", "IPv6-Route", "IPv6-Frag", "IDRP", "RSVP", "GRE", "DSR", "BNA",
    "ESP", "AH", "I-NLSP", "SWIPE", "NARP", "MOBILE", "TLSP", "SKIP",
    "IPv6-ICMP", "IPv6-NoNxt", "IPv6-Opts", "UNKNOWN", "CFTP", "UNKNOWN",
    "SAT-EXPAK", "KRYPTOLAN", "RVD", "IPPC", "UNKNOWN", "SAT-MON", "VISA",
    "IPCV", "CPNX", "CPHB", "WSN", "PVP", "BR-SAT-MON", "SUN-ND", "WB-MON",
    "WB-EXPAK", "ISO-IP", "VMTP", "SECURE-VMTP", "VINES", "TTP", "NSFNET-IGP",
    "DGP", "TCF", "EIGRP", "OSPFIGP", "Sprite-RPC", "LARP", "MTP", "AX.25",
    "IPIP", "MICP", "SCC-SP", "ETHERIP", "ENCAP", "UNKNOWN", "GMTP", "IFMP",
    "PNNI", "PIM", "ARIS", "SCPS", "QNX", "A/N", "IPComp", "SNP",
    "Compaq-Peer", "IPX-in-IP", "VRRP", "PGM", "UNKNOWN", "L2TP", "DDX",
    "IATP", "STP", "SRP", "UTI", "SMP", "SM", "PTP", "ISIS_V4", "FIRE",
    "CRTP", "CRUDP", "SSCOPMCE", "IPLT", "SPS", "PIPE", "SCTP", "FC",
    "RSVP-E2E", "Mobility", "UDPLite", "MPLS-in-IP", "manet", "HIP", "Shim6",
    "WESP", "ROHC", "Ethernet"
};

bool IsDns(u_short src_port, u_short dst_port) {
    return src_port == 53 || dst_port == 53;
}

bool IsMdns(u_short src_port, u_short dst_port) {
    return src_port == 5353 || dst_port == 5353;
}

#endif