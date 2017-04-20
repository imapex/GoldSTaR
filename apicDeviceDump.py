# import requests library
import requests
requests.packages.urllib3.disable_warnings()

#import json library
import json

#import getpass to mask password entries
import getpass

#import Base64 for encoding Prime username/password combo
import base64

#define variables
controller='devnetapi.cisco.com/sandbox/apic_em'
allPlatformIds=[]  #List to hold PlatformIDs
runningVersions=[]  #List to hold tuple items (PlatformIDs, Software Versions)

def getTicket(apic_username, apic_password):
    # put the ip address or dns of your apic-em controller in this url
    url = "https://" + controller + "/api/v1/ticket"

    #the username and password to access the APIC-EM Controller
    payload = {"username":apic_username,"password":apic_password}

    #Content type must be included in the header
    header = {"content-type": "application/json"}

    #Performs a POST on the specified url to get the service ticket
    response= requests.post(url,data=json.dumps(payload), headers=header, verify=False)

    #convert response to json format
    r_json=response.json()

    #parse the json to get the service ticket
    ticket = r_json["response"]["serviceTicket"]

    return ticket


def getDevicesFromAPICEM(ticket):
    #Define Globals
    global allPlatformIds
    global runningVersions

    # URL for network device REST API call to get list of existing devices on the network.
    url = "https://" + controller + "/api/v1/network-device"

    #Content type must be included in the header as well as the ticket
    header = {"content-type": "application/json", "X-Auth-Token":ticket}

    # this statement performs a GET on the specified network-device url
    response = requests.get(url, headers=header, verify=False)

    # json.dumps serializes the json into a string and allows us to
    # print the response in a 'pretty' format with indentation etc.
    #print ("Network Devices = ")
    #print (json.dumps(response.json(), indent=4, separators=(',', ': ')))

  #convert data to json format.
    r_json=response.json()

  #Iterate through network device data and print the id and series name of each device
    for i in r_json["response"]:
        #print(i["hostname"] + "   " + i["platformId"] + "   " + i["softwareVersion"])
        allPlatformIds.append(str(i["platformId"]))
        runningVersions.append((str(i["platformId"]), str(i["softwareVersion"])))

def suggestedSoftware():
    #Placeholder to house Suggested Software API code
    suggestedSofwareVersion = []
    print suggestedSoftwareVersion

def getDevicesFromPrime(pi_username,pi_password):
    #Get inventory information from Prime Infrastructure

    global allPlatformIds
    global runningVersions

    #encode username/password into Base64
    encoded = pi_username + ":" + pi_password
    encoded = base64.b64encode(bytes(encoded))

    url = "http://pi1.cisco.com/webacs/api/v1/data/Devices.json?.full=true"

    headers = {
    'authorization': "Basic " + encoded
    }

    response = requests.get(url, headers=headers, verify=False)

    response.raise_for_status()
    for i in response.json()['queryResponse']['entity']:
        if 'manufacturerPartNrs' in i['devicesDTO']:
            allPlatformIds.append(str(i['devicesDTO']['manufacturerPartNrs']['manufacturerPartNr']))
            #print (i['devicesDTO']['@id'], i['devicesDTO']['ipAddress'], i['devicesDTO']['manufacturerPartNrs']['manufacturerPartNr'])
        elif 'softwareVersion' in i['devicesDTO']:
            runningVersions.append((str(i['devicesDTO']['deviceType']), str(i['devicesDTO']['softwareVersion'])))
            #print (i['devicesDTO']['@id'], i['devicesDTO']['ipAddress'], i['devicesDTO']['deviceType'], i['devicesDTO']['softwareVersion'])

def main():
    #define Globals
    global allPlatformIds
    global runningVersions

    print "*************************************"
    print "*        Welcome to GoldSTaR        *"
    print "*************************************\n\n"

    print "Where Would You Like to Get Your Inventory From?\n"
    print "1) APIC-EM"
    print "2) Prime Infrastructure\n"

    inventoryMenu = raw_input("Selection >> ")

    if inventoryMenu == "1":

        apic_username = raw_input("Enter Your APIC-EM Username (devnetuser): >> ")
        apic_password = getpass.getpass("Enter Your APIC-EM Username (Cisco123!): >> ")

        #call the functions
        theTicket=getTicket(apic_username,apic_password)
        getDevicesFromAPICEM(theTicket)

    elif inventoryMenu == "2":

        pi_username = raw_input("Enter Your Prime Infrastructure Username (): >> ")
        pi_password = getpass.getpass("Enter Your Prime Infrastucture Password (): >> ")

        #call the functions
        getDevicesFromPrime(pi_username,pi_password)

    else:
        print "Wow, 1 or 2, is it really that difficult?"

    print "What Would You Like to Do?\n"
    print "1) Display Collected Platform IDs"
    print "2) Display Running Software Versions\n"

    menuSelection = raw_input("Selection >> ")

    if menuSelection == "1":
        print '\n'.join(str(p) for p in allPlatformIds)
    elif menuSelection == "2":
        print '\n'.join(str(p) for p in runningVersions)
    else:
        print "My God, Man! There's only 2 choices, you can't pick one of those?"

#Start the App
main()

