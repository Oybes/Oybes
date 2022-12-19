# Import the necessary libraries
from flask import Flask, request, send_file
import os
import zipfile

app = Flask(__name__)

# Define a route for the form submission
@app.route('/submit', methods=['POST'])
def submit():
  # Get the values from the form
  systemmailbox = request.form['systemmailbox']
  customername = request.form['customername']
  secureMailBoxGroup = request.form['secureMailBoxGroup']
  webAddinId = request.form['webAddinId']
  Url = request.form['Url']
  #value3 = request.form['value3']

  # Save the values to a file
  with open("values.txt", "w") as f:
    f.write(f"Systemmailbox: {systemmailbox}\n")
    f.write(f"Customername: {customername}\n")
    #f.write(f"Value 3: {value3}\n")

  generateSwaggerContent = '''http://localhost:8089/swagger/


[
 {
 "Name": "AddInAlwaysCheckAddressForTlsDeliveryIfEnabled",
 "Value": "false"
 },
 {
 "Name": "CalendarInvitesForceTlsForNonInternalRecipients",
 "Value": "true"
 },
 {
 "Name": "CheckTlsSslVersionPattern",
 "Value":"SSLv23:!SSLv3:!SSLv2:!TLSv1:!TLSv11;CHECKMTASTS=off;CHECKDANE=off;TIMEOUT=10;MXPREFLIMIT=1;IGNORENOCONNECT=on"
 },
 {
 "Name": "DpgPortalLoggerUrl",
 "Value": "https://portal.dpgapi.dk/logsvc/log-events"
 },
 {
 "Name": "ElasticSearchConnection",
 "Value": ""
 },
 {
 "Name": "InternalDomainAddressesAreHandled",
 "Value": "true"
 },
 {
 "Name": "LocalDiagnosticDatabaseIncludeErrorMessage",
 "Value": "true"
 },
 {
 "Name": "LocalDiagnosticDatabaseIncludeFromAndOriginalFrom",
 "Value": "true"
 },
 {
 "Name": "LocalDiagnosticDatabaseIncludeSubject",
 "Value": "true"
 },
 {
 "Name": "OmeFromHeader",
 "Value": "From"
 },
 {
 "Name": "OutboundMailtypeOrder",
 "Value": "TunnelmailOverSmimeOverTls"
 },
 {
 "Name": "Pkcs7CipherKeyLength",
 "Value": "256"
 },
 {
 "Name": "Pkcs7CipherAlgo",
 "Value": "aes"
 },
 {
 "Name": "SinkAzureApplicationInsightsKey",
 "Value": "5c7d1a62-0399-4bf9-aea3-524836b7766a"
 },
 {
 "Name": "SinkAzureDocDbKey",
 "Value": ""
 },
 {
 "Name": "SinkAzureDocDbUri",
 "Value": ""
 },
 {
 "Name": "SinkAzureTableStorageConnection",
 "Value": ""
 },
 {
 "Name": "SMTPRelayInsteadOfImapForInboundMailForSecuremailbox",
 "Value": "true"
 },
 {
 "Name": "SMTPRelayIfPresentForInbound",
 "Value": "true"
 },
 {
 "Name": "SMTPRelayIfPresentForOutboundOme",
 "Value": "true"
 },
 {
 "Name": "SurveillanceApplicationInsightsKey",
 "Value": "7c5bda75-1ae4-4bba-8161-79e86127c3d0"
 },
 {
 "Name": "TlsCacheItemFalseExpiryInDays",
 "Value": "1"
 },
 {
 "Name": "TlsCacheItemTrueExpiryInDays",
 "Value": "7"
 },
 {
 "Name": "TlsFromHeader",
 "Value": "From"
 },
 {
 "Name": "TunnelMailAddSignatureInfoAttachment",
 "Value": "true"
 },
 {
 "Name": "TunnelMailFromHeader",
 "Value": "From"
 },
 {
 "Name": "UnconfiguredMailboxUpdateIntervalInMinutes",
 "Value": "15"
 } 
]
Next, configure the below additional required and optional System Parameters. They can be
configured manually in the DPG Config tool or through http://localhost:8089/swagger/:
• AddInRestApiPassword
• AddInRestApiUsername (Important!: use only small and capital letters and numbers, e.g.
aaBB11223344ccDD, because of eBoks signature replies)
• DpgPortalLoggerApiKey, this is the unique "Jwt-API-Key" from portal.dpgapi.dk for this
specific customer
• ForwardMessageIdEncryptionPassword
• SMTPRelaySecretHeaderValue (Important!: use only small and capital letters and numbers,
e.g. aaBB11223344ccDD, because of "Receive Unencrypted" transport rule)
• ExchangeRestApplicationId
• ExchangeRestCertificateRfc822NameOrThumbprint (Important!: configure the certificate
thumbprint, e.g. A75CA48003B7943CAB1F39811718A3D8CDF1F339)
• ExchangeRestTenantId
• UnconfiguredMailboxExchangeGroup (to read out the group members, a.k.a. Unconfigured
Mailboxes)
• InternalDomains
• OmeForUnsecureMails (if relevant remember to enable it)
• WebAddInId (Important!: use only small and capital letters and numbers and create an id of
20 characters, e.g. Be6mOe32XapeXYF2j2Qs)
• WebAddInRestUrlPart (The DNS host name of the DPG solution, e.g. CUSTOMER.dpgapi.dk)
Swagger list of additional required and optional System Parameters:



[
 {
 "Name": "UnconfiguredMailboxExchangeGroup",
 "Value": "''',secureMailBoxGroup,'''"
 },
 {
 "Name": "WebAddInId",
 "Value": "''',webAddinId,'''"
 },
 {
 "Name": "WebAddInRestUrlPart",
 "Value": "''',Url,'''"
 }
] 
'''
 # Save the values to a file
  with open("Swaggerfile.txt", "w") as f:
    f.writelines(generateSwaggerContent)

  # Zip the file
  with zipfile.ZipFile("values.zip", "w", zipfile.ZIP_DEFLATED) as zip:
    zip.write("values.txt")
    zip.write("Swaggerfile.txt")

  # Send the zip file as a response
  return send_file("values.zip", as_attachment=True)

# Define a route for the form
@app.route('/form')
def form():
  return '''
  <form method="POST" action="/submit">
    <input type="text" name="systemmailbox" placeholder="Value 1"><br>
    <input type="text" name="customername" placeholder="Value 2"><br>
    <input type="text" name="secureMailBoxGroup" placeholder="Value 2"><br>
    <input type="text" name="webAddinId" placeholder="Value 2"><br>
    <input type="text" name="Url" placeholder="Value 2"><br>
    <!-- <input type="text" name="value3" placeholder="Value 3">--><br> 
    <button type="submit">Download</button>
  </form>
  '''

# Run the app
if __name__ == '__main__':
  app.run()
