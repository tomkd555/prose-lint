KINDS = {
 "white": ["w2", "w2b", "w4", "w4b", "w7"],
 "notice": ["n3", "n11", "n12", "n13"],
 "speech": ["r4", "b2", "b3", "b4"],
 "column": ["s1", "s2", "s_010", "s_030", "s_050", "s_070", "s_090", "s_110", "s_130", "s_160", "s_170", "k1", "k2", "k3", "k4"],
 "pr": ["m1", "m2", "m3"],
 "guide": ["p4", "j2"],
 "report": ["jtsb1", "cocoa"],
}
KIND_OF = {d: k for k, ds in KINDS.items() for d in ds}
