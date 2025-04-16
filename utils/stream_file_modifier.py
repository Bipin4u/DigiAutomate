import xml.etree.ElementTree as ET

def modifyStreamFile():
    root = ET.parse('C:Streamphoenix_35_060220_0948am.xa3')
    root.find('Atsc3/Subframe/Plp/Source/PcapFile').attrib['filename'] = "C:Stream\" + streamList[i]
    root.write("C:Streamdemo.XA3")