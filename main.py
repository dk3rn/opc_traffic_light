import asyncio
import threading

from asyncua import Server, Client, ua, Node
from asyncua.common.xmlimporter import XmlImporter
from gui import TrafficLightApp
from data_exchange import Traffic_Light_Container

server = None
endpoint = None
app = None



# Custom user
async def application_auth_method(auth):
    """This method handles user authentication."""
    if auth == (b'user', b'1234'):
        return True
    return False


async def make_nodes_writable(nodes):
    """ Recursively make all variable nodes writable """
    for node in nodes:
        nodeclass = await node.read_node_class()
        if nodeclass == ua.NodeClass.Variable:
            await node.set_writable()
            print(node)

        # Get children and recursively call function on each
        children = await node.get_children()
        if children:
            await make_nodes_writable(children)


async def run_server(endpoint):
    # Server einrichten
    # Set up user authentication

    server = Server()
    await server.init()
    server.set_endpoint(endpoint)
    server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
    server.security_policy_methods = [{"SecurityPolicyUri": "http://opcfoundation.org/UA/SecurityPolicy#None",
                                       "identityVerifier": application_auth_method}]

    # Registriere Namespace
    uri = "http://example.org/trafficlights"
    idx = await server.register_namespace(uri)

    # Hinweis: Manuelle existieren von Basisknoten/Typen-Check, falls benötigt
    objects = server.nodes.objects

    # Sicherstellen ob Basis-Referenzen eingeladen/eingerichtet sind
    base_object_type = server.get_node("i=58")
    print(f"BaseObjectType Node Exists: {await base_object_type.read_browse_name()}")

    # XML Import absichern
    importer = XmlImporter(server)
    await importer.import_xml("nodeset2_traffic_light.xml")

    # Debugging: Überprüfen der importierten Knoten
    children = await objects.get_children()
    print(f"Imported Objects: {[child for child in children]}\n")

    # Use get_children to get list of all top-level nodes
    imported_nodes = await objects.get_children()
    print(f"Imported Objects: {imported_nodes}\n")

    # Make all nodes writable
    await make_nodes_writable(imported_nodes)

    async with server:
        print("Server läuft...")
        await asyncio.sleep(500)


async def run_client(endpoint):
    await asyncio.sleep(5)

    async with Client(endpoint) as client:


        tlc = Traffic_Light_Container();
        namespace_array = await client.get_namespace_array()
        print("Namespace Array:", namespace_array)

        target_namespace = "http://example.org/trafficlights"
        if target_namespace in namespace_array:
            namespace_index = namespace_array.index(target_namespace)
            print(f"Der Namespace '{target_namespace}' hat den Index: {namespace_index}")
        else:
            print(f"Namespace '{target_namespace}' nicht im Server gefunden")

        # Zugriff auf die Knoten, die im Server erstellt wurden
        n_red_light = client.get_node(f"ns={namespace_index};i=3001")  # Beispielhafte NodeId
        n_yellow_light = client.get_node(f"ns={namespace_index};i=3002")  # Beispielhafte NodeId
        n_green_light = client.get_node(f"ns={namespace_index};i=3003")  # Beispielhafte NodeId
        n_request = client.get_node(f"ns={namespace_index};i=3004")  # Beispielhafte NodeId
        n_green_light_left = client.get_node(f"ns={namespace_index};i=3005")  # Beispielhafte NodeId

        while True:
            global app
            # Lese- und Schreiboperationen
            red_status = tlc.red
            await n_red_light.write_value(bool(red_status))

            yellow_status = tlc.yellow
            await n_yellow_light.write_value(bool(yellow_status))

            green_status = tlc.green
            await n_green_light.write_value(bool(green_status))

            time_left = tlc.green_time_left
            variantvalue = ua.Variant(time_left, ua.VariantType.Int16)
            await n_green_light_left.write_value(variantvalue)

            tlc.request = await n_request.read_value()
            if tlc.request:
                global app
                app.request_opc()
                await n_request.write_value(bool(0))




            # Kurze Pause zwischen den Aktionen, um die CPU zu schonen
            await asyncio.sleep(0.2)  # Beispiel für eine 10-sekündige Pause




        # Lese- und Schreiboperationen
        # red_status = await n_red_light.read_value()

def run_traffic_light():
    """Function to run the traffic light in a separate thread."""
    global app
    app = TrafficLightApp()
    app.mainloop()


async def main():
    endpoint = "opc.tcp://127.0.0.1:4840/th-koeln/traffic-light/"

    TrafficLightApp()
    trafficlightthread = threading.Thread(target=run_traffic_light)
    trafficlightthread.start()


    # Starte Server und Client in separaten Aufgaben
    server_task = asyncio.create_task(run_server(endpoint))
    client_task = asyncio.create_task(run_client(endpoint))
    # Lasse beide Aufgaben parallel laufen
    await asyncio.gather(server_task, client_task)




# Hauptprogramm ausführen
asyncio.run(main())

if __name__ == "__main__":
    server = Server()
    asyncio.run(main())