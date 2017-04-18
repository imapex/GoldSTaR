# import requests library
import requests
requests.packages.urllib3.disable_warnings()

#import json library
import json

#import getpass to mask password entries
import getpass

controller='devnetapi.cisco.com/sandbox/apic_em'

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


def getNetworkDevices(ticket):
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

    allPlatformIds=[]  #List to hold PlatformIDs
    runningVersions={}  #Dictionary to hold PlatformIDs, Software Versions
  #Iterate through network device data and print the id and series name of each device
    for i in r_json["response"]:
        print(i["hostname"] + "   " + i["platformId"] + "   " + i["softwareVersion"])
        allPlatformIds.append(str(i["platformId"]))
        runningVersions[str(i["platformId"])]=str(i["softwareVersion"])

def suggestedSoftware():
    #Placeholder to house Suggested Software API code
    suggestedSofwareVersion = []
    print suggestedSoftwareVersion

def main():

    print "*************************************"
    print "*        Welcome to GoldSTaR        *"
    print "*************************************\n\n"
    apic_username = raw_input("Enter Your APIC-EM Username (devnetuser): >> ")
    apic_password = getpass.getpass("Enter Your APIC-EM Username (Cisco123!): >> ")

    #call the functions
    theTicket=getTicket(apic_username,apic_password)
    getNetworkDevices(theTicket)

#Start the App
main()

