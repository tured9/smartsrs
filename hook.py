import xml.etree.ElementTree as ET
from pythonforandroid.toolchain import ToolchainCL

class Toolchain(ToolchainCL):
    def hook_add_xml_to_manifest(self, manifest_et):
        ns = '{http://schemas.android.com/apk/res/android}'
        ET.register_namespace('android', ns.replace('{', '').replace('}', ''))

        # العثور على عنصر الخدمة وإضافة السمة
        for service in manifest_et.findall(".//service"):
            service_name = service.get(f'{ns}name')
            if service_name and 'ServiceSrsservice' in service_name:  # اسم خدمتك
                service.set(f'{ns}foregroundServiceType', 'mediaPlayback')

        return manifest_et
